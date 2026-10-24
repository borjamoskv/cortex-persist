---
name: cortex-telemetry
display_name: Telemetría Runtime CORTEX, Exergía de Prompts y Drenaje de Sesiones
description: Inspección de telemetría runtime, logs transcript.jsonl, exergía de prompts
  (Chentsov-Markov) y consolidación de sesiones efímeras del brain.
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

# cortex-telemetry

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/cortex-telemetry/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
