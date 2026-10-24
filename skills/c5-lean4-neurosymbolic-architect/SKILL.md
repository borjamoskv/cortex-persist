---
name: c5-lean4-neurosymbolic-architect
display_name: Arquitecto Neuro-Simbólico Soberano en Lean 4
description: Arquitectura de agentes neuro-simbólicos y binarios soberanos en Lean
  4 (C-FFI, ITrees, lógica lineal).
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

# c5-lean4-neurosymbolic-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-lean4-neurosymbolic-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
