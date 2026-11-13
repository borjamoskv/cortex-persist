#!/usr/bin/env python3
# Copyright 2026 Borja Moskv (borjamoskv)
"""Execute an explicit benchmark runner under a finite campaign budget (POSIX)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.scalability.contract import (
    ValidationError,
    read_json,
    require,
    validate_policy,
)
from scripts.scalability.experiment import campaign
from scripts.scalability.planner import validate_space
from scripts.scalability.report import envelope, write_reports


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path, required=True, help="Append/resume campaign history JSONL"
    )
    parser.add_argument("--space", type=Path, required=True)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("logs/scalability"))
    parser.add_argument(
        "--runner",
        nargs=argparse.REMAINDER,
        required=True,
        help="Explicit argv; no shell interpolation",
    )
    args = parser.parse_args(argv)
    args.input = args.input.resolve()
    try:
        raw_space, space_source = read_json(args.space)
        raw_policy, policy_source = (
            read_json(args.policy) if args.policy else (None, None)
        )
        space, policy = validate_space(raw_space), validate_policy(raw_policy)
        protected = [args.space] + ([args.policy] if args.policy else [])
        outputs = [
            args.input,
            Path(str(args.input) + ".lock"),
            Path(str(args.input) + ".pending.json"),
            args.output_dir / "campaign.json",
            args.output_dir / "campaign.md",
        ]
        require(
            len({p.resolve() for p in outputs}) == len(outputs),
            "campaign outputs overlap",
        )
        require(
            not {p.resolve() for p in outputs} & {p.resolve() for p in protected},
            "campaign output would overwrite configuration",
        )
        payload, sources = campaign(
            args.input,
            space,
            policy,
            args.runner,
            args.output_dir,
            on_run=lambda r: print(
                f"Run {r['run_id']}: {r.get('run_status', 'completed')}", flush=True
            ),
        )
        sources.append(space_source)
        if policy_source:
            sources.append(policy_source)
        report = envelope("campaign", payload | {"space": space}, sources, policy)
        paths = write_reports(
            args.output_dir, "campaign", report, protected + [args.input]
        )
    except (ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print(
            "Interrupted; any pending reservation must be reconciled before resuming.",
            file=sys.stderr,
        )
        return 130
    print(f"Informational campaign report: {paths[0]}")
    return 130 if report["plan"]["reason"] == "interrupted" else 0


if __name__ == "__main__":
    raise SystemExit(main())
