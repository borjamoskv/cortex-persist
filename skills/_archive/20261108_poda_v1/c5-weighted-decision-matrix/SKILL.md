---
name: c5-weighted-decision-matrix
display_name: Matriz de Decisión Ponderada y Estimación PERT
description: Matrices de decisión multicriterio ponderadas para selección tecnológica,
  análisis de sensibilidad y estimación formal PERT.
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

# c5-weighted-decision-matrix

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/c5-weighted-decision-matrix/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
