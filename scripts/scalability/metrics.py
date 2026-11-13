# Copyright 2026 Borja Moskv (borjamoskv)
"""Finite-batch metrics. No steady-state or latent completion-time inference."""

from __future__ import annotations

import math

from .contract import ValidationError


def total(values):
    try:
        result = math.fsum(values)
    except (OverflowError, ValueError) as exc:
        raise ValidationError("aggregate exceeds finite numeric range") from exc
    if not math.isfinite(result):
        raise ValidationError("aggregate exceeds finite numeric range")
    return result


def percentile(values, probability=0.95):
    if not values:
        return None
    return sorted(values)[max(0, math.ceil(probability * len(values)) - 1)]


def metrics(runs: list[dict], deadline_ms=None) -> dict:
    tasks = [task for run in runs for task in run["tasks"]]
    duration = total(run["duration_seconds"] for run in runs)
    successes = [task for task in tasks if task["status"] == "success"]
    assessed = sum(task["critical_failure"] is not None for task in tasks)
    critical = sum(task["critical_failure"] is True for task in tasks)
    cost = (
        None
        if any(run["cost_total"] is None for run in runs)
        else total(run["cost_total"] for run in runs)
    )
    values, reasons = {}, {}

    def put(name, value, reason="non_finite_result"):
        if value is not None and not math.isfinite(value):
            value = None
        values[name] = value
        if value is None:
            reasons[name] = reason

    def ratio(name, numerator, denominator, missing="unknown_cost", scale=1):
        if numerator is None:
            put(name, None, missing)
        elif not denominator:
            put(name, None, "zero_denominator")
        else:
            put(name, numerator / denominator * scale)

    ratio("successes_per_hour", len(successes), duration, scale=3600)
    ratio("success_rate", len(successes), len(tasks))
    ratio("cost_per_hour", cost, duration, scale=3600)
    ratio("cost_per_success", cost, len(successes))
    put("p95_terminal_ms", percentile([t["latency_ms"] for t in tasks]), "no_tasks")
    rank = math.ceil(0.95 * len(tasks))
    if rank and len(successes) >= rank:
        put(
            "p95_time_to_success_ms",
            sorted(t["latency_ms"] for t in successes)[rank - 1],
        )
    else:
        put(
            "p95_time_to_success_ms",
            None,
            "no_tasks" if not rank else "non_success_mass_exceeds_5_percent",
        )
    if assessed == len(tasks):
        ratio("critical_failure_rate", critical, len(tasks))
    else:
        put("critical_failure_rate", None, "unknown_critical_classification")
    if deadline_ms is None:
        put("success_within_deadline_rate", None, "deadline_not_configured")
    else:
        ratio(
            "success_within_deadline_rate",
            sum(t["latency_ms"] <= deadline_ms for t in successes),
            len(tasks),
        )
    if all("occupancy_intervals" in run for run in runs):
        occupied = total(
            end - start for run in runs for start, end in run["occupancy_intervals"]
        )
        ratio("effective_concurrency", occupied, duration)
        nominal_slot_time = total(
            run["concurrency"] * run["duration_seconds"] for run in runs
        )
        ratio("occupancy_fraction", occupied, nominal_slot_time)
    else:
        put("effective_concurrency", None, "occupancy_not_measured")
        put("occupancy_fraction", None, "occupancy_not_measured")
    return {
        "run_count": len(runs),
        "task_count": len(tasks),
        "success_count": len(successes),
        "critical_assessed_count": assessed,
        "critical_count": critical,
        "status_counts": {
            s: sum(t["status"] == s for t in tasks)
            for s in ("success", "failure", "timeout", "cancelled")
        },
        "duration_seconds": duration,
        "cost_total": cost,
        "values": values,
        "null_reasons": reasons,
    }


def elasticity(left_n, left_x, right_n, right_x):
    if left_x is None or right_x is None:
        return None, "unknown_throughput"
    if left_x <= 0 or right_x <= 0:
        return None, "nonpositive_throughput"
    if right_n <= left_n:
        return None, "nonincreasing_concurrency"
    value = (math.log(right_x) - math.log(left_x)) / (
        math.log(right_n) - math.log(left_n)
    )
    return (value, None) if math.isfinite(value) else (None, "non_finite_result")
