---
name: safari_sovereign_automation_invariants
description: Invariantes estrictas de no-bloqueo, OCR local en silicio y centralización de activos para la automatización de Safari en macOS.
---

# Invariantes de Automatización Soberana en Safari macOS (C5-REAL)

## 1. Invariante de Watchdog Circuit Breaker (Anti-Deadlock OSA)
Toda invocación de scripting del sistema hacia Safari (`osascript`, AppleScript o JXA) DEBE ejecutarse bajo un temporizador estricto de desconexión (watchdog $\le 15.000$ ms).
- Queda terminantemente prohibido ejecutar `spawn("osascript")` o `execSync("osascript")` sin control de timeout destructivo (`SIGKILL`).
- Ante un cuelgue del navegador, modal inesperado o bloqueo de hilo, el proceso hijo debe ser purgado inmediatamente para devolver el control al agente sin asfixia de la sesión.

## 2. Invariante de OCR en Silicio Local (Cero Nube)
Para la extracción de texto a partir de capturas o regiones de pantalla en Safari sobre macOS:
- El agente DEBE priorizar el micro-binario nativo en Swift (`c5_vision_ocr`) ejecutado contra el framework nativo `Vision` (`VNRecognizeTextRequest`) de Apple Silicon.
- Queda prohibido enviar capturas de pantalla de Safari a APIs comerciales de visión o requerir librerías OCR no locales cuando el silicio de Apple pueda resolverlo en $<50$ ms.

## 3. Invariante de Resolución Dinámica de Python
En scripts o puentes de procesamiento que requieran librerías como Pillow (`PIL`) o `pypdf`:
- Queda estrictamente prohibido hardcodear `/usr/bin/python3` (entorno del sistema sin paquetes de terceros).
- El agente DEBE invocar `python3` desde el entorno (`PATH`), permitiendo la correcta carga de entornos Homebrew (`/opt/homebrew/bin/python3`) o virtuales.

## 4. Invariante de Centralización de Activos de Audio
Todo audio sintetizado (`safari_synthesize_text_to_speech`) o extraído de Safari (`safari_harvest_assets`) DEBE depositarse o enlazarse en la biblioteca raíz del usuario `~/Music/` (`/Users/borjafernandezangulo/Music/`), preservando la regla `music_assets_centralization_invariant`.

## 5. Invariante de Cierre Sexagesimal Base-60
El ecosistema de herramientas de Safari mantiene una cota canónica de 60 herramientas MCP, preservando la simetría sexagesimal de BABYLON-60 sin introducir componentes redundantes que no superen el test de independencia causal.
