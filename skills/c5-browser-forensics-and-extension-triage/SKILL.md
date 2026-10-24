---
name: c5-browser-forensics-and-extension-triage
display_name: Auditoría Forense de Navegadores y Triaje de Extensiones Chromium
description: Auditoría forense de navegadores, triaje de content_scripts, desinfección
  Chromium y navegador por defecto macOS.
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

# c5-browser-forensics-and-extension-triage

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/c5-browser-forensics-and-extension-triage/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
