---
name: c5-academic-peer-reviewer
display_name: Simulador de Revisión Académica por Pares
description: Módulo epistémico. Dispara con "peer review", "academic reviewer", "revisar
  paper", "auditoría de paper", "dictamen académico".
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

# c5-academic-peer-reviewer

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/c5-academic-peer-reviewer/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
