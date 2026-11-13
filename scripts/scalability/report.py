# Copyright 2026 Borja Moskv (borjamoskv)
"""Deterministic JSON and escaped Markdown reports."""

from __future__ import annotations

import hashlib
import html
import json
import os
import platform
import tempfile
from pathlib import Path

from . import VERSION
from .contract import fingerprint, require


def envelope(kind, payload, sources, policy):
    implementation = hashlib.sha256()
    package = Path(__file__).resolve().parent
    files = sorted(package.glob("*.py")) + sorted(
        package.parent.glob("*_scalability.py")
    )
    for path in files:
        implementation.update(
            str(path.relative_to(package.parent)).encode() + b"\0" + path.read_bytes()
        )
    return {
        "report_version": 1,
        "tool_version": VERSION,
        "kind": kind,
        "implementation_sha256": implementation.hexdigest(),
        "python_version": platform.python_version(),
        "input_contract_versions": [1],
        "sources": sources,
        "policy": policy,
        "policy_sha256": fingerprint(policy),
        "interpretation": "Observed finite-batch benchmark performance; "
        "not production capacity.",
        "uncertainty_scope": "Exploratory pointwise intervals, "
        "not simultaneous or anytime guarantees. "
        "Independent run clusters and fixed task counts are assumed; "
        "confirm adaptively selected configurations on fresh fixed-design runs.",
        "usl_status": "deferred: no predictive fit or extrapolation is used",
        "tenfold_improvement": "not_measured",
        **payload,
    }


def cell(value):
    if value is None:
        return "unknown"
    if isinstance(value, float):
        return f"{value:.6g}"
    escaped = html.escape(str(value), quote=True).replace("\n", " ")
    return escaped.translate({ord(c): f"&#{ord(c)};" for c in "|`[]()!*_~\\#"})


def markdown(report):
    lines = [
        "# Scalability report",
        "",
        report["interpretation"],
        "",
        "Informational only. No measured 10x claim. "
        "Recommendations require independent confirmation.",
        "",
        report["uncertainty_scope"],
        "",
    ]
    for group in report.get("groups", []):
        ident = group["identity"]
        lines.extend(
            [
                f"## {cell(ident['workload_id'])} / {cell(ident['config_id'])} "
                f"({cell(ident['currency'])})",
                "",
                "| Concurrency | Runs | Successes/h | Success rate | Cost/success "
                "| Terminal p95 ms | Critical rate | Policy |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for candidate in group["candidates"]:
            m = candidate["metrics"]
            values = m["values"]
            row = [
                candidate["concurrency"],
                m["run_count"],
                values["successes_per_hour"],
                values["success_rate"],
                values["cost_per_success"],
                values["p95_terminal_ms"],
                values["critical_failure_rate"],
                candidate["assessment"]["status"],
            ]
            lines.append("| " + " | ".join(cell(v) for v in row) + " |")
        decision = group["recommendation"]
        lines.extend(
            [
                "",
                f"Recommendation: **{cell(decision['status'])}**; concurrency: "
                f"{cell(decision['concurrency'])}; reason: {cell(decision['reason'])}.",
                "",
            ]
        )
    if "plan" in report:
        plan = report["plan"]
        lines.extend(
            [
                f"Plan: **{cell(plan['status'])}** — {cell(plan['reason'])}.",
                "",
                f"Budget charged/reserved: {cell(plan['budget_used'])}; "
                f"remaining: {cell(plan['budget_remaining'])}.",
                "",
            ]
        )
        if plan.get("next_candidate"):
            lines.extend(
                [f"Next candidate: {cell(plan['next_candidate']['candidate_id'])}.", ""]
            )
    aborted = [
        r["run_id"] for r in report.get("runs", []) if not r["included_in_comparisons"]
    ]
    if aborted:
        lines.extend(
            ["Excluded aborted runs: " + ", ".join(cell(r) for r in aborted) + ".", ""]
        )
    lines.extend(
        [
            "## Provenance",
            "",
            f"Tool version: {VERSION}. Contract: 1.",
            "",
            f"Policy SHA-256: `{report['policy_sha256']}`.",
            "",
        ]
    )
    for source in report["sources"]:
        lines.append(f"- {cell(source['path'])}: `{source['sha256']}`")
    lines.extend(
        [
            "",
            "JSON includes individual runs, intervals, configuration, "
            "run IDs and reasons for null metrics.",
            "",
        ]
    )
    return "\n".join(lines)


def write_reports(directory: Path, stem: str, report, protected=()):
    paths = [directory / f"{stem}.json", directory / f"{stem}.md"]
    protected = {Path(p).resolve() for p in protected}
    for path in paths:
        require(path.resolve() not in protected, "output would overwrite an input file")
    contents = [
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False)
        + "\n",
        markdown(report),
    ]
    directory.mkdir(parents=True, exist_ok=True)
    for path, content in zip(paths, contents):
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=directory, delete=False
            ) as stream:
                temporary = Path(stream.name)
                stream.write(content)
            os.replace(temporary, path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return paths
