---
name: webkit-memory-audit
display_name: Auditoría de Memoria WebKit (Vector 21)
description: Módulo SecOps. Dispara con "webkit audit", "vector 21", "gigacage", "auditoría
  memoria c++", "webkit memory", "bmalloc audit".
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

# webkit-memory-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/webkit-memory-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
