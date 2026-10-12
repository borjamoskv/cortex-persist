---
name: c5_whatsapp_formatting_invariant
description: Invariante de formateo tipográfico estricto para salidas destinadas a WhatsApp (cajas Unicode y sintaxis nativa de un solo asterisco).
---

# Invariante de Formateo Modo WhatsApp (C5-WHATSAPP-FORMAT)

## 1. Directiva Fundamental
Cuando el usuario solicite «modo whatsapp», «formato whatsapp» o la preparación de un texto para ser despachado a través de WhatsApp o clientes de mensajería afines, el agente DEBE aplicar de forma obligatoria la sintaxis de marcado nativa de WhatsApp y la maquetación tipográfica de cajas Unicode de alta exergía.

## 2. Restricciones Sintácticas Estrictas
1. **Negrita Nativa (Un solo asterisco):** Queda estrictamente prohibido usar markdown estándar de doble asterisco (`**texto**`), ya que en WhatsApp no se formatea y expone asteriscos planos. Se debe usar obligatoriamente `*texto*`.
2. **Cursiva:** Usar `_texto_`.
3. **Tachado:** Usar `~texto~`.
4. **Monoespaciado / Código:** Usar tres comillas invertidas (```texto```).

## 3. Arquitectura de Cajas Tipográficas Unicode
El texto debe estructurarse mediante bloques visuales modulares delimitados por caracteres de caja:
* Encabezados principales:
  ```
  ╔═════════════════════════════════════════════╗
  ║   ⚡ TÍTULO DEL BLOQUE OTR / C5-REAL ⚡     ║
  ╚═════════════════════════════════════════════╝
  ```
* Módulos de contenido y derivaciones:
  ```
  ╭─► 1. TÍTULO DEL MÓDULO O AFORISMO
  │
  ├─ Premisa o telemetría descriptiva.
  │
  ╰─► *Territorio / Conclusión:* Síntesis de asfalto.
  ```
* Separadores de sección: `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`.
