---
name: cloudflare-mcp-usage
display_name: Automatización & Operaciones Cloudflare MCP
description: Módulo SecOps. Dispara con "cloudflare", "mcp cloudflare", "zonas dns
  cloudflare", "cloudflare worker", "desplegar cloudflare", "kv r2 cloudflare", "cloudflare
  api mcp".
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

# cloudflare-mcp-usage

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/cloudflare-mcp-usage/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
