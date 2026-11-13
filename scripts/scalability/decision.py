# Copyright 2026 Borja Moskv (borjamoskv)
"""Exploratory cluster uncertainty and policy decisions, never a CI gate."""

from __future__ import annotations

import math
import random
from collections import defaultdict

from .contract import CONSTRAINTS, fingerprint, group_key, identity
from .metrics import elasticity, metrics, percentile


def uncertainty(runs, policy):
    point = metrics(runs, policy.get("deadline_ms"))
    names = point["values"]
    intervals = {
        name: {"lower": None, "upper": None, "reason": "insufficient_runs"}
        for name in names
    }
    if len(runs) < policy["min_runs"]:
        return intervals, {}
    alpha = 1 - policy["confidence"]
    seed = int(fingerprint([policy["seed"], [r["run_id"] for r in runs]])[:16], 16)
    rng = random.Random(seed)
    samples = {name: [] for name in names}
    for _ in range(policy["bootstrap_samples"]):
        draw = [runs[rng.randrange(len(runs))] for _ in runs]
        values = metrics(draw, policy.get("deadline_ms"))["values"]
        for name, value in values.items():
            samples[name].append(value)
    for name, values in samples.items():
        if any(v is None for v in values):
            intervals[name] = {
                "lower": None,
                "upper": None,
                "reason": point["null_reasons"].get(name, "undefined_bootstrap_draw"),
            }
        else:
            intervals[name] = {
                "lower": percentile(values, alpha / 2),
                "upper": percentile(values, 1 - alpha / 2),
                "method": "run_cluster_percentile_bootstrap",
                "confidence": policy["confidence"],
            }
    # Whole runs are independent units. Never certify a zero rare-event rate
    # merely because every observed bootstrap replicate contains zero failures.
    count = point["task_count"]
    weights = [len(r["tasks"]) / count for r in runs]
    radius = math.sqrt(sum(w * w for w in weights) * math.log(2 / alpha) / 2)
    for name in (
        "success_rate",
        "critical_failure_rate",
        "success_within_deadline_rate",
    ):
        value = point["values"][name]
        if value is not None:
            intervals[name] = {
                "lower": max(0, value - radius),
                "upper": min(1, value + radius),
                "method": "weighted_run_hoeffding",
                "confidence": policy["confidence"],
            }
    return intervals, samples


def assess(summary, intervals, policy, currency):
    violations, unresolved = [], []
    if (
        summary["run_count"] < policy["min_runs"]
        or summary["task_count"] < policy["min_tasks"]
    ):
        unresolved.append("insufficient_repetitions_or_tasks")
    if "currency" in policy and currency != policy["currency"]:
        unresolved.append("policy_currency_mismatch")
    for name, threshold in policy["constraints"].items():
        metric, direction = CONSTRAINTS[name]
        point = summary["values"][metric]
        bound = intervals[metric]["lower" if direction == "min" else "upper"]
        if point is None:
            unresolved.append(f"{name}:unknown")
        elif point < threshold if direction == "min" else point > threshold:
            violations.append(name)
        elif bound is None or (
            bound < threshold if direction == "min" else bound > threshold
        ):
            unresolved.append(f"{name}:uncertain")
    objective = policy["objective"]
    if summary["values"][objective] is None or intervals[objective]["lower"] is None:
        unresolved.append("objective_unknown_or_uncertain")
    return {
        "status": "violated"
        if violations
        else "uncertain"
        if unresolved
        else "admissible",
        "violations": violations,
        "unresolved": unresolved,
    }


def recommend(candidates, policy):
    contenders = [c for c in candidates if c["assessment"]["status"] != "violated"]
    eligible = [c for c in contenders if c["assessment"]["status"] == "admissible"]
    base = {
        "concurrency": None,
        "scope": "observed_concurrencies_only",
        "confirmation_required": True,
        "alternatives": [c["concurrency"] for c in eligible],
    }
    if not contenders:
        return base | {
            "status": "no_admissible_configuration",
            "reason": "observed_policy_violations",
        }
    metric = policy["objective"]
    if not eligible or any(c["intervals"][metric]["lower"] is None for c in contenders):
        return base | {"status": "abstain", "reason": "insufficient_evidence"}
    tolerance = policy["relative_tolerance"]
    if metric == "successes_per_hour":
        frontier = max(c["intervals"][metric]["upper"] for c in contenders)
        accepted = [
            c
            for c in eligible
            if c["intervals"][metric]["lower"] > 0
            and c["intervals"][metric]["lower"] >= (1 - tolerance) * frontier
        ]
    else:
        frontier = min(c["intervals"][metric]["lower"] for c in contenders)
        accepted = [
            c
            for c in eligible
            if c["intervals"][metric]["upper"] <= (1 + tolerance) * frontier
        ]
    if not accepted:
        return base | {"status": "abstain", "reason": "ranking_uncertain"}
    selected = min(accepted, key=lambda c: c["concurrency"])
    return base | {
        "status": "recommended",
        "concurrency": selected["concurrency"],
        "reason": "within_tolerance_by_exploratory_bounds",
    }


def analyze(runs, policy):
    groups = defaultdict(lambda: defaultdict(list))
    aborted = defaultdict(list)
    individuals = []
    for run in sorted(runs, key=lambda r: r["run_id"]):
        completed = run.get("run_status", "completed") == "completed"
        individuals.append(
            {
                "run_id": run["run_id"],
                "identity": identity(run),
                "concurrency": run["concurrency"],
                "included_in_comparisons": completed,
                "run_status": run.get("run_status", "completed"),
                "abort_reason": run.get("abort_reason"),
                "reserved_cost": run.get("reserved_cost"),
                "metrics": metrics([run], policy.get("deadline_ms")),
            }
        )
        if completed:
            groups[group_key(run)][run["concurrency"]].append(run)
        else:
            aborted[(group_key(run), run["concurrency"])].append(run)
    output = []
    for key, by_n in sorted(groups.items()):
        candidates, bootstraps = [], {}
        first = next(iter(by_n.values()))[0]
        for concurrency, repetitions in sorted(by_n.items()):
            summary = metrics(repetitions, policy.get("deadline_ms"))
            intervals, samples = uncertainty(repetitions, policy)
            excluded = aborted[(key, concurrency)]
            assessment = assess(summary, intervals, policy, first["currency"])
            if excluded:
                assessment["unresolved"].append("aborted_attempts_require_review")
                if policy["abort_on_critical"] and any(
                    t["critical_failure"] is True for r in excluded for t in r["tasks"]
                ):
                    assessment["violations"].append("critical_abort_policy")
                assessment["status"] = (
                    "violated" if assessment["violations"] else "uncertain"
                )
            candidates.append(
                {
                    "concurrency": concurrency,
                    "run_ids": [r["run_id"] for r in repetitions],
                    "metrics": summary,
                    "intervals": intervals,
                    "assessment": assessment,
                    "aborted_run_ids": [r["run_id"] for r in excluded],
                }
            )
            bootstraps[concurrency] = samples
        elasticities = []
        for left, right in zip(candidates, candidates[1:]):
            n1, n2 = left["concurrency"], right["concurrency"]
            value, reason = elasticity(
                n1,
                left["metrics"]["values"]["successes_per_hour"],
                n2,
                right["metrics"]["values"]["successes_per_hour"],
            )
            draws = [
                elasticity(n1, x, n2, y)[0]
                for x, y in zip(
                    bootstraps[n1].get("successes_per_hour", []),
                    bootstraps[n2].get("successes_per_hour", []),
                )
            ]
            interval = {
                "lower": None,
                "upper": None,
                "reason": "insufficient_or_undefined_draws",
            }
            if draws and all(d is not None for d in draws):
                alpha = 1 - policy["confidence"]
                interval = {
                    "lower": percentile(draws, alpha / 2),
                    "upper": percentile(draws, 1 - alpha / 2),
                    "method": "independent_run_cluster_bootstrap",
                    "confidence": policy["confidence"],
                }
            elasticities.append(
                {
                    "from_concurrency": n1,
                    "to_concurrency": n2,
                    "value": value,
                    "null_reason": reason,
                    "interval": interval,
                }
            )
        output.append(
            {
                "group_id": fingerprint(key),
                "identity": identity(first),
                "candidates": candidates,
                "elasticities": elasticities,
                "recommendation": recommend(candidates, policy),
            }
        )
    return {"runs": individuals, "groups": output}
