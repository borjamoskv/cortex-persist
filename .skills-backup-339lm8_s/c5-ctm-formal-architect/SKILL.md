---
name: c5-ctm-formal-architect
display_name: Arquitectura Formal y Diseño Empírico de Cognitive Transition Machines
  (CTM)
description: Módulo Ring-0. Dispara con "ctm benchmark", "ctm formalization", "lean
  4 ctm", "abduction vs deduction", "falsification matrix", "refinement trace".
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

# c5-ctm-formal-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-ctm-formal-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
