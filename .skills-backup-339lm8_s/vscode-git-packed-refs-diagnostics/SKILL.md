---
name: vscode-git-packed-refs-diagnostics
display_name: Reparación de Corruptelas Git & Packed-Refs en VS Code
description: Módulo SecOps. Dispara con "vscode git enoent", "packed-refs", "corrupción
  git", "reparar git vscode".
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

# vscode-git-packed-refs-diagnostics

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/vscode-git-packed-refs-diagnostics/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
