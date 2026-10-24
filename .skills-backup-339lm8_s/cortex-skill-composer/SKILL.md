---
name: cortex-skill-composer
display_name: Componedor & Orquestador de Cadenas de Skills
description: Módulo CORTEX. Dispara con "componer skills", "skill chain", "cadena
  de habilidades", "pipeline de skills", "cortex skill composer", "orquestación de
  habilidades", "skill pipeline".
role: arquitecto
allowed_roles:
- arquitecto
- ejecutor
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# cortex-skill-composer

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/cortex-skill-composer/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
