---
name: electron-asar-forensic-audit
display_name: Auditoría Forense In-Memory de Empaquetados Electron (app.asar)
description: Auditoría forense y extracción binaria in-memory de archivos Electron
  app.asar y binarios nativos auxiliares sin dependencias.
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

# electron-asar-forensic-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/electron-asar-forensic-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
