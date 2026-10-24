---
name: safari-browser-agent
display_name: Agente Autónomo de Navegación Safari (MCP Dual-Engine v6.0 Sexagesimal
  Apex Sovereign)
description: Orquestación MCP de Safari (nativo, sin WebDriver).
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

# safari-browser-agent

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/safari-browser-agent/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
