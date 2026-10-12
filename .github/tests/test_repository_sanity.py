# Copyright 2026 Borja Moskv (borjamoskv)

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import ClassVar, cast

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml"


class TestRepositorySanity(unittest.TestCase):
    step_commands: ClassVar[dict[str, str]]

    @classmethod
    def setUpClass(cls) -> None:
        workflow = cast(
            dict[str, object], yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
        )
        jobs = cast(dict[str, object], workflow["jobs"])
        sanity = cast(dict[str, object], jobs["sanity"])
        steps = cast(list[dict[str, object]], sanity["steps"])
        cls.step_commands = {
            cast(str, step["name"]): cast(str, step["run"])
            for step in steps
            if "run" in step
        }

    def setUp(self) -> None:
        fixture = tempfile.TemporaryDirectory(prefix="cortex-ci-regression-")
        self.addCleanup(fixture.cleanup)
        self.root = Path(fixture.name)
        for name in ("mcp_config.json", "hooks.json"):
            (self.root / name).write_text("{}\n", encoding="utf-8")
        for name in ("README.md", "AGENTS.md"):
            (self.root / name).write_text("# Required document\n", encoding="utf-8")
        for name in ("skills", "rules", "plugins"):
            directory = self.root / name
            directory.mkdir()
            (directory / "manifest.md").write_text(
                "# Valid manifest\n", encoding="utf-8"
            )
        self.plugin = self.root / "plugins" / "plugin with spaces"
        self.plugin.mkdir()
        for name in ("mcp_config.json", "hooks.json"):
            (self.plugin / name).write_text("{}\n", encoding="utf-8")

    def run_step(self, name: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            ["bash", "-e", "-o", "pipefail", "-c", self.step_commands[name]],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
            env=env,
            timeout=10,
        )

    def assert_rejected(self, step: str, path: Path) -> None:
        result = self.run_step(step)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(str(path.relative_to(self.root)), result.stderr)

    def test_valid_root_and_plugin_files_pass_all_checks(self) -> None:
        for name in (
            "Validate JSON configs",
            "Required files present",
            "Skill and rule manifests non-empty",
        ):
            with self.subTest(step=name):
                result = self.run_step(name)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_root_mcp_json_is_rejected(self) -> None:
        path = self.root / "mcp_config.json"
        path.write_text("{invalid", encoding="utf-8")
        self.assert_rejected("Validate JSON configs", path)

    def test_missing_root_mcp_config_is_rejected(self) -> None:
        path = self.root / "mcp_config.json"
        path.unlink()
        self.assert_rejected("Validate JSON configs", path)

    def test_invalid_root_hooks_json_is_rejected(self) -> None:
        path = self.root / "hooks.json"
        path.write_text("{invalid", encoding="utf-8")
        self.assert_rejected("Validate JSON configs", path)

    def test_missing_root_hooks_config_is_rejected(self) -> None:
        path = self.root / "hooks.json"
        path.unlink()
        self.assert_rejected("Validate JSON configs", path)

    def test_invalid_plugin_mcp_json_is_rejected(self) -> None:
        path = self.plugin / "mcp_config.json"
        path.write_text("{invalid", encoding="utf-8")
        self.assert_rejected("Validate JSON configs", path)

    def test_invalid_plugin_hooks_json_is_rejected(self) -> None:
        path = self.plugin / "hooks.json"
        path.write_text("{invalid", encoding="utf-8")
        self.assert_rejected("Validate JSON configs", path)

    def test_missing_readme_is_rejected(self) -> None:
        path = self.root / "README.md"
        path.unlink()
        self.assert_rejected("Required files present", path)

    def test_empty_agent_instructions_are_rejected(self) -> None:
        path = self.root / "AGENTS.md"
        path.write_text("", encoding="utf-8")
        self.assert_rejected("Required files present", path)

    def test_empty_nested_manifest_with_spaces_is_rejected(self) -> None:
        path = self.plugin / "empty manifest.md"
        path.touch()
        self.assert_rejected("Skill and rule manifests non-empty", path)

    def test_whitespace_only_manifest_is_rejected(self) -> None:
        path = self.plugin / "blank manifest.md"
        path.write_text(" \n\t\n", encoding="utf-8")
        self.assert_rejected("Skill and rule manifests non-empty", path)

    def test_broken_manifest_symlink_is_rejected(self) -> None:
        path = self.plugin / "missing manifest.md"
        path.symlink_to("nonexistent-target.md")
        self.assert_rejected("Skill and rule manifests non-empty", path)

    def test_invalid_utf8_manifest_is_rejected(self) -> None:
        path = self.plugin / "invalid manifest.md"
        path.write_bytes(b"\xff")
        self.assert_rejected("Skill and rule manifests non-empty", path)

    def test_missing_manifest_directory_is_rejected(self) -> None:
        path = self.root / "rules"
        (path / "manifest.md").unlink()
        path.rmdir()
        self.assert_rejected("Skill and rule manifests non-empty", path)

    def test_directory_named_markdown_is_not_treated_as_a_manifest(self) -> None:
        (self.plugin / "folder.md").mkdir()
        result = self.run_step("Skill and rule manifests non-empty")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
