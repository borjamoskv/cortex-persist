---
name: f5tts-voice-cloning-sota
display_name: Clonación Vocal Neuronal SOTA (F5-TTS / MPS / Ingeniería de Prosodia)
description: Clonación y síntesis de voz con F5-TTS en Apple Silicon MPS, prosodia orgánica y masterización Opus VOIP. Dispara con "clonar voz", "sintetizar voz", "f5-tts", "f5tts", "voice clone", "prosodia tts", "nota de voz ia".
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

# Habilidad: Clonación Vocal Neuronal SOTA (F5-TTS Flow-Matching)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Esta habilidad documenta las invariantes matemáticas, acústicas y de ingeniería de software para sintetizar voces hiperrealistas con F5-TTS, erradicando el fraseo antinatural, los cortes mecánicos por puntuación y las inconsistencias de cadencia.

---

## 1. Arquitectura de Ejecución en Silicio (macOS Apple Silicon)

- **Entorno Virtual Dedicado:** `/opt/homebrew/Caskroom/miniconda/base/envs/audio/bin/python`
- **Aceleración de Hardware:** `device="mps"` (Metal Performance Shaders con vaciado de caché `torch.mps.empty_cache()` y recolección de basura `gc.collect()`).
- **Checkpoints Locales:**
  - Modelo: `~/.cache/f5-tts-es/model_1250000.safetensors`
  - Vocabulario: `~/.cache/f5-tts-es/vocab.txt`
  - Vocoder: Vocos Mel 24kHz (`charactr/vocos-mel-24khz`).

---

## 2. Invariantes de Prosodia y Bypass del Chunker (`chunk_text`)

### Regla 1: Prohibición de Puntos Suspensivos Literales (`...`)
- **Fallo Físico:** `...` no existe como token único en `vocab.txt`. Se descompone en 3 paradas de sentencia consecutivas (`. . .`) y dispara el regex `re.split(r"(?<=[;:,.!?])\s+")` de `chunk_text`, partiendo la frase en lotes aislados. Cada lote fuerza la energía acústica a cero al final de la trayectoria ODE.
- **Protocolo de Remediación:**
  1. Sustituir `...` por guión de suspensión con espacio (` - ` o ` — `) o por coma de prolongación tonal (`,`).
  2. Para titubeos conversacionales orgánicos, inyectar conectores orales naturales (`es imposible que me— o sea, empieza a hablar...`).

### Regla 2: Unificación de Variedad en un Único Lote (`batches = 1`)
- Para oraciones de hasta 25-30 segundos de duración generada, **evitar la fragmentación multichunk**.
- Se debe asegurar que `max_chars` en `infer_process` sea suficientemente amplio o invocar directamente `infer_batch_process` pasando `gen_text_batches = [texto_completo]` para que el ODE solver integre una sola trayectoria armónica continua sin saltos de fase.

### Regla 3: Cinética ODE Segura (`speed = 1.02 - 1.06`) y Velocidad Ground-Truth
- **Prohibición de Aceleración Forzada en ODE:** Jamás superar `speed > 1.10` en el solver ODE creyendo acelerar artificialmente la voz. Acelerar el integrador comprime los fonemas oclusivos por debajo de 20ms provocando deglución de consonantes y balbuceo (*"apretado"* → *"periodado"*, *"copiar y pegar"* → *"escupí a pegar"*).
- **Origen de la Velocidad Real:** La cadencia rápida (150-185 WPM) debe heredarse de la **referencia nativa de WhatsApp** (muestreada a velocidad natural del personaje), manteniendo el motor ODE en su zona de máxima fidelidad articulatoria:
  - David Medina / Cadencia analítica reflexiva: `speed = 1.02` (111 WPM real).
  - Alain / Cadencia temperamental vasca: `speed = 1.05` (175 WPM real).
  - Mitxu / Cadencia eufórica consorcio/techno: `speed = 1.06` (150 WPM real).
  - Landeta (Poio) / Cadencia Laidatxu ultratumba: `speed = 1.15` (140 WPM real, voz gutural estable).
- **Tensión de Guiado (CFG) y Deformación Temporal ODE (Sway):**
  - Configurar `cfg_strength = 1.80` (erradica ataques consonánticos blandos y transiciones difusas de `cfg = 1.35`).
  - Activar deformación temporal `sway_sampling_coef = -0.8` para redistribuir la integración ODE hacia los límites articulatorios de alta curvatura.

### Regla 4: Normalización Numérica y Jerga Fonética
- Todo número debe expandirse fonéticamente antes de la inferencia (`25` → `veinticinco`; `45` → `cuarenta y cinco`).
- Neologismos locales (ej. `exerjo`) deben evaluarse con Whisper posterior para validar que el vocoder no genera consonantes espurias.

### Regla 5: Inicialización Determinista de la API F5-TTS
- **Fallo Común:** Pasar `model_type="F5TTS_Base"` genera `TypeError: F5TTS.__init__() got an unexpected keyword argument 'model_type'`.
- **Constructor Canónico:** Pasar `model="F5TTS_Base"`, `ckpt_file` y `vocab_file`.

### Regla 6: Prohibición de TTS Genérico en Contenido Nexus / Landpark
- Queda estrictamente prohibido utilizar motores de síntesis genérica (EdgeTTS, Kokoro, gTTS, macOS `say`) para los personajes de Lander, Borja, Alain, Mitxu o cualquier miembro de la cuadrilla Nexus.
- Toda síntesis DEBE ejecutar el pipeline de clonación F5-TTS sobre Metal (MPS) empleando las muestras de audio reales de WhatsApp limpiadas y normalizadas.

### Regla 7: Cadena de Mastering Cinético WhatsApp (Pegada, Cuerpo y Presencia)
- **Filtro Pasabanda:** Highpass $55\text{ Hz}$ (corte estricto de sub-rumble) + Lowpass $7800\text{ Hz}$ (preserva el centroide espectral en $>1600\text{ Hz}$ y el mordiente de sibilantes/oclusivas).
- **Ecualización Formántica:** Boost barítono en $180\text{ Hz}$ ($+1.5\text{ dB}$, $Q=1.2$, resonancia torácica) y presencia en $3200\text{ Hz}$ ($+1.8\text{ dB}$, $Q=1.0$, inteligibilidad).
- **Saturación Analógica:** `asoftclip=type=atan:param=1.2` (comprime picos con calidez analógica y aglutina formantes vocales sin distorsión áspera).
- **Compresor de Transitorios:** `acompressor=threshold=-20dB:ratio=2.5:attack=15:release=70:makeup=1.0dB` (permite que los primeros $15\text{ ms}$ del transitorio percutan con pegada antes de comprimir el cuerpo vocálico).
- **Normalización EBU R128 Estricta:** `loudnorm=I=-16:TP=-1.5:LRA=7` con pre-atenuación `volume=0.88` para evitar inter-sample peaks y distorsión en el códec Opus a $24\text{ kbps}$.

### Regla 8: Bypass Obligatorio del Segmentador RJieba (Preservación de Tildes en Español)
- **Fallo Crítico:** `convert_char_to_pinyin` en F5-TTS ejecuta internamente `rjieba.cut(text)`. En español, toda vocal acentuada (`á`, `é`, `í`, `ó`, `ú`) es aislada por rjieba y seguida por la inyección de un espacio en blanco (`pásame` $\to$ `['p', 'á', ' ', 's', 'a', 'm', 'e']`), partiendo las palabras y generando micro-pausas y tartamudeos antinaturales.
- **Protocolo de Parcheo en Silicio:**
  ```python
  import f5_tts.infer.utils_infer as utils_infer
  utils_infer.convert_char_to_pinyin = lambda text_list, **kw: [[c for c in text] for text in text_list]
  ```
  Esto preserva los caracteres UTF-8 puros sin alteración de fronteras de palabra.

### Regla 9: Supresión Obligatoria de Signos de Apertura Invertidos (`¡` / `¿`)
- **Fallo Físico:** En los modelos F5-TTS entrenados en español, el token inicial de apertura (`¡`, `¿`) colisiona con el embedding fonético de la primera vocal/consonante, provocando artefactos de sustitución (ej. `¡Aupa` → `Fopa`).
- **Protocolo:** Suprimir siempre `¡` y `¿` en `normalize_text` antes de pasarlo al tokenizador (`text = text.replace("¡", "").replace("¿", "")`), conservando la puntuación de cierre (`!`, `?`, `.`) para guiar la entonación.

### Regla 10: Desacoplamiento de Prefijo de Prompt (Anti-Prefix Collision)
- **Fallo Físico:** Si la frase a sintetizar comienza con las mismas palabras con las que inicia el texto de referencia (`ref_text`), el modelo Flow-Matching confunde la condición de contexto con la generación autorregresiva y salta tokens creyendo que ya fueron pronunciados.
- **Protocolo:** Asegurar que el inicio de la frase generada no comparta una subsecuencia idéntica de más de 2 palabras con el inicio del `ref_text`.

### Regla 11: Glosario Fonético de Jerga Electrónica y Clubbing
- Aplicar normalización estricta por regex antes de la inferencia:
  - `techno` / `tekno` → `tecno` (erradica la articulación errónea como che `/tʃ/`).
  - `subgraves` → `sub graves` (evita confusión con *"sus graves"*).
  - `bpm` / `bpms` → `be pe eme` / `be pe emes`.
  - `ia` → `i a`.
  - Asegurar terminación limpia de sentencia con punto final (`.`) para evitar truncamiento de las últimas sílabas en Vocos.

### Regla 12: Compuerta de Calidad Fonética Ground-Truth (`compare_diction.py`)
- Toda síntesis de producción en el estudio debe someterse a auditoría contra la referencia real:
  1. Transcripción con Whisper y cálculo de confianza media de tokens ($\ge 0.75$).
  2. Discrepancia de centroide espectral frente al audio real: $|\Delta\text{Cent}| \le 250\text{ Hz}$.
  3. Si no pasa la compuerta, reintentar variando la semilla o reubicando micro-pausas sintácticas.

---

## 3. Script Patrón de Inferencia SOTA

```python
import os, gc, torch, soundfile as sf, subprocess
from f5_tts.api import F5TTS
import f5_tts.infer.utils_infer as utils_infer
from f5_tts.infer.utils_infer import infer_batch_process, preprocess_ref_audio_text

# 1. Parcheo del tokenizador español (eliminación de fractura por rjieba)
utils_infer.convert_char_to_pinyin = lambda text_list, **kw: [[c for c in text] for text in text_list]

if torch.backends.mps.is_available():
    torch.mps.empty_cache()
gc.collect()

# 2. Inicialización resiliente con fallback determinista al hub local
ckpt = os.path.expanduser("~/.cache/f5-tts-es/model_1250000.safetensors")
vocab = os.path.expanduser("~/.cache/f5-tts-es/vocab.txt")
kwargs = {
    "model": "F5TTS_Base",
    "device": "mps" if torch.backends.mps.is_available() else "cpu"
}
if os.path.exists(ckpt) and os.path.exists(vocab):
    kwargs["ckpt_file"] = ckpt
    kwargs["vocab_file"] = vocab
f5 = F5TTS(**kwargs)

# 3. Preprocesamiento de audio de referencia
prep_file, prep_text = preprocess_ref_audio_text(ref_audio_path, ref_transcript)
d, sr = sf.read(prep_file)
audio = torch.from_numpy(d).float().unsqueeze(0) if d.ndim == 1 else torch.from_numpy(d.T).float()

# 4. Inferencia continua con ODE denso y cinética calibrada
wav, out_sr, _ = next(
    infer_batch_process(
        (audio, sr),
        prep_text,
        [text_normalized.lower()],
        f5.ema_model,
        f5.vocoder,
        mel_spec_type=f5.mel_spec_type,
        target_rms=0.1,
        cross_fade_duration=0.15,
        nfe_step=64,
        cfg_strength=1.80,
        sway_sampling_coef=-0.8,
        speed=1.14,
        device="mps" if torch.backends.mps.is_available() else "cpu"
    )
)

raw_tmp = "/tmp/raw_generation.wav"
sf.write(raw_tmp, wav, out_sr)

# 5. Masterización Cinética Analógica EBU R128 y compresión VOIP Opus
filter_chain = (
    "volume=0.88,"
    "highpass=f=55,lowpass=f=7800,"
    "equalizer=f=180:width_type=q:width=1.2:gain=1.5,"
    "equalizer=f=3200:width_type=q:width=1.0:gain=1.8,"
    "asoftclip=type=atan:param=1.2,"
    "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=70:makeup=1.0dB,"
    "loudnorm=I=-16:TP=-1.5:LRA=7"
)

cmd_opus = [
    "ffmpeg", "-y", "-i", raw_tmp,
    "-af", filter_chain,
    "-c:a", "libopus", "-b:a", "24k", "-vbr", "on", "-application", "voip",
    out_opus_path
]
subprocess.run(cmd_opus, check=True)
```

---

## 4. Invariante de Centralización y Despacho (`NSPasteboard`)
- Todo audio clonado se guarda canónicamente en `~/Music/`.
- Se inyecta inmediatamente en el portapapeles de macOS como descriptor `POSIX file` (`osascript -e 'set the clipboard to POSIX file "..."'`) para permitir pegado instantáneo (`Cmd + V`) en WhatsApp.
