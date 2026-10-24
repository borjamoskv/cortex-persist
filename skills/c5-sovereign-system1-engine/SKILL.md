---
name: c5-sovereign-system1-engine
display_name: Motor de Decisión Sistema 1 No Autorregresivo (LAYA Edge)
description: Diseño, compilación, despliegue y calibración on-device de motores de
  decisión de Sistema 1 no autorregresivos (LAYA / ModernBERT) en silicio local Apple
  Silicon.
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
