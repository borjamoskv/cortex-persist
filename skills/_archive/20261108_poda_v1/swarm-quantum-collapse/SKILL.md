---
name: swarm-quantum-collapse
display_name: Sincronización Swarm & Colapso Cuántico Multi-Repositorio
description: Orquesta un enjambre Python P×S calibrado empíricamente para forzar la
  sincronización (Colapso Cuántico) de múltiples repositorios simultáneos.
role: ejecutor
allowed_roles:
- ejecutor
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# swarm-quantum-collapse

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-cortex-swarm-orchestrator/references/modules/swarm-quantum-collapse/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
