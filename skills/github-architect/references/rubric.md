# Rubric & Disposition Taxonomy v2.0 — GitHub Architect

This document establishes the formal evaluation rubric, disposition taxonomy, impact vs. effort prioritization matrix, profile narrative alignment checks, and report skeleton for `github-architect` v2.0.

---

## 1. Disposition Taxonomy

Every repository evaluated by `github-architect` is classified into one of 6 primary dispositions based on activity, health score, strategic alignment, and repository structure:

| Disposition | Health Score Range | Definition & Criteria | Action Plan & Guidelines |
| :--- | :--- | :--- | :--- |
| **Flagship** | 85 – 100 (Grade A) | High-visibility active repositories representing core intellectual output, active maintenance, robust CI/CD, complete docs. | Maintain continuous integration, protect main branch, optimize README badges and visual presentation. |
| **Maintain** | 65 – 84 (Grade B/C) | Stable, functional projects in maintenance mode with low active commit frequency but reliable state. | Periodic security dependency updates, triage issues, document maintenance status. |
| **Incubate** | 50 – 74 (Grade C/D) | Experimental, active, or emerging projects with high potential but incomplete documentation or CI. | Add CI workflows via `--scaffold-ci`, complete README/License, establish clear roadmap before public promotion. |
| **Archive** | < 50 or Inactive > 1yr | Inactive, legacy, or completed repositories with historical value that should no longer receive commits. | **Default choice for abandoned repos.** Mark read-only/Archived via GitHub API. |
| **Delete** | 0 – 39 (Grade F) | Empty, accidental, temporary test repos or zero-value duplicates. | **Requires explicit imperative user request.** Never proposed as automatic default. |
| **Fork Hygiene** | Varies (Capped at 77) | Repositories forked from upstream orgs/users. | Evaluate if active contributions exist. Sync with upstream, convert to standalone if detached, or archive/delete if obsolete. |

---

## 2. Prioritization Matrix (Impact × Effort)

Actions generated during audits are prioritized into four quadrants:

```
                  HIGH IMPACT
         +-------------------+-------------------+
         |                   |                   |
         |    QUICK WINS     |    STRATEGIC      |
         |  - Add CI to      |  - Refactor docs  |
         |    Flagships      |    & architecture |
         |  - Fix broken     |  - Migrate forks  |
         |    links/badges   |    to packages    |
         |                   |                   |
LOW      +-------------------+-------------------+  HIGH
EFFORT   |                   |                   |  EFFORT
         |    FILL-INS       |   HARD CHOICES    |
         |  - Add License    |  - Complete       |
         |  - Update topic   |    abandoned      |
         |    tags           |    refactorings   |
         |  - Archive stale  |  - Full deprecation|
         |                   |                   |
         +-------------------+-------------------+
                  LOW IMPACT
```

---

## 3. Auto-Remediation & CI Scaffolds (v2.0)

`github-architect` v2.0 includes automated CI pipeline scaffolding for missing CI coverage:

- **Python Projects**: Installs dependencies (`pyproject.toml` / `requirements.txt`) and runs `pytest`.
- **Node/TypeScript/React Projects**: Installs npm dependencies and runs build + test steps.
- **Generic / Polyglot**: Lightweight Quality Gate checking build integrity.

Generate scaffolds on-demand:
```bash
python3 scripts/repo_health.py --scaffold-ci python
python3 scripts/repo_health.py --scaffold-ci node
```

---

## 4. Audit Report Skeleton (v2.0)

When executing an audit, `github-architect` produces a structured markdown report following this format:

```markdown
# 🏛️ GitHub Architecture Audit Report v2.0

**Account / Target**: `@<user>`  
**Total Repositories Evaluated**: `<count>`  
**Active**: `<active_count>` | **Archived**: `<archived_count>` | **Forks**: `<fork_count>`  

---

## 📊 Health Score Summary & Recommendation Engine

| Repository | Score | Grade | Disposition | Recency | CI Present | Recommended Action / Remediation |
| :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| `repo-a` | 100 | **A** | Flagship | 2 days ago | ✅ | Repositorio en estado óptimo. |
| `repo-b` | 77 | **B** | Fork Hygiene | 11 days ago | ✅ | Sync upstream con original. |
| `repo-c` | 49 | **D** | Archive | 400 days ago| ❌ | **Evaluar archivado por inactividad > 1 año** |

---

## 🎯 Prioritized Action Plan & Scaffolds

### 🚀 Quick Wins (Low Effort / High Impact)
- [ ] Deploy GitHub Actions CI workflow to `repo-x` (Scaffold ready)
- [ ] Add description and topic tags to `repo-y`

### 📦 Proposed Archivals (Recommended Inactive Cleanups)
- [ ] Archive `repo-c` (Inactive > 400 days, score 49/D)

---

## 🛡️ Guardrails & HITL Confirmation

> [!IMPORTANT]
> No destructive or state-changing actions (archiving, deleting, closing issues/PRs) will be executed without your explicit written approval.
```

---

## 5. C5-REAL Public vs. Private Visibility Matrix

| Category | Recommended Visibility | Rationale |
| :--- | :---: | :--- |
| **Flagships & Profile** | **PUBLIC** | Builds technical authority & profile presentation |
| **Open Standards & Specifications** | **PUBLIC** | Maximizes adoption, interoperability, and community value |
| **Mathematical/Logical Kernels & IDEs** | **PUBLIC** | Demonstrates scientific rigor and developer tools |
| **Trading, Arbitrage & Financial Models** | **PRIVATE** | Protects competitive alpha and prevents front-running |
| **Local System Mutators (macOS/RAM)** | **PRIVATE** | Prevents exposure of local machine attack surface |
| **Unreleased Alphas & Active Bot Tokens** | **PRIVATE** | Prevents early leaks and credential exposure |

