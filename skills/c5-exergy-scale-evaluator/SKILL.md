---
name: c5-exergy-scale-evaluator
display_name: Evaluador de Escala de Exergía 1-21.000 (Regla de 3 Evaluadores)
description: Auditoría de exergía estructural en escala 1 a 21.000 bajo la Regla de
  3 Evaluadores (Silicio, Kolmogorov, Causal).
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

# c5-exergy-scale-evaluator

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/c5-exergy-scale-evaluator/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
