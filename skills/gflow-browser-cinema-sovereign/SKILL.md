---
name: gflow-browser-cinema-sovereign
display_name: 'Estudio Cinematográfico Soberano y Automatización Google Flow (v5.0 Apex)'
description: 'Estudio virtual de cine, DAG narrativo, WebSocket bridge, encadenamiento I2V y audio EBU R128. Dispara con "gflow browser", "cine gflow", "flow google mcp", "sovereign cinema", "estudio gflow", "gflow v4", "character anchor veo", "veo 2 browser", "dialogue engine gflow", "cockpit gflow", "remotion gflow".'
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

# Skill: Estudio Cinematográfico Soberano y Automatización Google Flow (v5.0 Apex)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos)
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este protocolo rige la automatización profunda de Google Flow (`flow.google.com`) y Veo en Labs (`labs.google`), la orquestación cinematográfica en DAG mediante WebSocket bridge (:18981), el encadenamiento Image-to-Video continuo inmune a CSP, el diseño acústico EBU R128 resistente a clips mudos, subtitulado lossless `mov_text` y persistencia transaccional con auto-recovery en macOS Apple Silicon.

---

## 1. Arquitectura y Módulos de Silicio (gflow-cli / gflow-browser-mcp v5.0 Apex)

El ecosistema canónico integra el CLI Python (`/Users/borjafernandezangulo/10_PROJECTS/gflow-cli`), el bridge server y la extensión Safari (`safari-gflow-bridge`):

1. **Driver Nativo Safari & WebSocket Bridge (`bridge_server.py`):**
   - Servidor unificado HTTP/WS en puerto `18981` (protocolo websockets 17.2 via `process_request`).
   - Dashboard en vivo (`/dashboard`, `/api/status`, `/api/clips`, `/api/master`) con barra de progreso reactiva.
   - Resolución atómica de eventos de rodaje en bloque `finally` tras cosecha física e indexación.
2. **Secuenciador Cinemático en DAG (`cinema_sequencer.py`):**
   - Parser de manifiestos declarativos `movie.toml` (`load_movie_manifest`).
   - Compilación de prompts con inyección de estilo global, ratio y resolución.
   - Encadenamiento continuo Image-to-Video ($I2V$) a través de Data URIs Base64.
3. **Content Script Reactivo & Bypass CSP (`content.js` / `background.js`):**
   - Decodificación directa en memoria (`dataUriToBlob` via `atob` $\to$ `Uint8Array` $\to$ `Blob` $\to$ `File`) eludiendo la CSP `connect-src` de Google Labs.
   - Despacho DOM redundante sobre `input[type="file"]` y evento sintético `DragEvent('drop')`.
   - Pre-flight linter contra figuras públicas vivas antes del despacho.
4. **Masterización de Audio Broadcast (`audio_master.py`):**
   - Sonda previa `has_audio_stream` con `ffprobe` e inyección de colchón AAC 48 kHz silencioso (`anullsrc`) para clips mudos.
   - Normalización EBU R128 (`loudnorm`) con salvaguarda determinista ante `-inf LUFS` o silencio digital ($\le -70$ LUFS).
   - Mezcla sidechain auto-ducking con bypass inteligente cuando el clip base carece de sonido propio.
5. **Motor de Subtítulos Lossless (`subtitle_engine.py`):**
   - Generación de pistas SRT/ASS e incrustación nativa en flujo `mov_text` (`-c:s mov_text -c:v copy -c:a copy`) en tiempo $O(1)$.
6. **Catálogo Transaccional SQLite (`catalog_indexer.py`):**
   - Identidad canónica UUIDv5 de 36 caracteres derivada de SHA-256 (Invariante B1).
   - Manejo seguro de descriptores con cierre garantizado `store.close()` en `finally`.
7. **Persistencia Transaccional y Auto-Recovery (`CinemaSessionState`):**
   - Checkpoint transaccional en `~/.config/gflow/cinema_state_<manifest>.json`.
   - Reanudación (`resume=True`) sin repetir renders ya cosechados, extrayendo el fotograma final de tomas completadas.

---

## 2. Herramientas MCP Clave (Ecosistema Cinema)

- `gflow_cinema_status`: Consulta del estado actual de rodaje, tomas activas y telemetría de cola.
- `gflow_dashboard_open`: Apertura inmediata del dashboard de producción (`http://localhost:18981/dashboard`).
- `gflow_scene_create` / `gflow_scene_show`: Definición e inspección de escenas cinematográficas.
- `gflow_movie_template`: Generación de manifiestos declarativos `movie.toml` con configuración de tomas y audio.
- `gflow_movie_run`: Despacho y ejecución del secuenciador cinematográfico en segundo plano.
- `gflow_safari_navigate`: Control de navegación y foco de pestaña en Safari.
- `gflow_safari_harvest_media`: Descarga forzada, verificación de `ftyp` e indexación de clips terminados.

---

## 3. Cheatsheet CLI

```bash
# Diagnóstico integral de dependencias (ffmpeg, safari, sqlite, extension)
gflow doctor

# Generar plantilla declarativa de película
gflow cinema template --shots 4 --output movie.toml

# Iniciar servidor WebSocket bridge con dashboard en vivo
gflow cinema bridge --port 18981

# Rodaje completo con reanudación automática ante fallos
gflow cinema run movie.toml --resume

# Masterización de audio EBU R128 y auto-ducking sidechain
gflow cinema audio-master ./clips --soundtrack soundtrack.mp3 --output master.mp4

# Incrustar subtítulos en flujo nativo mov_text (lossless O(1))
gflow cinema burn-subs master.mp4 dialogue.srt master_subbed.mp4
```

---

## 4. Invariante de Pruebas Unitarias FastMCP

Al probar herramientas registradas en servidores FastMCP (`MCPServer`):
- `server.list_tools()` es una corrutina asíncrona.
- Todo test que inspeccione herramientas debe decorarse obligatoriamente con `@pytest.mark.asyncio` y usar `await server.list_tools()`.

---

## 5. Protocolo de Enlace WebSocket Bridge & Extensión Safari (:18981)

1. **Topología de Puertos y Protocolo:**
   - El puente escucha en `http://127.0.0.1:18981` y `ws://127.0.0.1:18981`.
   - La extensión Safari (`background.js`) mantiene reconexión exponencial con `MAX_RECONNECT_ATTEMPTS=5`.
2. **Cero Condición de Carrera en Despacho de Eventos:**
   - La llegada de `GENERATION_COMPLETED` desde Safari solo notifica la finalización en el navegador.
   - El `asyncio.Future` del secuenciador **NUNCA** debe resolverse inmediatamente tras recibir el mensaje.
   - Se debe ejecutar primero la descarga física del MP4, su verificación de integridad de cabecera (`ftyp`) y su inserción en `catalog.db`.
   - La resolución del `Future` con la ruta del clip verificado debe encapsularse en un bloque `finally` tras la cosecha.

---

## 6. Invariantes de Encadenamiento I2V y Bypass CSP en Silicio

1. **Prohibición de Rutas `file://` en Navegador:**
   - Las páginas en `https://labs.google` ejecutan en sandbox estricto; el DOM no tiene acceso a rutas POSIX locales (`/Users/.../frame.png`).
   - El último fotograma extraído debe codificarse obligatoriamente en Data URI Base64 (`encode_frame_as_data_uri`).
2. **Bypass de CSP `connect-src` en Content Script:**
   - Queda estrictamente prohibido invocar `fetch(dataUri)` dentro de `content.js` al violar la CSP de Google Labs.
   - Se debe realizar decodificación pura en memoria: `atob(base64)` $\to$ volcado a `Uint8Array` $\to$ creación de `Blob` $\to$ envoltura en `File(['image/png'])`.
3. **Inyección DOM Redundante:**
   - El objeto `File` generado se asigna a `input[type="file"]` mediante `DataTransfer.items.add(file)`.
   - Se despacha simultáneamente un `DragEvent('drop')` sintético sobre el área de entrada del prompt para asegurar que el framework reactivo de Google Flow monte la imagen de referencia sin interacción manual.

---

## 7. Estándar Acústico Broadcast EBU R128 y Resiliencia ante Clips Mudos

1. **Gestión de Streams Ausentes:**
   - Veo genera con frecuencia vídeos mudos (sin track de audio `0:a`).
   - Antes de cualquier procesamiento con `ffmpeg`, ejecutar sondeo `has_audio_stream`.
   - Si el clip carece de audio, inyectar inmediatamente un canal estéreo silencioso a 48 kHz (`anullsrc`) con `-c:v copy -c:a aac` para garantizar la paridad de streams en el demuxer `concat`.
2. **Guardia contra `-inf LUFS` en Loudnorm:**
   - El filtro `loudnorm=I=-23:LRA=7:TP=-2.0` falla o genera amplificación desmedida de ruido si el audio original es silencio absoluto ($\le -70$ LUFS o `-inf LUFS`).
   - El motor debe verificar la sonoridad integrada y omitir la normalización agresiva sobre pistas mudas.
3. **Auto-Ducking Sidechain Condicional:**
   - En `mix_soundtrack_with_sidechain_ducking`, si el vídeo ensamblado es completamente mudo, se hace bypass de la compresión sidechain y se remuxe la banda sonora directamente con corte limpio al final del metraje (`-shortest`).

---

## 8. Subtítulos Nativos mov_text y Auto-Recovery Transaccional

1. **Incrustación Lossless `mov_text`:**
   - En entornos macOS donde `ffmpeg` carece de soporte para filtros gráficos complejos (`libass`), incrustar los subtítulos como stream nativo 3GPP Timed Text:
     ```bash
     ffmpeg -y -i input.mp4 -i subtitles.srt -c:v copy -c:a copy -c:s mov_text output.mp4
     ```
   - Operación en tiempo $O(1)$ sin pérdida generacional de vídeo ni calentamiento de silicio, plenamente compatible con QuickTime y reproductores de Apple.
2. **Recuperación Transaccional de Rodaje (`resume=True`):**
   - El estado de rodaje se sincroniza atómicamente en `~/.config/gflow/cinema_state_<manifest>.json`.
   - Si el proceso se interrumpe (caída de red, recarga de pestaña o interrupción por el usuario), `gflow cinema run --resume` verifica los clips existentes en disco.
   - Las tomas ya completadas se saltan; si la toma siguiente requiere encadenamiento I2V, se extrae el fotograma final del clip previo ya descargado, reanudando la producción sin pérdida de presupuesto ni cuotas.

---

## 9. Invariante de Ejecución en la Sombra (Background Execution & Dock Invariant)

El subagente Safari (`gflow_safari_*`) opera mediante AppleScript nativo (`do JavaScript in targetTab`):

1. **Cero robo de foco:** Puede generar vídeos, interactuar con modales y cosechar medios en segundo plano mientras el operador trabaja en su IDE o terminal.
2. **Topología de ventanas:** Safari puede residir oculto detrás de ventanas de desarrollo o confinado en un **Espacio virtual secundario (Space)** de Mission Control.
3. **Veto a la Minimización en Dock (`Cmd+M`):** En macOS, miniaturizar la ventana al Dock provoca que WebKit suspenda los temporizadores de la SPA y colapse las coordenadas geométricas del DOM (`getBoundingClientRect()` a `0x0`), rompiendo la detección de elementos y Set-of-Marks. La ventana debe permanecer restaurada, aunque esté tapada o fuera del viewport activo.
4. **Restricción de Capturas:** `gflow_safari_screenshot` utiliza `screencapture -R` en coordenadas de pantalla. Si Safari está cubierto, capturará las capas superiores. La inspección lógica y el rodaje no dependen de capturas y operan con normalidad en la sombra.

---

## 10. Falsación Empírica del Modo API Directa en macOS (Chrome Keychain / Playwright)

En macOS, invocar los endpoints directos de `gflow-cli` (`gflow video t2v`, `gflow_generate_video`) incurre en dos cuellos de botella:
1. **Cifrado Keychain de Chrome:** La base de datos SQLite de cookies de Google Chrome está cifrada mediante claves del Llavero del sistema. Si la extracción en frío falla, el cliente realiza un fallback degradante levantando Google Chrome vía Playwright, consumiendo cientos de megabytes de RAM.
2. **Desacoplamiento de Sesión Labs/Flow:** Google migró la autenticación a `flow.google.com`, dejando sin token los endpoints heredados de `labs.google` (`AisandboxAuthError`).

**Directiva de Alta Exergía:** Priorizar siempre el motor **Safari JXA**, el cual reutiliza la sesión autenticada viva en el sustrato nativo de Apple Silicon a coste termodinámico casi nulo.

---

## 11. Protocolo de Despliegue y Sincronización en Caliente de FastMCP

Al introducir nuevas herramientas en el servidor FastMCP (`gflow_cli.mcp.tools` / `server.list_tools()`):
1. **Sincronización de Schemas:** Volcar los esquemas JSON de las herramientas a `~/.gemini/antigravity/mcp/gflow/<toolName>.json`.
2. **Purga de Procesos:** Terminar el proceso `gflow mcp run` previo (`kill <PID>`) para liberar el entorno de ejecución en memoria.
3. **Reconexión de Canal:** En Antigravity, pulsar **... > MCP Servers > gflow > Reload / Reconnect** o recargar la ventana (`Cmd+Shift+P` > *Developer: Reload Window*).

---

## 12. Protocolo de Transporte Wire Directo (Anillo-0 / Batchexecute)

Para ejecución masiva, pipelines desasistidos y sondeos de ultra-baja latencia sin sobrecarga de Chromium/Playwright:

1. **Extracción Pasiva de Sesión Safari (JXA / Apple Events):**
   - Extracción de cookies en tiempo real mediante `osascript` sobre la pestaña activa de `flow.google.com` en $<15\text{ ms}$.
   - Bypass del cifrado `v10` de macOS Keychain que bloquea la lectura directa de bases de datos SQLite en disco de Chromium.
   - Cálculo de token de cabecera First-Party:
     $$\text{SAPISIDHASH} = \text{timestamp} + \text{"\_"} + \text{SHA1}(\text{timestamp} + \text{" "} + \text{SAPISID} + \text{" "} + \text{origin})$$

2. **Matriz de RPCs Canónicos (`POST /data/batchexecute?rpcids=...`):**
   - `YhhmEf`: Despacho de vídeo Text-to-Video (T2V) e Image-to-Video (I2V).
   - `jwpduf`: Sondeo adaptativo de estado de generación (polling cada 5 s con jitter $\pm 15\%$).
   - `as29s`: Evento terminal de resolución; entrega URLs firmadas de CDN de Google para MP4 y poster.
   - `ogiZ0b`: Generación síncrona de imágenes (Imagen 3).

3. **Envelope Anti-XSSI y Registro Canónico CAE:**
   - La respuesta del servidor suprime el prefijo `)]}'` antes de la deserialización de bloques `["wrb.fr", "<rpcid>", "<json_string>"]`.
   - Localización estructural del registro de 8 tuplas:
     $$\mathcal{R}_{\text{CAE}} = \langle \text{workflow\_id}, \text{project\_id}, \text{media\_id}, \text{"CAE"}, \text{null}, \text{DETAILS}, \text{null}, \text{MEDIA\_INFO} \rangle$$
   - `DETAILS[8][0]`: Estado numérico ($6 = \text{Submitted}$, $2 = \text{Running}$, $3 = \text{Done}$).
   - `DETAILS[10]`: URL firmada del poster JPEG.
   - `DETAILS[13]`: Tamaño en bytes del vídeo.
   - `MEDIA_INFO[0][8]`: URL de descarga directa del MP4.

4. **Gobernanza de Cuota y Débito Atómico:**
   - En el tier **ULTRA** (`borjamoskv@gmail.com`), la base de cómputo parte de 10.000 puntos con ciclo de recarga periódica.
   - El cobro formal (~10-20 pts en Veo Fast) es estrictamente atómico y condicionado a la llegada exitosa a estado $3$ (`Done`). Renders cancelados, filtrados o con error de backend no descuentan puntos ($0$ coste de fallo).

