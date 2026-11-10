"""Offline regression tests for MOSKV GitHub Fleet Steward."""
import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

# Also works when this file lives in .github/tests in the source repo.
SRC = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SRC))
import github_fleet_steward as steward


class FakeGitHub:
    def __init__(self, records=None):
        self.records = records or {}
        self.writes = []

    def get(self, path, optional=False):
        return self.records.get(path)

    def post(self, path, payload):
        self.writes.append((path, payload))
        return {"html_url": "https://github.com/borjamoskv/proj/issues/1"}


def repo(name, archived=False, private=False):
    return {"name": name, "owner": {"login": "borjamoskv"}, "archived": archived,
            "private": private, "pushed_at": "2026-11-09T00:00:00Z", "default_branch": "main"}


def encoded(contents):
    return {"type": "file", "encoding": "base64", "content": base64.b64encode(contents.encode()).decode()}


class InventoryTests(unittest.TestCase):
    def test_pagination_over_100_and_private_owner_identity(self):
        page1 = [repo(f"project-{n:03d}") for n in range(100)]
        page2 = [repo(f"project-{n:03d}") for n in range(100, 136)]
        api = FakeGitHub({
            "/user": {"login": "borjamoskv"},
            "/user/repos?affiliation=owner&sort=full_name&direction=asc&per_page=100&page=1": page1,
            "/user/repos?affiliation=owner&sort=full_name&direction=asc&per_page=100&page=2": page2,
        })
        results = steward.paginated_repos(api, "borjamoskv", "all")
        self.assertEqual(len(results), 136)
        self.assertEqual(results[0]["name"], "project-000")
        self.assertEqual(results[-1]["name"], "project-135")

    def test_owner_mismatch_fails_closed(self):
        api = FakeGitHub({"/user": {"login": "not-owner"}})
        with self.assertRaises(PermissionError):
            steward.paginated_repos(api, "borjamoskv", "all")

    def test_cross_repo_link_has_evidence_but_not_invented_dependency(self):
        files = [{"name": "README.md", "type": "file"}]
        api = FakeGitHub({
            "/repos/borjamoskv/alpha/contents": files,
            "/repos/borjamoskv/alpha/contents/README.md": encoded("# Alpha\nSee https://github.com/borjamoskv/beta/docs\n"),
        })
        result = steward.inspect_repo(api, repo("alpha"), {"alpha": "alpha", "beta": "beta"})
        self.assertTrue(result["root_scanned"])
        self.assertEqual(result["edges"], [{"from": "alpha", "to": "beta", "kind": "documentation_reference", "evidence": "README.md:L2"}])
        self.assertFalse(result["ci"])

    def test_clone_urls_do_not_create_ghost_repositories(self):
        api = FakeGitHub({
            "/repos/borjamoskv/alpha/contents": [{"name": "README.md", "type": "file"}],
            "/repos/borjamoskv/alpha/contents/README.md": encoded("git clone https://github.com/borjamoskv/beta.git\n"),
        })
        result = steward.inspect_repo(api, repo("alpha"), {"alpha": "alpha", "beta": "beta"})
        self.assertEqual(result["edges"], [{"from": "alpha", "to": "beta", "kind": "documentation_reference", "evidence": "README.md:L1"}])

    def test_nonexistent_repos_do_not_generate_edges(self):
        api = FakeGitHub({
            "/repos/borjamoskv/alpha/contents": [{"name": "README.md", "type": "file"}],
            "/repos/borjamoskv/alpha/contents/README.md": encoded("https://github.com/other/beta\nhttps://github.com/borjamoskv/ghost\n"),
        })
        result = steward.inspect_repo(api, repo("alpha"), {"alpha": "alpha", "beta": "beta"})
        self.assertEqual(result["edges"], [])

    def test_archived_reference_flag_only_when_observed(self):
        scan = {"name": "alpha", "root_scanned": True, "readme": True,
                "ci": True, "security": True, "edges": [{"from": "alpha", "to": "beta", "kind": "documentation_reference", "evidence": "README.md:L2"}]}
        plan = steward.build_plan([repo("alpha"), repo("beta", archived=True)], {"alpha": scan}, datetime(2026, 11, 10, tzinfo=timezone.utc))
        self.assertIn("reference_to_archived_repo", [x["finding"] for x in plan])
        self.assertNotIn("readme_missing", [x["finding"] for x in plan])

    def test_private_output_rejects_git_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            (parent / ".git").mkdir()
            with self.assertRaises(PermissionError):
                steward.secure_output(parent / "reports", "all", {"report.md": "private"})

    def test_plan_confirm_and_exact_repo_gate(self):
        proposal = steward.item("proj", "readme_missing", "Root directory contains no README", "Add a scoped README via a reviewable PR", "medium")
        data = {"schema": "moskv-steward-plan/v1", "owner": "borjamoskv", "scope": "all", "proposals": [proposal]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(data))
            from types import SimpleNamespace
            args = SimpleNamespace(plan=path, repo="proj", approve=proposal["id"], confirm="wrong")
            api = FakeGitHub()
            with self.assertRaises(PermissionError):
                steward.apply_command(args, api)
            self.assertEqual(api.writes, [])
            args.confirm = "OPEN_REVIEW_ISSUE"
            args.repo = "another-project"
            api.records["/user"] = {"login": "borjamoskv"}
            with self.assertRaises(PermissionError):
                steward.apply_command(args, api)
            self.assertEqual(api.writes, [])

    def test_existing_issue_idempotent(self):
        proposal = steward.item("proj", "readme_missing", "Root directory contains no README", "Add a scoped README via a reviewable PR", "medium")
        data = {"schema": "moskv-steward-plan/v1", "owner": "borjamoskv", "scope": "all", "proposals": [proposal]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(data))
            from types import SimpleNamespace
            args = SimpleNamespace(plan=path, repo="proj", approve=proposal["id"], confirm="OPEN_REVIEW_ISSUE")
            api = FakeGitHub({
                "/user": {"login": "borjamoskv"},
                "/repos/borjamoskv/proj": repo("proj"),
                "/repos/borjamoskv/proj/issues?state=all&per_page=100&page=1": [{"body": f"<!-- moskv-steward:{proposal['id']} -->"}],
            })
            self.assertEqual(steward.apply_command(args, api), 0)
            self.assertEqual(api.writes, [])


if __name__ == "__main__":
    unittest.main()
