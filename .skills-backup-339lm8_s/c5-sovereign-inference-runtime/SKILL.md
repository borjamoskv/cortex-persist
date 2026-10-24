---
name: c5-sovereign-inference-runtime
display_name: Motor Soberano de Inferencia y Adaptador LM Studio C5-REAL
description: Módulo Ring-0. Dispara con "eridu-infer", "inferencia soberana", "appliance
  ia", "lm studio protocolo", "motor inferencia local", "air-gapped infer", "servidor
  openai local rust", "sovereign inference runtime", "desplegar eridu-infer", "tríada
  jurídica".
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

# c5-sovereign-inference-runtime

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-ring0-babylon-kernel/references/modules/c5-sovereign-inference-runtime/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
