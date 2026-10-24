---
name: c5-codebase-valuation-audit
display_name: Auditoría & Valoración Económica Empírica de Codebases e IP
description: Módulo Wetware/Venture. Dispara con "valorar software", "valoración económica",
  "audit codebase valuation", "software ip valuation", "acqui-hire valuation", "due
  diligence técnica".
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

# c5-codebase-valuation-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/c5-codebase-valuation-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
