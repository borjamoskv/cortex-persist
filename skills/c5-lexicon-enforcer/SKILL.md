---
name: c5-lexicon-enforcer
display_name: Oráculo de Verificación Epistemológica & Auditoría de Coste Involuntario
  (Aforismo 5)
description: Oráculo epistemológico C5-REAL y Linter del Aforismo 5 (purga de cheap
  talk voluntario hacia señales involuntarias).
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

# c5-lexicon-enforcer

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/c5-lexicon-enforcer/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
