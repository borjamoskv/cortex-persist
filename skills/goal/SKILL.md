---
name: goal
display_name: Protocolo de Ejecución por Contrato /goal (Zero-Waste Gate)
description: Destila cualquier tarea en un contrato cerrado de mínimo consumo de tokens
  y asigna el modelo/nivel exacto antes de tocar código.
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

# goal

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/goal/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
