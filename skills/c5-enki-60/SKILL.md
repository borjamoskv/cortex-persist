---
name: c5-enki-60
display_name: Motor Aritmético de Precisión Sexagesimal ENKI-60
description: Motor aritmético de precisión sexagesimal y cálculo pesado en silicio
  (ENKI-60).
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

# c5-enki-60

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-enki-60/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
