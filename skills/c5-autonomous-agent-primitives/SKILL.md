---
name: c5-autonomous-agent-primitives
display_name: Catálogo Canónico y Transductor de 47 Primitivas de Agente Autónomo
description: Catálogo y matriz de las 47 primitivas de agente autónomo colapsadas
  en los 4 macro-transductores C5-REAL.
role: arquitecto
allowed_roles:
- arquitecto
- ejecutor
- auditor
directives:
  worktree_mode: read-write
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# c5-autonomous-agent-primitives

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/c5-autonomous-agent-primitives/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
