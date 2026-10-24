---
name: c5-venture-pitch-architect
display_name: Arquitecto de Pitch Decks, Deal Memos & Investor Relations C5
description: Módulo Wetware/Venture. Dispara con "pitch deck", "investor pitch planner",
  "pitch deck creator", "investor letter writer", "vc deal memo", "plan de negocio
  pptx", "the ask pitch".
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

# c5-venture-pitch-architect

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/c5-venture-pitch-architect/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
