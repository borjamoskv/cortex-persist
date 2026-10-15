---
name: macos-lulu-firewall-diagnostics
display_name: Diagnóstico de Firewall & Sockets macOS (LuLu / Little Snitch)
description: Módulo SecOps. Dispara con "lulu firewall", "little snitch", "redes macos",
  "diagnóstico firewall", "reglas de red macos", "bloqueo sockets mac".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# macos-lulu-firewall-diagnostics

> **Directiva Declarativa:** Alias compatible del hub SecOps; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-secops-infra-devtools/references/modules/macos-lulu-firewall-diagnostics/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/macos-lulu-firewall-diagnostics` sigue disponible con el nombre original.
El hub se consulta con `/c5-secops-infra-devtools`.
La carga del alias no ejecuta auditorías, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
