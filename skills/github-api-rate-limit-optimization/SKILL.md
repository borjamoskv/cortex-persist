---
name: github-api-rate-limit-optimization
display_name: Optimización Resiliente de Tasa API GitHub (Error 429)
description: Módulo SecOps. Dispara con "github rate limit", "error 429 github", "optimizar
  github api", "secondary rate limit", "evitar 429 github", "resiliencia api github".
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

# github-api-rate-limit-optimization

> **Directiva Declarativa:** Alias compatible del hub SecOps; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-secops-infra-devtools/references/modules/github-api-rate-limit-optimization/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/github-api-rate-limit-optimization` sigue disponible con el nombre original.
El hub se consulta con `/c5-secops-infra-devtools`.
La carga del alias no ejecuta auditorías, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
