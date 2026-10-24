---
name: c5-tri-provider-swarm
display_name: Orquestador de Enjambre Híbrido Tri-Provider (OpenAI ⊗ Qwen ⊗ Kimi)
description: Módulo CORTEX. Dispara con "enjambre híbrido", "tri provider swarm",
  "kimi qwen openai", "orquestador tres modelos", "tri-provider swarm".
role: ejecutor
allowed_roles:
- ejecutor
- arquitecto
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# c5-tri-provider-swarm

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/c5-tri-provider-swarm/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
