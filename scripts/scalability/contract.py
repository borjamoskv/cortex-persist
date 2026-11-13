# Copyright 2026 Borja Moskv (borjamoskv)
"""Strict, versioned input contracts shared by all scalability commands."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from pathlib import Path


class ValidationError(ValueError):
    """Invalid input; never a benchmark regression."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def number(value, name: str, *, minimum: float = 0, positive: bool = False):
    require(type(value) in (int, float), f"{name}: expected a number")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    require(finite, f"{name}: expected a finite number")
    require(value > minimum if positive else value >= minimum, f"{name}: out of range")
    return value


def integer(value, name: str, *, minimum: int = 1) -> int:
    require(
        type(value) is int and value >= minimum,
        f"{name}: expected integer >= {minimum}",
    )
    return value


def identifier(value, name: str) -> str:
    require(
        isinstance(value, str) and bool(value.strip()),
        f"{name}: expected nonempty string",
    )
    require(
        len(value) <= 512 and not any(ord(c) < 32 for c in value),
        f"{name}: invalid identifier",
    )
    return value


def fields(value, required: set[str], optional: set[str], name: str) -> None:
    require(isinstance(value, dict), f"{name}: expected object")
    require(
        not required - value.keys(),
        f"{name}: missing fields {sorted(required - value.keys())}",
    )
    require(
        not value.keys() - required - optional,
        f"{name}: unknown fields {sorted(value.keys() - required - optional)}",
    )


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValidationError(f"non-finite JSON number: {value}")


def _finite_tree(value) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key.encode("utf-8")
            _finite_tree(item)
    elif isinstance(value, list):
        for item in value:
            _finite_tree(item)
    elif type(value) in (int, float):
        number(abs(value), "JSON number")
    elif isinstance(value, str):
        value.encode("utf-8")  # Reject lone surrogate code points.


def decode(data: str | bytes):
    try:
        value = json.loads(
            data, object_pairs_hook=_pairs, parse_constant=_reject_constant
        )
        _finite_tree(value)
        return value
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ValidationError(str(exc)) from exc


def canonical(value) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


def fingerprint(value) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def read_json(path: Path):
    data = path.read_bytes()
    return decode(data), {"path": str(path), "sha256": hashlib.sha256(data).hexdigest()}


IDENTITY_FIELDS = {
    "workload_id",
    "evaluator_id",
    "config_id",
    "configuration",
    "currency",
}


def validate_identity(value) -> None:
    for key in ("workload_id", "evaluator_id", "config_id"):
        identifier(value[key], key)
    require(
        isinstance(value["currency"], str)
        and re.fullmatch(r"[A-Z]{3}", value["currency"]) is not None,
        "currency: expected ISO-style code",
    )
    configuration = value["configuration"]
    require(isinstance(configuration, dict), "configuration: expected object")
    require(
        {"model", "hardware", "quotas"} <= configuration.keys(),
        "configuration: model, hardware and quotas are required",
    )
    identifier(configuration["model"], "configuration.model")
    identifier(configuration["hardware"], "configuration.hardware")
    require(
        isinstance(configuration["quotas"], dict),
        "configuration.quotas: expected object",
    )
    _finite_tree(configuration)


def identity(run) -> dict:
    return {key: run[key] for key in sorted(IDENTITY_FIELDS)}


def group_key(run) -> str:
    return canonical(identity(run))


def validate_task(task) -> dict:
    fields(task, {"task_id", "status", "latency_ms", "critical_failure"}, set(), "task")
    identifier(task["task_id"], "task_id")
    require(
        isinstance(task["status"], str)
        and task["status"] in {"success", "failure", "timeout", "cancelled"},
        "task.status: expected terminal state",
    )
    number(task["latency_ms"], "latency_ms")
    require(
        task["critical_failure"] is None or type(task["critical_failure"]) is bool,
        "critical_failure: expected boolean or null",
    )
    return task


def validate_run(run) -> dict:
    fields(
        run,
        IDENTITY_FIELDS
        | {
            "schema_version",
            "run_id",
            "concurrency",
            "duration_seconds",
            "cost_total",
            "tasks",
        },
        {
            "run_status",
            "abort_reason",
            "reserved_cost",
            "occupancy_intervals",
            "campaign_id",
            "candidate_id",
        },
        "run",
    )
    require(
        type(run["schema_version"]) is int and run["schema_version"] == 1,
        "unsupported run schema_version",
    )
    identifier(run["run_id"], "run_id")
    validate_identity(run)
    integer(run["concurrency"], "concurrency")
    number(run["duration_seconds"], "duration_seconds", positive=True)
    if run["cost_total"] is not None:
        number(run["cost_total"], "cost_total")
    if "reserved_cost" in run:
        number(run["reserved_cost"], "reserved_cost")
    status = run.get("run_status", "completed")
    require(
        isinstance(status, str) and status in {"completed", "aborted"},
        "invalid run_status",
    )
    if status == "aborted":
        identifier(run.get("abort_reason"), "abort_reason")
    else:
        require("abort_reason" not in run, "completed run cannot have abort_reason")
    require(isinstance(run["tasks"], list), "tasks: expected array")
    require(bool(run["tasks"]) or status == "aborted", "completed run has no tasks")
    seen = set()
    for task in run["tasks"]:
        validate_task(task)
        require(task["task_id"] not in seen, f"duplicate task_id: {task['task_id']}")
        seen.add(task["task_id"])
    require(
        ("campaign_id" in run) == ("candidate_id" in run),
        "campaign_id and candidate_id must occur together",
    )
    for key in ("campaign_id", "candidate_id"):
        if key in run:
            identifier(run[key], key)
    if "occupancy_intervals" in run:
        intervals = run["occupancy_intervals"]
        require(isinstance(intervals, list), "occupancy_intervals: expected array")
        events = []
        for pair in intervals:
            require(
                isinstance(pair, list) and len(pair) == 2,
                "occupancy interval: expected [start, end]",
            )
            start, end = pair
            number(start, "occupancy start")
            number(end, "occupancy end")
            require(
                start < end <= run["duration_seconds"], "occupancy interval outside run"
            )
            events.extend(((start, 1), (end, -1)))
        active = 0
        for _, delta in sorted(events):  # End before start at the same timestamp.
            active += delta
            require(
                active <= run["concurrency"], "occupancy exceeds nominal concurrency"
            )
    return run


def load_runs(paths: list[Path], *, allow_empty: bool = False):
    runs, sources, seen = [], [], set()
    for path in paths:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for line_number, data in enumerate(stream, 1):
                digest.update(data)
                require(bool(data.strip()), f"{path}:{line_number}: blank JSONL record")
                try:
                    run = validate_run(decode(data))
                    require(
                        run["run_id"] not in seen, f"duplicate run_id: {run['run_id']}"
                    )
                except ValidationError as exc:
                    raise ValidationError(f"{path}:{line_number}: {exc}") from exc
                seen.add(run["run_id"])
                runs.append(run)
        sources.append({"path": str(path), "sha256": digest.hexdigest()})
    require(bool(runs) or allow_empty, "input contains no runs")
    return runs, sources


DEFAULT_POLICY = {
    "schema_version": 1,
    "objective": "successes_per_hour",
    "min_runs": 5,
    "min_tasks": 20,
    "confidence": 0.95,
    "bootstrap_samples": 1000,
    "seed": 0,
    "relative_tolerance": 0.05,
    "constraints": {},
    "abort_on_critical": False,
}
CONSTRAINTS = {
    "min_success_rate": ("success_rate", "min"),
    "min_successes_per_hour": ("successes_per_hour", "min"),
    "max_cost_per_hour": ("cost_per_hour", "max"),
    "max_cost_per_success": ("cost_per_success", "max"),
    "max_p95_terminal_ms": ("p95_terminal_ms", "max"),
    "max_critical_failure_rate": ("critical_failure_rate", "max"),
    "min_success_within_deadline_rate": ("success_within_deadline_rate", "min"),
}


def validate_policy(value: dict | None) -> dict:
    value = {} if value is None else value
    fields(value, set(), set(DEFAULT_POLICY) | {"deadline_ms", "currency"}, "policy")
    policy = copy.deepcopy(DEFAULT_POLICY) | copy.deepcopy(value)
    require(
        type(policy["schema_version"]) is int and policy["schema_version"] == 1,
        "unsupported policy schema_version",
    )
    require(
        policy["objective"] in ("successes_per_hour", "cost_per_success"),
        "invalid objective",
    )
    integer(policy["min_runs"], "min_runs", minimum=2)
    integer(policy["min_tasks"], "min_tasks")
    integer(policy["bootstrap_samples"], "bootstrap_samples", minimum=100)
    require(policy["bootstrap_samples"] <= 10000, "bootstrap_samples exceeds 10000")
    integer(policy["seed"], "seed", minimum=0)
    number(policy["confidence"], "confidence")
    require(0.5 < policy["confidence"] < 1, "confidence must be between 0.5 and 1")
    number(policy["relative_tolerance"], "relative_tolerance")
    require(policy["relative_tolerance"] < 1, "relative_tolerance must be below 1")
    require(
        type(policy["abort_on_critical"]) is bool, "abort_on_critical: expected boolean"
    )
    fields(policy["constraints"], set(), set(CONSTRAINTS), "constraints")
    for key, limit in policy["constraints"].items():
        number(limit, key)
        if key.endswith("rate"):
            require(limit <= 1, f"{key}: expected fraction <= 1")
    if "deadline_ms" in policy:
        number(policy["deadline_ms"], "deadline_ms", positive=True)
    require(
        "min_success_within_deadline_rate" not in policy["constraints"]
        or "deadline_ms" in policy,
        "deadline constraint requires deadline_ms",
    )
    monetary = policy["objective"] == "cost_per_success" or any(
        "cost" in k for k in policy["constraints"]
    )
    if monetary or "currency" in policy:
        require(
            isinstance(policy.get("currency"), str)
            and re.fullmatch(r"[A-Z]{3}", policy["currency"]) is not None,
            "monetary policy requires currency",
        )
    return policy
