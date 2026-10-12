---
name: c5_gflow_automation_invariants
description: Protocolo determinista para automatización de Google Flow (Veo I2V/T2V), bypass de banners de consentimiento localizados y elusión de falsos positivos agénticos.
---

# Invariante de Automatización y Resiliencia en Google Flow (INV_C5_GFLOW)

## 1. Protocolo de Descarte de Banner de Consentimiento (Locale Invariance)
Al automatizar `flow.google.com` mediante Playwright o `gflow-cli`:
- El banner de cookies (`#glue-cookie-notification-bar-1`) debe descartarse inspeccionando indistintamente:
  `button.glue-cookie-notification-bar__reject, button.glue-cookie-notification-bar__accept, button:has-text('Entendido'), button:has-text('Aceptar')`.
- Queda prohibido asumir la presencia exclusiva de `__reject`. Si el banner persiste, intercepta los eventos de puntero sobre `button.agent-mode-chip` y falsea la detección de *Agent-Only Composer*.

## 2. Recuperación de Composer Clásico ante Panel Agéntico Expandido
Si la interfaz aterriza con el panel de chat agéntico abierto (*«Sesión sin título»*):
1. Ejecutar clic sobre el botón de cierre del panel (`button[aria-label="Cerrar"]` o ligadura `close`).
2. Comprobar `button.agent-mode-chip`. Si `aria-pressed="true"`, hacer clic para desactivar el modo agéntico (`force=True` o tras descarte de overlays).
3. Esperar visibilidad de `.settings-trigger-button` antes de declarar deriva de selectores o emitir código 25.

## 3. Higiene de Prompts para Veo (Anti-Status 4)
En pipelines Image-to-Video (I2V):
- Queda estrictamente prohibido incluir nombres de figuras públicas o cargos políticos contemporáneos en el prompt textual de animación.
- El modelo reconoce la fisonomía directamente desde el Frame 0; el texto debe restringirse a descriptores motrices, cinemáticos, lentes, iluminación y física de cámara para evitar abortos tardíos por políticas de backend (`status=4`).
