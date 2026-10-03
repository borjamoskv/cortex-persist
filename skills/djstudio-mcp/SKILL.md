---
name: djstudio-mcp
display_name: Controlador DSP & Playlist Mixer DJ.Studio MCP
description: Protocolo de integración nativa MCP con DJ.Studio y DJ.Studio Next, análisis armónico Camelot (0-23 a 1A-12B), optimización combinatoria Harmonize (TSP / recocido simulado), inferencia en silicio (Demucs v4 TorchScript MPS + MDX-Net CoreML, 7-Fold beatgrid), ingeniería inversa de formatos binarios (audioView Float32, compressedAudioView struct 8-bytes), semántica de cue points (type 0 vs 5), protocolo de memoria compartida POSIX (/dev/shm), DSP de audio shaders, física psicoacústica de transición (Plomp-Levelt/Sethares, 24 bandas Bark Zwicker), motor DSP V2 de transiciones continuas (Crossover Linkwitz-Riley LR4 24 dB/oct, Zero-Overlap Bass Swap en beat 1.1, dip de medios -1.2 dB, Space Echo Dub Tail 3/16), taxonomía de las 8 transiciones de club y serialización dual Ableton Live (.als) y Pioneer Rekordbox XML (DJ_PLAYLISTS 1.0.0). Dispara con "dj studio", "djstudio", "dj studio mcp", "dj studio bin", "audioview dj studio", "ingenieria inversa dj studio", "shared memory dj studio",
  "dj studio next", "harmonize dj studio", "stems dj studio", "dj studio ai", "transiciones dj", "crossover linkwitz riley", "zero overlap bass swap", "rekordbox xml", "dub echo transition", "setlist techno gemas".
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

# Protocolo DJ.Studio MCP & Arquitecto de Mezcla Armónica (C5-REAL)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este protocolo rige la interacción programática, agéntica e ingeniería inversa con el motor de **DJ.Studio** y **DJ.Studio Next** instalado en macOS (`/Applications/DJ.Studio.app` y `/Applications/DJ.Studio Next.app`), operando directamente sobre su sustrato de almacenamiento en `~/Music/DJ.Studio/`.

---

## 1. Topología del Sistema y Archivos de Base de Datos

* **Aplicación:** `/Applications/DJ.Studio.app` (v3) y `/Applications/DJ.Studio Next.app` (v4).
* **Directorio Raíz Canónico:** `~/Music/DJ.Studio/`
* **Base de Datos SQLite:** `~/Music/DJ.Studio/Database/studio.db`
  - Tabla `Tracks`: Metadatos ID3, BPM, clave armónica entera, ruta de archivo.
  - Tablas `Playlists` y `PlaylistTracks`: Listas de reproducción y secuencias.
* **Tablas Particionadas JSON:**
  - `projects-meta-table/`: Metadatos de proyectos (nombre, duración, pistas).
  - `projects-table/`: Grafo completo de la mezcla (transiciones, VSTs, automatizaciones).
  - `audio-library-table/`: Análisis acústico profundo shardeado (`energy`, `danceability`, `beatgrid`, `stems`).
  - `mix-data-table/`: Cuantización de beats, mapeo de transiciones y matriz `mixMap`.
  - `automation-data-table/`: Curvas paramétricas por pista (`bpm`, volumen, ecualización).
  - `video-settings-table/`: Ajustes de renderizado visual y shaders reactivos.
* **Almacenamiento Físico Binario (BIN):**
  - `audio-library-audioView/`: Waveform cruda en Float32 de alta resolución temporal.
  - `audio-library-compressedAudioView/`: Waveform compacta multicanal (relación 16:1).
  - `audio-library-compressedAudioViewInstrumentalHQ/` y `...VocalsHQ/`: Formatos binarios de stems aislados.
  - `audio-library-audioData/`: Audio decodificado en crudo (RIFF WAVE PCM 16-bit 44.1 kHz).

---

## 2. Arquitectura de Persistencia Binaria (`audioView` & `compressedAudioView`)

### 2.1. `audio-library-audioView` (Onda Continua Float32)
* **Formato:** Flujo escalar contiguo Little-Endian IEEE 754 Float32 (`<f`). Sin cabecera.
* **Tasa de Muestreo Temporal:** Exactamente $1378.125\text{ Hz} = \frac{44100\text{ Hz}}{32\text{ muestras}}$.
* **Régimen de Transferencia:** $1378.125 \times 4\text{ B} = 5512.50\text{ Bytes/segundo}$.
* **Dimensionamiento:** Para duración $T$ segundos, $\text{Bytes} \approx \lfloor T \times 5512.50 \rfloor$.

### 2.2. `audio-library-compressedAudioView` (Onda Compacta Multicanal)
* **Compresión:** Ratio 16:1 en tamaño (submuestreo 1:32 respecto a `audioView`).
* **Cabecera Fija:** 2 Bytes con valor mágico `0xFFFF` (`65535` en uint16 little-endian).
* **Estructura de Registro (8 Bytes por bloque, C-Struct `<hhhh`):**
  ```c
  struct CompressedAudioViewRecord {
      int16_t left_peak;        // 0 a 1000 nominal (0 dBFS = 1000, transitorios > 1000)
      int16_t right_peak;       // 0 a 1000 nominal
      int16_t energy_rms;       // Envolvente RMS / Gravedad de graves
      int16_t spectral_phase;   // Inclinación espectral / Fase (-32768 a +32767)
  };
  ```
* **Tasa Temporal:** $43.0664\text{ Hz} = \frac{44100}{1024}$. Cada bloque representa $23.22\text{ ms}$.
* **Invariante de Tamaño:** $\forall \text{ archivos},\; (\text{FileSize} - 2) \pmod 8 \equiv 0$.
* **Mapeo Cromático:** El campo `spectral_phase` modula el shader WebGPU Canvas para colorear la forma de onda según el balance tricromático (Rojo = Graves 20-250 Hz, Verde = Medios 250-2500 Hz, Azul = Agudos 2.5-22 kHz).

### 2.3. Acceso de Alto Rendimiento en Disco (`DatabaseChannel`)
En `preload.js`, la capa de renderizado no carga archivos enteros en RAM:
* Ejecuta *Range Reads* directos (`fs.open` + `read` de rango $[start, end]$).
* Transfiere los buffers resultantes como *Transferable Objects* vía `MessagePort` sin coste de duplicación.

---

## 3. Protocolo Zero-Copy IPC sobre Memoria Compartida (`/dev/shm`)

El módulo nativo C-ABI `@appmachine/shared-memory` (`shared_memory.node`) gestiona la transferencia masiva de audio entre el proceso Node/Electron y los motores de IA/DSP:

* **Nombres de Región POSIX:** `/dj-studio-${timestamp}`.
* **Vector 4-Stems (Demucs/HTDemucs - Clase `nd`):**
  - Tamaño: $2 \times \text{samplesPerChannel} \times 4 \times 4\text{ bytes} = 32 \times \text{samplesPerChannel}\text{ bytes}$.
  - Canales en orden: `[Drums, Bass, Other, Vocals]`.
* **Vector 2-Stems (MDX-Net - Clase `id`):**
  - Tamaño: $2 \times \text{samplesPerChannel} \times 2 \times 4\text{ bytes} = 16 \times \text{samplesPerChannel}\text{ bytes}$.
  - Canales: `[Vocals, Instrumental]`.
* **Chunking de Separación:** Bloques de 10 segundos ($441.000\text{ muestras}$ por canal, $14.112\text{ MB}$ por chunk en 4-stems). Techo de seguridad en RAM fijado en $2.800\text{ MB}$ ($\approx 198\text{ chunks}$); descarte FIFO de 50 chunks al saturarse.
* **Transducción de Beatgrid (Clase `od`):** Inyecta PCM estéreo en memoria compartida; el motor nativo escribe directamente el JSON de respuesta en el byte 0 de la región compartida (`readString(0)`).

---

## 4. Motor DSP de Audio Shaders (`@appmachine/synth-engine`)

Diseñado por André van Kammen, el motor `CPUSynth` procesa el audio bajo el paradigma de **Audio Shaders**, operando sobre matrices bidimensionales de muestras Float32 (`shdr_EQ`, `shdr_mixdown`, `shdr_EFFECTS`, `shdr_playTrack`).

### 4.1. Mapa Canónico de Controladores (MIDI CC / Automation IDs)
* **Canal & Ganancia:** Volumen `7`, Pan `10`, Pitch `129`, Velocidad/Dirección `140`.
* **Ecualización 3-Bandas:** Graves `106`, Medios `107`, Agudos `108`.
* **Cortes y Factores Q:** Graves Freq `109` / Ancho `110`, Agudos Freq `111` / Ancho `112`.
* **Filtro Campana Paramétrico:** Frecuencia `102`, Ancho `103`, Nivel `104`, Borde `105`.
* **Filtro Pasa-Banda & Resonancia:** Nivel `113`, Resonancia Graves `114`, Resonancia Agudos `115`.
* **Dinámica & Crossfade Espectral:** Compresión multibanda `160-164`, Merge espectral `166`, Sidechain `167`.
* **Efectos:** Bitcrusher `180`, Inyector White Noise `201`, Slicers métricos `1181-1187`.
* **JUCE & VST:** Subcutáneo JUCE `210-214` para hosting de plugins VST3/AU y ruteo CoreAudio.
* **Master:** Limitador brickwall `310`.

### 4.2. Formulación Matemática de Filtros
* **Pasa-Banda Logarítmico:**
  $$f_{\text{norm}} = \frac{\ln(f) - \ln(20)}{\ln(20000) - \ln(20)}$$
  $$H_{\text{pass}}(f) = \left[1.0 - \text{smoothstep}(0.55, 0.65, |f_{\text{norm}} - 0.5 - 1.05 \cdot C_{113}|)\right] \cdot \left[1.0 + \text{smoothstep}(0.5, 0.6, \text{dist}) \cdot R(f)\right]$$
* **Filtro de 3 Bandas:** Interpolación cúbica de Hermite ($\text{smoothstep}(a, b, x) = 3u^2 - 2u^3$) entre transiciones de frecuencia baja, media y alta.

---

## 5. Invariante de Mapeo Armónico Camelot (Enteros 0 a 23)

DJ.Studio codifica internamente las 24 claves musicales como enteros $[0, 23]$:

* **Tonalidades Mayores ($0-11$):**
  - $0 = \text{8B (Do M)}$, $1 = \text{3B (Re}\flat\text{ M)}$, $2 = \text{10B (Re M)}$, $3 = \text{5B (Mi}\flat\text{ M)}$
  - $4 = \text{12B (Mi M)}$, $5 = \text{7B (Fa M)}$, $6 = \text{2B (Fa}\sharp\text{ M)}$, $7 = \text{9B (Sol M)}$
  - $8 = \text{4B (La}\flat\text{ M)}$, $9 = \text{11B (La M)}$, $10 = \text{6B (Si}\flat\text{ M)}$, $11 = \text{1B (Si M)}$
* **Tonalidades Menores ($12-23$):**
  - $k_{\text{minor}} = k_{\text{major}} + 12$
  - $12 = \text{8A (La m)}$, $13 = \text{3A (Si}\flat\text{ m)}$, $14 = \text{10A (Si m)}$, $15 = \text{5A (Do m)}$
  - $16 = \text{12A (Re}\flat\text{ m)}$, $17 = \text{7A (Re m)}$, $18 = \text{2A (Mi}\flat\text{ m)}$, $19 = \text{9A (Mi m)}$
  - $20 = \text{4A (Fa m)}$, $21 = \text{11A (Fa}\sharp\text{ m)}$, $22 = \text{6A (Sol m)}$, $23 = \text{1A (La}\flat\text{ m)}$

---

## 6. Matriz de Deformación Temporal (`mixMap` en `mix-data-table`)

En `mix-data-table/<project_key>/<track_key>`, cada pista contiene la cuadrícula de sincronización de fase:
```json
{
  "mixMap": [
    { "time": -0.26256, "duration": 0.65934, "trackBeatIx": 0 },
    { "time": 0.39677,  "duration": 0.65934, "trackBeatIx": 1 }
  ],
  "gridBpm": 91.0,
  "beatMode": 2
}
```
Proyecta cada pulso musical discreto (`trackBeatIx`) sobre el tiempo continuo de la mezcla (`time`) con duraciones variables (`duration = 60 / BPM_local`), asegurando mezclas métricamente exactas sin desajuste de fase (*zero phase drift*).

---

## 7. Comandos CLI y Herramientas MCP

El paquete soberano reside en `~/10_PROJECTS/djstudio-mcp`:

```bash
# Diagnóstico de biblioteca
python3 -m djstudio_mcp.cli status

# Listar proyectos activos
python3 -m djstudio_mcp.cli projects

# Búsqueda en catálogo
python3 -m djstudio_mcp.cli search "Weatherall"

# Compatibilidad armónica
python3 -m djstudio_mcp.cli harmonic "8A"

# Lanzar servidor MCP
python3 -m djstudio_mcp.cli serve
```

---

## 8. Herramientas MCP Registradas

* `djstudio_status`: Telemetría del sistema, conteo de tracks SQLite y proyectos.
* `djstudio_list_projects`: Resumen de proyectos y fechas de modificación.
* `djstudio_get_project_detail`: Grafo de mezcla, automaciones y efectos VST.
* `djstudio_search_library`: Filtro de biblioteca por BPM, Camelot y género.
* `djstudio_get_harmonic_compatibility`: Compatibilidad armónica según la rueda de Camelot.
* `djstudio_get_track_acoustic_analysis`: Extracción de beatgrid, danceability y energía.
* `djstudio_create_mix_project`: Generación determinista de proyectos en DJ.Studio con curvas automáticas de ecualización y *bass swap*.

---

## 9. Subsistema de Inferencia Neuronal en Silicio (`ai-stems` & `ai-beatgrid`)

DJ.Studio Next (v4) desacopla la inferencia de machine learning en workers nativos N-API:

### 9.1. Motor de Separación de Stems (`@appmachine/ai-stems` v3.2.94)
* **Backends de Silicio:**
  * **macOS:** PyTorch C-ABI (`libtorch.dylib`, `libc10.dylib`, `libomp.dylib`) con aceleración MPS (Metal) para Demucs v4 (`htdemucs.pt`, `htdemucs_fast.pt`) + ONNX Runtime v1.22.1 (`libonnxruntime.1.22.1.dylib`) acoplado a **Apple CoreML** para MDX-Net (`mdx_vocals.onnx`, `mdx_instrumental.onnx`).
  * **Windows:** ONNX Runtime con aceleración DirectML.
* **Cifrado de Pesos:** Carga modelos `${model}_encrypted${ext}` con desencriptado en memoria C++ antes de la compilación de grafos.

### 9.2. Motor de Beatgrid y Fraseo (`@appmachine/ai-beatgrid` v1.2.2)
* **Ensamble de 7 Pliegues:** Modelos `model_fold_0.pt` a `model_fold_6.pt` (TorchScript) para el cálculo de downbeats y retícula métrica fija (`ai3`).
* **Modelo Flex (`model0.pt`):** Ajuste de tempo variable no lineal (`bpmLine`) para pistas con deriva humana o grabaciones de vinilo.
* **Clasificador de Fraseo (`model_phrases.pt`):** Segmentación estructural (Intro, Verso, Estribillo, Drop, Outro) con fallback a endpoint remoto en Paperspace Gradient.

---

## 10. Semántica de Puntos Cue y Enlaces Topológicos (`mix-data-table`)

En los descriptores JSON de `mix-data-table/<project_uuid>/<track_uuid>`:
* **`cueData.systemCuePoints`:**
  * `type: 0` (*Boundary Cue*): Inicio y final absoluto del audio en compases/segundos.
  * `type: 5` (*Transition Phrase Anchor*): Marcador métrico de downbeat (ej. compás 8 / beat 32) donde se ancla el inicio de la mezcla cruzada.
* **`linkMixRecordCue`:** Puntero entero que acopla topológicamente la salida de la pista actual con el punto cue de entrada de la sucesora.

---

## 11. Función de Coste y Optimización *Harmonize* (Combinatorial TSP)

El optimizador formula la ordenación de sesiones como un problema de búsqueda combinatoria minimizando la pérdida de energía y disonancia:

$$J(\pi) = \sum_{i=1}^{N-1} \Big( w_k \cdot D_{\text{harm}}(k_{\pi_i}, k_{\pi_{i+1}}) + w_b \cdot \frac{|b_{\pi_i} - b_{\pi_{i+1}}|}{\min(b_{\pi_i}, b_{\pi_{i+1}})} + w_e \cdot |e_{\pi_i} - e_{\pi_{i+1}}| \Big)$$

* **Matriz Toroidal de Camelot:**
  * Exact Match ($\Delta = 0$): Coste $0.0$.
  * Relativa Mayor $\leftrightarrow$ Menor ($c_1 = c_2$): Coste $0.5$.
  * Quinta / Cuarta ($\Delta = 1$ en el reloj): Coste $1.0$.
  * Tono Entero ($\Delta = 2$): Coste $3.0$.
  * Cruces disonantes (tritono / semitono no resuelto): Coste $\ge 8.0$.
* **Patrón de Escalera Tonal:** El resolvedor por recocido simulado (*Simulated Annealing* con 2-opt) genera de forma autónoma progresiones que alternan polaridad modal (ej. 8B $\to$ 8A $\to$ 9A $\to$ 9B $\to$ 10B $\to$ 10A...), reduciendo la fricción en más de un 75% respecto a ordenaciones lineales aleatorias.

---

## 12. Protocolo Psicoacústico de Mezcla Continua (Integración C5-REAL)

Para transiciones largas (64 a 128 compases), el sistema aplica los principios físicos de `flstudio-mcp`:
1. **Disonancia Sensorial de Plomp-Levelt / Sethares:** Evaluación de rugosidad en la membrana basilar coclear para parciales espectrales:
   $$d(f_1, f_2, A_1, A_2) = (A_1 \cdot A_2) \cdot \left[ e^{-a \cdot s \cdot (f_2 - f_1)} - e^{-b \cdot s \cdot (f_2 - f_1)} \right]$$
2. **Esculpido en 24 Bandas Críticas de Bark (Zwicker):** Monitoreo de SMR (*Signal-to-Mask Ratio*) para tallado dinámico en muesca (*notch carving*), impidiendo la cancelación y el barro psicoacústico.
3. **Alineación de Fase Sub-Muestra Anti-Comb Filtering:** Intercorrelación cruzada fraccional y retraso por filtro sinc FIR con ventana Kaiser para suma constructiva (+6 dB) de transitorios.

---

## 13. Serialización Multipista Ableton Live (`.als` Gzip XML)

Los sets exportados en `~/Music/DJ.Studio/Exports/` se serializan como archivos XML comprimidos con Gzip:
* **Cabecera:** `<Ableton MajorVersion="5" MinorVersion="11.0_11300" SchemaChangeCount="3" Creator="C5-REAL / DJ.Studio">`
* **Pistas Desacopladas:** `<AudioTrack Id="1">` (Deck A), `<AudioTrack Id="2">` (Deck B) y `<MasterTrack>` con tempo maestro `<Transport><Tempo><Manual Value="..." /></Transport>`.
* **Visualización:** Vinculable al servidor Cockpit en `http://localhost:6060` y visores interactivos Web Audio HUD.

---

## 14. Motor DSP V2 de Transición Continua (Crossover Linkwitz-Riley 4th Order & Zero-Overlap Bass Swap)

Para transiciones continuas de alta exergía sin emborronamiento espectral en frecuencias bajas ni acumulación de fase destructiva, el motor utiliza un pipeline DSP multietapa:

### 14.1. Crossover Linkwitz-Riley de 4º Orden (LR4)
* **Frecuencias de Corte Canónicas:**
  * Sub/Bajos: $f_{\text{low}} = 160\text{ Hz}$
  * Medios: $160\text{ Hz} \le f \le 2800\text{ Hz}$
  * Agudos: $f_{\text{high}} = 2800\text{ Hz}$
* **Topología:** Dos filtros Butterworth de 2º orden en cascada procesados en forward-backward (`scipy.signal.filtfilt`), resultando en una pendiente asintótica de $-24\text{ dB/octava}$.
* **Invariante de Fase Plana:** A diferencia de los filtros Butterworth estándar que generan un realce de $+3\text{ dB}$ en la frecuencia de corte, el crossover LR4 suma exactamente a ganancia unitaria ($0\text{ dB}$ ripple) con respuesta de fase plana:
  $$\sum (H_{\text{low}} + H_{\text{mid}} + H_{\text{high}}) = 1.0 \quad (\angle 0^\circ)$$
* **Guarda Numérica de Silicio:** Toda operación `filtfilt` debe protegerse contra colapso por `padlen` cuando el segmento de audio sea corto ($N < 30$ muestras):
  ```python
  def safe_filtfilt(b, a, x):
      if len(x) < 30:
          return x
      return filtfilt(b, a, x)
  ```

### 14.2. Zero-Overlap Bass Swap Cuantizado (Beat 1.1)
El error común de los crossfaders genéricos es solapar dos líneas de bajo durante 16 a 32 compases, provocando cancelaciones por peine (*comb filtering*) y lodo dinámico.
* **Política Determinista:** El canal de bajas frecuencias ($0-160\text{ Hz}$) de la pista saliente conmuta a $-\infty\text{ dB}$ de forma instantánea en el compás central de la transición (ej. compás 16 de 32, beat 1.1).
* La pista entrante abre su subgrave exactamente en ese mismo instante.
* Resultado: Cero interferencia de fase destructiva en el rango crítico $30-120\text{ Hz}$.

### 14.3. Dip Psicoacústico de Medios (-1.2 dB)
Para evitar la acumulación de energía en frecuencias medias donde conviven sintetizadores, cajas y elementos armónicos:
* Se aplica una curva de atenuación convexa en el crossfade de medios con un dip de $-1.2\text{ dB}$ en el punto central ($t = 0.5$).
* Previene la fatiga coclear y preserva la definición de las cajas y sintetizadores de ambas pistas.

### 14.4. Cola Dub Espacial Generativa (*Space Echo Tail*)
En transiciones atmosféricas o de ruptura, el canal de medios y agudos de la pista saliente se alimenta a una línea de retardo con puntillo ($3/16$ compás):
$$T_{\text{delay}} = \frac{60}{\text{BPM}} \times 0.75\text{ s}$$
* **Factor de Realimentación:** $42\%$ con amortiguamiento de altas frecuencias (*high-frequency damping*).
* **Decaimiento Natural:** $8-10$ segundos disipándose en el fondo de la pista entrante tras el corte del bajo.

---

## 15. Taxonomía Psicoacústica de las 8 Transiciones Canónicas de Club

1. **Corte Seco en Caída (Hard Drop Cut):**
   * *Duración:* 1 compás (4 tiempos).
   * *Mecánica:* Silencio o corte percusivo abrupto en beat 4.4; entrada del kick entrante en beat 1.1 con máximo impacto dinámico.
   * *Uso:* Rupturas disonantes o cambios drásticos de atmósfera.
2. **Relevo de Bajos en Cuadratura (Low-End Swap Standard):**
   * *Duración:* 32 compases (128 tiempos).
   * *Mecánica:* Los medios y agudos de la pista B se introducen suavemente durante los compases 1 a 16. En el compás 16 (beat 64), se ejecuta el corte de bajo 100% / 0%. Los compases 17 a 32 retiran los agudos de la pista A.
   * *Uso:* El estándar del techno hipnótico y dub techno.
3. **Fundido Progresivo de Pared Sónica (Wall of Sound / Deep Blend):**
   * *Duración:* 64 compases (256 tiempos).
   * *Mecánica:* Fusión prolongada donde ambas pistas conviven durante más de dos minutos. El bajo de la pista entrante entra filtrado progresivamente con un filtro paso-alto de $24\text{ dB/oct}$ bajando de $160\text{ Hz}$ a $30\text{ Hz}$.
   * *Uso:* Dub techno berlinés, ambient techno y clímax hipnóticos.
4. **Cola Dub Espacial / Congelación Resonante (Space Echo Freeze):**
   * *Duración:* 16 compases de mezcla + 8 compases de cola dub.
   * *Mecánica:* La pista A entra en bucle con delay estéreo sincronizado a corchea con puntillo ($3/16$) y feedback al 42%. La pista B entra desde el vacío.
   * *Uso:* Transición entre bloques temáticos o cambio de tempo.
5. **Transición Micro-Polirrítmica / Métrica Desfasada:**
   * *Duración:* 32 compases.
   * *Mecánica:* Superposición de patrones ternarios ($3/4$ o $6/8$) sobre métrica $4/4$ estricta, resolviendo en el downbeat del compás 33.
   * *Uso:* IDM, braindance y electro modular.
6. **Desaceleración / Aceleración Cinética (Tempo Ramp):**
   * *Duración:* 32 a 64 compases.
   * *Mecánica:* Rampa continua de BPM preservando el tono mediante algoritmos elastique o repitch cinético.
   * *Uso:* Transición entre actos con salto de velocidad (ej. 115 BPM a 130 BPM).
7. **Sustitución Percusiva (Percussion Stem Swap):**
   * *Duración:* 16 compases.
   * *Mecánica:* Intercambio de hi-hats, claps y elementos por encima de $2.8\text{ kHz}$ mientras el bajo y la armonía de la pista A permanecen intactos.
   * *Uso:* Inyección de energía rítmica antes de cambiar de track.
8. **Modulación Camelot con Tensión / Resonancia:**
   * *Duración:* 32 compases.
   * *Mecánica:* Transición entre tonalidades contiguas ($\pm 1$), relativas (A $\leftrightarrow$ B) o salto de energía ($+2$ tonos), gestionando la disonancia con un filtro notch dinámico en la frecuencia fundamental de choque.
   * *Uso:* Elevación armónica o inmersión melancólica.

---

## 16. Generador y Serializador Nativo Pioneer Rekordbox XML (`DJ_PLAYLISTS 1.0.0`)

Para garantizar la interoperabilidad universal entre DJ.Studio, CDJs, XDJ-XZ/3000, Engine DJ y reproductores de club profesionales, el sistema exporta colecciones y playlists bajo el esquema canónico XML de Pioneer Rekordbox:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DJ_PLAYLISTS Version="1.0.0">
  <PRODUCT Name="rekordbox" Version="6.0.0" Company="Pioneer DJ" />
  <COLLECTION Entries="20">
    <TRACK TrackID="1" Name="Track Title" Artist="Artist Name" 
           TotalTime="360" AverageBpm="128.00" Tonality="11A" 
           BitRate="320" SampleRate="44100" 
           Location="file://localhost/Users/borjafernandezangulo/Music/Setlist/01_track.mp3">
      <POSITION_MARK Name="Intro" Type="0" Start="0.000" Num="0" />
      <POSITION_MARK Name="Mix In" Type="0" Start="30.000" Num="1" />
      <POSITION_MARK Name="Bass Swap" Type="0" Start="120.000" Num="2" />
      <POSITION_MARK Name="Mix Out" Type="0" Start="300.000" Num="3" />
    </TRACK>
  </COLLECTION>
  <PLAYLISTS>
    <NODE Type="0" Name="ROOT">
      <NODE Type="1" Name="Setlist Name" KeyType="0" Entries="20">
        <TRACK Key="1" />
      </NODE>
    </NODE>
  </PLAYLISTS>
</DJ_PLAYLISTS>
```

### Reglas de Codificación:
* **`Location`:** URI con codificación de porcentaje estándar (`urllib.parse.quote`), comenzando por `file://localhost/`.
* **`Tonality`:** Clave armónica estandarizada en notación Camelot (`1A` a `12B`) o musical (`Am`, `F#m`).
* **`AverageBpm`:** Punto flotante con dos decimales exactos.
* **`POSITION_MARK`:** Marcadores tipo 0 (*Cue Points*) mapeados a los puntos clave de fraseo de la transición (Intro, Mix In, Bass Swap, Mix Out).

---

## 17. Arquitectura Narrativa en 5 Actos («El Circuito Disruptor»)

Toda sesión de alta exergía para club underground debe estructurarse siguiendo una dinámica termodinámica y psicofísica en 5 actos:

1. **Acto I: Génesis y Descompresión (BPM Inicial, 100-118 BPM):**
   * *Función:* Desacople del ruido exterior, anclaje corporal, texturas dub, post-punk/coldwave y groove elástico.
2. **Acto II: El Ascenso Hipnótico (120-128 BPM):**
   * *Función:* Densidad modular, dub techno berlinés, subgraves profundos, repetición microtonal y trance estocástico.
3. **Acto III: La Tormenta Cinética / Caos Controlado (130-138 BPM):**
   * *Función:* Máxima disrupción, techno industrial, broken beat británico, disonancias de tritono y polirritmias abrasivas.
4. **Acto IV: Mutación Modular y Trascendencia Electro (128-132 BPM):**
   * *Función:* Electro de Detroit, sintetizadores de transistores puros, melodías alienígenas y arpegios euclidianos.
5. **Acto V: El Horizonte de Sucesos y Disolución (130-140 BPM $\to$ Outro):**
   * *Función:* Braindance, drill & bass deconstruido, catarsis rítmica y retorno a la resonancia basal.
