---
name: youtube-remotion-sota
display_name: Síntesis Programática SOTA de Vídeo React/Remotion
description: Renderizado programático de vídeo SOTA utilizando React y Remotion engine. Dispara con "youtube remotion", "remotion render", "react video synthesis", "renderizar vídeo remotion".
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

# Habilidad SOTA: Generación y Animación Programática de Vídeo con Remotion (React Video Engine)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Esta habilidad rige el diseño, arquitectura, composición e invoice de motores de vídeo programáticos utilizando **Remotion** (React para vídeo) en el ecosistema macOS.

## 🎯 Criterios de Activación
- Solicitudes de creación de plantillas de vídeo animadas en React / TypeScript.
- Renderizado programático mediante CLI (`npx remotion render`, `remotion lambda`, `remotion studio`).
- Animaciones basadas en frames (`useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`).
- Integración de audio sincrónico, subtítulos dinámicos o capas de datos JSON en vídeo.

---

## 🛠️ Protocolo de Ejecución en 4 Fases

### Fase 1: Ingesta y Verificación del Entorno Remotion
1. **Verificar Dependencias:** Comprobar existencia de `node`, `npm` y paquete `remotion` en el directorio de trabajo.
2. **Estructura del Proyecto:** Asegurar la presencia de:
   - `src/Root.tsx`: Registro de composiciones (`<Composition />`).
   - `src/Composition.tsx`: Componente visual principal.
   - `remotion.config.ts`: Configuración de renderizado (fps, codec, concurrencia).

### Fase 2: Desarrollo de Composiciones (Invariantes React/Remotion)
1. **Paso del Tiempo Basado en Frames:** NUNCA usar `setTimeout` o `setInterval`. Toda animación debe derivar de `useCurrentFrame()` y `useVideoConfig()`.
2. **Interpolaciones Suaves:** Usar `interpolate(frame, [start, end], [valA, valB], { extrapolateRight: 'clamp' })` o animaciones físicas mediante `spring({ frame, fps, config })`.
3. **Gestión de Recursos Multimedia:**
   - Usar `<Img src={staticFile("image.png")} />` y `<Audio src={staticFile("audio.mp3")} />` para activos estáticos.
   - Para secuencias de audio o vídeo dinámicas, usar `<Sequence from={startFrame} durationInFrames={length}>`.

### Fase 3: Invariantes de Calidad y Rendimiento SOTA
- **Resoluciones Estándar:** 1920x1080 (Horizontal / YouTube), 1080x1920 (Vertical / Shorts / Reels).
- **Framerate:** 30fps o 60fps estables.
- **Audio Timing:** Sincronización milimétrica con forma de onda usando metadatos JSON.

### Fase 4: Invariantes de Realismo Cinemático SOTA (YouTube High Retention)
1. **Cero Partículas Estroboscópicas / Neón Psicodélico:** Salvo petición explícita, PROHIBIDO incluir partículas flotantes aleatorias o bucles de luces parpadeantes.
2. **Fondos y Entornos Reales:** Usar fotografía real tratada con contraste (`1.15-1.20`), viñeteado ambiental y desenfoque de profundidad de campo (`blur(2-3px)`).
3. **Sombras de Caída Naturales:** Aplicar `drop-shadow(0 35px 60px rgba(0,0,0,0.92))` sobre avatares y elementos superpuestos para integrarlos de forma orgánica.
4. **Cámara de Retención Dinámica (60 FPS Push-in):** Aplicar interpolación lenta `interpolate(frame, [0, 1800, 3600], [1.0, 1.06, 1.02])` a 60 FPS para mantener la retención de audiencia en YouTube.
5. **Soporte Dual Panorámico / Shorts:** Diseñar composiciones adaptativas que respondan a la relación de aspecto (1920x1080 Landscape y 1080x1920 Shorts).
6. **Subtítulos Cinéticos & Marca de Agua TV:** Incluir insignias de emisión (`4K ULTRA HD 60FPS`) y banners de estudio con indicador de directo en vivo.
7. **Invariante de Animación Flap-Mouth (South Park Style):**
   - **Cerrojo de Z-Index y Contexto de Apilamiento:** Al aplicar `filter: drop-shadow(...)` a la cabeza dividida (`_top.png` y `_jaw.png`), CSS genera un nuevo contexto de apilamiento. La cabeza DEBE definir explícitamente `zIndex: 10`, mientras que el torso/cuerpo subsiguiente declara `zIndex: 1`.
   - **Calibración de Margen:** Fijar `marginTop: -25px` en el cuerpo (anclado a la barbilla/cuello) en vez de `-60px` para prevenir que la chaqueta se superponga sobre la mandíbula inferior, el mentón o accesorios (como cigarrillos).
   - **Cavidad Bucal Oscura:** Incluir un elemento oval (`backgroundColor: '#1a0505'`, `zIndex: 0`) tras ambas capas para que, al elevarse `_top.png` (`top: -flapGap`), se visualice el interior de la boca y no el fondo escénico.

### Fase 5: Renderizado y Entrega de Salida (Invariante macOS QuickTime / Safari)
1. **Vista Previa:** Ofrecer comando para previsualización local:
   ```bash
   npx remotion render src/index.ts <CompositionId> out/video.mp4 --codec=h264 --pixel-format=yuv420p
   ```
2. **Directorio de Ejecución Obligatorio (CWD):** Ejecutar el CLI `remotion render` SIEMPRE dentro del directorio raíz del subproyecto donde residen `package.json` y `node_modules` (ej: `video-engine/`).
3. **Formato de Píxeles Obligatorio:** Incluir SIEMPRE `--pixel-format=yuv420p` en renderizados H.264 para garantizar compatibilidad con macOS QuickLook, QuickTime Player y navegadores Safari/Chromium.
4. **Verificación del Output:** Comprobar la existencia del archivo `.mp4` y verificar su reproducción con `ffprobe` / QuickLook.

---

### Fase 6: Pipeline de Larga Duración por Chunks Paralelos y Telemetría Relacional (>10-20 Minutos / >18.000 Frames)

Cuando una composición supera los 5-10 minutos (ej. podcast o vídeo de 20 minutos / 36.000 frames), el renderizado monolítico lineal resulta inviable. Se debe aplicar el siguiente protocolo de alta exergía:

1. **Compresión Relacional de Telemetría JSON (Reducción 85%+):**
   - Queda prohibido duplicar metadatos textuales (`text`, `speaker`, `badge`, `slide`) en cada objeto de frame.
   - Separar el JSON en dos capas:
     - `scenes: [...]`: Tabla de escenas (120 objetos con texto, nombres, slides).
     - `frames: [...]`: Array plano donde cada frame solo almacena valores numéricos redondeados (`r`: RMS, `g`: flapGap, `t`: isTalking flag, `b`: 8 bandas de ecualizador).
   - Esto comprime el JSON de ~20 MB a ~2.8 MB, permitiendo que Webpack empaquete el bundle en < 1 segundo sin riesgo de OOM.

2. **Particionado en Chunks Deterministas:**
   - Dividir los fotogramas en bloques uniformes (ej. 12 chunks de 3.000 frames = 100s por chunk).
   - Renderizar cada bloque a un archivo aislado en `/tmp/chunks/chunk_N.mp4`.

3. **Orquestación Multi-Worker Concurrente en Python:**
   - Utilizar `ProcessPoolExecutor(max_workers=3..4)` sobre Apple Silicon (M3 Pro / Max).
   - Parámetros CLI de Remotion obligatorios por chunk:
     `npx remotion render src/index.ts <CompositionId> /tmp/chunks/chunk_N.mp4 --frames=START-END --concurrency=4 --gl=angle`
   - Comprobación idempotente: si el archivo de chunk ya existe y supera el umbral de tamaño (>10 MB), se salta automáticamente.

4. **Concatenación Lossless y Muxing de Audio Master (Cero Desincronización ni Pops):**
   - Ensamblar los chunks de vídeo mediante demuxer de texto en FFmpeg sin transcodificación:
     `ffmpeg -y -f concat -safe 0 -i chunks_list.txt -c:v copy -an /tmp/video_stream.mp4`
   - Muxear el flujo de vídeo resultante con el archivo máster de audio (.wav o .mp3 a 320k):
     `ffmpeg -y -i /tmp/video_stream.mp4 -i audio_master.wav -c:v copy -c:a aac -b:a 320k -shortest /Users/borjafernandezangulo/Music/<Final_Video>.mp4`
   - Este paso toma apenas 2-3 segundos y garantiza 0,00 ms de desfase audiovisual a lo largo de los 20 minutos completos.

---

### Fase 7: Arquitectura de Animación para Podcasts Dinámicos de Alta Retención (Protocolo Landpark / Satírico)

Para animaciones de podcast cómico o satírico (estilo South Park / Landpark), queda prohibido el estatismo escénico. Se debe implementar la siguiente arquitectura modular:

1. **Sincronización por Timeline JSON Desacoplado:**
   - Generar un archivo `timeline.json` con los timestamps exactos (`start`, `end`, `duration`) de cada clip de voz generado.
   - En el componente Remotion, mapear los eventos para que los estados de habla, cámara y efectos visuales se sincronicen dinámicamente sin fotogramas fijos hardcodeados.

2. **Cutaway Posters Ilustrados (1920x1080) en PIP:**
   - Diseñar e insertar un póster satírico ilustrado por cada anécdota, gag o concepto bizarro clave (mínimo 1 por intervención relevante).
   - Composición en Picture-in-Picture (PIP) con entrada suave vía `spring()`, rotación sutil (`-2.5deg` a `+2.5deg`), sombra de profundidad (`boxShadow: '0 25px 50px rgba(0,0,0,0.8)'`) y marco contrastado de 4-6 px.

3. **Breakers Tipográficos de Impacto:**
   - Insertar transiciones de pantalla completa (10 a 20 frames) con tipografía ultra-condensada en mayúsculas, fondo contrastado (rojo/amarillo/negro), micro-sacudida (`shake`) y escala elástica (`spring()`) cuando un personaje formule una tesis absurda o meme clave.

4. **Stickers de Onomatopeyas Pop/Cómic:**
   - Ubicar insignias flotantes rotadas (`CLACK!`, `ZASCA!`, `CHOF!`, `BRRR!`, `ÑIIIC!`) en las transiciones de diálogo para acentuar el ritmo del cómic.

5. **Cámara con Seguimiento Suave:**
   - La cámara debe reencuadrar dinámicamente (`transform: scale(...) translate(...)`) al personaje activo con interpolación suave (`damping: 15`).

---

### Fase 8: Invariante de Compresión para Previsualización en IDE (< 20 MB)

- **Restricción de Entorno:** El visor multimedia del IDE Antigravity / Chromium colapsa o rechaza reproducir vídeos que superen los **20.0 MB**.
- **Protocolo de Compresión Obligatorio en FFmpeg:**
  Tras renderizar el master crudo con Remotion, es mandatario ejecutar una compresión H.264/AAC con bitrate acotado:
  ```bash
  ffmpeg -y -i /tmp/video_raw.mp4 \
    -c:v libx264 -b:v 750k -maxrate 1100k -bufsize 2000k -preset slow \
    -c:a aac -b:a 128k -movflags +faststart \
    /Users/borjafernandezangulo/Music/<Nombre_Video>_Master.mp4
  ```
- **Verificación:** Ejecutar `ls -lh` sobre el destino. Si el tamaño excede 20 MB, re-comprimir con `-b:v 600k`. Eliminar el archivo `.mp4` crudo temporal tras verificar.
