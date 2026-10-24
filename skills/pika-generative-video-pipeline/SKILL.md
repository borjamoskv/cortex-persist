---
name: pika-generative-video-pipeline
display_name: Pipeline de Generación y Control Parámetrico en Pika Art (A/V)
description: Generación de vídeo e integración de audio en Pika Art con control de
  física (-motion, -fps), Pikaffects y Pika Audio Models.
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

# pika-generative-video-pipeline

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/pika-generative-video-pipeline/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
