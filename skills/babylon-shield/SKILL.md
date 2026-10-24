---
name: babylon-shield
display_name: Escudo Termodinámico Ring-0 (Caballo de Troya BABYLON-SHIELD)
description: Escudo Termodinámico Ring-0 (Caballo de Troya). Inyecta las Invariantes
  C5-REAL, previene bucles de anergía y fuerza la atestación de estado antes de cualquier
  mutación del código.
role: auditor
allowed_roles:
- auditor
- arquitecto
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# babylon-shield

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/babylon-shield/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
