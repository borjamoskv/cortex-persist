---
name: safari-browser-agent
display_name: Agente Autónomo de Navegación Safari (MCP Dual-Engine v6.0 Sexagesimal
  Apex Sovereign)
description: Módulo SecOps. Dispara con "safari agent", "navegar safari", "mcp safari",
  "controlar safari", "safari browser agent", "safari automation", "inspeccionar safari",
  "mac maestro", "automatizar safari jxa", "bypass webdriver", "mac maestro bridge",
  "control jxa macos", "windowserver automation".
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

# safari-browser-agent

> **Directiva Declarativa:** Alias compatible del hub SecOps; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-secops-infra-devtools/references/modules/safari-browser-agent/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/safari-browser-agent` sigue disponible con el nombre original.
El hub se consulta con `/c5-secops-infra-devtools`.
La carga del alias no ejecuta auditorías, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
