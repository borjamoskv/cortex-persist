---
name: c5-socint-extraction-suite
display_name: Suite Soberana de Inteligencia Social (SOCINT C5-REAL)
description: Suite SOCINT omnivectorial en 11 plataformas (X, Substack, Reddit, YouTube,
  HN, Bluesky, Telegram, GitHub, Mastodon, Polymarket, Wikipedia) con detección de
  astroturfing y bóveda SQLite.
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

# c5-socint-extraction-suite

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/c5-socint-extraction-suite/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
