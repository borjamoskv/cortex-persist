---
name: c5-sharur-3600
display_name: Matriz de Enjambre Sexagesimal SHARUR-3600 (Legión 100 Agentes)
description: Define e instancia a SHARUR-3600. Matriz de enjambre estocástico de Ring-2
  para exploración masiva paralela y Surrealismo del Bueno.
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

# c5-sharur-3600

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/c5-sharur-3600/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
