---
name: c5-session-deskimming
display_name: Protocolo de Desnatado de Sesiones & Purga de Nata (Ring-2 -> Ring-0)
description: Módulo CORTEX. Dispara con "deskimming", "desnatar sesión", "purgar nata
  sesión", "archivos huérfanos".
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

# c5-session-deskimming

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/c5-session-deskimming/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
