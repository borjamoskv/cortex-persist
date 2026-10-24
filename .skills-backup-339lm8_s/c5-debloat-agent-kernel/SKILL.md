---
name: c5-debloat-agent-kernel
display_name: Arquitecto de Micro-Kernels Agénticos Bare-Metal (Anti-LangChain)
description: Módulo CORTEX. Dispara con "debloat llm", "microkernel agentes", "reemplazar
  langchain", "bare-metal agent", "autopsia langchain", "agente zero dependency".
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

# c5-debloat-agent-kernel

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/c5-debloat-agent-kernel/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
