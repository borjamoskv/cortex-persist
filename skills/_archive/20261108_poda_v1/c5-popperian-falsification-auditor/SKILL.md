---
name: c5-popperian-falsification-auditor
display_name: Auditor de Falsación Empírica de Documentos
description: Somete documentos locales, manifiestos o afirmaciones técnicas a falsación
  empírica C5-REAL contrastando con literatura científica primaria.
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

# c5-popperian-falsification-auditor

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/c5-popperian-falsification-auditor/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
