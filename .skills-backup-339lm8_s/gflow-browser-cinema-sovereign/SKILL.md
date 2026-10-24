---
name: gflow-browser-cinema-sovereign
display_name: Estudio Cinematográfico Soberano y Automatización Google Flow (v5.0
  Apex)
description: Módulo audiovisual. Dispara con "gflow browser", "cine gflow", "flow
  google mcp", "sovereign cinema", "estudio gflow", "gflow v4", "character anchor
  veo", "veo 2 browser", "dialogue engine gflow", "cockpit gflow", "remotion gflow".
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

# gflow-browser-cinema-sovereign

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/gflow-browser-cinema-sovereign/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
