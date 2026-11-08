---
name: dynamic-subagent-lifecycle
display_name: Supervisión del Ciclo de Vida de Subagentes Dinámicos
description: Gestión del ciclo de vida, mitigación de deadlocks y supervisión de subagentes
  dinámicos.
role: ejecutor
allowed_roles:
- ejecutor
- arquitecto
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# dynamic-subagent-lifecycle

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/dynamic-subagent-lifecycle/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
