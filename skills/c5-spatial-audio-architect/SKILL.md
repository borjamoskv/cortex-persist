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

> **Directiva Declarativa:** Alias compatible del hub audiovisual; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-audiovisual-acreativo-sota/references/modules/c5-spatial-audio-architect/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/c5-spatial-audio-architect` sigue disponible con el nombre original.
El hub se consulta con `/c5-audiovisual-acreativo-sota`.
La carga del alias no ejecuta renders, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
