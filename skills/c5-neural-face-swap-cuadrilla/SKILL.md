---
name: c5-neural-face-swap-cuadrilla
display_name: Pipeline Neural Face-Swap Cuadrilla (V4 SOTA CoreML)
description: "Pipeline industrial de alta velocidad para intercambio facial neuronal (deepfake) en vídeos reales o virales con identidades de la cuadrilla sobre Apple Silicon M-Series. Motor V4 SOTA con BiSeNet acelerado en CoreML (19ms), GPEN 512, transferencia de iluminación espacial 3D, preservación de párpados EAR y boca MAR, estabilizador anti-shimmer, fusión de dos bandas y codificación por hardware VideoToolbox. Dispara con 'pon la cara de', 'ponle la cara de', 'swap cara video', 'deepfake cuadrilla', 'videos miticos', 'inswapper coreml', 'vídeos míticos de los chavales', o al enviar un enlace de Instagram/TikTok/Shorts pidiendo sustituir un rostro."
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

## 3. Arquitectura del Motor V4 SOTA (`c5-face-swap`)

1. **Desacoplamiento de Silicio Híbrido & Aceleración CoreML (Apple Neural Engine):**
   - **Segmentación Semántica BiSeNet ResNet-34 en CoreML:** Inferencia despachada al Apple Neural Engine (ANE) / GPU (`CoreMLExecutionProvider`). Aceleración radical de $284{,}2\text{ ms}$ ($3{,}5\text{ FPS}$) a **$19{,}4\text{ ms}$ ($51{,}5\text{ FPS}$)** ($14{,}6\times$ de ganancia neta).
   - **Inswapper 128 FP16 en CoreML:** Modelo nativo en FP16 optimizado para latencia sub-$25\text{ ms}$.
   - **GPEN 512 en CPU Multi-Hilo (4 threads):** Inferencia con latencia balanceada sin contención de particiones.
   - **Codificación por Hardware VideoToolbox:** Muxing directo H.264/HEVC a 8.5 Mbps con filtros CAS y unsharp.
2. **Super-Resolución Neuronal a $512\times 512$ (`--enhancer`):**
   - **GPEN 512** (por defecto, nitidez cinematográfica de rasgos, poros y arrugas sin desenfoque).
   - **CodeFormer** (reconstrucción mediante Codebook Prior $\mathcal{Z}$, con fidelidad ajustable `--enhance-weight`).
   - **GFPGAN 1.4** (alternativa GAN clásica).
   - **None** (modo baseline ultrarrápido 128px).
3. **Mapeo de Puntos Densos 3D, Pose y Ratios Somáticos (FAN-68):**
   - Red `fan_68_5.onnx` con normalización afín RANSAC sobre plantilla FFHQ-512 ($0{,}017\text{ ms}$).
   - Estimación de pose tridimensional (Pitch, Yaw, Roll) en tiempo real mediante `cv2.solvePnP`.
   - Detección métrica de Mouth Aspect Ratio (MAR) y Eye Aspect Ratio (EAR).
4. **Transferencia de Iluminación Espacial 3D y Sombras (`--lighting spatial`):**
   - Extracción de gradiente de iluminación ambiental de baja frecuencia mediante filtros espaciales multiescala.
   - Sincroniza luces de estudio, reflejos especulares en frente/nariz y sombras en pómulos, eliminando el aspecto plano de "recorte pegado" sin alterar la textura de la piel.
5. **Preservación Orgánica de Párpados y Parpadeo Natural (`--preserve-eyes auto`):**
   - Métrica EAR: cuando $EAR < 0.18$ (parpadeo o cierre ocular del orador), se activa la exclusión geométrica de párpados mediante polígonos convexos difuminados.
   - El parpadeo, pestañas y arrugas perioculares orgánicas del vídeo original se preservan al 100%, evitando que el deepfake superponga ojos abiertos artificiales.
6. **Articulación Bucal Orgánica y Desoclusión Semántica (`--preserve-mouth auto`):**
   - Exclusión dinámica de la cavidad bucal interna (clase 11 de BiSeNet) cuando $MAR > 0.14$, conservando dientes y lengua reales durante el habla o gritos.
   - Desoclusión completa de micrófonos, manos, vasos, gafas y pelo en primer plano.
7. **Estabilizador Temporal Inter-Frame de Parches (`--no-stabilize-patch` para desactivar):**
   - Atenuación de micro-parpadeo y ebullición de texturas GAN (*GAN shimmer*) en un $60\%$ en áreas cutáneas estáticas mediante diferencia SIMD NEON.
   - Modulación adaptativa sin latencia ni estelas (*zero-ghosting*) en boca, ojos y gestos dinámicos.
8. **Fusión Espectral de Dos Bandas (`--blend two-band`):**
   - Descomposición en frecuencias bajas (irradiancia y tono) y altas (detalle, poros y vello) en espacio canónico $512\times 512$ a $>110\text{ FPS}$.
   - Erradicación total de costuras, saltos de color y halos.
9. **Fusión Multi-Referencia y Selección Adaptativa por Giro Yaw 3D:**
   - Soporte para sintaxis de múltiples fotos con `+` (e.g. `--identity "mitxu_gafas+mitxu_real"`).
   - Cálculo de la Media Fréchet Riemanniana sobre $\mathbb{S}^{511}$ para fotos frontales.
   - Selección adaptativa e interpolación esférica (SLERP) hacia el ángulo más cercano al giro de cabeza ($Yaw$) del metraje.
10. **Rastreador Zero-Drop con Filtros 1-Euro Independientes:**
    - Extrapolación inercial de hasta 2 frames ante desenfoque cinético, previniendo caídas de swap.
    - Instancia de `OneEuroFilter` y `TemporalPatchStabilizer` por cada trayectoria.
11. **Worker Chunking Paralelo (`--workers N`):**
    - Escisión temporal determinista en subprocesos independientes y concatenación $O(1)$ sin recodificación.
12. **Modo Watcher Daemon (`--watch <inbox>`):**
    - Monitorización reactiva autónoma de carpetas locales para procesar vídeos y enlaces en segundo plano.

---

## 4. Uso de la CLI de Producción (V4 SOTA)

```bash
# 1. Render SOTA V4 estándar (GPEN 512 + Two-Band + CoreML BiSeNet + Spatial Lighting + EAR Blink Gate + Anti-Shimmer)
c5-face-swap --video soria.mp4 --identity Mitxu --workers 2

# 2. Fusión Multi-Referencia adaptativa por ángulo 3D
c5-face-swap --video soria.mp4 --identity "mitxu_gafas+mitxu_real" --workers 2

# 3. Intercambio selectivo (sólo el presentador secundario, índice 1)
c5-face-swap --video chiringuito.mp4 --identity Alain --target-face-index 1 --workers 2

# 4. Intercambio múltiple en escena (Pedrerol -> Alain, Soria -> Mitxu)
c5-face-swap --video chiringuito.mp4 --identity "alain,mitxu" --swap-all --workers 2

# 5. Render de Máxima Calidad Cinematográfica (CodeFormer HD a w=0.7)
c5-face-swap --video clip.mp4 --identity Borja --enhancer codeformer --enhance-weight 0.7 --workers 2

# 6. Forzar preservación o sustitución estricta de ojos y boca
c5-face-swap --video clip.mp4 --identity Alain --preserve-mouth true --preserve-eyes true

# 7. Ingesta directa desde enlace web (Instagram / TikTok / YouTube)
c5-face-swap --video "https://www.instagram.com/reel/Dd4MioYDy3E/..." --identity Alain

# 8. Modo Rápido Baseline 128px (sin super-resolución)
c5-face-swap --video clip.mp4 --identity Eder --enhancer none --workers 4

# 9. Modo Watcher Daemon reactivo en segundo plano
c5-face-swap --watch ~/Downloads/c5_inbox/ --identity Alain --workers 2
```

---

## 5. Protocolo de Verificación y Doble Persistencia

1. **Atestación Visual:** Extraer fotograma de control representativo y auditar con `view_file`.
2. **Doble Persistencia Invariante:**
   - Archivo de trabajo: `$PWD/<nombre>_<identidades>_c5swap.mp4`
   - Biblioteca canónica: `/Users/borjafernandezangulo/Movies/VIDEOS_MITICOS/<nombre>_<identidades>_c5swap.mp4`

