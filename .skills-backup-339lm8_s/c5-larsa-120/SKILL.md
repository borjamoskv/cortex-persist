---
name: c5-larsa-120
display_name: Consenso BFT Isostático LARSA-120 (Tríada Rust/Lean4/Z3)
description: Módulo Ring-0. Dispara con "larsa", "larsa-120", "consenso bft", "tríada
  arquitectónica", "consenso isostático".
role: auditor
allowed_roles:
- auditor
- arquitecto
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# c5-larsa-120

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-larsa-120/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
