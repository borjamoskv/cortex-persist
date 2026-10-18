---
name: c5_audiovisual_render_exergy_invariant
description: Invariante C5-REAL de exergía de renderizado en hipervisores multi-superficie (MOSKV-1). Enforce caché BLAKE3, mutex flock de cola única, modo dual borrador/final y SiliconMediaGate (ebur128/ffprobe).
trigger: "model_decision"
---

# Invariante de Exergía de Renderizado Audiovisual en Hipervisores Multi-Superficie (INV_C5_RENDER_EXERGY)

## 1. Axioma Fundamental
$$\hat{\Phi}_{\text{render}} = \frac{U_i \cdot \mathbf{1}[\operatorname{VerifiedOutcome}_i]}{C_{\mathrm{inf}} + \lambda_t T + \lambda_h H + \lambda_r R}$$
1. **El render más barato es el que no se hace:** Si los parámetros causales no mutan, el renderizado es redundante ($O(1)$ en caché de contenido).
2. **Un render no verificado vale 0:** Por rápido o libre de errores que finalice el proceso, si no supera el test en silicio, su exergía es idénticamente nula ($\Phi = 0$).

## 2. Las 4 Palancas Operativas Invariantes

### Palanca 1: Caché Direccionada por Contenido (`BLAKE3`)
- Todo trabajo de renderizado audiovisual (Remotion, ffmpeg, DSP de síntesis) DEBE calcular el digest canónico `BLAKE3` (o SHA-256 en fallback) de sus entradas:
  $$\text{ManifestHash} = \operatorname{BLAKE3}(\text{código\_composición} \parallel \text{props\_canónicos} \parallel \text{audio\_master} \parallel \text{toolchain} \parallel \text{tier})$$
- Si el hash ya cuenta con un artefacto y un recibo inmutable con `verified = True` en `~/.babylon60/render_cache/`, el motor DEBE devolver el archivo directamente en $O(1)$ sin invocar el runtime de renderizado ($\hat{\Phi} = 21.000$).

### Palanca 2: Mutex Global de Cola Única (`SingleRenderQueueMutex`)
- En entornos coordinados por MOSKV-1 (13 IDEs/CLIs coexistiendo sobre la misma máquina), los renders pesados no pueden ejecutarse concurrentemente.
- Es obligatorio adquirir un cerrojo exclusivo inter-proceso (`fcntl.flock` sobre `/tmp/moskv1_render_queue.lock`) antes de iniciar `npx remotion render` o transcodificaciones masivas. Un único trabajo a la vez usando los núcleos P asignados para evitar contención de CPU y la aparición de *swap* en memoria unificada (18 GB en M3 Pro).

### Palanca 3: Modo Dual Borrador / Final (Validación de Bloque)
- No se optimiza el workflow completo sin validar el bloque:
  - **Nivel Borrador (`--draft`):** Iteración visual rápida con `--scale=0.5`, decodificación/codificación hardware (`VideoToolbox` en Apple Silicon) y renderizado de frames parciales.
  - **Nivel Final (`--final`):** Masterización definitiva con codec de alta compresión por bit (`libx264`/`libx265`), concurrencia acotada a núcleos P físicos y multiplexado de audio estéreo con fase certificada.

### Palanca 4: Gate de Silicio Pre-Humano (`SiliconMediaGate`)
- Queda terminantemente prohibido entregar un archivo de vídeo o audio al operador biológico sin verificación física automatizada:
  - **Audio:** Medición EBU R128 (`ebur128=peak=true` en ffmpeg). El audio debe satisfacer $-45.0 \le I \le -5.0\text{ LUFS}$ y $TP \le -0.1\text{ dBTP}$ (cero clipping).
  - **Vídeo:** Prospección determinista con `ffprobe` validando geometría ($W, H > 0$), presencia de stream de vídeo activo y ausencia de frames corruptos.
  - Si el gate falla: el archivo provisional se elimina físicamente de disco y la tarea aborta en `Fail-Closed` con $\Phi = 0$.
