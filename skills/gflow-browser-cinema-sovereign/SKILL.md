---
name: gflow-browser-cinema-sovereign
display_name: Estudio Cinematográfico Soberano y Automatización Google Flow (v5.0
  Apex)
description: Módulo audiovisual. Dispara con "gflow browser", "cine gflow", "flow
  google mcp", "sovereign cinema", "estudio gflow", "gflow v4", "character anchor
  veo", "veo 2 browser", "dialogue engine gflow", "cockpit gflow", "remotion gflow".
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

# gflow-browser-cinema-sovereign

> **Directiva Declarativa:** Alias compatible del hub audiovisual; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-audiovisual-acreativo-sota/references/modules/gflow-browser-cinema-sovereign/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/gflow-browser-cinema-sovereign` sigue disponible con el nombre original.
El hub se consulta con `/c5-audiovisual-acreativo-sota`.
La carga del alias no ejecuta renders, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
