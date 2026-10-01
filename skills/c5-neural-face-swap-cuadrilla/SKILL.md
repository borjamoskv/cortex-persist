---
name: c5-neural-face-swap-cuadrilla
display_name: Pipeline Neural Face-Swap Cuadrilla (InsightFace CoreML)
description: Pipeline industrial de alta velocidad para intercambio facial neuronal (deepfake) en vídeos reales o virales con identidades de la cuadrilla sobre Apple Silicon M-Series. Utiliza InsightFace buffalo_l, inswapper_128.onnx con CoreML, mezcla continua C^\infty, FaceTracker IoU, worker chunking paralelo y codificación por hardware VideoToolbox. Dispara con "pon la cara de", "ponle la cara de", "swap cara video", "deepfake cuadrilla", "videos miticos", "inswapper coreml", "vídeos míticos de los chavales", o al enviar un enlace de Instagram/TikTok/Shorts pidiendo sustituir un rostro.
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

# Pipeline Neural Face-Swap para Vídeos Míticos de la Cuadrilla

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este skill proporciona el procedimiento de ejecución determinista para sustituir rostros en vídeos reales/virales con las identidades de la cuadrilla en macOS Apple Silicon (M3 Pro / Max).

## 0. Regla de Oro de Desambiguación (Territorio vs. Paradigma)

* **Vídeo Real / Reel / Clip Viral + «pon la cara de X»:** SIEMPRE aplicar **Deepfake Neuronal** (InsightFace + Inswapper 128 con `c5-face-swap`). Queda terminantemente PROHIBIDO intentar recortar avatares 2D de South Park o simular bocas animadas sobre metraje real.
* **Avatares South Park (`_top.png` / `_jaw.png`):** Reservados exclusivamente para escenas de animación generadas desde cero sobre fondos fijos o proyectos de sketches tipo `render_boda_hugo_video.py`.

---

## 1. Entorno de Silicio y Modelos Canónicos

* **CLI Global Desplegada:**
  `c5-face-swap` (enlace simbólico en `~/.local/bin/c5-face-swap`)
* **Intérprete Python verificado con CoreML:**
  `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`
* **Modelo Inswapper:**
  `/tmp/inswapper_128.onnx`
* **Directorio de Rostros Fuente:**
  `/Users/borjafernandezangulo/Downloads/VIDEO BODA HUGO/faces/<personaje>_real.png`
* **Directorio Canónico de Salida:**
  `~/Movies/VIDEOS_MITICOS/<TITULO>.mp4` (con copia en el workspace activo si aplica).

---

## 2. Roster Canónico de Identidades (17 Miembros)

| Personaje / Alias | Archivo Fuente Canónico |
| :--- | :--- |
| **Alain** (Elektronische / Elektrocaniche) | `faces/alain_real.png` |
| **Eder** (Dual Sound / Balcón de la LOLA) | `faces/eder_real.png` |
| **Luengo** (Tigre Máquina) | `faces/luengo_real.png` |
| **Xabi** (Cabeza Gigante / Moñas) | `faces/xabi_real.png` |
| **Borja** (Moskv) | `faces/borja_real.png` |
| **Hugo** (Hugo Pink / El Novio) | `faces/hugo_real.png` / `hugo_pink_real.png` |
| **Mitxu** (El Mitxus) | `faces/mitxu_real.png` |
| **Pedrerol** (Josep Pedrerol) | `faces/pedrerol_real.png` |
| **Tosso** (Jacuzzi Llanes) | `faces/tosso_real.png` |
| **Lander** | `faces/lander_real.png` |
| **Medina** | `faces/medina_real.png` |
| **Patxi** | `faces/patxi_real.png` |
| **David Landeta** (Basques on Decks) | `faces/david_landeta_real.png` |
| **Aloisio** | `faces/aloisio_real.png` |
| **Jorge Malatesta** | `faces/jorge_malatesta_real.png` |
| **Txinorris** | `faces/txinorris_real.png` |
| **The Brother** | `faces/the_brother_real.png` |

---

## 3. Arquitectura del Motor V3 SOTA (`c5-face-swap`)

1. **Desacoplamiento de Silicio Híbrido:**
   - Detección SCRFD confinada a CPU pura (`CPUExecutionProvider`) a $320\times 320$: $29{,}5\text{ ms}$ ($33{,}9\text{ FPS}$) con $0\text{ MB}$ de overhead de compilación CoreML.
   - Inswapper 128 FP16 despachado a Apple Neural Engine (ANE) / GPU (`CoreMLExecutionProvider`): modelo optimizado de $264\text{ MB}$ en FP16.
   - Codificación acelerada por hardware: `h264_videotoolbox` a 8.5 Mbps con filtros CAS y unsharp.
2. **Super-Resolución Neuronal a $512\times 512$ (`--enhancer`):**
   - **GPEN 512** (por defecto, latencia ultrabaja y nitidez extrema de rasgos, poros y arrugas).
   - **CodeFormer** (reconstrucción mediante Codebook Prior $\mathcal{Z}$, ideal para primeros planos cinematográficos con fidelidad `--enhance-weight`).
   - **GFPGAN 1.4** (alternativa GAN clásica).
   - **None** (modo baseline ultrarrápido 128px).
3. **Mapeo de Puntos Densos 3D y Estimación de Pose (FAN-68):**
   - Red `fan_68_5.onnx` con normalización afín RANSAC sobre plantilla FFHQ-512 ($0{,}017\text{ ms}$).
   - Estimación de pose tridimensional de cabeza mediante `cv2.solvePnP`: cálculo de Yaw, Pitch y Roll en tiempo real.
   - Detección del ratio de apertura bucal (MAR - Mouth Aspect Ratio) para dinámicas fonéticas.
4. **Articulación Bucal Orgánica y Desoclusión Semántica (`--preserve-mouth auto`):**
   - Red BiSeNet ResNet-34 ($89\text{ MB}$) para segmentación de 19 clases anatómicas.
   - Exclusión de la clase 11 (cavidad bucal interna): cuando el orador habla, grita o sonríe ($MAR > 0.14$), se preservan los dientes y la lengua orgánicos originales del vídeo, erradicando los "dientes de plástico" de las fotos estáticas.
   - Protección infalible ante oclusiones: micrófonos, manos, vasos, gafas y pelo en primer plano se excluyen de la máscara y quedan 100% preservados.
5. **Fusión Espectral de Dos Bandas (`--blend two-band`):**
   - Descomposición en frecuencias bajas (iluminación global e irradiancia) y altas (textura cutánea, poros y vello).
   - Ejecutada en el espacio canónico normalizado $512\times 512$ a $>110\text{ FPS}$ antes de la desproyección afín inversa.
   - Anulación absoluta de saltos tonales, costuras y halos de recorte.
6. **Fusión Multi-Referencia y Media de Fréchet en $\mathbb{S}^{511}$:**
   - Soporte para sintaxis de múltiples fotos separadas por `+` (e.g. `--identity "mitxu_gafas+mitxu_real"`) o carpetas con diferentes ángulos.
   - Cálculo de la Media Fréchet Riemanniana sobre la hiperesfera unitaria de 512 dimensiones: $\mu = \frac{\sum e_i}{\|\sum e_i\|_2}$, combinando rasgos para máxima generalización.
7. **Selección Selectiva de Rostros y Purgado de Falsos Positivos:**
   - `--target-face-index N`: Permite intercambiar exclusivamente el rostro del rango deseado (0 = rostro principal/mayor, 1 = presentador secundario).
   - `--swap-all`: Intercambio de todos los rostros de la escena.
   - Prevención de swaps redundantes: las caras secundarias que no tengan identidad explícita asignada no se computan, duplicando el rendimiento en escenas concurridas.
8. **Rastreador Zero-Drop con Filtros 1-Euro Independientes:**
   - Extrapolación inercial de hasta 2 frames ante desenfoque por movimiento rápido, eliminando el parpadeo de fotogramas originales.
   - Instancia de `OneEuroFilter` por cada trayectoria activa.
9. **Worker Chunking Paralelo (`--workers N`):**
   - Escisión temporal determinista en subprocesos aislados.
   - Concatenación $O(1)$ sin recodificación con FFmpeg concat demuxer.
10. **Modo Watcher Daemon (`--watch <inbox>`):**
    - Procesamiento reactivo en segundo plano de cualquier vídeo o enlace depositado en la carpeta monitorizada.

---

## 4. Uso de la CLI de Producción (V3 SOTA)

```bash
# 1. Render SOTA V3 estándar (GPEN 512 + Two-Band Blend + Mouth Passthrough Auto + MKL)
c5-face-swap --video soria.mp4 --identity Mitxu --workers 2

# 2. Fusión Multi-Referencia con Fréchet Mean en S^511
c5-face-swap --video soria.mp4 --identity "mitxu_gafas+mitxu_real" --workers 2

# 3. Intercambio selectivo (sólo el presentador secundario, índice 1)
c5-face-swap --video chiringuito.mp4 --identity Alain --target-face-index 1 --workers 2

# 4. Intercambio múltiple en escena (Pedrerol -> Alain, Soria -> Mitxu)
c5-face-swap --video chiringuito.mp4 --identity "alain,mitxu" --swap-all --workers 2

# 5. Render de Máxima Calidad Cinematográfica (CodeFormer HD a w=0.7)
c5-face-swap --video clip.mp4 --identity Borja --enhancer codeformer --enhance-weight 0.7 --workers 2

# 6. Ingesta directa desde enlace web (Instagram / TikTok / YouTube)
c5-face-swap --video "https://www.instagram.com/reel/Dd4MioYDy3E/..." --identity Alain

# 7. Modo Rápido Baseline 128px (sin super-resolución)
c5-face-swap --video clip.mp4 --identity Eder --enhancer none --workers 4

# 8. Modo Watcher Daemon reactivo en segundo plano
c5-face-swap --watch ~/Downloads/c5_inbox/ --identity Alain --workers 2
```

---

## 5. Protocolo de Verificación y Doble Persistencia

1. **Atestación Visual:** Extraer fotograma de control representativo y auditar con `view_file`.
2. **Doble Persistencia Invariante:**
   - Archivo de trabajo: `$PWD/<nombre>_<identidades>_c5swap.mp4`
   - Biblioteca canónica: `/Users/borjafernandezangulo/Movies/VIDEOS_MITICOS/<nombre>_<identidades>_c5swap.mp4`

