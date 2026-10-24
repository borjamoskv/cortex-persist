---
name: electron-mac-bundle-collision-diagnostics
display_name: Diagnóstico de Crashes & Colisiones Electron en macOS
description: Módulo SecOps. Dispara con "electron crash mac", "crash ips macos", "bundle
  collision electron", "diagnóstico electron mac", "leveldb lock purge", "cierre inesperado
  electron".
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

# electron-mac-bundle-collision-diagnostics

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/electron-mac-bundle-collision-diagnostics/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
