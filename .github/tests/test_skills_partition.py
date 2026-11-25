# Copyright 2026 Borja Moskv (borjamoskv)

from __future__ import annotations

import unittest
import json
import tempfile
from pathlib import Path

from scripts.check_skills_source_of_truth import DEFAULT_B60_MOUNT, verify_partition

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


class TestSkillsPartition(unittest.TestCase):
    def test_standalone_partition_and_links_pass(self) -> None:
        report = verify_partition(cp_root=REPOSITORY_ROOT, extra_mounts=[])
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["declared_total"], 127)
        self.assertEqual(report["local_ring2_3_count"], 32)
        self.assertEqual(report["workspace_ring0_1_count"], 22)
        self.assertEqual(report["cp_registry_count"], 32)
        self.assertEqual(report["cp_materialized_count"], 32)
        self.assertEqual(report["archived_count"], 73)
        self.assertEqual(report["incomplete_routing_metadata"], ["c5-bounty-specialist"])
        self.assertEqual(report["missing_routing_fields"]["c5-bounty-specialist"], [
            "canonical_alias", "category", "exergy_audit", "tier", "triggers"
        ])
        self.assertEqual(report["invalid_routing_fields"], {})
        self.assertEqual(report["routing_readiness"], "NOT_VERIFIED")
        self.assertEqual(report["workspace_verification"], "NOT_CHECKED")
        self.assertEqual(report["overlap_declared"], [])
        self.assertEqual(report["missing_local"], [])
        self.assertEqual(report["broken_local_links"], [])

    def test_partition_rejects_missing_or_unregistered_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active = root / "skills" / "active" / "SKILL.md"
            archived = root / "skills" / "_archive" / "20261108_poda_v1" / "old" / "SKILL.md"
            active.parent.mkdir(parents=True)
            archived.parent.mkdir(parents=True)
            active.write_text("active", encoding="utf-8")
            archived.write_text("archived", encoding="utf-8")
            (root / "skills" / "skills.json").write_text(json.dumps({
                "total_skills": 1,
                "entries": [{"name": "active", "path": "active/SKILL.md"}],
                "archived_entries": [
                    {"name": "old", "status": "archived", "path": "_archive/20261108_poda_v1/old/SKILL.md"},
                ],
                "adjacency": [], "archived_adjacency": [],
            }), encoding="utf-8")
            (archived.parent.parent / "MANIFEST_PODA_V1.json").write_text(
                json.dumps({"moved": [{"name": "old"}]}), encoding="utf-8"
            )
            (root / "SKILLS.md").write_text(
                "| [`active`](skills/active/SKILL.md) |\n"
                "| [`old`](skills/_archive/20261108_poda_v1/old/SKILL.md) |\n"
                "## 3. Protocolo Funtorial\n", encoding="utf-8"
            )
            self.assertEqual(verify_partition(root, [])["status"], "PASS")
            registry_path = root / "skills" / "skills.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            entry = registry["entries"][0]
            entry.update({
                "tier": None, "category": " ", "canonical_alias": None,
                "triggers": ["valid", ""], "exergy_audit": {},
            })
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            report = verify_partition(root, [])
            self.assertEqual(report["status"], "PASS")  # Partition, not routing.
            self.assertEqual(report["missing_routing_fields"], {})
            self.assertEqual(report["invalid_routing_fields"], {"active": [
                "canonical_alias", "category", "exergy_audit", "tier", "triggers"
            ]})
            self.assertEqual(report["routing_readiness"], "NOT_VERIFIED")
            entry.update({"tier": True, "triggers": []})
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            report = verify_partition(root, [])
            self.assertIn("tier", report["invalid_routing_fields"]["active"])
            self.assertIn("triggers", report["invalid_routing_fields"]["active"])
            entry.update({
                "tier": 1, "category": "Security", "canonical_alias": "active",
                "triggers": ["active"], "exergy_audit": {"source": "fixture"},
            })
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            report = verify_partition(root, [])
            self.assertEqual(report["incomplete_routing_metadata"], [])
            self.assertEqual(report["routing_readiness"], "NOT_ASSESSED")
            active.unlink()
            report = verify_partition(root, [])
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["missing_local"], ["active"])
            active.write_text("active", encoding="utf-8")
            extra = root / "skills" / "extra" / "SKILL.md"
            extra.parent.mkdir()
            extra.write_text("extra", encoding="utf-8")
            report = verify_partition(root, [])
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["unregistered_local"], ["extra"])
            extra.unlink()
            archived.unlink()
            report = verify_partition(root, [])
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["missing_archived"], ["old"])
            archived.write_text("archived", encoding="utf-8")
            registry_path = root / "skills" / "skills.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["entries"][0]["path"] = "old/SKILL.md"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            report = verify_partition(root, [])
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["invalid_registry_paths"], ["active"])
            registry["entries"][0]["path"] = "active/SKILL.md"
            registry["adjacency"] = [{"source": "active", "target": "old", "relation": "example"}]
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            report = verify_partition(root, [])
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["invalid_edges"]), 1)

    def test_multi_mount_partition_when_babylon60_present(self) -> None:
        if not DEFAULT_B60_MOUNT.is_dir():
            self.skipTest("BABYLON-60 mount not present on this runner")
        report = verify_partition(
            cp_root=REPOSITORY_ROOT, extra_mounts=[DEFAULT_B60_MOUNT]
        )
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["workspace_materialized_count"], 22)
        self.assertEqual(report["overlap_mounts"], [])
        self.assertEqual(report["missing_workspace"], [])


if __name__ == "__main__":
    unittest.main()
