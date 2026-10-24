---
name: c5_scroll_substep_dynamics_invariant
description: Invariante C5-REAL de Dinámica de Scroll Inmersivo y Subpasos Continuos (INV_C5_SCROLL_SUBSTEP_DYNAMICS). Prohíbe descartar frames de cámara en microtareas Promise.all, enforce interpolación inercial (minipasos) en RAF con render síncrono, prefetch asíncrono desacoplado y scroll nativo no secuestrado.
trigger: "model_decision"
---

# Invariante de Dinámica de Scroll Inmersivo y Subpasos Continuos (INV_C5_SCROLL_SUBSTEP_DYNAMICS)

## 1. Axioma Fundamental
En experiencias interactivas y galerías inmersivas donde la cámara o la escena se sincronizan con el scroll del usuario:
$$\hat{\Phi}_{\text{scroll}} = \frac{\text{FluidezVerificada} \cdot \mathbf{1}[\text{ZeroDroppedFrames}]}{C_{\mathrm{render}} + \text{LatenciaPerceptual}}$$
Queda estrictamente prohibido subordinar el frame de dibujo del viewport a la resolución de promesas o microtareas de red/disco. El ciclo de renderizado de la cámara debe ser síncrono, determinista y desacoplado de la carga de activos.

## 2. Las 4 Leyes Invariantes de Dinámica de Scroll

### Ley 1: Interpolación de Minipasos en Silicio (`Sub-Step Inertial Follow`)
- Todo evento de scroll nativo actualiza exclusivamente la coordenada objetivo (`motion.target`).
- La coordenada actual (`motion.current`) debe aproximarse a `motion.target` mediante un bucle de amortiguamiento crítico en `requestAnimationFrame`:
  $$\text{current}_{t+1} = \text{current}_t + (\text{target}_t - \text{current}_t) \cdot \alpha \quad (\alpha \approx 0.14 - 0.18)$$
- Esto transforma cualquier salto discreto (ej. 100 px de un notch de ratón o un impulso de trackpad) en una cascada continua de **15 a 25 minipasos fluidos**, permitiendo control milimétrico y lectura de micro-transiciones.

### Ley 2: Render Síncrono a Tasa de Refresco Nativa (Cero Microtask Drop)
- `render()` se invoca obligatoriamente de forma síncrona dentro del callback de `requestAnimationFrame`, a la tasa de refresco del panel (60 Hz / 120 Hz ProMotion en Apple Silicon).
- Queda terminantemente prohibido condicionar el avance de la cámara con construcciones que descarten frames como `Promise.all([ensureImage(...)]).then(() => { if (request !== motion.request) return; ... })`.

### Ley 3: Precarga Asíncrona Desacoplada (Fire-and-Forget)
- La decodificación o carga de activos vecinos (`ensureImage`, `preloadNeighbours`) debe dispararse como tarea asíncrona en segundo plano sin bloquear ni posponer el bucle de renderizado visual.

### Ley 4: Desplazamiento Nativo No Secuestrado y Reposo Absoluto ($O(1)$)
- **Cero `preventDefault()` en `wheel`:** El oyente de `wheel` debe ser pasivo (`{ passive: true }`) para garantizar compatibilidad con accesibilidad, zoom del navegador y gestos nativos de macOS/iOS.
- **Reposo a $0\%$ CPU:** Cuando $|\text{target} - \text{current}| < \epsilon$, el estado se fija (`current = target`) y se detiene la programación de nuevos frames de RAF, retornando el hipervisor a reposo térmico absoluto ($0\%$ uso de CPU).
- **Paridad con Suites de Test:** En entornos de prueba automatizada (`flush()`), la condición de asentamiento debe converger en $< 30$ frames para garantizar atestación determinista a 0 fallos.
