---
name: c5-ctm-formal-architect
display_name: Arquitectura Formal y Diseño Empírico de Cognitive Transition Machines
  (CTM)
description: Arquitectura formal y empírica de Cognitive Transition Machines (CTM)
  e invariantes Lean 4 (AP-01 a AP-09).
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
