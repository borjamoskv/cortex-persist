---
name: c5-thermos-audit
display_name: Auditoría Termonuclear de Silicio & Código (Double Thermo)
description: Módulo Ring-0. Dispara con "thermos", "thermos audit", "auditoría termonuclear",
  "double thermo", "revisión termonuclear", "revisar rama a fondo", "thermo review".
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

# c5-thermos-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-thermos-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
