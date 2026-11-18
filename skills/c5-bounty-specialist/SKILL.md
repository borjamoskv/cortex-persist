---
name: c5-bounty-specialist
display_name: 'Especialista C5-REAL en Bug Bounties & Triaje Immunefi/REA'
description: 'Auditoría adversarial de bug bounties Web3/híbridos, triaje Primacy of Rules (Immunefi/GHSA), atestación REA 6.8 y PoCs Foundry/Rust sin mocks. Dispara con "especialista en bounties", "bug bounty", "immunefi", "triaje de bounty", "elegibilidad immunefi", "ghsa privado".'
role: auditor
allowed_roles:
- auditor
- ejecutor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: operador
    downstream: ejecutor
---

# c5-bounty-specialist

> **Directiva Declarativa:** Habilidad soberana de auditoría adversarial y triaje de elegibilidad de bug bounties; conserva rol `auditor`, modo `audit-only` por defecto y cero efectos externos automáticos.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/c5-bounty-specialist/MODULE.md) cuando la tarea requiera auditar contratos/protocolos bajo programas de recompensas (Immunefi, Cantina, Sherlock, Code4rena o `SECURITY.md`), verificar paridad de bytecode on-chain frente a JSON de alcance, reconstruir artefactos con `rea@6.8+` o decidir entre envío remunerado, GHSA privado o PR de *doc-drift*.

## Compuerta Determinista de Elegibilidad y Valor Esperado (`bounty_gate.py`, schema v4)

Antes de preparar cualquier envío externo, valida el recibo con [bounty_gate.py](scripts/bounty_gate.py). Es fail-closed: lo que no está probado o está malformado se bloquea y nunca se redirige.

**Recibo (`schema_version: 4`):**
- `target`: `{"kind":"evm","chain_id","address","block"}` (fork fijado, nunca `latest`), `{"kind":"commit","repo","sha"}` (SHA completo 40/64 hex), o `{"kind":"web_bundle","origin","bundle_sha256"}` (`http(s)://host[:port]` sin ruta/query/userinfo + SHA-256 de 64 hex minúsculas).
- 11 flags obligatorios: `asset_in_scope`, `impact_in_scope`, `onchain_or_commit_verified`, `silicon_poc_passes`, `uses_mocks`, `algebraic_invariant_verified`, `self_inflicted_only`, `admin_recovery_excluded_by_rules`, `public_remote_clean`, `not_known_issue_or_prior_audit`, `inference_retention_verified`. Opcionales: `is_doc_drift_only` y `patch_regression_free`.
- `estimated_payout_usd`, `payout_probability`, `validity_probability` y `pay_to_submit_fee_usd`.
- `rea_evidence_ids` y `evidence_map`: cada afirmación positiva cita al menos un `ev_*` registrado, y un `ev_*` solo respalda afirmaciones de un grupo (scope, target, poc, invariant, known_issues, retention).
- Las claves desconocidas o duplicadas se bloquean.

**Orden de evaluación:** embargo → falsación → evidencia no probada (mocks, versión) → doc-drift → issue conocido → exclusiones por reglas → EV.

**EV con reembolso en créditos:** `EV = p_pay·payout − (1 − p_valid)·fee`, con `p_pay ≤ p_valid`.

**Evidencia verificada:** `rea` no mantiene un registro persistente de `ev_*`: devuelve Evidence JSON por comando. Guarda cada salida como archivo y genera un manifiesto `{ev_id: {path, sha256}}`. El gate recalcula el SHA-256 y bloquea si un archivo falta, está vacío, no coincide, es el mismo archivo o el mismo contenido que otro id, o es el propio recibo o manifiesto. La evidencia de `silicon_poc_passes` debe ser una ejecución de tests aprobada: `forge test --json > poc.json` (≥ 1 `Success`, 0 `Failure`), resumen libtest de `cargo test` (≥ 1 passed y 0 failed) o salida de `python -m unittest` (`Ran ≥ 1 test(s) ... OK` con ≥ 1 pasado efectivo y 0 failed/errors). Sin manifiesto, los veredictos que salen al exterior (`SUBMIT_BOUNTY`, `REDIRECT_*`) se bloquean.

| Veredicto | Exit | Acción |
|---|---|---|
| `SUBMIT_BOUNTY` | 0 | Enviar (adjuntar parche solo si `include_remediation_patch`) |
| `REDIRECT_PRIVATE_GHSA` / `REDIRECT_DOC_DRIFT_PR` | 0 | Advisory privado / PR |
| `DROP_FALSIFIED` / `DROP_KNOWN_ISSUE` | 3 | Cerrar |
| `HOLD_NON_POSITIVE_EV` | 3 | Decisión humana; nunca auto-redirect |
| `BLOCKED_INCOMPLETE_EVIDENCE` / `BLOCKED_EMBARGO_VIOLATION` | 1 | Corregir el recibo, la evidencia o el embargo |

**Atestación:** la salida incluye `receipt_sha256`, `manifest_sha256`, `gate_sha256` (bytes del script) y `decision_sha256`. Es determinista y se puede anclar en un ledger.

```bash
G=~/.gemini/config/skills/c5-bounty-specialist/scripts/bounty_gate.py
python3 $G --selftest
forge test --match-test test_exploit --json > evidence/poc.json
python3 $G --build-manifest evidence/manifest.json ev_forge_poc=evidence/poc.json ev_scope_json=evidence/scope.json ...
python3 $G --evaluate receipt.json --evidence-manifest evidence/manifest.json
```

Subagente hoja dedicado ($d = 1$) para delegación aislada: `~/.gemini/config/agents/bounty-specialist.md`.
