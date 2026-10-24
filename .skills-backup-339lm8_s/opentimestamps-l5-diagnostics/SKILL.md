---
name: opentimestamps-l5-diagnostics
display_name: Atestación Criptográfica & Diagnóstico Bitcoin L5 (OpenTimestamps)
description: Módulo Ring-0. Dispara con "opentimestamps", "ots verify", "atestación
  l5", "bitcoin timestamp", "l5 diagnostics", "ots bitcoin", "sellado temporal l5".
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

# opentimestamps-l5-diagnostics

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/opentimestamps-l5-diagnostics/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
