---
name: c5-tamkarum-60
display_name: Transductor de Arbitraje Soberano TAMKARUM-60 (Ring-1)
description: Módulo Wetware/Venture. Dispara con "tamkarum", "tamkarum-60", "/tamkarum",
  "arbitraje publicitario", "auditar roas", "optimizar campañas", "equipo marketing",
  "enjambre marketing", "11 agentes", "scitt".
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

# c5-tamkarum-60

> **Directiva Declarativa:** Alias compatible del hub Wetware/Venture; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-wetware-and-venture-ops/references/modules/c5-tamkarum-60/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/c5-tamkarum-60` sigue disponible con el nombre original.
El hub se consulta con `/c5-wetware-and-venture-ops`.
La carga del alias no ejecuta procedimientos, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
