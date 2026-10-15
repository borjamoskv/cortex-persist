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

> **Directiva Declarativa:** Alias compatible del hub SecOps; conserva el contrato del módulo original.

## Cargar el módulo

Lee [las instrucciones originales](../c5-secops-infra-devtools/references/modules/whatsapp-nexus-protocol/MODULE.md) antes de aplicar esta habilidad.
Conserva sus triggers, rol, restricciones, procedimiento y alcance.
Carga únicamente los recursos pertinentes a la petición.

## Recursos y rutas

Los recursos originales permanecen junto a este alias y se conservan completos dentro del hub.
Resuelve las referencias relativas desde el archivo del módulo que hayas leído.
Mantén el directorio de trabajo del proyecto elegido por el usuario.
Las rutas absolutas del paquete original continúan disponibles.

## Invocación

El comando `/whatsapp-nexus-protocol` sigue disponible con el nombre original.
El hub se consulta con `/c5-secops-infra-devtools`.
La carga del alias no ejecuta auditorías, scripts, búsquedas ni comunicaciones por sí misma.
El procedimiento del módulo se aplica únicamente dentro del trabajo solicitado.
