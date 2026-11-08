---
name: jujutsu-vcs-management
display_name: Control de Versiones Determinista Jujutsu VCS (jj)
description: Control de versiones determinista con Jujutsu VCS (jj) e integración
  con Git DAG.
role: ejecutor
allowed_roles:
- ejecutor
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# jujutsu-vcs-management

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/jujutsu-vcs-management/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
