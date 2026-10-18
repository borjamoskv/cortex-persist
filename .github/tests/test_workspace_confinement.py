# Copyright 2026 Borja Moskv (borjamoskv)

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Sequence
from pathlib import Path
from typing import cast

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = REPOSITORY_ROOT / "hooks" / "workspace_confinement.py"


class TestWorkspaceConfinement(unittest.TestCase):
    def setUp(self) -> None:
        fixture = tempfile.TemporaryDirectory(prefix="cortex-hook-regression-")
        self.addCleanup(fixture.cleanup)
        self.root = Path(fixture.name).resolve()
        self.projects = self.root / "projects with spaces"
        self.config = self.root / "config with spaces"
        self.outside = self.root / "outside"
        for directory in (self.projects, self.config, self.outside):
            directory.mkdir()
        (self.config / "hooks").mkdir()
        shutil.copyfile(HOOK_PATH, self.config / "hooks" / HOOK_PATH.name)
        data = cast(
            dict[str, dict[str, object]],
            json.loads((REPOSITORY_ROOT / "hooks.json").read_text(encoding="utf-8")),
        )
        entries = cast(
            list[dict[str, object]], data["workspace-confinement-gate"]["PreToolUse"]
        )
        handlers = cast(list[dict[str, object]], entries[0]["hooks"])
        self.configured_command = cast(str, handlers[0]["command"])

    def request(self, target: Path | str, name: str = "write_to_file") -> bytes:
        return json.dumps(
            {"toolCall": {"name": name, "args": {"TargetFile": str(target)}}}
        ).encode("utf-8")

    def run_hook(
        self,
        raw: bytes,
        roots: Sequence[Path] | None = None,
        *,
        configured: bool = False,
    ) -> dict[str, str]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
        if configured:
            env["CORTEX_CONFIG_ROOT"] = str(self.config)
            env["CORTEX_PROJECTS_ROOT"] = str(self.projects)
            command = ["bash", "-e", "-o", "pipefail", "-c", self.configured_command]
        else:
            command = [sys.executable, "-B", str(HOOK_PATH)]
            for root in (self.projects, self.config) if roots is None else roots:
                command.extend(["--allow-root", str(root)])
        before = sorted(str(path) for path in self.root.rglob("*"))
        result = subprocess.run(
            command,
            input=raw,
            cwd=self.root,
            env=env,
            capture_output=True,
            check=False,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8"))
        self.assertEqual(result.stderr, b"")
        self.assertEqual(len(result.stdout.splitlines()), 1, result.stdout)
        response = cast(dict[str, str], json.loads(result.stdout))
        self.assertIn(response["decision"], ("allow", "deny"))
        if response["decision"] == "deny":
            self.assertTrue(response["reason"])
        self.assertEqual(before, sorted(str(path) for path in self.root.rglob("*")))
        return response

    def assert_denied(self, raw: bytes, roots: Sequence[Path] | None = None) -> None:
        self.assertEqual(self.run_hook(raw, roots)["decision"], "deny")

    def test_both_supported_writers_can_target_authorized_project_files(self) -> None:
        for name in ("write_to_file", "replace_file_content"):
            with self.subTest(tool=name):
                response = self.run_hook(self.request(self.projects / "new.py", name))
                self.assertEqual(response, {"decision": "allow"})

    def test_configuration_files_under_an_authorized_root_are_allowed(self) -> None:
        response = self.run_hook(self.request(self.config / "new-rule.md"))
        self.assertEqual(response["decision"], "allow")

    def test_new_files_with_missing_parent_directories_are_allowed_inside_roots(
        self,
    ) -> None:
        response = self.run_hook(
            self.request(self.projects / "new" / "nested" / "file.py")
        )
        self.assertEqual(response["decision"], "allow")

    def test_existing_files_inside_roots_are_allowed_without_modification(self) -> None:
        target = self.projects / "existing.py"
        target.write_text("original\n", encoding="utf-8")
        self.assertEqual(self.run_hook(self.request(target))["decision"], "allow")
        self.assertEqual(target.read_text(encoding="utf-8"), "original\n")

    def test_external_destinations_are_rejected(self) -> None:
        self.assert_denied(self.request(self.outside / "new.py"))

    def test_temporary_filenames_do_not_bypass_external_destination_rejection(
        self,
    ) -> None:
        for name in ("temp.py", "tmp.py", "scratch.py", "ephemeral.py", "bomb.py"):
            with self.subTest(name=name):
                self.assert_denied(self.request(self.outside / name))

    def test_sibling_path_prefixes_do_not_count_as_authorized_roots(self) -> None:
        sibling = self.root / f"{self.projects.name}-other"
        sibling.mkdir()
        self.assert_denied(self.request(sibling / "new.py"))

    def test_parent_traversal_cannot_escape_an_authorized_root(self) -> None:
        self.assert_denied(self.request(self.projects / ".." / "outside" / "new.py"))

    def test_relative_paths_are_rejected(self) -> None:
        self.assert_denied(self.request("projects with spaces/new.py"))

    def test_empty_and_malformed_inputs_are_rejected(self) -> None:
        for raw in (b"", b" \n\t", b'{"toolCall":', b"{}{}", b"\xff"):
            with self.subTest(raw=raw):
                self.assert_denied(raw)

    def test_non_object_payloads_are_rejected(self) -> None:
        for value in (None, True, 1, "event", []):
            with self.subTest(value=value):
                self.assert_denied(json.dumps(value).encode("utf-8"))

    def test_missing_or_mistyped_tool_calls_are_rejected(self) -> None:
        for payload in (
            {},
            {"toolCall": None},
            {"toolCall": []},
            {"toolCall": "write"},
        ):
            with self.subTest(payload=payload):
                self.assert_denied(json.dumps(payload).encode("utf-8"))

    def test_missing_mistyped_and_unknown_tool_names_are_rejected(self) -> None:
        for name in (None, [], 1, "run_command", "unexpected"):
            with self.subTest(name=name):
                payload = {
                    "toolCall": {
                        "name": name,
                        "args": {"TargetFile": str(self.projects / "new.py")},
                    }
                }
                self.assert_denied(json.dumps(payload).encode("utf-8"))
        self.assert_denied(b'{"toolCall":{"args":{}}}')

    def test_missing_or_mistyped_arguments_are_rejected(self) -> None:
        for args in (None, [], "args", 1):
            with self.subTest(args=args):
                payload = {"toolCall": {"name": "write_to_file", "args": args}}
                self.assert_denied(json.dumps(payload).encode("utf-8"))
        self.assert_denied(b'{"toolCall":{"name":"write_to_file"}}')

    def test_missing_empty_mistyped_and_nul_target_paths_are_rejected(self) -> None:
        for target in (None, [], 1, "", " \n", "\x00invalid"):
            with self.subTest(target=target):
                payload = {
                    "toolCall": {
                        "name": "write_to_file",
                        "args": {"TargetFile": target},
                    }
                }
                self.assert_denied(json.dumps(payload).encode("utf-8"))
        self.assert_denied(b'{"toolCall":{"name":"write_to_file","args":{}}}')

    def test_duplicate_keys_are_rejected_at_every_event_level(self) -> None:
        request = self.request(self.projects / "new.py").decode("utf-8")
        for raw in (
            request.replace('"toolCall":', '"toolCall": {}, "toolCall":', 1),
            request.replace('"name":', '"name": "replace_file_content", "name":', 1),
            request.replace('"args":', '"args": {}, "args":', 1),
            request.replace(
                '"TargetFile":', '"TargetFile": "/outside", "TargetFile":', 1
            ),
        ):
            with self.subTest(raw=raw):
                self.assert_denied(raw.encode("utf-8"))

    def test_non_finite_numbers_are_rejected_even_in_other_event_fields(self) -> None:
        request = self.request(self.projects / "new.py").decode("utf-8")
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                raw = request[:-1] + f', "metadata": {constant}' + "}"
                self.assert_denied(raw.encode("utf-8"))

    def test_event_supplied_roots_cannot_authorize_external_paths(self) -> None:
        payload = cast(
            dict[str, object], json.loads(self.request(self.outside / "new.py"))
        )
        payload["allowedRoots"] = [str(self.outside)]
        self.assert_denied(json.dumps(payload).encode("utf-8"))

    def test_authorization_requires_at_least_one_root(self) -> None:
        self.assert_denied(self.request(self.projects / "new.py"), roots=[])

    def test_all_authorized_roots_must_be_existing_absolute_directories(self) -> None:
        root_file = self.root / "not-a-directory"
        root_file.touch()
        for root in (Path("relative"), self.root / "missing", root_file):
            with self.subTest(root=root):
                self.assert_denied(
                    self.request(self.projects / "new.py"), roots=[self.projects, root]
                )

    def test_directory_destinations_and_roots_themselves_are_rejected(self) -> None:
        nested = self.projects / "existing-directory"
        nested.mkdir()
        for target in (self.projects, nested):
            with self.subTest(target=target):
                self.assert_denied(self.request(target))

    def test_symlinks_to_external_directories_are_rejected(self) -> None:
        link = self.projects / "escape"
        link.symlink_to(self.outside, target_is_directory=True)
        self.assert_denied(self.request(link / "new.py"))

    def test_symlinks_to_external_files_are_rejected(self) -> None:
        target = self.outside / "existing.py"
        target.touch()
        link = self.projects / "linked.py"
        link.symlink_to(target)
        self.assert_denied(self.request(link))

    def test_dangling_symlinks_to_external_paths_are_rejected(self) -> None:
        link = self.projects / "dangling"
        link.symlink_to(self.outside / "missing")
        self.assert_denied(self.request(link / "new.py"))

    def test_symlink_loops_are_rejected(self) -> None:
        link = self.projects / "loop"
        link.symlink_to("loop")
        self.assert_denied(self.request(link / "new.py"))

    def test_symlinks_remaining_inside_authorized_roots_are_allowed(self) -> None:
        nested = self.projects / "nested"
        nested.mkdir()
        link = self.projects / "alias"
        link.symlink_to(nested, target_is_directory=True)
        self.assertEqual(
            self.run_hook(self.request(link / "new.py"))["decision"], "allow"
        )

    def test_authorized_symlink_roots_are_canonicalized(self) -> None:
        link = self.root / "projects alias"
        link.symlink_to(self.projects, target_is_directory=True)
        self.assertEqual(
            self.run_hook(self.request(link / "new.py"), roots=[link])["decision"],
            "allow",
        )

    def test_paths_traversing_through_a_file_are_rejected(self) -> None:
        target = self.projects / "file.py"
        target.touch()
        self.assert_denied(self.request(target / "child.py"))

    def test_configured_command_allows_project_and_configuration_files_with_spaces(
        self,
    ) -> None:
        for root in (self.projects, self.config):
            with self.subTest(root=root):
                result = self.run_hook(
                    self.request(root / "new file.py"), configured=True
                )
                self.assertEqual(result["decision"], "allow")

    def test_configured_command_rejects_external_and_malformed_events(self) -> None:
        for raw in (self.request(self.outside / "temp.py"), b"", b'{"toolCall":'):
            with self.subTest(raw=raw):
                self.assertEqual(
                    self.run_hook(raw, configured=True)["decision"], "deny"
                )


if __name__ == "__main__":
    unittest.main()
