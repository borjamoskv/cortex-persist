#!/usr/bin/env python3
# Copyright 2026 Borja Moskv (borjamoskv)
"""Verify the partition and report structural routing metadata separately.

The partition status does not certify routing or the truth of metadata values.
"""

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

    archive_prefix = "skills/_archive/20261108_poda_v1/"
    local_declared = {
        name for name, target in sec2_rows
        if not target.startswith("http") and not target.startswith(archive_prefix)
    }
    archive_declared = {
        name for name, target in sec2_rows if target.startswith(archive_prefix)
    }
    workspace_declared = {name for name, target in sec2_rows if target.startswith("http")}

    cp_registry = json.loads(skills_json_path.read_text(encoding="utf-8"))
    entries = cp_registry["entries"]
    archived_entries = cp_registry["archived_entries"]
    all_entries = entries + archived_entries
    cp_entries = {entry["name"] for entry in entries}
    archived = {entry["name"] for entry in archived_entries}
    routing_fields = {"tier", "category", "canonical_alias", "triggers", "exergy_audit"}
    missing_routing_fields: dict[str, list[str]] = {}
    invalid_routing_fields: dict[str, list[str]] = {}
    for entry in entries:
        missing = sorted(routing_fields - entry.keys())
        invalid = []
        for field in sorted(routing_fields & entry.keys()):
            value = entry[field]
            if field == "tier":
                valid = type(value) is int and value > 0
            elif field in {"category", "canonical_alias"}:
                valid = isinstance(value, str) and bool(value.strip())
            elif field == "triggers":
                valid = isinstance(value, list) and bool(value) and all(
                    isinstance(item, str) and bool(item.strip()) for item in value
                )
            else:
                valid = isinstance(value, dict) and bool(value)
            if not valid:
                invalid.append(field)
        if missing:
            missing_routing_fields[entry["name"]] = missing
        if invalid:
            invalid_routing_fields[entry["name"]] = invalid
    incomplete_routing_metadata = sorted(missing_routing_fields.keys() | invalid_routing_fields.keys())
    invalid_edges = [
        edge for edge in cp_registry["adjacency"]
        if edge.get("source") not in cp_entries or edge.get("target") not in cp_entries
    ]
    invalid_archived_edges = [
        edge for edge in cp_registry["archived_adjacency"]
        if edge.get("source") not in cp_entries | archived
        or edge.get("target") not in cp_entries | archived
        or not ({edge.get("source"), edge.get("target")} & archived)
    ]
    archive_manifest = json.loads(
        (cp_root / archive_prefix / "MANIFEST_PODA_V1.json").read_text(encoding="utf-8")
    )
    archived_by_manifest = {entry["name"] for entry in archive_manifest["moved"]}
    invalid_registry_paths = sorted(
        entry["name"] for entry in all_entries
        if entry.get("path") != (
            f"_archive/20261108_poda_v1/{entry['name']}/SKILL.md"
            if entry.get("status") == "archived"
            else f"{entry['name']}/SKILL.md"
        )
    )
    invalid_declared_paths = sorted(
        name for name, target in sec2_rows
        if not target.startswith("http") and target != (
            f"{archive_prefix}{name}/SKILL.md"
            if target.startswith(archive_prefix)
            else f"skills/{name}/SKILL.md"
        )
    )
    missing_archived = sorted(
        name for name in archived
        if not (cp_root / archive_prefix / name / "SKILL.md").is_file()
    )
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
    unregistered_local = sorted(cp_materialized - cp_entries)
    missing_workspace = (
        sorted(workspace_declared - workspace_materialized) if mounts else []
    )
    overlap_mounts = (
        sorted(cp_entries & workspace_materialized) if mounts else []
    )

    ok = (
        len(sec2_rows) == len(local_declared) + len(archive_declared) + len(workspace_declared)
        and all(entry.get("status", "active") == "active" for entry in entries)
        and all(entry.get("status") == "archived" for entry in archived_entries)
        and len({entry["name"] for entry in all_entries}) == len(all_entries)
        and len(cp_entries) == len(entries)
        and len(archived) == len(archived_entries)
        and cp_registry["total_skills"] == len(entries)
        and local_declared == cp_entries
        and archive_declared == archived
        and archived <= archived_by_manifest
        and not (cp_entries & archived)
        and not invalid_registry_paths
        and not invalid_declared_paths
        and not invalid_edges
        and not invalid_archived_edges
        and not overlap_declared
        and not missing_local
        and not unregistered_local
        and not missing_archived
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
        "archived_count": len(archived),
        "incomplete_routing_metadata": incomplete_routing_metadata,
        "missing_routing_fields": missing_routing_fields,
        "invalid_routing_fields": invalid_routing_fields,
        "routing_readiness": "NOT_VERIFIED" if incomplete_routing_metadata else "NOT_ASSESSED",
        "missing_archived": missing_archived,
        "unregistered_local": unregistered_local,
        "invalid_registry_paths": invalid_registry_paths,
        "invalid_declared_paths": invalid_declared_paths,
        "invalid_edges": invalid_edges,
        "invalid_archived_edges": invalid_archived_edges,
        "workspace_mounts_checked": [str(m) for m in mounts],
        "workspace_verification": "CHECKED" if mounts else "NOT_CHECKED",
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
