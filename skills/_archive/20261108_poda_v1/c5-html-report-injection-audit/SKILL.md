---
name: c5-html-report-injection-audit
display_name: Auditoría de Inyección HTML en Generadores de Reportes
description: Verifica el escape HTML de datos del ledger en exportadores Jinja2 y
  string.Template.
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

# c5-html-report-injection-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/c5-html-report-injection-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
