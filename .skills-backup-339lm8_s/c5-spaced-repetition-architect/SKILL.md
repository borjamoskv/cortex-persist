---
name: c5-spaced-repetition-architect
display_name: Arquitecto de Repetición Espaciada, Anki & Control Entrópico Cognitivo
  C5
description: Módulo Wetware/Venture. Dispara con "anki maker", "tarjetas anki", "anki
  flashcards", "repetición espaciada", "adhd assistant", "descomposición de tareas",
  "micro-tasking", "spaced repetition".
role: ejecutor
allowed_roles:
- ejecutor
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# c5-spaced-repetition-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/c5-spaced-repetition-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
