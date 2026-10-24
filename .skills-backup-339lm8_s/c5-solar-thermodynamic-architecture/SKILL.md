---
name: c5-solar-thermodynamic-architecture
display_name: Arquitectura Helio-Termodinámica y Confort Bioclimático
description: Módulo audiovisual. Dispara con "sun path", "análisis solar", "confort
  térmico", "estudio de sombras", "fanger pmv", "helio-arquitectura", "bioclimático".
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

# c5-solar-thermodynamic-architecture

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/c5-solar-thermodynamic-architecture/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
