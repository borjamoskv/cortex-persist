# Copyright 2026 Borja Moskv (borjamoskv)
"""CLI/process integration and crash accounting, using only the stdlib."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from scripts.scalability.contract import (
    ValidationError,
    canonical,
    fingerprint,
    load_runs,
    validate_policy,
)
from scripts.scalability.experiment import atomic_write, campaign, execute
from scripts.scalability.planner import validate_space

ROOT = Path(__file__).resolve().parents[2]
FAULT_RUNNER = ROOT / ".github/tests/fixtures/scalability_runner.py"
SYNTHETIC_RUNNER = ROOT / "examples/scalability/synthetic_runner.py"


@unittest.skipUnless(os.name == "posix", "runner uses POSIX process groups")
class ExecutionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cortex-scalability-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.space = validate_space(
            json.loads((ROOT / "examples/scalability/space.json").read_text())
        )
        self.space["candidates"] = [self.space["candidates"][0]]
        self.space["budget"]["max_runs"] = 2
        self.policy = validate_policy(
            {"min_runs": 2, "min_tasks": 2, "bootstrap_samples": 100}
        )
        self.history = self.directory / "runs.jsonl"
        self.candidate = self.space["candidates"][0]
        self.request = {
            "protocol_version": 1,
            "run_id": "assigned-run",
            "campaign_id": self.space["campaign_id"],
            "candidate": self.candidate,
            "space_sha256": fingerprint(self.space),
        }

    def execute_mode(self, mode):
        return execute(
            [sys.executable, str(FAULT_RUNNER), mode],
            self.request,
            self.policy,
            self.directory / "stderr.log",
        )

    def test_completed_runner_preserves_results(self):
        result = self.execute_mode("good")
        self.assertEqual(result["run_id"], "assigned-run")
        self.assertEqual(len(result["tasks"]), 10)
        self.assertEqual(result["cost_total"], 0.05)
        self.assertEqual(result["reserved_cost"], self.candidate["max_cost"])

    def test_timeout_is_aborted_with_unknown_bill(self):
        self.candidate["timeout_seconds"] = 0.2
        started = time.monotonic()
        result = self.execute_mode("timeout")
        self.assertLess(time.monotonic() - started, 3)
        self.assertEqual(result["abort_reason"], "runner_timeout")
        self.assertIsNone(result["cost_total"])
        self.assertEqual(result["reserved_cost"], self.candidate["max_cost"])
        self.assertEqual(result["tasks"], [])

    def test_critical_task_aborts_immediately_and_preserves_observation(self):
        self.policy["abort_on_critical"] = True
        started = time.monotonic()
        result = self.execute_mode("critical")
        self.assertLess(time.monotonic() - started, 3)
        self.assertEqual(result["abort_reason"], "critical_failure")
        self.assertEqual(len(result["tasks"]), 1)
        self.assertIsNone(result["cost_total"])

    def test_protocol_errors_are_not_completed_benchmarks(self):
        for mode in (
            "invalid",
            "mismatch",
            "missing",
            "trailing",
            "nonzero",
            "oversize",
        ):
            with self.subTest(mode=mode):
                result = self.execute_mode(mode)
                self.assertEqual(result["run_status"], "aborted")
                self.assertIn("abort_reason", result)

    def test_child_processes_are_terminated(self):
        marker = self.directory / "child-survived"
        result = execute(
            [sys.executable, str(FAULT_RUNNER), "child", str(marker)],
            self.request,
            self.policy,
            self.directory / "stderr.log",
        )
        self.assertEqual(result["run_status"], "aborted")
        time.sleep(1)
        self.assertFalse(marker.exists())

    def test_launch_failure_cost_is_known_zero(self):
        result = execute(
            [str(self.directory / "does-not-exist")],
            self.request,
            self.policy,
            self.directory / "stderr.log",
        )
        self.assertEqual(result["run_status"], "aborted")
        self.assertEqual(result["cost_total"], 0)

    def test_malformed_event_diagnostic_is_bounded_and_serializable(self):
        result = self.execute_mode("badkey")
        self.assertEqual(result["run_status"], "aborted")
        self.assertLessEqual(len(result["abort_reason"]), 512)
        self.assertNotIn("\n", result["abort_reason"])
        json.dumps(result, allow_nan=False)

    def test_campaign_budget_resume_and_input_hash(self):
        args = (
            self.history,
            self.space,
            self.policy,
            [sys.executable, str(SYNTHETIC_RUNNER)],
            self.directory,
        )
        report, sources = campaign(*args)
        self.assertEqual(report["plan"]["reason"], "run_budget_exhausted")
        self.assertEqual(report["plan"]["budget_used"], 0.1)
        runs, actual_sources = load_runs([self.history])
        self.assertEqual(sources[0]["sha256"], actual_sources[0]["sha256"])
        self.assertEqual(
            Path(sources[0]["path"]).resolve(),
            Path(actual_sources[0]["path"]).resolve(),
        )
        self.assertEqual(len(runs), 2)
        self.assertFalse(Path(str(self.history) + ".pending.json").exists())
        original = self.history.read_bytes()
        campaign(*args)
        self.assertEqual(original, self.history.read_bytes())

    def test_early_abort_charges_reservation_and_stops_same_arm(self):
        self.policy["abort_on_critical"] = True
        report, _ = campaign(
            self.history,
            self.space,
            self.policy,
            [sys.executable, str(FAULT_RUNNER), "critical"],
            self.directory,
        )
        self.assertEqual(report["plan"]["attempts"], 1)
        self.assertEqual(report["plan"]["budget_used"], 0.1)
        self.assertEqual(report["groups"], [])

    def test_overcharge_stops_before_second_dispatch(self):
        report, _ = campaign(
            self.history,
            self.space,
            self.policy,
            [sys.executable, str(FAULT_RUNNER), "overcharge"],
            self.directory,
        )
        self.assertEqual(report["plan"]["attempts"], 1)
        self.assertEqual(report["plan"]["reason"], "runner_cost_cap_breached")

    def test_reservation_is_written_before_start(self):
        pending = Path(str(self.history) + ".pending.json")
        code = (
            "import pathlib,sys; assert pathlib.Path(sys.argv[1]).exists(); sys.exit(9)"
        )
        report, _ = campaign(
            self.history,
            self.space,
            self.policy,
            [sys.executable, "-c", code, str(pending)],
            self.directory,
        )
        self.assertEqual(report["runs"][0]["abort_reason"], "runner_exit_9")

    def test_unresolved_dispatch_cannot_be_retried(self):
        pending = Path(str(self.history) + ".pending.json")
        atomic_write(pending, canonical(self.request))
        with self.assertRaisesRegex(ValidationError, "unresolved dispatch"):
            campaign(
                self.history,
                self.space,
                self.policy,
                ["must-not-launch"],
                self.directory,
            )
        self.assertTrue(pending.exists())
        self.assertFalse(self.history.exists())

    def test_completed_dispatch_reconciles_after_crash(self):
        self.space["budget"]["max_runs"] = 1
        self.request["space_sha256"] = fingerprint(self.space)
        record = self.execute_mode("good")
        atomic_write(self.history, canonical(record) + "\n")
        pending = Path(str(self.history) + ".pending.json")
        atomic_write(pending, canonical(self.request))
        report, _ = campaign(
            self.history, self.space, self.policy, ["must-not-launch"], self.directory
        )
        self.assertEqual(report["plan"]["reason"], "run_budget_exhausted")
        self.assertFalse(pending.exists())

    def test_two_executors_cannot_spend_same_budget(self):
        import fcntl

        with Path(str(self.history) + ".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(ValidationError, "another executor"):
                campaign(
                    self.history,
                    self.space,
                    self.policy,
                    ["must-not-launch"],
                    self.directory,
                )
            self.history.touch()
            alias = self.directory / "alias.jsonl"
            alias.symlink_to(self.history)
            with self.assertRaisesRegex(ValidationError, "another executor"):
                campaign(
                    alias, self.space, self.policy, ["must-not-launch"], self.directory
                )


class CliTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cortex-cli-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)

    def cli(self, name, *arguments):
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / name), *map(str, arguments)],
            cwd=self.directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_analyzer_requires_input(self):
        self.assertEqual(self.cli("analyze_scalability.py").returncode, 2)

    def test_planner_works_without_history_and_never_executes(self):
        output = self.directory / "output"
        result = self.cli(
            "plan_scalability.py",
            "--space",
            ROOT / "examples/scalability/space.json",
            "--output-dir",
            output,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        plan_report = json.loads((output / "plan.json").read_text())
        self.assertEqual(plan_report["plan"]["attempts"], 0)
        self.assertEqual(plan_report["plan"]["status"], "propose")

    def test_full_example_and_policy_violation_are_informational(self):
        output = self.directory / "output"
        history = self.directory / "results.jsonl"
        result = self.cli(
            "run_scalability.py",
            "--input",
            history,
            "--space",
            ROOT / "examples/scalability/space.json",
            "--policy",
            ROOT / "examples/scalability/policy.json",
            "--output-dir",
            output,
            "--runner",
            sys.executable,
            SYNTHETIC_RUNNER,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((output / "campaign.json").read_text())
        self.assertEqual(report["groups"][0]["recommendation"]["concurrency"], 2)
        self.assertEqual(report["plan"]["attempts"], 15)
        restrictive = self.directory / "policy.json"
        restrictive.write_text(
            json.dumps({"constraints": {"min_successes_per_hour": 1e9}})
        )
        result = self.cli(
            "analyze_scalability.py",
            "--input",
            history,
            "--policy",
            restrictive,
            "--output-dir",
            output,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(
            report["groups"][0]["recommendation"]["status"],
            "no_admissible_configuration",
        )
        result = self.cli(
            "plan_scalability.py",
            "--input",
            history,
            "--space",
            ROOT / "examples/scalability/space.json",
            "--output-dir",
            output,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_json_is_error_not_performance_failure(self):
        path = self.directory / "bad.jsonl"
        path.write_text("{bad}\n")
        result = self.cli("analyze_scalability.py", "--input", path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("bad.jsonl:1:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_campaign_rejects_output_collision_before_dispatch(self):
        source = json.loads((ROOT / "examples/scalability/space.json").read_text())
        path = self.directory / "history.pending.json"
        path.write_text(json.dumps(source))
        before = path.read_bytes()
        result = self.cli(
            "run_scalability.py",
            "--input",
            self.directory / "history",
            "--space",
            path,
            "--runner",
            "must-not-launch",
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
