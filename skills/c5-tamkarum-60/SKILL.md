---
name: c5-tamkarum-60
display_name: Transductor de Arbitraje Soberano TAMKARUM-60 (Ring-1)
description: Motor soberano de arbitraje RTB, orquestación de matriz de 11 agentes
  de distribución, diseño y atestación SCITT bajo KudurruBudgetGate en BABYLON-60.
role: ejecutor
allowed_roles:
- ejecutor
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# c5-tamkarum-60

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/c5-tamkarum-60/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
