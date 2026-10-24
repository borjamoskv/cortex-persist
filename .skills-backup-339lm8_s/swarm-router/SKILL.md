---
name: swarm-router
display_name: Enrutador Maestro y Despachador Inteligente de Enjambres
description: Módulo CORTEX. Dispara con "enjambre", "enjmabres", "swarm", "swarms",
  "sarm", "sarms", "lanzar enjambre", "ejecutar enjambre", "orquestar enjambre", "swarm
  call", "disparar enjambres", "matriz de enjambres", "mejora los enjambres".
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

# swarm-router

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/swarm-router/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
