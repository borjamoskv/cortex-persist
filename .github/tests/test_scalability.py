# Copyright 2026 Borja Moskv (borjamoskv)
"""Independent arithmetic, adversarial input, decision and planning cases."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path

from scripts.scalability.contract import (
    ValidationError,
    canonical,
    decode,
    load_runs,
    validate_policy,
    validate_run,
)
from scripts.scalability.decision import analyze
from scripts.scalability.metrics import elasticity, metrics, percentile
from scripts.scalability.planner import critical_sequence, plan, validate_space
from scripts.scalability.report import envelope, markdown, write_reports

ROOT = Path(__file__).resolve().parents[2]


def run_record(run_id="r1", *, n=1, duration=1, cost=0.05, count=10, status="success"):
    return {
        "schema_version": 1,
        "run_id": run_id,
        "workload_id": "load-v1",
        "evaluator_id": "eval-v1",
        "config_id": "config-v1",
        "configuration": {"model": "fixture", "hardware": "fixture", "quotas": {}},
        "currency": "EUR",
        "concurrency": n,
        "duration_seconds": duration,
        "cost_total": cost,
        "tasks": [
            {
                "task_id": str(i),
                "status": status,
                "latency_ms": (i + 1) * 100,
                "critical_failure": False,
            }
            for i in range(count)
        ],
    }


def policy(**kwargs):
    return validate_policy(
        {"min_runs": 2, "min_tasks": 2, "bootstrap_samples": 100, **kwargs}
    )


def space(**kwargs):
    result = json.loads((ROOT / "examples/scalability/space.json").read_text())
    result.update(kwargs)
    return validate_space(result)


def campaign_run(candidate, run_id="r1", **kwargs):
    record = run_record(
        run_id, n=candidate["concurrency"], count=candidate["task_count"], **kwargs
    )
    for field in (
        "workload_id",
        "evaluator_id",
        "config_id",
        "configuration",
        "currency",
        "candidate_id",
    ):
        record[field] = copy.deepcopy(candidate[field])
    record["campaign_id"] = "synthetic-demo-v1"
    return record


class ContractTests(unittest.TestCase):
    def test_rejects_duplicate_keys_at_any_depth(self):
        for value in ('{"x":1,"x":2}', '{"configuration":{"x":1,"x":2}}'):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                decode(value)

    def test_rejects_nonfinite_and_invalid_unicode(self):
        for value in (
            "NaN",
            "Infinity",
            "-Infinity",
            "1e999",
            '{"x": [1e999]}',
            '"\\ud800"',
            b"\xff",
        ):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                decode(value)

    def test_rejects_invalid_run_fields(self):
        changes = [
            ("schema_version", 2),
            ("schema_version", True),
            ("duration_seconds", 0),
            ("duration_seconds", -1),
            ("duration_seconds", float("inf")),
            ("concurrency", 0),
            ("concurrency", True),
            ("concurrency", 1.5),
            ("cost_total", True),
            ("cost_total", -1),
            ("run_id", ""),
            ("run_id", "x\ny"),
            ("currency", "eur"),
            ("tasks", []),
            ("run_status", "running"),
            ("configuration", {}),
            ("configuration", None),
        ]
        for key, value in changes:
            record = run_record()
            record[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValidationError):
                validate_run(record)

    def test_rejects_invalid_task_fields(self):
        for key, value in [
            ("status", "pending"),
            ("status", []),
            ("latency_ms", -1),
            ("latency_ms", math.nan),
            ("critical_failure", 1),
            ("task_id", ""),
        ]:
            record = run_record()
            record["tasks"][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValidationError):
                validate_run(record)

    def test_missing_and_unknown_fields_fail(self):
        for mutation in (
            lambda r: r.pop("cost_total"),
            lambda r: r.update(cost_totla=1),
            lambda r: r["tasks"][0].pop("critical_failure"),
        ):
            record = run_record()
            mutation(record)
            with self.assertRaises(ValidationError):
                validate_run(record)

    def test_unknown_values_and_success_with_critical_side_effect_are_allowed(self):
        record = run_record(cost=None)
        record["tasks"][0]["critical_failure"] = None
        record["tasks"][1]["critical_failure"] = True
        self.assertIs(validate_run(record), record)

    def test_task_ids_are_unique_only_within_run(self):
        record = run_record()
        record["tasks"][1]["task_id"] = record["tasks"][0]["task_id"]
        with self.assertRaisesRegex(ValidationError, "duplicate task"):
            validate_run(record)

    def test_aborted_empty_run_requires_reason(self):
        record = run_record(count=0)
        record.update(run_status="aborted", abort_reason="timeout")
        validate_run(record)
        del record["abort_reason"]
        with self.assertRaises(ValidationError):
            validate_run(record)

    def test_occupancy_validates_overlap_and_wall_bounds(self):
        for intervals in ([[0, 2]], [[-1, 0.5]], [[0.5, 0.2]], [[0, 1], [0, 1]], [[0]]):
            record = run_record()
            record["occupancy_intervals"] = intervals
            with self.subTest(intervals=intervals), self.assertRaises(ValidationError):
                validate_run(record)
        record["occupancy_intervals"] = [[0, 0.5], [0.5, 1]]
        validate_run(record)

    def test_input_hashes_and_duplicate_run_ids_across_files(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a.jsonl", Path(directory) / "b.jsonl"
            data = (canonical(run_record()) + "\n").encode()
            a.write_bytes(data)
            b.write_bytes(data)
            runs, sources = load_runs([a])
            self.assertEqual(len(runs), 1)
            self.assertEqual(sources[0]["sha256"], hashlib.sha256(data).hexdigest())
            with self.assertRaisesRegex(ValidationError, "duplicate run_id"):
                load_runs([a, b])

    def test_jsonl_errors_have_line_numbers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            for tail in ("\n", "{bad}\n"):
                path.write_text(canonical(run_record()) + "\n" + tail)
                with self.assertRaisesRegex(ValidationError, r"bad.jsonl:2:"):
                    load_runs([path])

    def test_policy_rejects_typos_wrong_types_and_unscoped_money(self):
        for value in (
            {"bootstrap_samples": 1},
            {"min_runs": True},
            {"confidence": 1},
            {"constraints": {"unknown": 1}},
            {"constraints": {"min_success_rate": 1.1}},
            {"objective": "cost_per_success"},
            {"abort_on_critical": 1},
            {"constraints": {"min_success_within_deadline_rate": 0.5}},
        ):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_policy(value)


class MetricsTests(unittest.TestCase):
    def test_ratio_of_totals_and_pooled_percentile(self):
        a = run_record("a", duration=10, cost=2, count=4)
        for task, state, latency in zip(
            a["tasks"],
            ("success", "failure", "timeout", "cancelled"),
            (10, 100, 1000, 5),
        ):
            task.update(status=state, latency_ms=latency)
        b = run_record("b", duration=20, cost=3, count=2)
        actual = metrics([a, b])["values"]
        self.assertEqual(actual["successes_per_hour"], 360)
        self.assertEqual(actual["success_rate"], 0.5)
        self.assertEqual(actual["cost_per_hour"], 600)
        self.assertAlmostEqual(actual["cost_per_success"], 5 / 3)
        self.assertEqual(actual["p95_terminal_ms"], 1000)

    def test_unknown_cost_and_classification_are_not_zero(self):
        a, b = run_record("a"), run_record("b", cost=None)
        b["tasks"][0]["critical_failure"] = None
        result = metrics([a, b])
        for key in ("cost_per_hour", "cost_per_success", "critical_failure_rate"):
            self.assertIsNone(result["values"][key])
            self.assertIn(key, result["null_reasons"])
        self.assertEqual(result["critical_assessed_count"], 19)

    def test_percentile_rank_and_success_penalty_boundary(self):
        self.assertEqual(percentile(list(range(1, 21))), 19)
        record = run_record(count=100)
        for task in record["tasks"][95:]:
            task["status"] = "timeout"
        self.assertEqual(metrics([record])["values"]["p95_time_to_success_ms"], 9500)
        record["tasks"][94]["status"] = "cancelled"
        result = metrics([record])
        self.assertIsNone(result["values"]["p95_time_to_success_ms"])
        self.assertEqual(result["values"]["p95_terminal_ms"], 9500)

    def test_deadline_includes_boundary_and_all_task_denominators(self):
        record = run_record(count=3)
        record["tasks"][0]["status"] = "failure"
        self.assertEqual(
            metrics([record], 200)["values"]["success_within_deadline_rate"], 1 / 3
        )

    def test_zero_success_cost_and_elasticity_are_undefined(self):
        result = metrics([run_record(status="failure")])
        self.assertEqual(result["values"]["successes_per_hour"], 0)
        self.assertIsNone(result["values"]["cost_per_success"])
        self.assertEqual(elasticity(1, 0, 2, 5), (None, "nonpositive_throughput"))
        self.assertAlmostEqual(elasticity(1, 5, 2, 10)[0], 1)

    def test_occupancy_is_measured_not_inferred_from_latencies(self):
        record = run_record(n=2, duration=10)
        record["tasks"][0]["latency_ms"] = 100000
        self.assertIsNone(metrics([record])["values"]["effective_concurrency"])
        record["occupancy_intervals"] = [[0, 5], [0, 5]]
        result = metrics([validate_run(record)])["values"]
        self.assertEqual(result["effective_concurrency"], 1)
        self.assertEqual(result["occupancy_fraction"], 0.5)

    def test_aggregate_overflow_is_explicit(self):
        with self.assertRaises(ValidationError):
            metrics([run_record("a", cost=1e308), run_record("b", cost=1e308)])
        self.assertIsNone(
            metrics([run_record(duration=1e-320)])["values"]["successes_per_hour"]
        )


class DecisionTests(unittest.TestCase):
    def test_clear_observed_winner(self):
        runs = [
            run_record(f"{n}-{i}", n=n, duration=10 / n)
            for n in (1, 2)
            for i in range(2)
        ]
        result = analyze(runs, policy())["groups"][0]
        self.assertEqual(result["recommendation"]["concurrency"], 2)
        self.assertTrue(result["recommendation"]["confirmation_required"])
        self.assertAlmostEqual(result["elasticities"][0]["value"], 1)

    def test_one_repetition_cannot_recommend(self):
        self.assertEqual(
            analyze([run_record()], policy())["groups"][0]["recommendation"]["status"],
            "abstain",
        )

    def test_overlapping_uncertainty_abstains(self):
        runs = [
            run_record(f"{n}-{i}", n=n, duration=duration)
            for n in (1, 2)
            for i, duration in enumerate((1, 10, 2, 9))
        ]
        self.assertEqual(
            analyze(runs, policy())["groups"][0]["recommendation"]["reason"],
            "ranking_uncertain",
        )

    def test_zero_observed_critical_events_do_not_certify_zero_risk(self):
        runs = [run_record(str(i)) for i in range(4)]
        result = analyze(runs, policy(constraints={"max_critical_failure_rate": 0}))[
            "groups"
        ][0]
        self.assertGreater(
            result["candidates"][0]["intervals"]["critical_failure_rate"]["upper"], 0
        )
        self.assertEqual(result["recommendation"]["status"], "abstain")

    def test_unknown_critical_cost_and_currency_force_abstention(self):
        cases = [
            (policy(objective="cost_per_success", currency="EUR"), "cost"),
            (policy(constraints={"max_critical_failure_rate": 0.5}), "critical"),
            (policy(currency="USD"), "currency"),
        ]
        for selected_policy, kind in cases:
            runs = [
                run_record(str(i), cost=None if kind == "cost" else 1) for i in range(2)
            ]
            if kind == "critical":
                runs[0]["tasks"][0]["critical_failure"] = None
            result = analyze(runs, selected_policy)["groups"][0]
            self.assertEqual(result["recommendation"]["status"], "abstain")

    def test_violated_policy_is_reported(self):
        runs = [run_record(str(i), status="failure") for i in range(2)]
        result = analyze(runs, policy(constraints={"min_success_rate": 0.8}))["groups"][
            0
        ]
        self.assertEqual(
            result["recommendation"]["status"], "no_admissible_configuration"
        )

    def test_bootstrap_is_clustered_and_reproducible(self):
        runs = [
            run_record("a", count=100),
            run_record("b", count=100, status="failure"),
        ]
        first = analyze(runs, policy())
        self.assertEqual(first, analyze(list(reversed(runs)), policy()))
        bounds = first["groups"][0]["candidates"][0]["intervals"]["successes_per_hour"]
        self.assertEqual(bounds["lower"], 0)
        self.assertEqual(bounds["upper"], 360000)

    def test_aborted_rows_are_visible_but_never_ranked(self):
        record = run_record()
        record.update(run_status="aborted", abort_reason="critical_failure")
        result = analyze([record], policy())
        self.assertFalse(result["runs"][0]["included_in_comparisons"])
        self.assertEqual(result["groups"], [])

    def test_all_identity_dimensions_separate_comparisons(self):
        runs = [run_record("base")]
        for key in (
            "workload_id",
            "evaluator_id",
            "config_id",
            "configuration",
            "currency",
        ):
            record = run_record(key)
            record[key] = (
                {"model": "other", "hardware": "fixture", "quotas": {}}
                if key == "configuration"
                else "USD"
            )
            runs.append(record)
        self.assertEqual(len(analyze(runs, policy())["groups"]), 6)

    def test_aborted_trials_cannot_create_a_survivor_only_recommendation(self):
        runs = [run_record("a"), run_record("b"), run_record("aborted")]
        runs[-1].update(run_status="aborted", abort_reason="timeout")
        result = analyze(runs, policy())["groups"][0]
        self.assertEqual(result["recommendation"]["status"], "abstain")
        self.assertEqual(result["candidates"][0]["aborted_run_ids"], ["aborted"])
        runs[-1]["tasks"][0]["critical_failure"] = True
        result = analyze(runs, policy(abort_on_critical=True))["groups"][0]
        self.assertEqual(result["candidates"][0]["assessment"]["status"], "violated")

    def test_cost_objective_selects_lower_cost(self):
        runs = [
            run_record(f"{n}-{i}", n=n, cost=1 / n) for n in (1, 2) for i in range(2)
        ]
        result = analyze(runs, policy(objective="cost_per_success", currency="EUR"))
        self.assertEqual(result["groups"][0]["recommendation"]["concurrency"], 2)


class PlannerTests(unittest.TestCase):
    def test_original_reservation_survives_new_space_caps(self):
        s = space()
        record = campaign_run(s["candidates"][0], cost=None)
        record["reserved_cost"] = 0.1
        s["candidates"][0]["max_cost"] = 0.05
        result = plan([record], s, policy())["plan"]
        self.assertEqual(result["budget_used"], 0.1)

    def test_initial_coverage_selects_unmeasured_arm(self):
        s = space()
        first = plan([], s, policy())["plan"]["next_candidate"]
        result = plan([campaign_run(first)], s, policy())["plan"]
        self.assertNotEqual(
            result["next_candidate"]["candidate_id"], first["candidate_id"]
        )

    def test_decimal_budget_boundary(self):
        s = space()
        s["budget"]["total_cost"] = 0.3
        s["candidates"] = [s["candidates"][0]]
        c = s["candidates"][0]
        c["max_cost"] = 0.2
        result = plan([campaign_run(c, cost=0.1)], s, policy())["plan"]
        self.assertEqual(result["status"], "propose")
        c["max_cost"] = 0.20001
        self.assertEqual(
            plan([campaign_run(c, cost=0.1)], s, policy())["plan"]["status"], "stop"
        )

    def test_unknown_cost_reserves_cap_and_breach_stops(self):
        s = space()
        run = campaign_run(s["candidates"][0], cost=None)
        run["reserved_cost"] = 0.1
        result = plan([run], s, policy())["plan"]
        self.assertEqual(result["budget_used"], 0.1)
        self.assertEqual(result["unknown_cost_run_ids"], ["r1"])
        run["cost_total"] = 0.11
        self.assertEqual(
            plan([run], s, policy())["plan"]["reason"], "runner_cost_cap_breached"
        )

    def test_unknown_historical_bill_without_reservation_stops_dispatch(self):
        s = space()
        run = campaign_run(s["candidates"][0], cost=None)
        result = plan([run], s, policy())["plan"]
        self.assertEqual(result["status"], "stop")
        self.assertEqual(result["reason"], "unknown_cost_without_original_reservation")
        self.assertIsNone(result["budget_used"])
        self.assertIsNone(result["budget_remaining"])

    def test_run_budget_and_critical_hold(self):
        s = space()
        record = campaign_run(s["candidates"][0])
        s["budget"]["max_runs"] = 1
        self.assertEqual(
            plan([record], s, policy())["plan"]["reason"], "run_budget_exhausted"
        )
        s["budget"]["max_runs"] = 10
        record["tasks"][0]["critical_failure"] = True
        result = plan([record], s, policy(abort_on_critical=True))["plan"]
        self.assertEqual(
            result["candidate_evidence"][0]["hold_reason"], "critical_policy_hold"
        )

    def test_timeout_is_cooled_down_not_permanently_pruned(self):
        s = space(reprobe_after=1)
        record = campaign_run(s["candidates"][0])
        record.update(run_status="aborted", abort_reason="runner_timeout")
        held = plan([record], s, policy())["plan"]["candidate_evidence"][0]
        self.assertEqual(held["hold_reason"], "abort_cooldown")
        later = campaign_run(s["candidates"][1], "r2")
        resumed = plan([record, later], s, policy())["plan"]["candidate_evidence"][0]
        self.assertIsNone(resumed["hold_reason"])

    def test_sequential_bound_accounts_for_looks_and_arms(self):
        runs = [run_record(str(i), count=1) for i in range(100)]
        for record in runs:
            record["tasks"][0]["critical_failure"] = True
        a, b = critical_sequence(runs, 0.01, 1), critical_sequence(runs, 0.01, 10)
        self.assertGreater(a["lower"], 0.5)
        self.assertLess(b["lower"], a["lower"])
        runs[0]["tasks"][0]["critical_failure"] = None
        self.assertIsNone(critical_sequence(runs, 0.01, 1)["lower"])

    def test_control_drift_stops_pooling_regimes(self):
        s = space()
        c = s["candidates"][0]
        runs = [campaign_run(c, str(i), duration=1 if i < 3 else 0.1) for i in range(4)]
        result = plan(runs, s, policy())["plan"]
        self.assertIn("possible_control_drift", result["reason"])

    def test_foreign_history_and_changed_config_rejected(self):
        s = space()
        for key, value in (
            ("campaign_id", "other"),
            ("concurrency", 999),
            ("candidate_id", "other"),
        ):
            record = campaign_run(s["candidates"][0])
            record[key] = value
            with self.subTest(key=key), self.assertRaises(ValidationError):
                plan([record], s, policy())

    def test_space_rejects_duplicate_arms_and_invalid_caps(self):
        s = space()
        s["candidates"].append(copy.deepcopy(s["candidates"][0]))
        with self.assertRaises(ValidationError):
            validate_space(s)
        s = space()
        s["candidates"][0]["max_cost"] = 0.001
        with self.assertRaises(ValidationError):
            validate_space(s)

    def test_currency_mismatch_rejected_before_dispatch(self):
        with self.assertRaises(ValidationError):
            plan([], space(), policy(currency="USD"))


class ReportTests(unittest.TestCase):
    def test_untrusted_identity_is_escaped_and_json_is_strict(self):
        record = run_record()
        record["workload_id"] = (
            "<script>alert(1)</script>|`![tracking](https://example.invalid)"
        )
        report = envelope("analysis", analyze([record], policy()), [], policy())
        text = markdown(report)
        self.assertNotIn("<script>", text)
        self.assertIn("&lt;script&gt;", text)
        self.assertIn("&#124;", text)
        self.assertNotIn("![tracking]", text)
        json.dumps(report, allow_nan=False)

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected = root / "report.json"
            protected.write_text("original")
            report = envelope(
                "analysis", analyze([run_record()], policy()), [], policy()
            )
            with self.assertRaises(ValidationError):
                write_reports(root, "report", report, [protected])
            self.assertEqual(protected.read_text(), "original")


if __name__ == "__main__":
    unittest.main()
