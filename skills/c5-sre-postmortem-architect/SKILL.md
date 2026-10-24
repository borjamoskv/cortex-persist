---
name: c5-sre-postmortem-architect
display_name: Arquitecto de Postmortems e Incidentes SRE
description: Redacción de informes postmortem sin culpa (blameless) siguiendo mejores
  prácticas SRE, análisis 5 Whys, líneas temporales y cálculo MTTR.
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

# c5-sre-postmortem-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/c5-sre-postmortem-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
