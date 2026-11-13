#!/usr/bin/env python3
# Copyright 2026 Borja Moskv (borjamoskv)
"""Analyze version-1 JSONL benchmarks with Python 3.12 and the standard library."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.scalability.contract import (
    ValidationError,
    load_runs,
    read_json,
    validate_policy,
)
from scripts.scalability.decision import analyze
from scripts.scalability.report import envelope, write_reports


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        action="append",
        help="JSONL; repeat for multiple files",
    )
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("logs/scalability"))
    args = parser.parse_args(argv)
    try:
        runs, sources = load_runs(args.input)
        raw, policy_source = read_json(args.policy) if args.policy else (None, None)
        policy = validate_policy(raw)
        if policy_source:
            sources.append(policy_source)
        report = envelope("analysis", analyze(runs, policy), sources, policy)
        paths = write_reports(
            args.output_dir,
            "report",
            report,
            args.input + ([args.policy] if args.policy else []),
        )
    except (ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Informational report: {paths[0]}")
    return 0  # Policy violations and abstention are data, not CI failures.


if __name__ == "__main__":
    raise SystemExit(main())
