---
name: c5-terminological-archaeology
display_name: Arqueología Terminológica (Anagnórisis Conceptual C5-REAL)
description: Módulo epistémico. Dispara con "arqueología terminológica", "busca mis
  perífrasis", "anagnórisis", "ya existe ese término", "tiene nombre esto", "cómo
  se llama esto en ciencia", "cómo se llama cuando".
role: auditor
allowed_roles:
- auditor
- arquitecto
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: operador
    downstream: notario
---

# c5-terminological-archaeology

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/c5-terminological-archaeology/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
