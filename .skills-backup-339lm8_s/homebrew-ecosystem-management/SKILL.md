---
name: homebrew-ecosystem-management
display_name: Gestión & Auditoría de Paquetes Homebrew en macOS
description: Módulo SecOps. Dispara con "homebrew", "brew audit", "dependencias macos",
  "paquetes homebrew", "gestión homebrew", "entorno brew".
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

# homebrew-ecosystem-management

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/homebrew-ecosystem-management/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
