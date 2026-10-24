---
name: whatsapp-nexus-protocol
display_name: Pasarela Soberana de Mensajería WhatsApp (Baileys v7 / Rust NAPI-RS
  / C5-REAL v2.6)
description: Módulo SecOps. Dispara con "whatsapp nexus", "bot whatsapp", "baileys
  rust", "pasarela whatsapp", "whatsapp gateway", "enviar whatsapp", "mensajes whatsapp",
  "wa-nexus".
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

# whatsapp-nexus-protocol

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/whatsapp-nexus-protocol/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
