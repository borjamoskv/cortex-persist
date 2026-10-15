---
name: c5-socint-extraction-suite
display_name: Suite Soberana de Inteligencia Social (SOCINT C5-REAL)
description: Módulo SecOps. Dispara con "socint suite", "inteligencia social", "scraping
  redes", "reddit socint", "substack socint", "auditar tweet", "analizar hilo x".
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

# c5-socint-extraction-suite

> **Directiva Declarativa:** Alias compatible del hub SecOps; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-secops-infra-devtools/references/modules/c5-socint-extraction-suite/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/c5-socint-extraction-suite` sigue disponible con el nombre original.
El hub se consulta con `/c5-secops-infra-devtools`.
La carga del alias no ejecuta auditorías, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
