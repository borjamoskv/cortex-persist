---
name: cortex-skill-auditor
display_name: Auditor Exergético de Skills CORTEX Engine
description: Audita estructura, rutas, enlaces y coherencia de instrucciones cuando
  se pide revisar una biblioteca de skills; conserva comprobaciones independientes
  y explicita su cobertura.
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

# cortex-skill-auditor

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/cortex-skill-auditor/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
