---
name: c5-sovereign-binary-architect
display_name: Arquitecto de Binarios Soberanos C5-REAL
description: Módulo Ring-0. Dispara con "binario estático", "aislar dependencias",
  "soberanía termodinámica", "c5-sovereign-binary", "compilación musl", "binario soberano".
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

# c5-sovereign-binary-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-sovereign-binary-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
