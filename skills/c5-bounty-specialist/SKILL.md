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

## Compuerta Determinista de Elegibilidad y Valor Esperado (`bounty_gate.py`)

Antes de preparar cualquier envío externo, valida el recibo de las 7 compuertas (`Scope`, `Bytecode Parity`, `REA ev_*`, `No-Mock Silicon PoC`, `Algebraic Pre-Falsification`, `Primacy of Rules / Pay-to-Submit EV`, `Embargo Clean Remote`) mediante [bounty_gate.py](scripts/bounty_gate.py):

```bash
python3 ~/.gemini/config/skills/c5-bounty-specialist/scripts/bounty_gate.py --selftest
```

Subagente hoja dedicado ($d = 1$) para delegación aislada: `~/.gemini/config/agents/bounty-specialist.md`.
