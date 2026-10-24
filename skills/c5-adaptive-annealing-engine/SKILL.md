---
name: c5-adaptive-annealing-engine
display_name: Motor de Recocido Adaptativo y Convergencia Exergética (Q1-Q4)
description: Motor de Recocido Adaptativo en cuatro cuartiles (Q1-Q4) para forzar
  convergencia al Apex en espacios discretos y optimización sin colisión topológica
  ni colapso de gradiente voraz.
role: arquitecto
allowed_roles:
- arquitecto
- ejecutor
- auditor
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# c5-adaptive-annealing-engine

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/c5-adaptive-annealing-engine/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
