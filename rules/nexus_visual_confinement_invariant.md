---
name: nexus-visual-confinement-invariant
description: Invariante estricta de confinamiento visual y OPSEC para Nexus. Prohíbe terminantemente el despacho de capturas de pantalla (pantallazos) o imágenes sin el permiso previo y explícito de Borja.
trigger: "always_on"
---

# Invariante de Confinamiento Visual y Despacho en Nexus (Zero-Leakage Invariant)

## 1. Directiva Fundamental (Fail-Closed)
Queda **estrictamente prohibido** que cualquier agente, subagente, bot o pasarela (`wa-nexus`, `Moskv-1`, o integraciones agénticas) despache, comparta o envíe **capturas de pantalla («pantallazos»), imágenes generadas o archivos visuales** en el entorno de Nexus (sea el grupo de WhatsApp de la Cuadrilla Nexus, la pasarela de mensajería o cualquier canal anexo) **sin el permiso explícito, previo e inequívoco de Borja (el Operador Raíz)**.

## 2. Ámbito y Superficie de Confinamiento
Esta prohibición aplica universalmente a:
1. **Sub-Red Nexus / Cuadrilla Nexus:** Conversaciones, hilos y grupos asociados al círculo Nexus de WhatsApp.
2. **Herramientas de Pasarela WhatsApp (`wa-nexus`):** Invocaciones a `whatsapp_send_message` cuando el parámetro `media_path` o adjuntos contengan imágenes, gráficos o capturas del sistema.
3. **Generación Visual en Canal:** Invocaciones a `gemini_generate_image` u otras herramientas generativas destinadas a ser despachadas a dicho canal.
4. **Capturas de Pantalla Automatizadas:** Capturas provenientes de DevTools (`safari_take_screenshot`), terminales o escritorios.

## 3. Protocolo de Acción ante Solicitudes o Intentos de Envío
1. **Bloqueo Preventivo por Defecto:** Si durante la interacción surge una solicitud, sugerencia o heurística que implique enviar una captura o imagen a Nexus, el sistema debe pausar y bloquear la acción inmediatamente.
2. **Requerimiento Imperativo de Autorización:** El agente debe solicitar explícitamente la confirmación de Borja antes de cualquier transmisión de datos visuales: *«Se requiere autorización previa y explícita del Operador para despachar material visual o capturas a Nexus»*.
3. **Cero Suposición de Consentimiento:** Las autorizaciones otorgadas para otros canales o en turnos previos no se heredan; cada despacho visual hacia Nexus requiere validación directa e independiente.
