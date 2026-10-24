---
name: c5-kudurru-64
display_name: Cerrojo Lock-Free KUDURRU-64 (Ring-0 Gravity Filter)
description: Filtro de gravedad Lock-Free Seqlock 64B en frontera Ring-0 contra DDoS
  cognitivo (KUDURRU-64).
role: auditor
allowed_roles:
- auditor
- arquitecto
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# c5-kudurru-64

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-kudurru-64/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
