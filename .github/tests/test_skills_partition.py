# Copyright 2026 Borja Moskv (borjamoskv)

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.check_skills_source_of_truth import DEFAULT_B60_MOUNT, verify_partition

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


class TestSkillsPartition(unittest.TestCase):
    def test_standalone_partition_and_links_pass(self) -> None:
        report = verify_partition(cp_root=REPOSITORY_ROOT, extra_mounts=[])
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["declared_total"], 131)
        self.assertEqual(report["local_ring2_3_count"], 104)
        self.assertEqual(report["workspace_ring0_1_count"], 27)
        self.assertEqual(report["cp_registry_count"], 104)
        self.assertEqual(report["cp_materialized_count"], 104)
        self.assertEqual(report["overlap_declared"], [])
        self.assertEqual(report["missing_local"], [])
        self.assertEqual(report["broken_local_links"], [])

    def test_multi_mount_partition_when_babylon60_present(self) -> None:
        if not DEFAULT_B60_MOUNT.is_dir():
            self.skipTest("BABYLON-60 mount not present on this runner")
        report = verify_partition(
            cp_root=REPOSITORY_ROOT, extra_mounts=[DEFAULT_B60_MOUNT]
        )
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["workspace_materialized_count"], 27)
        self.assertEqual(report["overlap_mounts"], [])
        self.assertEqual(report["missing_workspace"], [])


if __name__ == "__main__":
    unittest.main()
