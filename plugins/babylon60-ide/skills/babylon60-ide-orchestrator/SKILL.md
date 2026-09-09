---
name: babylon60-ide-orchestrator
description: Orquestación de la INTERFAZ y telemetría del IDE BABYLON-60. Keywords: interfaz babylon, orquestar ide, telemetría visual.
---

# Skill: BABYLON-60 IDE Orchestrator

Este protocolo orquesta la interacción entre las 31 habilidades de CORTEX y el entorno **BABYLON-60 IDE** (Visual Cortex & Thermodynamic Ark).

---

## 1. Conexión de Telemetría

- **Sidecar HTML**: `sidecars/cortex_telemetry.html`
- **Agentes Integrados**: `moskv1`, `moskvbot`
- **Grafo de Skills**: Sincronizado vía `skills.json` y `KERNEL.md`.

---

## 2. Invariantes BABYLON-60

1. **Monitoreo C5-REAL**: Todo cálculo de exergía en BABYLON-60 se alinea con la escala 1 — 23.000 definida en [KERNEL.md](file:///Users/borjafernandezangulo/.gemini/config/skills/KERNEL.md).
2. **Visual Cortex**: Renderizado de telemetría y grafo de adyacencia de habilidades en tiempo real.
3. **Inmunización AST (Split-Brain):** Si el IDE crashea por OOM o acusa la existencia de "clones parasitarios" en el workspace, NUNCA amputar el código funcional asumiendo anergía. Se debe auditar empíricamente la existencia de *symlinks* y aislar la topología excluyendo la ruta anidada en `.vscode/settings.json` (`python.analysis.exclude` y `files.watcherExclude`) para evitar la colisión de indexación dual y preservar el C5-REAL state.
4. **Traducción Visual de Capa Comercial (Proyector Balístico):** Todo frontend o vista ejecutiva de BABYLON-60 DEBE proyectar la colisión de estados (entropía roja disipada vs escudo verde de Ring-0) reflejando exclusivamente los 3 vectores CIO: *Fail-Stop Garantizado*, *Reproducibilidad 100%* y *Coste Marginal Cloud 0.00€*.
5. **Scaffolding Hermético:** Ante restricciones de CLI/sandbox en la creación de aplicaciones web, generar directamente los artefactos (`package.json`, `vite.config.ts`, `App.tsx`, `index.css`) mediante herramientas de escritura de archivos en lugar de depender de scripts interactivos de `npx`.
6. **Mapeo Hexadecimal de Memoria Compartida:** El componente `RingBufferVisualizer` DEBE reflejar la estructura física de los 8 slots alineados a 4096 Bytes desde la dirección base `0x10000000`, mostrando offsets hex, estado atómico (Idle, Ready, Validating, Active, Retired, Quarantine), conteo de `Active_Readers` y digest SHA3-256 inmutable.
7. **Sonificación Procedural Pura (Zero-Asset Web Audio):** Toda retroalimentación acústica en BABYLON-60 (`AudioSynthesizer.ts`) DEBE sintetizarse proceduralmente en tiempo de ejecución mediante la Web Audio API (osciladores senoidales, filtros paso-banda Biquad, generadores de ruido blanco y envolventes ADSR), quedando estrictamente prohibida la dependencia de archivos de audio pre-grabados (.wav/.mp3).


