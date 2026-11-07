#!/usr/bin/env python3
# Copyright 2026 Borja Moskv (borjamoskv)
"""Verify disjoint multi-mount skill partition (104 cp/skills + 27 b60/.agents/skills = 131/131)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_B60_MOUNT = Path.home() / "10_PROJECTS" / "BABYLON-60" / ".agents" / "skills"


def verify_partition(
    cp_root: Path = REPOSITORY_ROOT,
    extra_mounts: list[Path] | None = None,
) -> dict[str, object]:
    skills_md_path = cp_root / "SKILLS.md"
    skills_json_path = cp_root / "skills" / "skills.json"

    skills_md_text = skills_md_path.read_text(encoding="utf-8")
    sec2_text = skills_md_text.split("## 3. Protocolo Funtorial", 1)[0]
    sec2_rows = re.findall(r"^\| \[`([^`]+)`\]\(([^)]+)\) \|", sec2_text, re.M)

    local_declared = {name for name, target in sec2_rows if not target.startswith("http")}
    workspace_declared = {name for name, target in sec2_rows if target.startswith("http")}

    cp_registry = json.loads(skills_json_path.read_text(encoding="utf-8"))
    cp_entries = {entry["name"] for entry in cp_registry["entries"]}
    cp_materialized = {
        p.parent.name
        for p in (cp_root / "skills").glob("*/SKILL.md")
        if p.is_file() and p.stat().st_size > 0
    }

    mounts = list(extra_mounts) if extra_mounts is not None else []
    if extra_mounts is None and DEFAULT_B60_MOUNT.is_dir():
        mounts.append(DEFAULT_B60_MOUNT)

    workspace_materialized: set[str] = set()
    for mount in mounts:
        if mount.is_dir():
            workspace_materialized.update(
                p.parent.name
                for p in mount.glob("*/SKILL.md")
                if p.is_file() and p.stat().st_size > 0
            )

    # Check local links in SKILLS.md (both Section 2 and Section 3)
    all_links = re.findall(r"\[`([^`]+)`\]\(([^)]+)\)", skills_md_text)
    broken_local_links = [
        target
        for _, target in all_links
        if not target.startswith("http") and not (cp_root / target).is_file()
    ]

    overlap_declared = sorted(local_declared & workspace_declared)
    missing_local = sorted(cp_entries - cp_materialized)
    missing_workspace = (
        sorted(workspace_declared - workspace_materialized) if mounts else []
    )
    overlap_mounts = (
        sorted(cp_entries & workspace_materialized) if mounts else []
    )

    ok = (
        len(sec2_rows) == 131
        and len(local_declared) == 104
        and len(workspace_declared) == 27
        and local_declared == cp_entries
        and not overlap_declared
        and not missing_local
        and not missing_workspace
        and not overlap_mounts
        and not broken_local_links
    )

    return {
        "status": "PASS" if ok else "FAIL",
        "declared_total": len(sec2_rows),
        "local_ring2_3_count": len(local_declared),
        "workspace_ring0_1_count": len(workspace_declared),
        "cp_registry_count": len(cp_entries),
        "cp_materialized_count": len(cp_entries & cp_materialized),
        "workspace_mounts_checked": [str(m) for m in mounts],
        "workspace_materialized_count": len(workspace_materialized),
        "overlap_declared": overlap_declared,
        "overlap_mounts": overlap_mounts,
        "missing_local": missing_local,
        "missing_workspace": missing_workspace,
        "broken_local_links": broken_local_links,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cp-root",
        type=Path,
        default=REPOSITORY_ROOT,
        help="Path to cortex-persist root",
    )
    parser.add_argument(
        "--mount",
        type=Path,
        action="append",
        default=None,
        help="Additional skill mount directory (e.g. BABYLON-60/.agents/skills)",
    )
    args = parser.parse_args()
    report = verify_partition(cp_root=args.cp_root, extra_mounts=args.mount)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
