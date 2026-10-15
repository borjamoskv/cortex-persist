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

> **Directiva Declarativa:** Alias compatible del hub audiovisual; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-audiovisual-acreativo-sota/references/modules/remotion-audio-reactive-video/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/remotion-audio-reactive-video` sigue disponible con el nombre original.
El hub se consulta con `/c5-audiovisual-acreativo-sota`.
La carga del alias no ejecuta renders, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
