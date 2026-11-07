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

## Oráculo Determinista de la Tríada Trans-Dominio (`Z3 SMT`)

Para auditar formalmente cualquier topología DAG, longitud de bloque entre `Micro-Gates` y coste de falsificación de oráculo bajo las 3 Leyes de Conservación C5-REAL (`Tutte-Hopfield`, `Eigen-Wright`, `Bode-Wiener`), ejecuta [c5_triad_gate.py](scripts/c5_triad_gate.py):

```bash
python3 ~/.gemini/config/skills/c5-plan-omega/scripts/c5_triad_gate.py --selftest
```
