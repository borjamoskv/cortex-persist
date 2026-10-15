---
name: c5-poster-and-sign-craft
display_name: Pipeline de Remasterización Gráfica, Rotulación en Perspectiva y Filtrado
  Analógico
description: Módulo audiovisual. Dispara con "remasterizar cartel", "rotular letrero",
  "cambiar texto cartel", "sign craft", "filtro vintage comic", "bajar contraste imagen",
  "quitar contraste duro", "poster remaster", "maquetación cartel", "analizar cartel",
  "flyer underground", "auditoría tipográfica cartel".
role: ejecutor
allowed_roles:
- ejecutor
- arquitecto
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# c5-poster-and-sign-craft

> **Directiva Declarativa:** Alias compatible del hub audiovisual; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-audiovisual-acreativo-sota/references/modules/c5-poster-and-sign-craft/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/c5-poster-and-sign-craft` sigue disponible con el nombre original.
El hub se consulta con `/c5-audiovisual-acreativo-sota`.
La carga del alias no ejecuta renders, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
