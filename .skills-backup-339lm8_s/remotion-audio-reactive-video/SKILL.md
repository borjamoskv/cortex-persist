---
name: remotion-audio-reactive-video
display_name: Síntesis de Vídeo Reactivo a Audio & Música (Remotion + DSP)
description: Módulo audiovisual. Dispara con "video reactivo a la musica", "audio
  reactivo", "remotion audio reactive", "visualizador de musica", "audio visualizer",
  "video musical reactivo".
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

# remotion-audio-reactive-video

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/remotion-audio-reactive-video/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
