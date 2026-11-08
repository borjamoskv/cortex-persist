---
name: epistemic-extinction-protocol
display_name: Protocolo de Extinción Epistémica (Punto Fijo Ω)
description: Protocolo de reducción dimensional y extinción epistémica (Punto Fijo
  Ω).
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

# epistemic-extinction-protocol

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/epistemic-extinction-protocol/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
