---
name: flstudio-mcp-production
display_name: Producción Nativa MCP FL Studio 2025 & DSP Microtonal
description: Módulo audiovisual. Dispara con "FL Studio", "flstudio-mcp", "balag-omega",
  "generador de musica", "compilar flp", "piano roll script", "microtonal house".
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

# flstudio-mcp-production

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/flstudio-mcp-production/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
