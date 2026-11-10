# MOSKV GitHub Fleet Steward

Read-only inventory and evidence-backed topology for a mixed public/private GitHub account, plus an explicitly approved review-issue gate. **Python 3.11+, zero packages**.

### Use on your Mac

```sh
gh auth login                        # one-time, with access to your private repos
python3 scripts/github_fleet_steward.py scan --owner borjamoskv --scope all
open ~/.local/share/moskv-github-steward/all/report.md
```

**Outputs:** `inventory.json` (metadata), `graph.mmd` (observed links), `plan.json` (stable proposal IDs), `report.md` (human review backlog). All-scope output stays local, outside tracked Git trees, mode 0700 directory / 0600 files. Nothing is archived, deleted, renamed, pushed or made public by `scan`.

For public-only recurring inspection:

```sh
python3 scripts/github_fleet_steward.py scan --owner borjamoskv --scope public
```

To open **one** explicitly approved review issue:

```sh
python3 scripts/github_fleet_steward.py apply \
  --plan ~/.local/share/moskv-github-steward/all/plan.json \
  --repo REPOSITORY_NAME \
  --approve STW-REVIEWED_ID \
  --confirm OPEN_REVIEW_ISSUE
```

The issue gate checks live account ownership, target archival status, and prior issues for a matching marker before posting. Other mutations require separate human review in GitHub. GitHub Actions is configured with `contents: read` and scans only public repositories, never using a token that has private-repo access.

### Operating model

- **Inventory:** 100/page GitHub REST pagination, private owner identity check, no partial silent truncation.
- **Topology:** only actual `github.com/<owner>/<repository>` links found in README or common manifests; every observed edge stores its source file and line. Not a proven dependency graph.
- **Hygiene:** flagged missing docs, potential duplicate names, CI policy review, archived targets referenced by active repositories. Nothing auto-archives.
- **Review gate:** all recommendations are non-binding. `apply` creates a single *review issue*, not a PR/merge.
- **No token leakage:** uses `GH_TOKEN`, `GITHUB_TOKEN` or `gh auth token`; tokens never enter output or command arguments.

Known boundaries: root README/manifest scanning does not search every branch or every nested module; it does not prove whether a repo is in production, abandoned, or safe to delete. GitHub's `pushed_at` is a weak activity signal. High-quality dependency contracts must be verified within the relevant project before wiring code. Run a new scan immediately before acting on old reports.

### Copilot custom agent

After merging the draft PR to the repository default branch, GitHub Copilot can discover the native profile at `.github/agents/moskv-github-steward.agent.md` (user-invocable only). Copilot's built-in token is scoped to the source repository; the cloud profile runs public-only by default, while a local GitHub CLI session with the owner's credentials can scan the full private fleet. Do not treat a profile file as an autonomous running process.