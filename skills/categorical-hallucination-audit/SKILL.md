---
name: categorical-hallucination-audit
display_name: Auditoría Categórica de Alucinación & Cota Kl(D)
description: Formalización en Categorías de Markov, desintegración bayesiana y cota
  cuantitativa de alucinación en Kl(D).
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

# categorical-hallucination-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/categorical-hallucination-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
