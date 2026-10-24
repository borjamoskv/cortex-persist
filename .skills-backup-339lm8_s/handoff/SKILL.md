---
name: handoff
display_name: Protocolo Soberano de Traspaso de Contexto C5-REAL
description: Módulo CORTEX. Dispara con "handoff", "/handoff", "traspaso de contexto",
  "traspaso de sesión", "generar handoff", "traspaso formal", "context handover".
role: auditor
allowed_roles:
- auditor
- arquitecto
- ejecutor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# handoff

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/handoff/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
