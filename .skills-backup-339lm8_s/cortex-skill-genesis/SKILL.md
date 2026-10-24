---
name: cortex-skill-genesis
display_name: Génesis Autónoma de Skills CORTEX
description: Módulo CORTEX. Dispara con "generar skill", "skill genesis", "crear habilidad",
  "cortex skill genesis", "sintetizar skill", "auto skill creator".
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

# cortex-skill-genesis

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/cortex-skill-genesis/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
