---
name: handoff
display_name: Protocolo Soberano de Traspaso de Contexto C5-REAL
description: Genera un documento completo de traspaso de contexto (HANDOFF.md) para
  transferir lecciones aprendidas, estado del sistema y próximos pasos a una nueva
  sesión.
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
