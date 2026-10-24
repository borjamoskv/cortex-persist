---
name: c5-neural-face-swap-cuadrilla
display_name: Pipeline Neural Face-Swap Cuadrilla (V5 SOTA Hybrid)
description: Módulo audiovisual. Dispara con "face swap", "deepfake cuadrilla", "intercambio
  facial", "c5 face swap".
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

# c5-neural-face-swap-cuadrilla

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/c5-neural-face-swap-cuadrilla/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
