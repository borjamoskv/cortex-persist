---
name: c5-sovereign-system1-engine
display_name: Motor de Decisión Sistema 1 No Autorregresivo (LAYA Edge)
description: Módulo Ring-0. Dispara con 'laya', 'sistema 1 edge', 'jev local', 'triage
  desacoplado', 'kudurru 64 socket', 'decision engine local'.
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

# c5-sovereign-system1-engine

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-sovereign-system1-engine/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
