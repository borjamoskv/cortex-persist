---
name: c5-neural-face-swap-cuadrilla
display_name: "Pipeline Neural Face-Swap Cuadrilla (V5 SOTA Hybrid)"
description: "Pipeline industrial de alta velocidad para intercambio facial neuronal (deepfake) en vídeos reales o virales con identidades de la cuadrilla sobre Apple Silicon M-Series. Motor V5 SOTA con inyección de grano de sensor de cámara (Poisson-Gaussian matching), super-resolución adaptativa consciente de escala, exportación nativa vertical 9:16 con Pan & Scan dinámico, alineación de mirada orgánica (gaze alignment), BiSeNet en CoreML, transferencia de iluminación espacial 3D y codificación por hardware VideoToolbox."
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
> - **Modo de Acceso a Worktree:** `read-write` (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos)
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
  `/tmp/inswapper_128.onnx` / `~/.insightface/models/inswapper_128_fp16.onnx`
* **Directorio de Rostros Fuente:**
  `/Users/borjafernandezangulo/Downloads/VIDEO BODA HUGO/faces/<personaje>_real.png`
* **Directorio Canónico de Salida:**
  `~/Movies/VIDEOS_MITICOS/<TITULO>.mp4` (con copia en el workspace activo si aplica).

---

## 2. Roster Canónico de Identidades (17 Miembros + Invitados)

| Personaje / Alias | Archivo Fuente Canónico |
| :--- | :--- |
| **Alain** (Elektronische / Elektrocaniche) | `faces/alain_real.png` |
| **Eder** (Dual Sound / Balcón de la LOLA) | `faces/eder_real.png` |
| **Luengo** (Tigre Máquina) | `faces/luengo_real.png` |
| **Xabi** (Cabeza Gigante / Moñas) | `faces/xabi_real.png` |
| **Borja** (Moskv) | `faces/borja_real.png` |
| **Hugo** (Hugo Pink / El Novio) | `faces/hugo_real.png` / `hugo_pink_real.png` |
| **Mitxu** (El Mitxus / Mitxu Gafas) | `faces/mitxu_gafas_tecnicas.jpg` / `faces/mitxu_real.png` |
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

## 3. Arquitectura del Motor V5 SOTA (`c5-face-swap`)

1. **Inyección de Grano de Sensor y Ruido de Cámara (`--grain 0.5`):**
   - Estimación robusta de la varianza residual de alta frecuencia ($\sigma_{\text{sensor}}$) del fotograma objetivo.
   - Síntesis de ruido Poisson-Gaussian correlacionado por canal BGR, modulado según la curva de luminancia de tonos medios de piel.
   - **Erradicación definitiva de la "piel de cera / plástico digital GAN"**, mimetizando la textura analógica del broadcast o sensor móvil.
2. **Super-Resolución Adaptativa Consciente de Escala (`--enhancer adaptive`):**
   - Análisis métrico del tamaño del rostro objetivo: si $\text{bbox}_{\text{height}} < 140\text{ px}$ (planos generales/medios), omite el GAN y aplica afilado CAS sub-milisegundo ($<0{,}1\text{ ms}$), acelerando la velocidad hasta $10\times$.
   - Si $\text{bbox}_{\text{height}} \ge 140\text{ px}$ (primeros planos), despacha la reconstrucción completa GPEN 512 con respaldo determinista en CPU multi-hilo (4 threads).
   - Respaldo de tolerancia a fallos (*fault-tolerant fallback*): si la sesión neural sufre cualquier excepción por frame corrupto, commuta transparentemente a CAS sharpening sin interrumpir el render.
3. **Exportación Nativa en Formato Vertical 9:16 (`--format 9:16` / `--format both`):**
   - Motor `VerticalFramingTracker` integrado con filtro 1-Euro y deadband dinámico.
   - Genera automáticamente versiones verticales a $1080\times 1920$ listas para Instagram Reels, TikTok, YouTube Shorts y Estados de WhatsApp.
   - `--vertical-bg crop` (por defecto): Pan & Scan inteligente siguiendo suavemente al protagonista.
   - `--vertical-bg blur`: fondo panorámico ampliado y desenfocado con el orador centrado.
   - `--format both`: produce simultáneamente el master 16:9 y el reel vertical 9:16 en un único pase.
4. **Preservación de Mirada Viva y Párpados (`--preserve-eyes gaze` / `--preserve-eyes auto`):**
   - `--preserve-eyes gaze`: excluye suavemente el globo ocular (iris, pupila, esclera) con difuminado gaussiano $11\times 11$, transfiriendo al swap la dirección exacta de la mirada, micro-sacadas y destellos especulares del actor real.
   - `--preserve-eyes auto`: compuerta por métrica EAR ($EAR < 0.18$) para parpadeo y cierre ocular natural.
5. **Aceleración CoreML en Segmentación BiSeNet:**
   - Despacho al Apple Neural Engine (ANE) con latencia de **$19{,}4\text{ ms}$** vs $284\text{ ms}$ en CPU ($14{,}6\times$ speedup).
6. **Transferencia de Iluminación Espacial 3D y Sombras (`--lighting spatial`):**
   - Extrae el gradiente lumínico ambiental del metraje y modula la irradiancia del rostro 3D, fusionando brillos y sombras sin aplastar poros.
7. **Estabilizador Temporal de Parches (`--no-stabilize-patch` para desactivar):**
   - Algoritmo de diferencia temporal acelerado por SIMD NEON que suprime el parpadeo de micro-texturas (*GAN shimmer*) manteniendo respuesta instantánea en expresiones dinámicas.
8. **Fusión Espectral de Dos Bandas (`--blend two-band`):**
   - Descomposición en frecuencias bajas (irradiancia y tono) y altas (detalle, poros y vello) en espacio canónico $512\times 512$ a $>110\text{ FPS}$.
9. **Fusión Multi-Referencia y Selección Adaptativa por Giro Yaw 3D:**
   - Sintaxis multi-foto con `+` (e.g. `--identity "mitxu_gafas+mitxu_real"`).
   - Cálculo de la Media Fréchet Riemanniana sobre $\mathbb{S}^{511}$ para fotos frontales e interpolación esférica (SLERP) según el ángulo $Yaw$ de la cabeza.
10. **Rastreador Zero-Drop con Filtros 1-Euro Independientes:**
    - Extrapolación inercial de hasta 2 frames ante desenfoque cinético, previniendo caídas de swap.
11. **Codificación Acelerada por Hardware Apple Silicon VideoToolbox:**
    - Salida H.264 / HEVC a 8.5 Mbps con filtros `cas=strength=0.6,unsharp=5:5:0.7:5:5:0.3`.

---

## 4. Uso de la CLI de Producción (V5 SOTA)

```bash
# 1. Render SOTA V5 estándar (Adaptive 512p + Sensor Grain + CoreML BiSeNet + Spatial Lighting + Gaze + Two-Band)
c5-face-swap --video soria.mp4 --identity Mitxu --workers 2

# 2. Generación simultánea de Master 16:9 y Reel Vertical 9:16 para TikTok / Reels
c5-face-swap --video soria.mp4 --identity "mitxu_gafas+mitxu_real" --format both --workers 2

# 3. Reel vertical exclusivo 9:16 (1080x1920) con Pan & Scan dinámico
c5-face-swap --video clip.mp4 --identity Alain --format 9:16 --vertical-bg crop --workers 2

# 4. Ajuste de intensidad de grano de sensor (e.g. metraje analógico o vintage)
c5-face-swap --video archivo.mp4 --identity Alain --grain 0.75 --workers 2

# 5. Alineación orgánica de la mirada viva original del actor
c5-face-swap --video debate.mp4 --identity Borja --preserve-eyes gaze --workers 2

# 6. Intercambio múltiple en escena (Pedrerol -> Alain, Soria -> Mitxu)
c5-face-swap --video chiringuito.mp4 --identity "alain,mitxu" --swap-all --workers 2

# 7. Render de Máxima Calidad Cinematográfica (CodeFormer HD a w=0.7)
c5-face-swap --video clip.mp4 --identity Borja --enhancer codeformer --enhance-weight 0.7 --workers 2

# 8. Ingesta directa desde enlace web (Instagram / TikTok / YouTube)
c5-face-swap --video "https://www.instagram.com/reel/Dd4MioYDy3E/..." --identity Alain

# 9. Modo Watcher Daemon reactivo en segundo plano
c5-face-swap --watch ~/Downloads/c5_inbox/ --identity Alain --workers 2
```

---

## 5. Protocolo de Verificación y Doble Persistencia

1. **Atestación Visual:** Extraer fotograma de control representativo y auditar con `view_file`.
2. **Doble Persistencia Invariante:**
   - Archivo de trabajo: `$PWD/<nombre>_<identidades>_c5swap.mp4`
   - Biblioteca canónica: `/Users/borjafernandezangulo/Movies/VIDEOS_MITICOS/<nombre>_<identidades>_c5swap.mp4`
   - Versión vertical si aplica: `..._vertical_916.mp4` en ambas ubicaciones.
