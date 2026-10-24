---
name: c5-systemic-dissection-protocol
display_name: Protocolo de Disección Sistémica y Termodinámica
description: Módulo epistémico. Dispara con "disección sistémica", "auditar sistema
  completo", "c5-systemic-dissection", "disección termodinámica", "protocolo de disección",
  "100 primitivas".
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

# c5-systemic-dissection-protocol

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/c5-systemic-dissection-protocol/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
