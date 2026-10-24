---
name: macos-lulu-firewall-diagnostics
display_name: Diagnóstico de Firewall & Sockets macOS (LuLu / Little Snitch)
description: Módulo SecOps. Dispara con "lulu firewall", "little snitch", "redes macos",
  "diagnóstico firewall", "reglas de red macos", "bloqueo sockets mac".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# macos-lulu-firewall-diagnostics

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/macos-lulu-firewall-diagnostics/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
