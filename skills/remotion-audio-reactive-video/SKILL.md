---
name: remotion-audio-reactive-video
display_name: Síntesis de Vídeo Reactivo a Audio & Música (Remotion + DSP)
description: Diseño, arquitectura y renderizado de vídeos reactivos a música y audio utilizando Remotion, @remotion/media-utils (useAudioData, visualizeAudio), análisis FFT espectral (sub-bass, mids, highs), sincronización de grids BPM y shaders WebGL/Canvas. Dispara con "video reactivo a la musica", "audio reactivo", "remotion audio reactive", "visualizador de musica", "audio visualizer", "video musical reactivo", "reactivo al ritmo".
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

# Habilidad SOTA: Síntesis de Vídeo Reactivo a la Música con Remotion & DSP (Tier 21.000)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Esta habilidad rige la arquitectura, transducción matemática de señal acústica y renderizado de vídeo cinemático reactivo al audio en el ecosistema macOS / Apple Silicon M3 Pro con Remotion.

---

## 🎯 Criterios de Activación
- Solicitudes de creación de visualizadores de audio, videoclips o espectrogramas dinámicos.
- Integración de pistas musicales, beats, stems de FL Studio (`kick.wav`, `bass.wav`) o voces en Remotion.
- Modulación determinista de parámetros visuales (cámara, escala, deformación SVG, aberración cromática, partículas).
- Eliminación de jitter/flicker estroboscópico mediante filtrado balístico y detección de transitorios.

---

## 📐 1. Principios Psicoacústicos Fundamentales

> **Invariante C5 (Aforismo 1):** *Transformar ruido en conceptos.*
> La amplitud bruta de un bin FFT es ruido. El concepto musical es el **transitorio (onset)**, la **fase de compás (BPM)** y la **distribución en bandas cocleares de Bark**.

### Algoritmos Críticos (Implementados en `examples/SpectralFlux.ts`):
1. **Flujo Espectral (Spectral Flux Onset Detection):**
   $$SF(t) = \sum_{k} \mathcal{H}\Big( |X(t, k)| - |X(t-1, k)| \Big)$$
   Captura únicamente inyecciones netas de potencia percusiva, ignorando resonancias mantenidas.
2. **Filtro Balístico Asimétrico (Attack / Release):**
   Ataque rápido ($\alpha_{\text{att}} = 0.85$) para clavar el impacto en el frame exacto; decaimiento exponencial suave ($\alpha_{\text{rel}} = 0.14$) para evitar el temblor retiniano.
3. **Bandas Perceptivas:**
   - **Sub-Bass (20–80 Hz):** Empuje de cámara focal y sacudida sísmica (*screen shake*).
   - **Bass (80–250 Hz):** Escala volumétrica y deformación de geometría SVG.
   - **Low-Mids (250–1000 Hz):** Modulación de color y ondas armónicas.
   - **High-Mids (1000–4000 Hz):** Espectrograma de barras radiales y presencia vocal.
   - **Air (>4000 Hz):** Aberración cromática, halos de dispersión y grano analógico 35mm.

---

## ⏱️ 2. Sincronización de Fase BPM

Cálculo de compás determinista sin desfases temporales:

$$\text{framesPerBeat} = \frac{\text{fps} \cdot 60}{\text{BPM}}$$

Animación de caída percusiva natural por decaimiento exponencial:
```tsx
const framesPerBeat = (fps * 60) / bpm;
const beatPhase = (frame % framesPerBeat) / framesPerBeat;
const beatDecay = Math.exp(-beatPhase * 4.0); // Curva balística de transitorio
```

---

## 🎛️ 3. Desacoplamiento Multi-Stem (Flujo FL Studio)

Para evitar la compresión destructiva del audio masterizado:
1. Exportar pistas por separado desde FL Studio (`~/10_PROJECTS/flstudio-mcp/`):
   - `stems/kick.wav` $\to$ Gobierna el `scale` global de la cámara y el *screen shake*.
   - `stems/bass.wav` $\to$ Gobierna el radio del orbe central.
   - `stems/synth.wav` $\to$ Gobierna las barras radiales del espectrograma.
   - `stems/vocals.wav` $\to$ Gobierna los títulos cinéticos y glow óptico.
2. En Remotion, cargar los stems con `useAudioData(staticFile("stems/kick.wav"))` de manera no bloqueante.

---

## 📁 4. Módulos y Plantillas de Producción

Los componentes listos para ejecución se encuentran alojados en la subcarpeta `examples/`:

- [`SpectralFlux.ts`](./examples/SpectralFlux.ts): Motor matemático de transducción, Bark grouping y suavizado balístico.
- [`AudioReactiveMaster.tsx`](./examples/AudioReactiveMaster.tsx): Composición completa lista para renderizado 1080p / 4K.

---

## ⚡ 5. Protocolo de Renderizado Acelerado (M3 Pro Metal)

Para garantizar 60 FPS y cero artefactos de cuantización de color en macOS:

```bash
npx remotion render src/index.ts AudioReactiveMaster out/reactive_sota.mp4 \
  --gl=angle \
  --codec=h264 \
  --pixel-format=yuv420p \
  --concurrency=10 \
  --crf=18 \
  --enforce-audio-track
```

### Invariantes de Entrega:
- **`--gl=angle`**: Ejecuta las capas WebGL y shaders en la GPU Metal de Apple Silicon.
- **`--pixel-format=yuv420p`**: Obligatorio para reproducción sin fallo en QuickTime, Safari y plataformas de distribución.
- **`--enforce-audio-track`**: Previene desfases de sincronización A/V en vídeos de larga duración.
