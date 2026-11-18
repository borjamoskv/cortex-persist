# Copyright 2026 Borja Moskv (borjamoskv)
"""Cost-aware finite-arm planning; no unvalidated predictive extrapolation."""

from __future__ import annotations

import math
from decimal import Decimal, localcontext
from statistics import median

from .contract import (
    IDENTITY_FIELDS,
    fields,
    group_key,
    identifier,
    integer,
    number,
    require,
    validate_identity,
)
from .decision import analyze
from .metrics import metrics


def money(value):
    return Decimal(str(value))


def validate_space(space):
    fields(
        space,
        {"schema_version", "campaign_id", "budget", "candidates"},
        {"control_every", "reprobe_after", "drift_tolerance", "sequential_alpha"},
        "space",
    )
    require(
        type(space["schema_version"]) is int and space["schema_version"] == 1,
        "unsupported space schema_version",
    )
    identifier(space["campaign_id"], "campaign_id")
    fields(space["budget"], {"currency", "total_cost", "max_runs"}, set(), "budget")
    number(space["budget"]["total_cost"], "budget.total_cost", positive=True)
    integer(space["budget"]["max_runs"], "budget.max_runs")
    require(
        isinstance(space["candidates"], list) and bool(space["candidates"]),
        "candidates must be nonempty",
    )
    seen, arms = set(), set()
    for candidate in space["candidates"]:
        fields(
            candidate,
            IDENTITY_FIELDS
            | {
                "candidate_id",
                "concurrency",
                "expected_cost",
                "max_cost",
                "timeout_seconds",
                "task_count",
            },
            set(),
            "candidate",
        )
        validate_identity(candidate)
        identifier(candidate["candidate_id"], "candidate_id")
        require(candidate["candidate_id"] not in seen, "duplicate candidate_id")
        seen.add(candidate["candidate_id"])
        integer(candidate["concurrency"], "concurrency")
        integer(candidate["task_count"], "task_count")
        number(candidate["expected_cost"], "expected_cost", positive=True)
        number(candidate["max_cost"], "max_cost", positive=True)
        number(candidate["timeout_seconds"], "timeout_seconds", positive=True)
        require(
            candidate["expected_cost"] <= candidate["max_cost"],
            "expected_cost exceeds max_cost",
        )
        require(
            candidate["currency"] == space["budget"]["currency"],
            "budget currency mismatch",
        )
        arm = (group_key(candidate), candidate["concurrency"])
        require(arm not in arms, "duplicate experimental arm")
        arms.add(arm)
    result = {
        "control_every": 5,
        "reprobe_after": 3,
        "drift_tolerance": 0.5,
        "sequential_alpha": 0.01,
    } | space
    integer(result["control_every"], "control_every")
    integer(result["reprobe_after"], "reprobe_after")
    number(result["drift_tolerance"], "drift_tolerance", positive=True)
    number(result["sequential_alpha"], "sequential_alpha", positive=True)
    require(result["sequential_alpha"] < 0.5, "sequential_alpha must be below 0.5")
    return result


def validate_history(runs, space):
    candidates = {c["candidate_id"]: c for c in space["candidates"]}
    for run in runs:
        require(
            run.get("campaign_id") == space["campaign_id"],
            "history belongs to another campaign",
        )
        require(
            run.get("candidate_id") in candidates,
            "history candidate is absent from space",
        )
        candidate = candidates[run["candidate_id"]]
        require(
            group_key(run) == group_key(candidate)
            and run["concurrency"] == candidate["concurrency"],
            "history configuration differs from candidate",
        )
        if run.get("run_status", "completed") == "completed":
            require(
                len(run["tasks"]) == candidate["task_count"],
                "completed run task_count differs from space",
            )
        else:
            require(
                len(run["tasks"]) <= candidate["task_count"],
                "aborted run exceeds task_count",
            )


def critical_sequence(runs, alpha, arm_count):
    """Union-bound confidence sequence over independent, bounded run means.

    alpha/(arm_count*t*(t+1)) sums to alpha across arms and all looks.
    Unknown classifications suspend the inference instead of dropping records.
    """
    if not runs or any(t["critical_failure"] is None for r in runs for t in r["tasks"]):
        return {
            "lower": None,
            "upper": None,
            "reason": "missing_complete_assessed_runs",
        }
    rates = [
        sum(t["critical_failure"] is True for t in r["tasks"]) / len(r["tasks"])
        for r in runs
    ]
    t = len(rates)
    tail = alpha / (arm_count * t * (t + 1))
    radius = math.sqrt(math.log(2 / tail) / (2 * t))
    mean = sum(rates) / t
    return {
        "lower": max(0, mean - radius),
        "upper": min(1, mean + radius),
        "method": "run_mean_hoeffding_alpha_spending",
        "looks": t,
        "family_error_budget": alpha,
        "assumption": "independent fixed-size runs with stable distribution",
    }


def plan(runs, space, policy):
    validate_history(runs, space)
    require(
        "currency" not in policy or policy["currency"] == space["budget"]["currency"],
        "policy and campaign currencies differ",
    )
    candidates = {c["candidate_id"]: c for c in space["candidates"]}
    report = analyze(runs, policy)
    state = {
        "status": "stop",
        "reason": "",
        "next_candidate": None,
        "budget_used": None,
        "budget_remaining": None,
        "budget_currency": space["budget"]["currency"],
        "attempts": len(runs),
        "unknown_cost_run_ids": [r["run_id"] for r in runs if r["cost_total"] is None],
        "budget_assumption": "unknown costs reserve the original recorded maximum; "
        "external billing is not enforced here",
        "candidate_evidence": [],
    }
    if any(r["cost_total"] is None and "reserved_cost" not in r for r in runs):
        state["reason"] = "unknown_cost_without_original_reservation"
        return report | {"plan": state}
    with localcontext() as context:
        # Preserve small reservations even beside very large finite amounts.
        context.prec = 1000
        used = sum(
            (
                money(
                    r["cost_total"]
                    if r["cost_total"] is not None
                    else r["reserved_cost"]
                )
                for r in runs
            ),
            Decimal(0),
        )
        remaining = money(space["budget"]["total_cost"]) - used
    number(float(used), "total campaign cost")
    state.update(
        budget_used=float(used), budget_remaining=float(max(Decimal(0), remaining))
    )
    if any(
        r["cost_total"] is not None
        and money(r["cost_total"])
        > money(r.get("reserved_cost", candidates[r["candidate_id"]]["max_cost"]))
        for r in runs
    ):
        state["reason"] = "runner_cost_cap_breached"
        return report | {"plan": state}
    if len(runs) >= space["budget"]["max_runs"]:
        state["reason"] = "run_budget_exhausted"
        return report | {"plan": state}
    indexed = {
        (group_key(g["identity"]), c["concurrency"]): c
        for g in report["groups"]
        for c in g["candidates"]
    }
    available = []
    drift = False
    for candidate in sorted(candidates.values(), key=lambda c: c["candidate_id"]):
        cid = candidate["candidate_id"]
        attempts = [(i, r) for i, r in enumerate(runs) if r["candidate_id"] == cid]
        complete = [
            r for _, r in attempts if r.get("run_status", "completed") == "completed"
        ]
        sequence = critical_sequence(
            complete, space["sequential_alpha"], len(candidates)
        )
        reason = None
        if policy["abort_on_critical"] and any(
            t["critical_failure"] is True for _, r in attempts for t in r["tasks"]
        ):
            reason = "critical_policy_hold"
        # Statistical violation pauses the arm; control re-probes are permitted
        # after other trials, to avoid permanently deleting a transient regime.
        threshold = policy["constraints"].get("max_critical_failure_rate")
        recently_tried = (
            bool(attempts) and len(runs) - 1 - attempts[-1][0] < space["reprobe_after"]
        )
        if (
            reason is None
            and threshold is not None
            and sequence["lower"] is not None
            and sequence["lower"] > threshold
        ):
            if recently_tried:
                reason = "sequential_critical_hold"
        if (
            reason is None
            and attempts
            and attempts[-1][1].get("run_status") == "aborted"
            and recently_tried
        ):
            reason = "abort_cooldown"
        if money(candidate["max_cost"]) > remaining:
            reason = "insufficient_budget_for_reservation"
        evidence = indexed.get((group_key(candidate), candidate["concurrency"]))
        # Control arms are the lowest concurrency within an identity group.
        is_control = candidate["concurrency"] == min(
            c["concurrency"]
            for c in candidates.values()
            if group_key(c) == group_key(candidate)
        )
        if is_control and len(complete) >= 4:
            throughput = [
                metrics([r])["values"]["successes_per_hour"] for r in complete
            ]
            reference = median(throughput[:-1])
            if (
                reference > 0
                and abs(throughput[-1] / reference - 1) > space["drift_tolerance"]
            ):
                drift = True
        info = {
            "candidate_id": cid,
            "completed_runs": len(complete),
            "hold_reason": reason,
            "critical_sequence": sequence,
        }
        state["candidate_evidence"].append(info)
        if reason is None:
            available.append((candidate, info, evidence, is_control))
    if drift:
        state["reason"] = "possible_control_drift_relabel_configuration_before_resuming"
        return report | {"plan": state}
    if not available:
        state["reason"] = "budget_or_policy_holds"
        return report | {"plan": state}
    cold = [
        entry for entry in available if entry[1]["completed_runs"] < policy["min_runs"]
    ]
    if cold:
        chosen = min(
            cold,
            key=lambda e: (
                e[1]["completed_runs"],
                e[0]["expected_cost"],
                e[0]["candidate_id"],
            ),
        )
        reason = "initial_coverage_and_repetitions"
    else:
        # Only finish if every arm has sufficient completed evidence or a hard
        # critical hold; a merely unaffordable/unobserved arm cannot be ignored.
        covered = all(
            e["completed_runs"] >= policy["min_runs"]
            or e["hold_reason"] == "critical_policy_hold"
            for e in state["candidate_evidence"]
        )
        resolved = report["groups"] and all(
            g["recommendation"]["status"] == "recommended" for g in report["groups"]
        )
        if covered and resolved:
            state["reason"] = (
                "exploratory_candidates_identified_independent_confirmation_required"
            )
            return report | {"plan": state}
        controls = [e for e in available if e[3]]
        if len(runs) % space["control_every"] == 0 and controls:
            chosen = controls[(len(runs) // space["control_every"]) % len(controls)]
            reason = "control_probe_for_drift"
        else:

            def score(entry):
                candidate, info, evidence, _ = entry
                if evidence is None:
                    return float("inf")
                bounds = evidence["intervals"][policy["objective"]]
                if bounds["lower"] is None:
                    return 1 / candidate["expected_cost"]
                midpoint = (bounds["lower"] + bounds["upper"]) / 2
                width = (bounds["upper"] - bounds["lower"]) / max(abs(midpoint), 1e-12)
                return (width + 1 / (1 + info["completed_runs"])) / candidate[
                    "expected_cost"
                ]

            chosen = max(available, key=score)
            reason = "relative_uncertainty_per_expected_cost_heuristic"
    state.update(status="propose", reason=reason, next_candidate=chosen[0])
    return report | {"plan": state}
