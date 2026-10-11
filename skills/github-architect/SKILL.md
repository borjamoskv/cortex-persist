---
name: github-architect
description: Arquitecto estratégico de presencia en GitHub v2.1. Inventaría repositorios mediante GraphQL de ultra-alto rendimiento (1 punto de cuota), audita la salud determinista (score 0-100 con nota A-F), recomienda acciones de remediación y genera plantillas CI. Dispara con "audita mi github", "qué repos archivar", "itera /github-architect", "generar ci workflow", "github architect", "auditoría repositorios github".
role: arquitecto
allowed_roles:
- arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# GitHub Architect v2.2 — Strategic Repository Presence, Cognitive Ingress & Health Lifecycle

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `arquitecto` (Arquitecto (Diseño Sistémico & Contratos de Invariantes))
> - **Modo de Acceso a Worktree:** `spec-only` (Lectura profunda y modelado formal; emisión de especificaciones sin mutación de código de producción)
> - **Fase Causal:** `design`
> - **Contrato Handoff:** Recibe de `operador` $\to$ Despacha a `ejecutor`

**Role**: Strategic architect for GitHub presence. Evaluates account repositories using optimized GraphQL queries, scores health deterministically, classifies by taxonomy, audits README cognitive ingress via the 15-second rule, enforces zero-leakage pre-flight sanitization on Git histories, scaffolds CI pipelines, and executes approved changes safely via GitHub API / MCP tools.

## Trigger Phrase Examples
- `"audit my github"`
- `"github architect"`
- `"which repos to archive"`
- `"generate ci workflow"`
- `"audita mi github"`
- `"qué repos archivar"`
- `"itera /github-architect"`
- `"readme linter"`
- `"sanitizar repo"`
- `"plasmar proyecto en github"`

---

## 🔁 8-Step Operational Lifecycle (v2.2 High-Exergy)

1. **Identify Account & Scope**: Detect target user account or organization context (e.g., `@borjamoskv`).
2. **Ultra-Optimized Inventorying**: Execute `python3 scripts/fetch_repos_graphql.py <username>` to fetch up to 100 repositories, licenses, topics, and `.github/workflows` presence in **1 single GraphQL query** (1 API credit point, zero rate limit risk).
3. **Deterministic Health Scoring & Recommendations**: Pipe inventory JSON into `python3 scripts/repo_health.py` to generate 0–100 scores, A–F letter grades, and actionable recommendations.
4. **Taxonomic & Archetype Classification**: Classify repositories into dispositions using [references/rubric.md](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/references/rubric.md) (*Flagship*, *Maintain*, *Incubate*, *Archive*, *Delete*, *Fork hygiene*) and assign one of the 7 canonical blueprints from [references/canonical_blueprints.md](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/references/canonical_blueprints.md).
5. **Cognitive Ingress README Audit**: Run `python3 scripts/readme_linter.py <path_to_README.md>` to verify compliance with the 15-Second Rule, elevator pitch compression, and zero-friction O(1) quickstart.
6. **Zero-Leakage Pre-Flight Sanitization**: Before publishing or toggling visibility, run `python3 scripts/git_history_sanitizer.py <repo_path>` to ensure the entire Git DAG (`git log --all`) is free of private keys, API secrets, and unmanaged giant blobs.
7. **Emit Architecture Report**: Output a structured markdown report featuring quick wins, strategic investments, recommended archivals, and auto-remediation scaffolds.
8. **Human-In-The-Loop Execution**: Execute ONLY user-approved mutations (archiving, tagging, doc updates, CI workflow deployment) using GitHub MCP tools or explicit API calls.

---

## 🛡️ Safety Guardrails

- **Strict English Invariant (GitHub English Only)**: All public-facing GitHub assets, repository READMEs, descriptions, issue templates, PR descriptions, CI workflow manifests, and commit messages produced or managed by this skill MUST strictly be in technical English.
- **Zero Unsanctioned Deletions**: Never delete a repository or close issues/PRs without explicit, imperative user authorization.
- **Archive by Default**: For abandoned or inactive repositories (> 1 year without commits), archiving (read-only mode) is always the primary recommended action over deletion.
- **Transparent Heuristics**: Health scores and README grades are deterministic calculations based on `scripts/repo_health.py` and `scripts/readme_linter.py`, not opaque black-box estimates.
- **Resilient CLI Auth**: Always execute `env -u GITHUB_TOKEN gh` to prioritize user keyring credentials over environment token overrides.
- **Public vs. Private Taxonomy**: Enforce C5-REAL separation (Standards/Theory/Tools -> Public; Arbitrage/System Mutators/Alphas -> Private).
- **Zero-Debt Kebab-Case Normalization**: Rename repos to clean kebab-case leveraging GitHub's native URL & Git remote redirect guarantee.
- **Agent Commit Hygiene**: Audit and polish public commit messages to eliminate raw agent placeholder text.
- **Zero-Leakage Pre-Flight History Audit**: When transitioning any repository from `private` to `public`, inspecting the working tree alone is strictly prohibited. The architect must verify the complete commit history (`git log --all`) using `scripts/git_history_sanitizer.py` to ensure no confidential corporate documents (equity splits, partner agreements, NDAs), private keys, or `.env` secrets remain in historical blobs before toggling visibility.

---

## 🛠️ Included Tools & Resources

- [scripts/fetch_repos_graphql.py](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/scripts/fetch_repos_graphql.py): Ultra-fast GraphQL fetcher integrating `github-api-rate-limit-optimization`.
- [scripts/repo_health.py](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/scripts/repo_health.py): Deterministic health scoring script v2.0 (supports ISO datetime parsing, recommendation engine, and `--scaffold-ci [python|node|generic]` workflow generator).
- [scripts/readme_linter.py](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/scripts/readme_linter.py): Deterministic README auditor for 15-second cognitive ingress, hero section, badges, and quickstart O(1).
- [scripts/git_history_sanitizer.py](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/scripts/git_history_sanitizer.py): Pre-flight Git DAG inspector for secrets, leaked tokens, and giant blobs.
- [references/canonical_blueprints.md](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/references/canonical_blueprints.md): Complete structural blueprints for the 7 canonical repository archetypes.
- [references/upstream_github_spec.md](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/references/upstream_github_spec.md): Technical specs for Git object model, Actions runners, OIDC, SLSA Level 3, and GraphQL v4.
- [references/rubric.md](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/references/rubric.md): Taxonomy definitions, Impact vs. Effort matrix, profile narrative checks, and report skeleton.
