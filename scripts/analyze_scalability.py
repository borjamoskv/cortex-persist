#!/usr/bin/env python3
"""Analyze exported benchmark results without executing workloads or calling APIs."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile

SCHEMA_VERSION = 1
STATES = {"success", "failure", "timeout", "cancelled"}
LIMITS = (
    ("cost_per_hour", "budget_per_hour", "max"),
    ("success_rate", "min_success_rate", "min"),
    ("latency_p95_ms", "max_p95_ms", "max"),
    ("critical_failure_rate", "max_critical_failure_rate", "max"),
)
NOTICE = (
    "Observed benchmark throughput only. Results describe supplied measurements, "
    "not sustained production capacity or a statistical safety guarantee. "
    "Zero observed critical failures does not establish zero risk."
)


class ValidationError(ValueError):
    """Invalid input contract or unrepresentable numeric data."""


def object_value(value, where):
    if not isinstance(value, dict):
        raise ValidationError(f"{where}: expected an object")
    return value


def text_value(value, where):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{where}: expected a non-empty string")
    return value


def number(value, where, *, positive=False, maximum=None):
    if type(value) not in (int, float):
        raise ValidationError(f"{where}: expected a finite number")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite or value < 0 or (positive and value == 0):
        raise ValidationError(f"{where}: expected a finite {'positive' if positive else 'nonnegative'} number")
    if maximum is not None and value > maximum:
        raise ValidationError(f"{where}: must be <= {maximum}")
    return value


def positive_integer(value, where):
    if type(value) is not int or value < 1:
        raise ValidationError(f"{where}: expected a positive integer")
    return value


def currency(value, where):
    if not isinstance(value, str) or re.fullmatch(r"[A-Z]{3}", value) is None:
        raise ValidationError(f"{where}: expected a three-letter uppercase currency code")
    return value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValidationError(f"non-finite JSON number: {value}")


def parse_json(text, where):
    try:
        value = json.loads(text, object_pairs_hook=unique_object, parse_constant=invalid_constant)
        json.dumps(value, allow_nan=False)
        return value
    except (ValueError, OverflowError, RecursionError) as exc:
        raise ValidationError(f"{where}: {exc}") from exc


def read_source(path):
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path}: expected UTF-8") from exc
    return text, {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}


def validate_run(value, where):
    run = object_value(value, where)
    if type(run.get("schema_version")) is not int or run["schema_version"] != SCHEMA_VERSION:
        raise ValidationError(f"{where}: schema_version must be 1")
    for key in ("run_id", "workload_id", "evaluator_id"):
        text_value(run.get(key), f"{where}.{key}")
    positive_integer(run.get("concurrency"), f"{where}.concurrency")
    number(run.get("duration_s"), f"{where}.duration_s", positive=True)
    currency(run.get("currency"), f"{where}.currency")
    if "total_cost" not in run:
        raise ValidationError(f"{where}.total_cost: required; use null if unknown")
    if run["total_cost"] is not None:
        number(run["total_cost"], f"{where}.total_cost")
    config = object_value(run.get("configuration"), f"{where}.configuration")
    for key in ("model", "hardware", "quotas"):
        text_value(config.get(key), f"{where}.configuration.{key}")
    tasks = run.get("tasks")
    if not isinstance(tasks, list):
        raise ValidationError(f"{where}.tasks: expected an array")
    ids = set()
    for index, task in enumerate(tasks):
        location = f"{where}.tasks[{index}]"
        object_value(task, location)
        task_id = text_value(task.get("task_id"), f"{location}.task_id")
        if task_id in ids:
            raise ValidationError(f"{location}: duplicate task_id {task_id}")
        ids.add(task_id)
        if not isinstance(task.get("status"), str) or task["status"] not in STATES:
            raise ValidationError(f"{location}.status: expected a terminal status")
        number(task.get("latency_ms"), f"{location}.latency_ms")
        if "critical_failure" not in task or (
            task["critical_failure"] is not None and type(task["critical_failure"]) is not bool
        ):
            raise ValidationError(f"{location}.critical_failure: expected boolean or null")
    return run


def load_runs(path):
    text, source = read_source(path)
    runs, ids = [], set()
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        where = f"{path}:{line_number}"
        run = validate_run(parse_json(line, where), where)
        if run["run_id"] in ids:
            raise ValidationError(f"{where}: duplicate run_id {run['run_id']}")
        ids.add(run["run_id"])
        runs.append(run)
    if not runs:
        raise ValidationError(f"{path}: no benchmark runs")
    return runs, source


def load_policy(path):
    text, source = read_source(path)
    policy = object_value(parse_json(text, str(path)), str(path))
    allowed = {
        "schema_version", "currency", "budget_per_hour", "min_success_rate",
        "max_p95_ms", "max_critical_failure_rate", "min_repetitions",
    }
    if set(policy) - allowed:
        raise ValidationError(f"{path}: unknown policy fields {sorted(set(policy) - allowed)}")
    if type(policy.get("schema_version")) is not int or policy["schema_version"] != SCHEMA_VERSION:
        raise ValidationError(f"{path}: schema_version must be 1")
    currency(policy.get("currency"), f"{path}.currency")
    for key in ("budget_per_hour", "max_p95_ms"):
        number(policy.get(key), f"{path}.{key}")
    for key in ("min_success_rate", "max_critical_failure_rate"):
        number(policy.get(key), f"{path}.{key}", maximum=1)
    policy = dict(policy)
    policy["min_repetitions"] = positive_integer(
        policy.get("min_repetitions", 3), f"{path}.min_repetitions"
    )
    return policy, source


def finite_sum(values):
    try:
        result = math.fsum(values)
    except OverflowError as exc:
        raise ValidationError("numeric range exceeded while aggregating measurements") from exc
    if not math.isfinite(result):
        raise ValidationError("non-finite aggregate")
    return result


def metrics(runs):
    tasks = [task for run in runs for task in run["tasks"]]
    duration = finite_sum(run["duration_s"] for run in runs)
    successes = sum(task["status"] == "success" for task in tasks)
    unknown_critical = sum(task["critical_failure"] is None for task in tasks)
    critical = sum(task["critical_failure"] is True for task in tasks)
    cost = None if any(run["total_cost"] is None for run in runs) else finite_sum(
        run["total_cost"] for run in runs
    )
    reasons = {}

    def divide(name, numerator, denominator, reason, scale=1):
        if numerator is None or denominator == 0:
            reasons[name] = reason
            return None
        try:
            result = numerator / denominator * scale
        except OverflowError:
            reasons[name] = "non_finite_result"
            return None
        if not math.isfinite(result):
            reasons[name] = "non_finite_result"
            return None
        return result

    latencies = sorted(task["latency_ms"] for task in tasks)
    if not latencies:
        reasons["latency_p95_ms"] = "no_tasks"
    result = {
        "task_count": len(tasks),
        "success_count": successes,
        "known_critical_failures": critical,
        "unknown_critical_classifications": unknown_critical,
        "duration_s": duration,
        "total_cost": cost,
        "goodput_per_hour": divide("goodput_per_hour", successes, duration, "no_duration", scale=3600),
        "success_rate": divide("success_rate", successes, len(tasks), "no_tasks"),
        "cost_per_hour": divide(
            "cost_per_hour", cost, duration, "unknown_cost", scale=3600
        ),
        "cost_per_success": divide(
            "cost_per_success", cost, successes, "unknown_cost" if cost is None else "no_successes"
        ),
        "latency_p95_ms": latencies[(95 * len(latencies) + 99) // 100 - 1] if latencies else None,
        "critical_failure_rate": divide(
            "critical_failure_rate", None if unknown_critical else critical, len(tasks),
            "unknown_critical_classification" if unknown_critical else "no_tasks",
        ),
        "undefined_reasons": reasons,
    }
    if cost is None:
        reasons["total_cost"] = "unknown_cost"
    return result


def assess(run_reports, level_metrics, unit_currency, policy):
    violations, missing = [], []
    if policy is None:
        return {"status": "not_evaluated", "violations": [], "missing_data": ["policy_not_provided"]}
    if unit_currency != policy["currency"]:
        violations.append("currency_mismatch")
    if len(run_reports) < policy["min_repetitions"]:
        missing.append(f"requires_{policy['min_repetitions']}_repetitions")
    if level_metrics["goodput_per_hour"] is None:
        missing.append("aggregate.goodput_per_hour: undefined")
    if level_metrics["cost_per_success"] is None:
        missing.append("aggregate.cost_per_success: " + level_metrics["undefined_reasons"]["cost_per_success"])
    for run in run_reports:
        for metric, threshold, direction in LIMITS:
            value = run["metrics"][metric]
            if value is None:
                missing.append(f"{run['run_id']}.{metric}: {run['metrics']['undefined_reasons'][metric]}")
            elif (value > policy[threshold] if direction == "max" else value < policy[threshold]):
                violations.append(f"{run['run_id']}.{metric}: {value} violates {threshold}={policy[threshold]}")
    return {
        "status": "failed" if violations else "insufficient_data" if missing else "passed",
        "violations": violations,
        "missing_data": missing,
    }


def elasticity(previous, current):
    result = {
        "from_concurrency": previous["concurrency"],
        "to_concurrency": current["concurrency"],
        "value": None, "reason": None,
    }
    before, after = previous["metrics"]["goodput_per_hour"], current["metrics"]["goodput_per_hour"]
    if before is None or after is None or before <= 0 or after <= 0:
        result["reason"] = "nonpositive_or_unknown_goodput"
        return result
    denominator = math.log(current["concurrency"]) - math.log(previous["concurrency"])
    if denominator == 0:
        result["reason"] = "indistinguishable_log_concurrency"
        return result
    value = (math.log(after) - math.log(before)) / denominator
    if math.isfinite(value):
        result["value"] = value
    else:
        result["reason"] = "non_finite_result"
    return result


def analyze(runs, policy=None):
    grouped = {}
    for run in runs:
        comparison = {key: run[key] for key in ("workload_id", "evaluator_id", "configuration", "currency")}
        key = json.dumps(comparison, sort_keys=True, ensure_ascii=True, allow_nan=False)
        grouped.setdefault(key, []).append(run)
    groups = []
    for key, members in sorted(grouped.items()):
        levels = []
        for concurrency in sorted({run["concurrency"] for run in members}):
            repetitions = sorted(
                (run for run in members if run["concurrency"] == concurrency), key=lambda run: run["run_id"]
            )
            run_reports = [{"run_id": run["run_id"], "metrics": metrics([run])} for run in repetitions]
            aggregate = metrics(repetitions)
            levels.append({
                "concurrency": concurrency,
                "repetitions": len(repetitions),
                "run_ids": [run["run_id"] for run in repetitions],
                "metrics": aggregate,
                "runs": run_reports,
                "assessment": assess(run_reports, aggregate, members[0]["currency"], policy),
            })
        candidates = [level for level in levels if level["assessment"]["status"] == "passed"]
        best = min(candidates, key=lambda level: (
            -level["metrics"]["goodput_per_hour"], level["metrics"]["cost_per_success"], level["concurrency"]
        )) if candidates else None
        groups.append({
            "group_id": hashlib.sha256(key.encode("utf-8")).hexdigest(),
            "comparison": json.loads(key),
            "levels": levels,
            "elasticities": [elasticity(before, after) for before, after in zip(levels, levels[1:])],
            "recommendation": {
                "concurrency": best["concurrency"],
                "goodput_per_hour": best["metrics"]["goodput_per_hour"],
                "cost_per_success": best["metrics"]["cost_per_success"],
                "run_ids": best["run_ids"],
            } if best else None,
            "recommendation_reason": (
                "highest_observed_goodput_within_policy" if best else
                "policy_not_provided" if policy is None else "no_admissible_measured_configuration"
            ),
        })
    return {"schema_version": SCHEMA_VERSION, "notice": NOTICE, "policy": policy, "groups": groups}


def cell(value):
    if value is None:
        return "null"
    return html.escape(str(value), quote=True).replace("\\", "\\\\").replace("|", "\\|").replace(
        "\n", " "
    ).replace("\r", " ").replace(chr(96), "\\" + chr(96))


def metric_details(values):
    return [f"- {key}: {cell(value)}" for key, value in sorted(values.items()) if key != "undefined_reasons"] + [
        f"- Undefined {key}: {cell(reason)}" for key, reason in sorted(values["undefined_reasons"].items())
    ]


def render_markdown(report):
    lines = ["# Observed scalability report", "", NOTICE, "",
             f"Schema version: {report['schema_version']}", "", "## Provenance", ""]
    for name, source in report["sources"].items():
        if source is not None:
            lines.append(f"- {name}: {cell(source['path'])}; SHA-256: {source['sha256']}")
    lines += ["", "## Policy", "", *["    " + line for line in json.dumps(
        report["policy"], indent=2, sort_keys=True, ensure_ascii=True
    ).splitlines()]]
    for group in report["groups"]:
        lines += ["", f"## Group {group['group_id']}", ""]
        lines += ["    " + line for line in json.dumps(
            group["comparison"], indent=2, sort_keys=True, ensure_ascii=True
        ).splitlines()]
        lines += [
            "", "| N | Runs | Correct/h | Success rate | Cost/h | Cost/correct | p95 ms | Critical rate | Status |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for level in group["levels"]:
            m = level["metrics"]
            row = [level["concurrency"], level["repetitions"], m["goodput_per_hour"], m["success_rate"],
                   m["cost_per_hour"], m["cost_per_success"], m["latency_p95_ms"],
                   m["critical_failure_rate"], level["assessment"]["status"]]
            lines.append("| " + " | ".join(cell(value) for value in row) + " |")
        lines += ["", "Recommendation: " + cell(
            group["recommendation"]["concurrency"] if group["recommendation"] else None
        ), "Reason: " + group["recommendation_reason"], "", "### Elasticities", ""]
        for edge in group["elasticities"]:
            lines.append(
                f"- {edge['from_concurrency']} -> {edge['to_concurrency']}: "
                f"{cell(edge['value'])}; reason: {cell(edge['reason'])}"
            )
        for level in group["levels"]:
            lines += ["", f"### N = {level['concurrency']}: aggregate", "", *metric_details(level["metrics"])]
            for kind in ("violations", "missing_data"):
                for reason in level["assessment"][kind]:
                    lines.append(f"- {kind}: {cell(reason)}")
            for run in level["runs"]:
                lines += ["", "#### Run " + cell(run["run_id"]), "", *metric_details(run["metrics"])]
    return "\n".join(lines) + "\n"


def atomic_write(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Version 1 benchmark JSONL")
    parser.add_argument("--policy", type=Path, help="Optional complete policy JSON")
    parser.add_argument("--output-dir", type=Path, default=Path("logs/scalability"))
    args = parser.parse_args(argv)
    try:
        runs, input_source = load_runs(args.input)
        policy, policy_source = load_policy(args.policy) if args.policy else (None, None)
        report = analyze(runs, policy)
        report["sources"] = {"input": input_source, "policy": policy_source}
        outputs = (args.output_dir / "report.json", args.output_dir / "report.md")
        inputs = {path.resolve() for path in (args.input, args.policy) if path is not None}
        if any(path.resolve() in inputs for path in outputs):
            raise ValidationError("output paths must not overwrite input or policy")
        serialized = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n"
        markdown = render_markdown(report)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        atomic_write(outputs[0], serialized)
        atomic_write(outputs[1], markdown)
    except ValidationError as exc:
        print(f"Invalid benchmark input: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Report I/O error: {exc}", file=sys.stderr)
        return 1
    print(f"Reports written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
