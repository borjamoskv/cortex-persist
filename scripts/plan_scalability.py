#!/usr/bin/env python3
# Copyright 2026 Borja Moskv (borjamoskv)
"""Propose one bounded benchmark experiment without executing it."""

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
from scripts.scalability.planner import plan, validate_space
from scripts.scalability.report import envelope, write_reports


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        action="append",
        default=[],
        help="Existing campaign JSONL; optional for first proposal",
    )
    parser.add_argument("--space", type=Path, required=True)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("logs/scalability"))
    args = parser.parse_args(argv)
    try:
        runs, sources = load_runs(args.input, allow_empty=True)
        raw_space, source = read_json(args.space)
        sources.append(source)
        raw_policy, source = read_json(args.policy) if args.policy else (None, None)
        if source:
            sources.append(source)
        policy, space = validate_policy(raw_policy), validate_space(raw_space)
        report = envelope(
            "plan", plan(runs, space, policy) | {"space": space}, sources, policy
        )
        paths = write_reports(
            args.output_dir,
            "plan",
            report,
            args.input + [args.space] + ([args.policy] if args.policy else []),
        )
    except (ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Informational plan: {paths[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
