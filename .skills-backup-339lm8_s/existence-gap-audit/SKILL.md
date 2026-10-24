---
name: existence-gap-audit
display_name: Auditoría de Huecos de Existencia & Supply-Chain Slop
description: Módulo SecOps. Dispara con "revisa este repo", "código alucinado", "dependencias
  fantasma", "slopsquatting", "vibe coding", "supply chain", "¿esto se ejecuta?",
  "imports rotos", "auditar workflows".
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

# existence-gap-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/existence-gap-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
