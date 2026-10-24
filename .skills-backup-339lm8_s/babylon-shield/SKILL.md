---
name: babylon-shield
display_name: Escudo Termodinámico Ring-0 (Caballo de Troya BABYLON-SHIELD)
description: Módulo Ring-0. Dispara con "babylon shield", "escudo termodinámico",
  "ring-0 shield", "prevenir anergía", "atestación babylon", "invariantes ring-0",
  "protección ring-0".
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
