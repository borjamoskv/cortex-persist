#!/usr/bin/env python3
"""MOSKV GitHub Steward: paginated fleet inventory, evidence graph, safe issue gate.

Python 3.11+; standard library only. `scan` is strictly read-only.
`apply` can create ONE review issue only after a specific human confirmation.
"""
from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from difflib import SequenceMatcher
from email.utils import parsedate_to_datetime
import hashlib
from http.client import HTTPException
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

API = "https://api.github.com"
VERSION = "2026-11-10-v3"
EXIT_OK, EXIT_ERROR, EXIT_PARTIAL = 0, 2, 3
MAX_PLAN_AGE_SECONDS = 7 * 24 * 60 * 60
MAX_RETRY_AFTER_SECONDS = 60
ALLOWED_FINDINGS = frozenset({
    "reference_to_archived_repo", "readme_missing", "ci_not_observed",
    "security_policy_missing", "deep_scan_incomplete", "stale_180_days",
    "no_observed_inbound_links", "possible_duplicate_name",
})
SLUG = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")
URL_REF = re.compile(r"https?://(?:www\.)?github\.com/([\w.-]+)/([\w.-]+)", re.I)
ACTION_REF = re.compile(r"^\s*(?:-\s*)?uses:\s*['\"]?([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:/[^@ ]+)?@", re.I)
SOURCE_FILES = {"pyproject.toml", "package.json", "Cargo.toml", "go.mod", "requirements.txt", ".gitmodules"}
PUBLIC_GROUPS = {
    "runtime-security": ("babylon", "c5-rea", "cassandra", "sanedrin", "guard", "socint"),
    "knowledge-formal": ("cortex", "axiom", "anvil", "teorema", "corpus", "epistemic"),
    "music-media": ("flstudio", "audio", "master", "music", "montage"),
    "sites-design": ("site", "web", "naroa", "landing", ".com", ".online"),
    "automation-tools": ("mcp", "maestro", "gflow", "mandato", "agents", "bot"),
}


def slug(value: str) -> str:
    if not SLUG.fullmatch(value):
        raise ValueError(f"Invalid GitHub owner/repo slug: {value!r}")
    return value


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def auth_token(required: bool) -> str:
    token = os.getenv("GH_TOKEN", "").strip() or os.getenv("GITHUB_TOKEN", "").strip()
    if not token:
        try:
            token = subprocess.run(
                ["gh", "auth", "token"], capture_output=True, text=True,
                timeout=5, check=False,
            ).stdout.strip()
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    if not token and required:
        raise ValueError("Private inventory needs GH_TOKEN or `gh auth login`.")
    # http.client refuses such a header value with an error that quotes it, token included.
    if any(ch.isspace() or not ch.isprintable() for ch in token):
        raise ValueError("Invalid GitHub token format")
    return token


class RateLimitError(RuntimeError):
    """GitHub will not answer again soon: rate limit exhausted, or a Retry-After too long to sit out."""


class NoRedirectHandler(HTTPRedirectHandler):
    """Refuses redirects: urllib would forward the token and replay a POST as a GET without its body."""

    def redirect_request(self, req, fp, code, msg, headers, newurl) -> None:
        return None


urlopen = build_opener(NoRedirectHandler).open


def retry_after_seconds(value: str | None, now: datetime) -> int | None:
    """Wait asked for by a Retry-After value (integer seconds or HTTP-date), at least 1; None if absent or unparseable."""
    try:
        return max(1, int(value or ""))
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value or "")
    except (ValueError, OverflowError):
        return None
    if when.tzinfo is None:  # An HTTP-date is GMT even when its zone is missing or "-0000".
        when = when.replace(tzinfo=timezone.utc)
    return max(1, math.ceil((when - now).total_seconds()))


def reset_time(value: str | None) -> str | None:
    """UTC ISO-8601 form of an x-ratelimit-reset epoch; None if absent, not a number or out of range."""
    try:
        return datetime.fromtimestamp(int(value or ""), timezone.utc).isoformat(timespec="seconds")
    except (ValueError, OverflowError, OSError):
        return None


def failure_name(exc: Exception) -> str:
    """Type name of a transport failure. Its text is never reported: it can echo the URL with its query string."""
    cause = exc.reason if isinstance(exc, URLError) and isinstance(exc.reason, Exception) else exc
    return type(cause).__name__


class Github:
    def __init__(self, token: str = "", timeout: int = 20):
        self.token, self.timeout = token, timeout

    def request(self, method: str, path: str, payload: dict | None = None, optional: bool = False):
        route = path.split("?", 1)[0]
        dot_segment = any(part in (".", "..") for part in route.split("/"))
        if not path.startswith("/") or "//" in route or dot_segment or "?" not in path and "#" in path:
            raise ValueError("Invalid GitHub API path")
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "moskv-github-steward/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        data = json.dumps(payload).encode() if payload is not None else None
        if data is not None:
            headers["Content-Type"] = "application/json"
        request = Request(API + path, method=method, headers=headers, data=data)
        # Only reads are repeated: a write whose answer was lost may already have taken effect.
        retries = 2 if method == "GET" else 0
        for attempt in range(retries + 1):
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    body = response.read(5_000_000)
                    return json.loads(body) if body else None
            except HTTPError as exc:
                exc.close()  # Frees the connection; the status and headers stay readable.
                if exc.code == 404 and optional:
                    return None
                if exc.code in (403, 429) and exc.headers.get("x-ratelimit-remaining") == "0":
                    reset = reset_time(exc.headers.get("x-ratelimit-reset"))
                    raise RateLimitError(f"GitHub rate limit exhausted for {method} {route}"
                                         + (f"; resets at {reset}" if reset else "")) from None
                if exc.code in (301, 302, 303, 307, 308):
                    raise RuntimeError(f"GitHub HTTP {exc.code} redirect refused for {method} {route}") from None
                retry_after = exc.headers.get("Retry-After")
                retryable = method == "GET" and (
                    exc.code in (429, 500, 502, 503, 504) or exc.code == 403 and bool(retry_after)
                )
                delay = retry_after_seconds(retry_after, utc_now()) if retryable else None
                if delay is not None and delay > MAX_RETRY_AFTER_SECONDS:
                    raise RateLimitError(
                        f"GitHub asked to wait {delay} seconds before retrying {method} {route} (HTTP {exc.code})"
                    ) from None
                if not retryable or attempt == retries:
                    raise RuntimeError(f"GitHub HTTP {exc.code} for {method} {route}") from None
                time.sleep(2**attempt if delay is None else delay)
            except (OSError, HTTPException, ValueError) as exc:
                failure = f"GitHub request failed for {method} {route}: {failure_name(exc)}"
                if method != "GET":
                    raise RuntimeError(failure + "; outcome unknown, not retried") from None
                if attempt == retries:
                    raise RuntimeError(failure) from None
                time.sleep(2**attempt)
        raise RuntimeError("GitHub API retry exhausted")

    def get(self, path: str, optional: bool = False):
        return self.request("GET", path, optional=optional)

    def post(self, path: str, payload: dict):
        return self.request("POST", path, payload=payload)


def paginated_repos(api: Github, owner: str, scope: str) -> list[dict]:
    owner = slug(owner)
    if scope == "all":
        me = api.get("/user")
        if not me or me.get("login", "").casefold() != owner.casefold():
            raise PermissionError("Authenticated GitHub identity must match --owner for private scan.")
        prefix = "/user/repos?affiliation=owner&sort=full_name&direction=asc"
    else:
        prefix = f"/users/{owner}/repos?sort=full_name&direction=asc"
    output: dict[str, dict] = {}
    for page in range(1, 21):
        batch = api.get(f"{prefix}&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Unexpected repository API response")
        for repo in batch:
            if (repo.get("owner") or {}).get("login", "").casefold() == owner.casefold():
                if scope != "public" or not repo.get("private", False):
                    output[repo["name"].casefold()] = repo
        if len(batch) < 100:
            break
    else:
        raise RuntimeError("Repository pagination exceeded 2000 results; refusing partial inventory")
    return sorted(output.values(), key=lambda x: x["name"].casefold())


def text_content(obj: dict | None) -> str | None:
    if not obj or obj.get("type") not in (None, "file"):
        return None
    if obj.get("encoding") != "base64" or not obj.get("content"):
        return None
    try:
        return base64.b64decode(obj["content"], validate=False).decode("utf-8", "replace")[:180_000]
    except (ValueError, TypeError):
        return None


def inspect_repo(api: Github, repo: dict, names: dict[str, str]) -> dict:
    owner, name = slug(repo["owner"]["login"]), slug(repo["name"])
    path = f"/repos/{owner}/{name}"
    inspection: dict = {"name": name, "root_scanned": False, "readme": None, "ci": None,
                        "security": None, "files_checked": [], "edges": [], "errors": []}
    try:
        entries = api.get(path + "/contents", optional=True)
        if not isinstance(entries, list):
            inspection["errors"].append("root_contents_unavailable")
            return inspection
        inspection["root_scanned"] = True
        files = {x.get("name", "").casefold(): x.get("name", "") for x in entries if x.get("type") == "file"}
        dirs = {x.get("name", "").casefold() for x in entries if x.get("type") == "dir"}
        inspection["readme"] = any(n.startswith("readme") for n in files)
        inspection["security"] = "security.md" in files or ".github" in dirs  # May exist in .github; unknown unless checked.
        inspection["ci"] = None  # Do not infer CI from presence of .github alone.
        workflow_files = []
        if ".github" in dirs:
            workflows = api.get(path + "/contents/.github/workflows", optional=True)
            inspection["ci"] = bool(workflows) if isinstance(workflows, list) else None
            if isinstance(workflows, list):
                workflow_files = [".github/workflows/" + item["name"] for item in workflows
                                  if item.get("type") == "file" and item.get("name", "").endswith((".yml", ".yaml"))][:12]
            else:
                inspection["errors"].append("workflows_unavailable")
            if "security.md" not in files:
                inspection["security"] = None  # Unknown until .github/SECURITY.md checked.
        else:
            inspection["ci"] = False
            inspection["security"] = "security.md" in files
        candidate_files = [p for p in files.values() if p.casefold().startswith("readme")]
        candidate_files += [files[p.casefold()] for p in SOURCE_FILES if p.casefold() in files]
        candidate_files = list(dict.fromkeys(candidate_files))[:7] + workflow_files
        for filename in candidate_files:
            try:
                item = api.get(path + "/contents/" + quote(filename, safe="/"), optional=True)
                contents = text_content(item)
                if contents is None:
                    continue
                inspection["files_checked"].append(filename)
                for lineno, line in enumerate(contents.splitlines(), start=1):
                    if filename.startswith(".github/workflows/"):
                        action = ACTION_REF.search(line)
                        if action and action.group(1).casefold() == owner.casefold():
                            target = names.get(action.group(2).casefold())
                            if target and target.casefold() != name.casefold():
                                edge = {"from": name, "to": target, "kind": "workflow_action_reference",
                                        "evidence": f"{filename}:L{lineno}"}
                                if edge not in inspection["edges"] and len(inspection["edges"]) < 120:
                                    inspection["edges"].append(edge)
                    for match in URL_REF.finditer(line):
                        if match.group(1).casefold() != owner.casefold():
                            continue
                        candidate = match.group(2).rstrip(".,);]")
                        if candidate.casefold().endswith(".git"):
                            candidate = candidate[:-4]  # Clone URL, not a different repository.
                        dest = names.get(candidate.casefold())
                        if not dest or dest.casefold() == name.casefold():
                            continue
                        edge = {"from": name, "to": dest, "kind": "manifest_reference" if filename in SOURCE_FILES else "documentation_reference",
                                "evidence": f"{filename}:L{lineno}"}
                        if edge not in inspection["edges"] and len(inspection["edges"]) < 120:
                            inspection["edges"].append(edge)
            except RuntimeError:
                inspection["errors"].append(f"cannot_read:{filename}")
        # `SECURITY.md` under .github is a valid location but not proof of an implemented security process.
        if inspection["security"] is None:
            inspection["security"] = api.get(path + "/contents/.github/SECURITY.md", optional=True) is not None
    except RuntimeError:
        inspection["errors"].append("inspection_request_failed")
    return inspection


def group_for(name: str) -> str:
    lower = name.casefold()
    for group, words in PUBLIC_GROUPS.items():
        if any(word in lower for word in words):
            return group
    return "other"


def age_days(value: str | None, now: datetime) -> int | None:
    if not value:
        return None
    try:
        return max(0, (now - datetime.fromisoformat(value.replace("Z", "+00:00"))).days)
    except (ValueError, TypeError):
        return None


def normalize_name(name: str) -> str:
    return re.sub(r"(?:-vieja|-old|-alpha|-v\d+|-\d+)$", "", name.casefold())


def item(repo: str, finding: str, evidence: str, proposal: str, priority: str) -> dict:
    digest = hashlib.sha256("\x1f".join([repo, finding, evidence, proposal]).encode()).hexdigest()[:14]
    return {"id": "STW-" + digest, "repo": repo, "finding": finding,
            "evidence": evidence, "proposal": proposal, "priority": priority,
            "action": "open_review_issue"}


def build_plan(repos: list[dict], inspections: dict[str, dict], now: datetime, deep_requested: bool = True) -> list[dict]:
    findings: list[dict] = []
    incoming = {r["name"].casefold(): 0 for r in repos}
    archive_by_name = {r["name"].casefold(): bool(r.get("archived")) for r in repos}
    for scan in inspections.values():
        for edge in scan["edges"]:
            if edge["to"].casefold() not in incoming:
                continue
            incoming[edge["to"].casefold()] += 1
            if archive_by_name[edge["to"].casefold()] and not archive_by_name.get(scan["name"].casefold(), False):
                findings.append(item(edge["from"], "reference_to_archived_repo", edge["evidence"] + " => " + edge["to"],
                                     "Verify integration, document replacement or unarchive after explicit approval", "high"))
    # Weak "no observed inbound links" findings require complete active-fleet
    # source inspection; a skipped or inaccessible repo must not imply isolation.
    all_active_inspected = all(
        (entry := inspections.get(r["name"].casefold())) is not None
        and entry.get("root_scanned") and not entry.get("errors")
        for r in repos if not r.get("archived")
    )
    for repo in repos:
        name = repo["name"]
        scan = inspections.get(name.casefold())
        if repo.get("archived"):
            continue
        if scan and scan["root_scanned"]:
            if scan["readme"] is False:
                findings.append(item(name, "readme_missing", "Root directory contains no README", "Add a scoped README via a reviewable PR", "medium"))
            if scan["ci"] is False:
                findings.append(item(name, "ci_not_observed", "No .github/workflows found", "Assess whether this repository needs a CI workflow", "low"))
            if not repo.get("private") and scan["security"] is False:
                findings.append(item(name, "security_policy_missing", "No root or .github/SECURITY.md found", "Assess vulnerability disclosure process", "low"))
        if deep_requested and (scan is None or not scan["root_scanned"]):
            findings.append(item(name, "deep_scan_incomplete", "Repository content scan not completed", "Re-run scan with adequate permission and rate budget", "low"))
        age = age_days(repo.get("pushed_at"), now)
        if age is not None and age > 180:
            findings.append(item(name, "stale_180_days", f"Last push {age} days ago", "Review project lifecycle; never auto-archive", "low"))
        if incoming[name.casefold()] == 0 and all_active_inspected:
            findings.append(item(name, "no_observed_inbound_links", "No inbound references observed in fully inspected active repos", "Review documentation links; this does not prove isolation", "low"))
    # Names alone are weak evidence, so a duplicate flag is *never* a delete request.
    candidates = sorted(repos, key=lambda r: r["name"].casefold())
    for i, left in enumerate(candidates):
        for right in candidates[i + 1:]:
            a, b = normalize_name(left["name"]), normalize_name(right["name"])
            if a == b or (min(len(a), len(b)) >= 8 and SequenceMatcher(None, a, b).ratio() >= .91):
                target = left if not left.get("archived") else right
                findings.append(item(target["name"], "possible_duplicate_name",
                                     left["name"] + " vs " + right["name"],
                                     "Compare source trees, releases and consumers before any consolidation", "low"))
    return sorted({f["id"]: f for f in findings}.values(), key=lambda f: (0 if f["priority"] == "high" else 1 if f["priority"] == "medium" else 2, f["repo"], f["finding"]))


def markdown_report(owner: str, scope: str, repos: list[dict], scans: dict[str, dict], plan: list[dict], now: datetime) -> str:
    active = sum(not r.get("archived") for r in repos)
    private = sum(bool(r.get("private")) for r in repos)
    edges = sum(len(x["edges"]) for x in scans.values())
    lines = [f"# GitHub fleet audit: `{owner}`", "", f"Observed at: {now.isoformat(timespec='seconds')}",
             f"Scope: `{scope}` | Total: **{len(repos)}** | Active: **{active}** | Archived: **{len(repos)-active}** | Private: **{private}**",
             f"Content inspections attempted: **{len(scans)}** | Root successful: **{sum(x.get('root_scanned', False) for x in scans.values())}** | With errors: **{sum(bool(x.get('errors')) for x in scans.values())}** | Intentionally unscanned: **{len(repos)-len(scans)}**",
             f"Observed explicit link occurrences: **{edges}**", "",
             "> References are evidence of *links*, not proof of runtime dependencies. Name similarities are review candidates, not duplicates.",
             "> GitHub state is not changed by `scan`. This report may be sensitive in `all` scope.", "",
             "## Review backlog", "", "| Priority | Repo | Finding | Evidence | Plan ID |", "|:--|:--|:--|:--|:--|" ]
    for p in plan:
        # Slug-validated repository names; evidence always generated by the scanner.
        evidence = p["evidence"].replace("|", "/").replace("\n", " ")
        lines.append(f"| {p['priority']} | `{p['repo']}` | {p['finding']} | {evidence} | `{p['id']}` |")
    if not plan:
        lines.append("| - | - | No findings with current rules | - | - |")
    lines += ["", "## Observed cross-repository references", "",
              "| Source | Target | Reference type | Evidence | Target state |",
              "|:--|:--|:--|:--|:--|"]
    status = {r["name"].casefold(): "archived" if r.get("archived") else "active" for r in repos}
    observed = sorted((edge for inspection in scans.values() for edge in inspection["edges"]),
                      key=lambda e: (e["from"].casefold(), e["to"].casefold(), e["evidence"]))
    for edge in observed:
        safe = lambda t: str(t).replace("|", "/").replace("\n", " ").replace("`", "'")
        lines.append(f"| `{safe(edge['from'])}` | `{safe(edge['to'])}` | {edge['kind']} | `{safe(edge['evidence'])}` | {status.get(edge['to'].casefold(), 'unknown')} |")
    if not observed:
        lines.append("| - | - | No references observed within scan coverage | - | - |")
    lines += ["", "## Active repository groups (name-based only)", ""]
    groups: dict[str, list[str]] = {}
    for repo in repos:
        if not repo.get("archived"):
            groups.setdefault(group_for(repo["name"]), []).append(repo["name"])
    for group, members in sorted(groups.items()):
        lines.append(f"- **{group}**: " + ", ".join(f"`{x}`" for x in sorted(members)))
    return "\n".join(lines) + "\n"


def mermaid_graph(repos: list[dict], scans: dict[str, dict]) -> str:
    lines = ["flowchart LR", "  %% Observed README/manifest references, not verified runtime dependencies."]
    present = {r["name"].casefold(): r for r in repos}
    node = lambda n: "R" + hashlib.sha1(n.casefold().encode()).hexdigest()[:10]
    for repo in repos:
        name = repo["name"]
        lines.append(f'  {node(name)}["{name}"]')
        if repo.get("archived"):
            lines.append(f"  class {node(name)} archived")
    links = {(e["from"], e["to"], e["kind"]) for x in scans.values() for e in x["edges"]}
    for source, target, kind in sorted(links):
        if source.casefold() in present and target.casefold() in present:
            lines.append(f"  {node(source)} -->|{ 'action' if kind == 'workflow_action_reference' else 'manifest' if kind == 'manifest_reference' else 'docs' }| {node(target)}")
    lines.append("  classDef archived fill:#ddd,stroke:#888,color:#555")
    return "\n".join(lines) + "\n"


def secure_output(out: Path, scope: str, payloads: dict[str, str]) -> None:
    """Write reports as owner-only atomic replacements, never following leaf symlinks."""
    raw = out.expanduser().absolute()
    if scope == "all":
        # Do not allow redirects through symlinked output path components.
        for parent in (raw, *raw.parents):
            if parent.is_symlink():
                raise PermissionError("Private output directory contains a symlink")
            if (parent / ".git").exists():
                raise PermissionError("Refusing private reports inside a Git worktree")
    destdir = raw.resolve()
    destdir.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Enforce private report permissions even when an existing directory was lax.
    if scope == "all":
        destdir.chmod(0o700)
    for filename, content in payloads.items():
        if not re.fullmatch(r"[a-zA-Z0-9_-]+\.(?:json|md|mmd)", filename):
            raise ValueError("Invalid output filename")
        dest = destdir / filename
        fd, temporary = tempfile.mkstemp(dir=destdir, prefix=".moskv-steward-")
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, dest)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def scan_command(args, api: Github) -> int:
    repos = paginated_repos(api, args.owner, args.scope)
    names = {r["name"].casefold(): r["name"] for r in repos}
    selected = [r for r in repos if not r.get("archived") or args.deep_archived]
    inspections: dict[str, dict] = {}
    if not args.no_deep:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            pending = {pool.submit(inspect_repo, api, r, names): r["name"] for r in selected}
            for fut in as_completed(pending):
                inspection = fut.result()
                inspections[inspection["name"].casefold()] = inspection
    now = utc_now()
    plan = build_plan(repos, inspections, now, deep_requested=not args.no_deep)
    output = {
        "schema": "moskv-steward/v1", "version": VERSION, "owner": args.owner,
        "scope": args.scope, "observed_at": now.isoformat(),
        "repos": [
            {"name": r["name"], "archived": bool(r.get("archived")), "private": bool(r.get("private")),
             "default_branch": r.get("default_branch"), "pushed_at": r.get("pushed_at"),
             "language": r.get("language"), "fork": bool(r.get("fork")),
             "html_url": r.get("html_url")}
            for r in repos
        ],
        "inspections": sorted(inspections.values(), key=lambda x: x["name"].casefold()),
        "coverage": {
            "active_total": sum(not r.get("archived") for r in repos),
            "archived_total": sum(bool(r.get("archived")) for r in repos),
            "attempted": 0 if args.no_deep else len(selected),
            "completed": sum(bool(x.get("root_scanned")) for x in inspections.values()),
            "incomplete": sum(bool(x.get("errors")) or not x.get("root_scanned") for x in inspections.values()),
            "skipped_intentionally": len(repos) if args.no_deep else len(repos) - len(selected),
        },
    }
    plan_doc = {"schema": "moskv-steward-plan/v1", "owner": args.owner, "scope": args.scope,
                "generated_at": now.isoformat(), "proposals": plan}
    dest = args.out or Path.home() / ".local" / "share" / "moskv-github-steward" / args.scope
    secure_output(dest, args.scope, {
        "inventory.json": json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        "plan.json": json.dumps(plan_doc, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        "report.md": markdown_report(args.owner, args.scope, repos, inspections, plan, now),
        "graph.mmd": mermaid_graph(repos, inspections),
    })
    print(f"[READ-ONLY] {len(repos)} repositories; {len(inspections)} inspected; {len(plan)} review proposals. Reports: {dest}")
    return 0


def apply_command(args, api: Github) -> int:
    if args.confirm != "OPEN_REVIEW_ISSUE":
        raise PermissionError("Required: --confirm OPEN_REVIEW_ISSUE")
    document = json.loads(args.plan.read_text(encoding="utf-8"))
    if document.get("schema") != "moskv-steward-plan/v1":
        raise ValueError("Unknown plan schema")
    owner = slug(document["owner"])
    repo = slug(args.repo)
    scope = document.get("scope")
    if scope not in ("all", "public"):
        raise PermissionError("Unknown report scope")
    try:
        generated = datetime.fromisoformat(document["generated_at"].replace("Z", "+00:00"))
        age = (utc_now() - generated).total_seconds()
        if generated.tzinfo is None or age < -300 or age > MAX_PLAN_AGE_SECONDS:
            raise ValueError("Scan is expired or has an invalid timestamp")
    except (KeyError, ValueError, TypeError) as exc:
        raise PermissionError("Plan must have a recent, time-stamped scan (maximum 7 days)") from exc
    me = api.get("/user")
    if not me or me.get("login", "").casefold() != owner.casefold():
        raise PermissionError("GitHub identity mismatch")
    proposals = [p for p in document.get("proposals", []) if p.get("id") == args.approve and p.get("repo", "").casefold() == repo.casefold()]
    if len(proposals) != 1:
        raise PermissionError("No unique exact matching approval ID and repository")
    p = proposals[0]
    expected_id = item(p["repo"], p["finding"], p["evidence"], p["proposal"], p["priority"])["id"]
    if (p.get("action") != "open_review_issue" or expected_id != p["id"]
        or p.get("finding") not in ALLOWED_FINDINGS or p.get("priority") not in ("high", "medium", "low")
        or any(not isinstance(p.get(k), str) or len(p[k]) > 240 or "\n" in p[k] or "\r" in p[k]
               for k in ("finding", "evidence", "proposal"))):
        raise PermissionError("Tampered or non-allowlisted proposal")
    base = f"/repos/{owner}/{repo}"
    identity = api.get(base)
    if not identity or identity.get("archived") or (identity.get("owner") or {}).get("login", "").casefold() != owner.casefold():
        raise PermissionError("Target repo is archived or not owned")
    # Never publish evidence from private-fleet scans into a public issue.
    if scope == "all" and not identity.get("private", False):
        raise PermissionError("Public target requires a public-scope plan; rescan --scope public")
    marker = f"<!-- moskv-steward:{p['id']} -->"
    for page in range(1, 31):
        issues = api.get(base + f"/issues?state=all&per_page=100&page={page}")
        if any(marker in (issue.get("body") or "") for issue in issues):
            print(f"Existing review issue already recorded for {p['id']}; no new issue created")
            return 0
        if len(issues) < 100:
            break
    else:
        raise RuntimeError("Too many issues to verify idempotency; aborting")
    # Never interpolate file contents or untrusted repository descriptions into an issue.
    body = ("## Human review requested\n\n"
            + f"Finding: `{p['finding']}`\n\nEvidence: `{p['evidence']}`\n\n"
            + f"Proposed next step: {p['proposal']}\n\n"
            + "No repository deletion, archive, rename, visibility change, or merge is authorized by this issue.\n\n"
            + marker)
    created = api.post(base + "/issues", {"title": f"[GitHub Steward] Review {p['finding']}", "body": body})
    print(f"Created one review issue: {created.get('html_url', '(URL unavailable)')}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan", help="Read-only inventory, relationship graph and review backlog")
    scan.add_argument("--owner", default="borjamoskv")
    scan.add_argument("--scope", choices=("public", "all"), default="all")
    scan.add_argument("--out", type=Path)
    scan.add_argument("--deep-archived", action="store_true")
    scan.add_argument("--no-deep", action="store_true")
    scan.add_argument("--workers", type=int, choices=range(1, 9), default=3)
    apply = sub.add_parser("apply", help="Create ONE explicitly approved review issue; never mutates code")
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--repo", required=True)
    apply.add_argument("--approve", required=True)
    apply.add_argument("--confirm", required=True)
    args = parser.parse_args(argv)
    try:
        token = auth_token(required=(args.command == "apply" or (args.command == "scan" and args.scope == "all")))
        api = Github(token)
        return scan_command(args, api) if args.command == "scan" else apply_command(args, api)
    except (RuntimeError, ValueError, PermissionError, OSError, KeyError, TypeError) as exc:
        print(f"STEWARD ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
