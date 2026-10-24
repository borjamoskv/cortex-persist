---
name: c5-real-legaltech-analysis
display_name: Auditoría LegalTech & Cumplimiento EU AI Act Art. 9-14
description: Auditoría LegalTech, análisis de cumplimiento EU AI Act (Artículos 9-14)
  y análisis de contratos inteligentes bajo estándar C5-REAL.
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

# c5-real-legaltech-analysis

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/c5-real-legaltech-analysis/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
