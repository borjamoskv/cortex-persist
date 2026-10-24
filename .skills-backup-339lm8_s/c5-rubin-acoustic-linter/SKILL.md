---
name: c5-rubin-acoustic-linter
display_name: Linter Acústico de Exergía y Purga de Nata (Protocolo Rubin)
description: Módulo audiovisual. Dispara con "linter acústico", "auditoría de mezcla",
  "purga de nata en audio", "rubin audit", "dedup apfs audio", "crest factor audio",
  "medir compresión".
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

# c5-rubin-acoustic-linter

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/c5-rubin-acoustic-linter/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
