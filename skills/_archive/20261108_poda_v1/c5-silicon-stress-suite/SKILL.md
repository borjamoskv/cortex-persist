---
name: c5-silicon-stress-suite
display_name: Suite de Estrés Concurrente de Silicio y Enjambres (C5-REAL)
description: Pruebas de estrés en paralelo y benchmarks de silicio (multicast O(1),
  Seqlock KUDURRU-64, BFT y Touch ID COSE_Sign1).
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# c5-silicon-stress-suite

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-silicon-stress-suite/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
