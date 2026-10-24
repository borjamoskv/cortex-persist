---
name: c5-spatial-audio-architect
display_name: Arquitecto de Audio Espacial, Ambisonics (HOA) y Auditoría DSP
description: Módulo audiovisual. Dispara con "auditoría dsp", "audio espacial", "criticar
  estéreo", "hoa", "binaural", "ambisonics", "spatial audio".
role: arquitecto
allowed_roles:
- arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# c5-spatial-audio-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/c5-spatial-audio-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
