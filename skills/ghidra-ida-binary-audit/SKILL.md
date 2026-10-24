---
name: ghidra-ida-binary-audit
display_name: Auditoría de Binarios Crudos & Descompilación Ghidra/IDA
description: Ingeniería inversa, descompilación y auditoría de binarios ejecutables
  crudos mediante Ghidra / IDA Pro headless.
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

# ghidra-ida-binary-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/ghidra-ida-binary-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
