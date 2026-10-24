---
name: c5-plan-omega
display_name: Protocolo PLAN-Ω de Planificación Causal Determinista
description: Motor de planificación determinista en DAG (Protocolo PLAN-Ω). Sustituye
  checklists planas por matrices topológicas de 4 niveles, sondeo pre-flight en 60s,
  puertas Two-Way/One-Way con rollback y micro-gates Fail-Stop.
role: arquitecto
allowed_roles:
- arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# c5-plan-omega

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/c5-plan-omega/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
