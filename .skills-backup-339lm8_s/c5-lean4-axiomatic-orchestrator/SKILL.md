---
name: c5-lean4-axiomatic-orchestrator
display_name: Orquestador Axiomático y Verificación Formal en Lean 4
description: Módulo Ring-0. Dispara con "lean 4", "formalizar en lean", "oráculo axiomático",
  "lake build", "verificación formal", "axiomas lean", "probar teorema", "neuro-simbólico".
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

# c5-lean4-axiomatic-orchestrator

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-lean4-axiomatic-orchestrator/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
