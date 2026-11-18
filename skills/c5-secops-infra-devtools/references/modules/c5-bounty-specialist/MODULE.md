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

# Procedimiento Especializado: Bug Bounty Specialist & Eligibility Gate (`C5-REAL`)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Verificación Adversarial, Falsación Algebraica & Gate de Elegibilidad Fail-Closed)
> - **Modo de Acceso a Worktree:** `audit-only` por defecto en repositorios objetivo; escritura de PoCs/parches únicamente en clones dedicados autorizados en `~/10_PROJECTS/` (jamás en `scratch/`).
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `operador` -> Despacha a `ejecutor` (o bloquea envío si $\mathrm{EV} \le 0$)

## 1. Secuencia Operativa Obligatoria (7 Compuertas en Serie)

### Compuerta 1 — Territorio On-Chain vs. Alcance Declarado (`Scope & Bytecode Parity`)
1. Leer el manifiesto exacto del programa (`project/<slug>.json`, tabla de `assets_in_scope`, `SECURITY.md` y exclusiones de impactos).
2. Para cada contrato EVM o programa on-chain candidato:
   - Obtener bytecode vivo, implementación detrás de proxy (EIP-1967 / Beacon / UUPS) y bloque de despliegue (`cast code`, `cast implementation`, `cast storage`).
   - Cruzar byte a byte o contra código verificado qué tag/commit real está desplegado (nunca confiar en la etiqueta nominal del JSON si el bytecode coincide con una versión anterior).
   - Comprobar permisos y estado operativo reales (`hasRole`, `owner`, `paused`, balances/TVL reales). Un contrato dado de baja (`hasRole == false`, `TVL == 0`) carece de impacto crítico activo salvo que las reglas cubran explícitamente código pre-producción.

### Compuerta 2 — Reconstrucción Estática Autenticada con `REA@6.8+`
1. Antes de instrumentar o ejecutar nada, extraer evidencia determinista con `/opt/homebrew/bin/rea`:
   - Bytecode EVM local: `rea inspect-evm-interface <bytecode_file> --format json --full-output`
   - Bundles Web/Electron de frontends DeFi o trading híbrido: `rea analyze-javascript-application`, `rea compare-source-to-bundle`, `rea inspect-web-network-capture` (sobre `.har` exportado limpia y pasivamente).
   - Binarios nativos / validadores / nodos Rust o Mach-O: `rea inspect-rust-binary`, `rea inspect-artifact`, `rea inspect-macho`.
2. Conservar cada `evidence_id` (`ev_...`) y `sha256` en `evidence/`. Declarar `NO_VERIFICADO` todo parámetro escalar de servidor que no figure en el bundle ni en capturas reales.

### Compuerta 3 — Falsación Matemática y Semántica (`Anti-Ghost-Bug`)
1. Derivar la ecuación cerrada en multi-época/multi-bloque antes de afirmar acumulación de deuda, *dust griefing* o desbordamiento:
   - Verificar idempotencia algebraica (ej. $\max(u - K, 0) + K = \max(u, K)$) y cotas IEEE-754 `float64` / `uint256`.
   - Trazar llamadas externas aguas abajo completas (ej. comprobar si un callee revierte con `amount == 0` en lugar de iterar hasta OOG).
2. Descartar de inmediato todo hallazgo procedente de scripts heurísticos que no evalúen invariantes semánticas reales.

### Compuerta 4 — Reproducción en Silicio Sin Mocks (`No-Mock PoC`)
1. **Prohibición de Mocks:** En plataformas con *No-Mock Policy* (Immunefi y equivalentes), el PoC debe instanciar los contratos reales del protocolo (o fork de mainnet en bloque fijo `--fork-block-number <N>`).
2. Medir explícitamente invariantes antes y después de la traza adversarial: solvencia del vault/escrow, fondos de terceros congelados e imposibilidad de recuperación no privilegiada a través de cambios de época/día UTC.

### Compuerta 5 — Triaje `Primacy of Rules` y Filtro `Pay-to-Submit`
Evaluar mediante `scripts/bounty_gate.py` la matriz de disposición:
- **`SUBMIT_BOUNTY`:** Activo en `assets_in_scope` + impacto listado en `impacts_in_scope` + fondos de terceros o insolvencia real + `0` mocks + no excluido por *self-inflicted* / recuperación admin + $\mathrm{EV} > 0$.
- **`REDIRECT_PRIVATE_GHSA`:** Vulnerabilidad real verificada con PoC y parche limpio en código upstream, pero fuera del alcance remunerado o excluida por *Primacy of Rules* / *Pay-to-Submit* -> preparar paquete privado conforme a `SECURITY.md` (`/security/advisories/new`).
- **`REDIRECT_DOC_DRIFT_PR`:** Divergencia entre comentarios/ADRs/SDK docs y la lógica real on-chain segura -> abrir PR público mínimo con `Signed-off-by` (DCO) si el proyecto lo acepta, sin mezclar jamas ramas bajo embargo.
- **`DROP_FALSIFIED`:** Hipótesis refutada algebraicamente o en silicio -> registrar la falsación para no repetir la ruta.

### Compuerta 6 — Verificación de Solidez del Parche (`Patch Soundness`)
Si se entrega remediación junto al reporte o GHSA:
1. Demostrar que el parche preserva todas las propiedades de seguridad ortogonales (ej. no introducir minteo/liberación ante pruebas o timeouts falsificados al corregir un bloqueo de reembolso).
2. Pasar `100%` de la suite existente + tests nuevos de regresión + linters (`forge fmt --check`, `solhint -w 0`, `cargo test`, `rustfmt --check`) con `git diff --stat` limpio sobre archivos ajenos.

### Compuerta 7 — Higiene de Embargo y Remotos (`Zero Public Leak`)
1. Jamás empujar ramas de vulnerabilidades (`cv/*`, `poc/*`, `sec/*`) a un fork público.
2. Verificar en silicio antes y después de `git push`:
   - `gh repo view <owner>/<repo> --json isPrivate,visibility` -> exigir `"isPrivate": true`.
   - `git ls-remote --heads <public_fork>` -> certificar ausencia total de ramas bajo embargo.
