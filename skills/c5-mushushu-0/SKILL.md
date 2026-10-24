---
name: c5-mushushu-0
display_name: Oráculo Formal & Firewall de Apoptosis MUSHUSHU-0 (Ring-0)
description: Oráculo formal y firewall epistémico Ring-0 para validación determinista
  y apoptosis (MUSHUSHU-0).
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

# c5-mushushu-0

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-mushushu-0/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
