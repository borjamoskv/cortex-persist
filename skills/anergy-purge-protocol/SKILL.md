---
name: anergy-purge-protocol
display_name: Motor de Purga de Anergía, Código Muerto y Entropía APFS
description: Purga de código muerto, artefactos efímeros, ghost listeners, saturación
  APFS y prompt bloat.
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# anergy-purge-protocol

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/anergy-purge-protocol/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
