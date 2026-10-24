---
name: f5tts-voice-cloning-sota
display_name: Clonación Vocal Neuronal SOTA (F5-TTS / MPS / Ingeniería de Prosodia)
description: Módulo audiovisual. Dispara con "clonar voz", "sintetizar voz", "f5-tts",
  "f5tts", "voice clone", "prosodia tts", "nota de voz ia".
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

# f5tts-voice-cloning-sota

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/f5tts-voice-cloning-sota/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
