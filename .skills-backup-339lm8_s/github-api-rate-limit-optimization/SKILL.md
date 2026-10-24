---
name: github-api-rate-limit-optimization
display_name: Optimización Resiliente de Tasa API GitHub (Error 429)
description: Módulo SecOps. Dispara con "github rate limit", "error 429 github", "optimizar
  github api", "secondary rate limit", "evitar 429 github", "resiliencia api github".
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

# github-api-rate-limit-optimization

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/github-api-rate-limit-optimization/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
