---
name: c5-venture-pitch-architect
display_name: Arquitecto de Pitch Decks, Deal Memos & Investor Relations C5
description: Módulo Wetware/Venture. Dispara con "pitch deck", "investor pitch planner",
  "pitch deck creator", "investor letter writer", "vc deal memo", "plan de negocio
  pptx", "the ask pitch".
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

# c5-venture-pitch-architect

> **Directiva Declarativa:** Alias compatible del hub Wetware/Venture; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-wetware-and-venture-ops/references/modules/c5-venture-pitch-architect/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/c5-venture-pitch-architect` sigue disponible con el nombre original.
El hub se consulta con `/c5-wetware-and-venture-ops`.
La carga del alias no ejecuta procedimientos, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
