---
name: pika-generative-video-pipeline
display_name: Pipeline de Generación y Control Parámetrico en Pika Art (A/V)
description: Módulo audiovisual. Dispara con "pika art", "pika tutorial", "pika camera",
  "pikaffects", "pika prompt", "generación vídeo pika", "pikaffects sota".
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

# pika-generative-video-pipeline

> **Directiva Declarativa:** Alias compatible del hub audiovisual; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-audiovisual-acreativo-sota/references/modules/pika-generative-video-pipeline/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/pika-generative-video-pipeline` sigue disponible con el nombre original.
El hub se consulta con `/c5-audiovisual-acreativo-sota`.
La carga del alias no ejecuta renders, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
