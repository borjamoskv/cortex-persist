---
name: github-architect
display_name: Arquitecto Estratégico de Presencia y Salud en GitHub (GraphQL v2.1)
description: Arquitecto estratégico de GitHub v2.1 vía GraphQL (auditoría 0-100, remediación
  de repositorios y plantillas CI).
role: arquitecto
allowed_roles:
- arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# github-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/github-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
