---
name: c5-video-quality-audit
display_name: Auditoría de Calidad y Compresión de Video (PSNR/SSIM/VMAF)
description: Auditoría cuantitativa de compresión y fidelidad de video comparando
  secuencias cuadro a cuadro mediante PSNR, SSIM y VMAF.
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

# c5-video-quality-audit

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-audiovisual-acreativo-sota/references/modules/c5-video-quality-audit/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
