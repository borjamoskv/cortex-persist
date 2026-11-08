---
name: djstudio-mcp
display_name: Controlador DSP & Playlist Mixer DJ.Studio MCP
description: Protocolo MCP, automatización de mezclas, stems y DSP Linkwitz-Riley
  para DJ.Studio y Rekordbox XML.
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

# djstudio-mcp

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/djstudio-mcp/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
