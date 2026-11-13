# Copyright 2026 Borja Moskv (borjamoskv)

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "analyze_scalability.py"
FIXTURES = ROOT / ".github" / "tests" / "fixtures" / "scalability"
spec = importlib.util.spec_from_file_location("scalability_analysis", SCRIPT)
analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer)


class ScalabilityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="scalability-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.runs, self.source = analyzer.load_runs(FIXTURES / "synthetic.jsonl")
        self.policy, self.policy_source = analyzer.load_policy(FIXTURES / "policy.json")

    def report(self, runs=None, policy=None):
        result = analyzer.analyze(self.runs if runs is None else runs, self.policy if policy is None else policy)
        result["sources"] = {"input": self.source, "policy": self.policy_source}
        return result

    def cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *map(str, arguments)],
            cwd=self.root, capture_output=True, text=True, timeout=15, check=False,
        )

    def write_runs(self, runs):
        path = self.root / "runs.jsonl"
        path.write_text("".join(json.dumps(run) + "\n" for run in runs), encoding="utf-8")
        return path

    def test_reference_example_and_recommendation(self):
        group = self.report()["groups"][0]
        for level, expected_goodput, expected_cost, expected_hourly in zip(
            group["levels"], [100, 160, 170], [.2, .25, 8 / 17], [20, 40, 80]
        ):
            with self.subTest(n=level["concurrency"]):
                self.assertEqual(level["repetitions"], 3)
                self.assertAlmostEqual(level["metrics"]["goodput_per_hour"], expected_goodput)
                self.assertAlmostEqual(level["metrics"]["cost_per_success"], expected_cost)
                self.assertAlmostEqual(level["metrics"]["cost_per_hour"], expected_hourly)
        self.assertAlmostEqual(group["elasticities"][0]["value"], math.log(1.6) / math.log(2))
        self.assertAlmostEqual(group["elasticities"][1]["value"], math.log(170 / 160) / math.log(2))
        self.assertEqual(group["recommendation"]["concurrency"], 20)
        self.assertEqual(group["levels"][-1]["assessment"]["status"], "failed")

    def test_aggregation_uses_totals_and_pools_latencies(self):
        runs = copy.deepcopy(self.runs[:2])
        runs[0]["tasks"] = runs[0]["tasks"][:1]
        runs[0]["tasks"][0]["latency_ms"] = 10000
        runs[0]["duration_s"], runs[0]["total_cost"] = 10, 2
        runs[1]["duration_s"], runs[1]["total_cost"] = 100, 3
        runs[1]["tasks"] = [
            {"task_id": str(i), "status": "success", "latency_ms": 1, "critical_failure": False}
            for i in range(100)
        ]
        m = analyzer.metrics(runs)
        self.assertAlmostEqual(m["goodput_per_hour"], 101 * 3600 / 110)
        self.assertAlmostEqual(m["cost_per_success"], 5 / 101)
        self.assertEqual(m["latency_p95_ms"], 1)

    def test_failed_repetition_cannot_be_hidden_by_aggregation(self):
        runs = copy.deepcopy(self.runs)
        runs[3]["tasks"][0]["critical_failure"] = True
        policy = dict(self.policy, max_critical_failure_rate=.03)
        group = self.report(runs, policy)["groups"][0]
        level = group["levels"][1]
        self.assertLess(level["metrics"]["critical_failure_rate"], .03)
        self.assertEqual(level["assessment"]["status"], "failed")
        self.assertEqual(group["recommendation"]["concurrency"], 10)

    def test_consolidated_retries_and_terminal_failures(self):
        run = copy.deepcopy(self.runs[0])
        run["tasks"] = [
            {"task_id": "retried", "status": "success", "latency_ms": 7000, "critical_failure": True},
            {"task_id": "failed", "status": "failure", "latency_ms": 500, "critical_failure": False},
            {"task_id": "timed-out", "status": "timeout", "latency_ms": 12000, "critical_failure": False},
            {"task_id": "cancelled", "status": "cancelled", "latency_ms": 100, "critical_failure": False},
        ]
        analyzer.validate_run(run, "test")
        m = analyzer.metrics([run])
        self.assertEqual(m["success_count"], 1)
        self.assertEqual(m["task_count"], 4)
        self.assertEqual(m["success_rate"], .25)
        self.assertEqual(m["critical_failure_rate"], .25)
        self.assertEqual(m["latency_p95_ms"], 12000)
        self.assertEqual(m["cost_per_success"], run["total_cost"])

    def test_unknown_cost_and_risk_are_not_zero(self):
        runs = copy.deepcopy(self.runs[:3])
        runs[0]["total_cost"] = None
        runs[1]["tasks"][0]["critical_failure"] = None
        group = self.report(runs)["groups"][0]
        m = group["levels"][0]["metrics"]
        for key in ("total_cost", "cost_per_hour", "cost_per_success", "critical_failure_rate"):
            self.assertIsNone(m[key])
            self.assertIn(key, m["undefined_reasons"])
        self.assertEqual(group["levels"][0]["assessment"]["status"], "insufficient_data")
        self.assertIsNone(group["recommendation"])

    def test_zero_successes_and_empty_runs(self):
        for empty in (False, True):
            with self.subTest(empty=empty):
                runs = copy.deepcopy(self.runs)
                for run in runs:
                    if empty:
                        run["tasks"] = []
                    for task in run["tasks"]:
                        task["status"] = "failure"
                group = self.report(runs)["groups"][0]
                self.assertIsNone(group["recommendation"])
                for level in group["levels"]:
                    self.assertEqual(level["metrics"]["goodput_per_hour"], 0)
                    self.assertIsNone(level["metrics"]["cost_per_success"])
                self.assertIsNone(group["elasticities"][0]["value"])
                self.assertIsNotNone(group["elasticities"][0]["reason"])

    def test_groups_separate_workloads_evaluators_configuration_and_currency(self):
        runs = [copy.deepcopy(self.runs[0]) for _ in range(7)]
        for i, run in enumerate(runs):
            run["run_id"] = str(i)
        runs[1]["workload_id"] = "different-workload"
        runs[2]["evaluator_id"] = "different-evaluator"
        runs[3]["configuration"]["hardware"] = "different-hardware"
        runs[4]["configuration"]["model"] = "different-model"
        runs[5]["configuration"]["quotas"] = "different-quota"
        runs[6]["currency"] = "USD"
        groups = self.report(runs)["groups"]
        self.assertEqual(len(groups), 7)
        self.assertTrue(all(group["recommendation"] is None for group in groups))
        usd = next(group for group in groups if group["comparison"]["currency"] == "USD")
        self.assertIn("currency_mismatch", usd["levels"][0]["assessment"]["violations"])

    def test_descriptive_mode_and_single_concurrency(self):
        group = analyzer.analyze(self.runs[:3])["groups"][0]
        self.assertEqual(group["levels"][0]["assessment"]["status"], "not_evaluated")
        self.assertIsNone(group["recommendation"])
        self.assertEqual(group["recommendation_reason"], "policy_not_provided")
        self.assertEqual(group["elasticities"], [])

    def test_exact_boundaries_are_inclusive(self):
        policy = dict(self.policy, budget_per_hour=20, min_success_rate=1, max_p95_ms=4000,
                      max_critical_failure_rate=0)
        group = self.report(self.runs[:3], policy)["groups"][0]
        self.assertEqual(group["levels"][0]["assessment"]["status"], "passed")
        self.assertEqual(group["recommendation"]["concurrency"], 10)

    def test_repetition_requirement_default_and_override(self):
        self.assertEqual(self.policy["min_repetitions"], 3)
        self.assertIsNone(self.report(self.runs[:2])["groups"][0]["recommendation"])
        policy = dict(self.policy, min_repetitions=2)
        self.assertIsNotNone(self.report(self.runs[:2], policy)["groups"][0]["recommendation"])

    def test_no_admissible_configuration_and_tie_breaks(self):
        self.assertIsNone(self.report(policy=dict(self.policy, budget_per_hour=0))["groups"][0]["recommendation"])
        runs = copy.deepcopy(self.runs)
        for run in runs:
            run["tasks"] = run["tasks"][:10]
            run["total_cost"] = 2 if run["concurrency"] == 10 else 1
            for task in run["tasks"]:
                task["latency_ms"] = 100
        self.assertEqual(self.report(runs)["groups"][0]["recommendation"]["concurrency"], 20)
        for run in runs:
            run["total_cost"] = 1
        self.assertEqual(self.report(runs)["groups"][0]["recommendation"]["concurrency"], 10)

    def test_negative_elasticity_is_reported(self):
        runs = copy.deepcopy(self.runs)
        for run in runs:
            if run["concurrency"] == 20:
                run["duration_s"] *= 10
        self.assertLess(self.report(runs)["groups"][0]["elasticities"][0]["value"], 0)

    def test_input_order_does_not_change_analysis(self):
        self.assertEqual(self.report(), self.report(list(reversed(self.runs))))

    def test_duplicates_and_nonfinite_json_rejected(self):
        run = self.runs[0]
        bad_inputs = [
            json.dumps(run) + "\n" + json.dumps(run),
            json.dumps(dict(run, tasks=run["tasks"] + [run["tasks"][0]])),
            '{"schema_version":1,"schema_version":1}',
            '{"total_cost": NaN}', '{"total_cost": Infinity}', '{"total_cost": 1e999}',
            "{", "[]", "", " \n",
        ]
        for bad in bad_inputs:
            with self.subTest(bad=bad[:60]):
                path = self.root / "invalid.jsonl"
                path.write_text(bad, encoding="utf-8")
                with self.assertRaises(analyzer.ValidationError):
                    analyzer.load_runs(path)

    def test_invalid_run_fields_rejected(self):
        changes = [
            ("schema_version", True), ("schema_version", 2), ("run_id", ""),
            ("concurrency", True), ("concurrency", 0), ("concurrency", 1.5),
            ("duration_s", 0), ("duration_s", -1), ("duration_s", math.inf),
            ("total_cost", -1), ("total_cost", True), ("currency", "eur"),
            ("workload_id", None), ("configuration", {}), ("tasks", {}),
        ]
        for key, value in changes:
            with self.subTest(field=key, value=value):
                run = dict(self.runs[0], **{key: value})
                with self.assertRaises(analyzer.ValidationError):
                    analyzer.validate_run(run, "test")

    def test_invalid_task_fields_and_missing_cost_rejected(self):
        for key, value in [
            ("task_id", ""), ("latency_ms", -1), ("latency_ms", math.nan),
            ("status", "running"), ("status", []), ("critical_failure", 0),
        ]:
            with self.subTest(field=key):
                run = copy.deepcopy(self.runs[0])
                run["tasks"][0][key] = value
                with self.assertRaises(analyzer.ValidationError):
                    analyzer.validate_run(run, "test")
        for field in ("total_cost",):
            run = dict(self.runs[0])
            del run[field]
            with self.assertRaises(analyzer.ValidationError):
                analyzer.validate_run(run, "test")
        run = copy.deepcopy(self.runs[0])
        del run["tasks"][0]["critical_failure"]
        with self.assertRaises(analyzer.ValidationError):
            analyzer.validate_run(run, "test")

    def test_policy_requires_complete_valid_thresholds(self):
        changes = [
            ("schema_version", True), ("budget_per_hour", None), ("budget_per_hour", -1),
            ("min_success_rate", 1.1), ("max_critical_failure_rate", -0.1),
            ("max_p95_ms", math.inf), ("min_repetitions", 0), ("min_repetitions", True),
            ("currency", "eu"), ("unexpected", 1),
        ]
        for key, value in changes:
            with self.subTest(field=key):
                path = self.root / "policy.json"
                path.write_text(json.dumps(dict(self.policy, **{key: value})), encoding="utf-8")
                with self.assertRaises(analyzer.ValidationError):
                    analyzer.load_policy(path)
        path.write_text('{"schema_version":1}', encoding="utf-8")
        with self.assertRaises(analyzer.ValidationError):
            analyzer.load_policy(path)

    def test_unrepresentable_rates_are_null_with_reason(self):
        runs = copy.deepcopy(self.runs[:3])
        for run in runs:
            run["duration_s"] = 5e-324
        group = self.report(runs)["groups"][0]
        self.assertIsNone(group["levels"][0]["metrics"]["goodput_per_hour"])
        self.assertIsNone(group["recommendation"])

    def test_cli_reports_hashes_parity_and_reproducibility(self):
        self.maxDiff = None
        args = ["--input", FIXTURES / "synthetic.jsonl", "--policy", FIXTURES / "policy.json"]
        result = self.cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.root / "logs" / "scalability"
        raw_json, raw_md = (output / "report.json").read_bytes(), (output / "report.md").read_bytes()
        report = json.loads(raw_json)
        markdown = raw_md.decode("utf-8")
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["sources"]["input"]["sha256"],
                         hashlib.sha256((FIXTURES / "synthetic.jsonl").read_bytes()).hexdigest())
        self.assertEqual(report["sources"]["policy"]["sha256"],
                         hashlib.sha256((FIXTURES / "policy.json").read_bytes()).hexdigest())
        self.assertEqual(markdown, analyzer.render_markdown(report))
        self.assertIn("Recommendation: 20", markdown)
        self.assertIn("Schema version: 1", markdown)
        self.assertIn("not sustained production capacity", markdown)
        for level in report["groups"][0]["levels"]:
            for key, value in level["metrics"].items():
                if key != "undefined_reasons":
                    self.assertIn(f"- {key}: {analyzer.cell(value)}", markdown)
        self.assertEqual(self.cli(*args).returncode, 0)
        self.assertEqual(raw_json, (output / "report.json").read_bytes())
        self.assertEqual(raw_md, (output / "report.md").read_bytes())

    def test_cli_policy_failure_is_informational(self):
        policy = self.root / "policy.json"
        policy.write_text(json.dumps(dict(self.policy, budget_per_hour=0)), encoding="utf-8")
        result = self.cli("--input", FIXTURES / "synthetic.jsonl", "--policy", policy)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((self.root / "logs/scalability/report.json").read_text())
        self.assertIsNone(report["groups"][0]["recommendation"])

    def test_large_finite_cost_rates_avoid_intermediate_overflow(self):
        run = copy.deepcopy(self.runs[0])
        run["total_cost"], run["duration_s"] = 10 ** 308, 1e308
        analyzer.validate_run(run, "test")
        self.assertAlmostEqual(analyzer.metrics([run])["cost_per_hour"], 3600)

    def test_nonfinite_aggregate_is_validation_error(self):
        runs = copy.deepcopy(self.runs[:3])
        for run in runs:
            run["total_cost"] = 1e308
        result = self.cli("--input", self.write_runs(runs))
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_nearest_rank_percentile_and_known_critical_count(self):
        run = copy.deepcopy(self.runs[0])
        run["tasks"] = [
            {"task_id": str(i), "status": "success", "latency_ms": i, "critical_failure": i == 20}
            for i in range(1, 21)
        ]
        m = analyzer.metrics([run])
        self.assertEqual(m["latency_p95_ms"], 19)
        self.assertEqual(m["known_critical_failures"], 1)
        self.assertEqual(m["critical_failure_rate"], .05)

    def test_missing_input_flag_and_policy_utf8_fail_as_specified(self):
        self.assertEqual(self.cli("--unknown").returncode, 2)
        policy = self.root / "invalid-policy.json"
        policy.write_bytes(b"\xff")
        result = self.cli("--input", FIXTURES / "synthetic.jsonl", "--policy", policy)
        self.assertEqual(result.returncode, 2)

    def test_cli_invalid_arguments_data_encoding_and_io_errors(self):
        self.assertEqual(self.cli().returncode, 2)
        path = self.root / "bad.jsonl"
        for raw in (b"{", b"\xff"):
            path.write_bytes(raw)
            self.assertEqual(self.cli("--input", path).returncode, 2)
        self.assertEqual(self.cli("--input", self.root / "missing.jsonl").returncode, 1)
        blocked = self.root / "not-a-directory"
        blocked.write_text("occupied")
        result = self.cli("--input", FIXTURES / "synthetic.jsonl", "--output-dir", blocked)
        self.assertEqual(result.returncode, 1)
        self.assertFalse((self.root / "logs/scalability/report.json").exists())

    def test_cli_refuses_to_overwrite_source(self):
        path = self.root / "report.json"
        original = (FIXTURES / "synthetic.jsonl").read_bytes()
        path.write_bytes(original)
        result = self.cli("--input", path, "--output-dir", self.root)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(path.read_bytes(), original)

    def test_markdown_escapes_external_labels(self):
        report = self.report()
        report["sources"]["input"]["path"] = "<script>|bad\npath"
        report["groups"][0]["levels"][0]["runs"][0]["run_id"] = "<script>|bad\nrun"
        markdown = analyzer.render_markdown(report)
        self.assertNotIn("<script>", markdown)
        self.assertIn("&lt;script&gt;\\|bad path", markdown)

    def test_workflow_demo_and_summary_execute(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8"))
        steps = {step.get("name"): step["run"] for step in workflow["jobs"]["sanity"]["steps"] if "run" in step}
        (self.root / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.root / "scripts/analyze_scalability.py")
        destination = self.root / ".github/tests/fixtures/scalability"
        shutil.copytree(FIXTURES, destination)
        summary = self.root / "summary.md"
        env = dict(os.environ, GITHUB_STEP_SUMMARY=str(summary),
                   PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"])
        for name in ("Analyze synthetic scalability fixtures", "Publish synthetic scalability report"):
            result = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", steps[name]],
                                    cwd=self.root, env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
        text = summary.read_text(encoding="utf-8")
        self.assertIn("Synthetic demonstration", text)
        self.assertIn("Recommendation: 20", text)


if __name__ == "__main__":
    unittest.main()
