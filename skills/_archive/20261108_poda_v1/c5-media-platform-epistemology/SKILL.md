---
name: c5-media-platform-epistemology
display_name: Epistemología de Plataformas Media y Adquisición Nativa Opus
description: Heurísticas para audio largo, evasión de falsos positivos SPA y adquisición
  directa Opus (itag 251) sin MP3.
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

# c5-media-platform-epistemology

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/c5-media-platform-epistemology/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
