---
name: soulseek-p2p-audio-acquisition
display_name: Adquisición P2P de Audio en Soulseek y Auditoría Espectral Anti-Fake
  FLAC
description: Módulo audiovisual. Dispara con "descargar musica", "descargar cancion",
  "soulseek download", "adquisicion audio p2p", "auditoria espectral flac", "bajar
  flac soulseek", "fake flac".
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

# soulseek-p2p-audio-acquisition

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/soulseek-p2p-audio-acquisition/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
