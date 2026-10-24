---
name: c5-poster-and-sign-craft
display_name: Pipeline de Remasterización Gráfica, Rotulación en Perspectiva y Filtrado
  Analógico
description: Módulo audiovisual. Dispara con "remasterizar cartel", "rotular letrero",
  "cambiar texto cartel", "sign craft", "filtro vintage comic", "bajar contraste imagen",
  "quitar contraste duro", "poster remaster", "maquetación cartel", "analizar cartel",
  "flyer underground", "auditoría tipográfica cartel".
role: ejecutor
allowed_roles:
- ejecutor
- arquitecto
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# c5-poster-and-sign-craft

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/c5-poster-and-sign-craft/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
