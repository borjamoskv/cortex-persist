---
name: kimi-mcp-orchestrator
display_name: Orquestador MCP Moonshot Kimi K3 para Auditoría de Gran Contexto
description: Orquestación de tareas vía Moonshot AI (Kimi K3) MCP bridge, delegación
  de auditorías a instancias swarm o interacción con la API de Kimi.
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

# kimi-mcp-orchestrator

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/kimi-mcp-orchestrator/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
