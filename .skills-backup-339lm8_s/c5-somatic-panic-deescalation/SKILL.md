---
name: c5-somatic-panic-deescalation
display_name: Desescalada Neurofisiológica y Cibernética de Pánico Somático
description: Módulo Wetware/Venture. Dispara con "ataque de ansiedad", "ataque de
  pánico", "hiperfijación somática", "no puedo dormir por la respiración", "bucle
  de pánico", "siento que me muero", "desescalar pánico".
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

# c5-somatic-panic-deescalation

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/c5-somatic-panic-deescalation/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
