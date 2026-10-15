---
name: c5-codebase-valuation-audit
display_name: Auditoría & Valoración Económica Empírica de Codebases e IP
description: Módulo Wetware/Venture. Dispara con "valorar software", "valoración económica",
  "audit codebase valuation", "software ip valuation", "acqui-hire valuation", "due
  diligence técnica".
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

# c5-codebase-valuation-audit

> **Directiva Declarativa:** Alias compatible del hub Wetware/Venture; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-wetware-and-venture-ops/references/modules/c5-codebase-valuation-audit/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/c5-codebase-valuation-audit` sigue disponible con el nombre original.
El hub se consulta con `/c5-wetware-and-venture-ops`.
La carga del alias no ejecuta procedimientos, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
