---
name: flstudio-mcp-production
display_name: Producción Nativa MCP FL Studio 2025 & DSP Microtonal
description: Protocolo de integración nativa MCP con FL Studio 2025, automatización MIDI/CoreMIDI bidireccional, compilación binaria headless de proyectos .flp, orquestación de 10 subagentes especialistas, falso drop determinista en compás 12, microtonalidad xenarmónica (26 perfiles Scala .scl/.kbm), carving psicoacústico de 24 bandas Bark y masterización EBU R128. Dispara con "FL Studio", "flstudio-mcp", "compilar flp", "10 agentes musica", "falso drop compas 12", "piano roll script", "microtonal house", "satin jackets loop", "falso drop", "maceo plex kick", "psychoacoustic carver", "bark scale fl studio".
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

# FL Studio 2025 MCP & Audio Engineering Protocol (C5-REAL SOTA Zenith)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este skill define la arquitectura soberana para componer, controlar, micro-afinar, mezclar y automatizar en **FL Studio 2025** mediante agentes IA, scripts de Piano Roll interactivos (`flpianoroll`), control MIDI MPE bidireccional de 14 bits, 26 perfiles de afinación xenarmónica y controladores hardware dedicados.

---

## 🧭 1. Mastermind CLI Unificado (`flstudio_mcp_cli.py`)

Toda la suite de herramientas puede ejecutarse y auditarse desde una única interfaz centralizada:

```bash
# Diagnóstico completo del entorno (FL Studio, carpetas, librerías, tunings):
python3 ~/.gemini/config/skills/flstudio-mcp-production/scripts/flstudio_mcp_cli.py doctor

# Validación de sintaxis AST y puntos de entrada de los 24 scripts:
python3 ~/.gemini/config/skills/flstudio-mcp-production/scripts/flstudio_mcp_cli.py validate

# Despliegue atómico de todos los scripts, hardware y afinaciones a FL Studio:
python3 ~/.gemini/config/skills/flstudio-mcp-production/scripts/flstudio_mcp_cli.py deploy

# Sincronización del directorio de activos musicales centralizado ~/Music/:
python3 ~/.gemini/config/skills/flstudio-mcp-production/scripts/flstudio_mcp_cli.py sync-music
```

---

## 🎛️ 2. Controlador Hardware Bidireccional (`device_Antigravity_MCP.py`)

Ubicación en el sistema:
`~/Documents/Image-Line/FL Studio/Settings/Hardware/AntigravityMCP/device_Antigravity_MCP.py`

Convierte a FL Studio en un receptor y emisor de telemetría en tiempo real:

| Canal MIDI | Parámetro Controlado | Mapeo / Valores |
| :--- | :--- | :--- |
| **Ch 1 (0)** | Volumen de Pistas del Mezclador | CC 0 = Master, CC 1..125 = Pistas 1..125 |
| **Ch 2 (1)** | Paneo Estéreo de Pistas | CC 0..125 (Centro en 64, Rango -1.0 a 1.0) |
| **Ch 3 (2)** | Silenciar Pista (Mute) | CC 0..125 (Valor > 64 = Mute) |
| **Ch 4 (3)** | Solo de Pista | CC 0..125 (Valor > 64 = Solo) |
| **Ch 5 (4)** | Separación Estéreo | CC 0..125 (0 = Mono puro, 64 = Normal, 127 = 100% Side) |
| **Ch 6 (5)** | Macros de Plugins / TB-303 | Modulación de Cutoff, Resonancia y Macros 1..8 |
| **Ch 7 (6)** | Channel Rack | CC 0..15 (Seleccionar), CC 16..31 (Mute), CC 32..47 (Solo) |
| **Ch 8 (7)** | Navegación de Patrones y Marcadores | CC 1 (Marcador Ant), CC 2 (Marcador Sig), CC 4 (Patrón) |
| **Ch 16 (15)**| Transporte Master y Sistema | Play (CC 10), Stop (CC 11), Rec (CC 12), BPM (CC 15), Undo (CC 16), Redo (CC 17), Sidechain (CC 18) |

---

## 🎹 3. API Nativa de Piano Roll (`flpianoroll` / `.pyscript`)

Ubicación de scripts en macOS:
`~/Documents/Image-Line/FL Studio/Settings/Piano roll scripts/`

### Ciclo de Vida Interactivo con GUI:
```python
import flpianoroll as flp

def createDialog():
    form = flp.ScriptDialog("Herramienta C5-REAL", "Transformación algorítmica interactiva.")
    form.AddInputKnob("Swing Roger Linn", 62, 50, 75)
    form.AddInputCombo("Modo Escala", "24-TET,Makam Bayati,Bohlen-Pierce", 0)
    form.AddInputCheckbox("Slide Glissando", True)
    return form

def apply(form):
    swing = form.GetInputValue("Swing Roger Linn")
    flp.score.clear()
    # Generación y manipulación algorítmica...
```

### Propiedades de `flp.Note`:
* `note.number`: Tono MIDI (0..127).
* `note.time` / `note.length`: Posición y duración en ticks (480 PPQ estándar).
* `note.velocity` / `note.pan`: Dinámica (0.0 a 1.0) y ubicación estéreo (-1.0 a 1.0).
* `note.pitchoffset`: Desviación microtonal en cents (-100 a +100).
* `note.slide`: Portamento nativo en FL Studio sin redisparo de fase ni filtro.
* `note.color`: Canal MIDI interno / articulación (0 a 15).

---

## 🎼 4. Catálogo de 19 Scripts Curados y Desplegados

Todos los scripts cuentan con GUI interactiva nativa (`createDialog`) y modo fallback (`createScore`):

### A. Algorítmicos & Autómatas
1. **[`Euclidean_Polyrhythm_Generator.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Euclidean_Polyrhythm_Generator.py):** Algoritmo de Bjorklund $E(k, n)$ para polirritmias y polímetros.
2. **[`Cellular_Automata_Music.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Cellular_Automata_Music.py):** Autómatas celulares 1D de Stephen Wolfram (Reglas 30, 90, 110, 150).
3. **[`Markov_Chain_Melody.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Markov_Chain_Melody.py):** Matrices de transición de Markov para melodías estocásticas con leyes de la Gestalt.
4. **[`Brownian_Motion_Walk.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Brownian_Motion_Walk.py):** Caminatas gaussianas fractales con atracción gravitatoria hacia la tónica.
5. **[`Harmonic_Series_Spectral_Cloud.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Harmonic_Series_Spectral_Cloud.py):** Parciales de la serie armónica (1 a 16) con microtonalidad pura y disipación natural.

### B. Geometría Armónica & Jazz
6. **[`Neo_Riemannian_Tonnetz.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Neo_Riemannian_Tonnetz.py):** Caminatas cinematográficas en el Tonnetz ($P$, $L$, $R$).
7. **[`Bill_Evans_Rootless_Voicings.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Bill_Evans_Rootless_Voicings.py):** Voicings Type A y Type B sin fundamental para ii-V-I.
8. **[`Satin_Jackets_Penrose.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Satin_Jackets_Penrose.py):** Bucle infinito Penrose ($Ab\text{maj7} \to Bb9 \to Cm9 \to Fm9$) y Falso Drop con Tercera de Picardía.

### C. Rítmica, Micro-Groove & Humanización
9. **[`Dilla_Behind_The_Beat_Physics.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Dilla_Behind_The_Beat_Physics.py):** Desfase físico de J Dilla (cajas rezagadas, bombos rushing, hats elásticos).
10. **[`Bernard_Purdie_Shuffle.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Bernard_Purdie_Shuffle.py):** Medio tiempo shuffle con tresillos continuos y ghost notes dinámicas.
11. **[`Kerri_Chandler_MPC60.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Kerri_Chandler_MPC60.py):** Matriz de swing Roger Linn MPC-60 (50%-75%) con capas de ghost notes.

### D. Expresión, Slides & Producción Moderna
12. **[`TB303_Acid_Pattern_Generator.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/TB303_Acid_Pattern_Generator.py):** Líneas Acid 303 con notas *slide* nativas, acentos y saltos de octava.
13. **[`Trap_808_Glide_Architect.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Trap_808_Glide_Architect.py):** Sub-graves 808 con glissandos multi-octava y preservación de transitorios.
14. **[`Maceo_Plex_Kick.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Maceo_Plex_Kick.py):** Bombo analógico $F_2$ ($43.65\,\text{Hz}$) y sub-rumble en semicorcheas sin colisión de fase.
15. **[`Stephan_Bodzin_Moog_Arp.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Stephan_Bodzin_Moog_Arp.py):** Arpegiador Melodic Techno con barrido de envolvente de filtro y acentos Moog.
16. **[`Four_Tet_Organic_Microcollage.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Four_Tet_Organic_Microcollage.py):** Puntillismo acústico, micro-timing analógico y paneo dinámico.
17. **[`AIR_Moon_Safari_Rhodes.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/AIR_Moon_Safari_Rhodes.py):** Voicings Space-Pop ($Am9 \to D9 \to F\text{maj7} \to E7\sharp 9$) con micro-timing en Rhodes.
18. **[`Xenharmonic_24TET_Bayati.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/Xenharmonic_24TET_Bayati.py):** Makam Bayati en cuartos de tono con notas slide y afinación Sikah (-50 cents).
19. **[`C5_Full_Track_Arranger.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/examples/C5_Full_Track_Arranger.py):** Estructura completa de 56 compases con marcadores nativos (`flp.Marker`).

---

## 📐 5. Afinación Xenarmónica & Psicoacústica SOTA (26 Perfiles)

Herramienta: [`scripts/scala_generator.py`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/scripts/scala_generator.py)
Directorio nativo en FL Studio: `~/Documents/Image-Line/FL Studio/Settings/Tuning/`

* **Temperamentos Iguales:** 12-TET, 19-TET, 24-TET, 31-TET, 41-TET, 53-TET (quintas puras), 72-TET (bizantino/turco).
* **Temperamentos Históricos:** Werckmeister III, Kirnberger III, Pitagórico, Meantone de 1/4 de coma.
* **Makamaat Árabes:** Bayati, Rast, Hijaz, Saba, Sikah.
* **Thats Hindúes:** Bhairav, Todi, Yaman.
* **Entonación Justa (JI):** 5-limit (Ptolemaica), 7-limit (Septimal), Serie armónica (parciales 8 a 16).
* **Escalas No-Octava:** Bohlen-Pierce (tritave 3:1), Wendy Carlos Alpha, Beta, Gamma.
* **Modos de Tensión:** Lócrio de 2da neutra (-50 cents).
* **Modelo Psicoacústico de Rugosidad Sensorial:** Evaluación Plomp-Levelt / Sethares de la disonancia para optimizar timbres de sintetizador con afinaciones no-12-TET.

---

## 🧮 6. Ecuaciones DSP & Arquitecturas de Mezcla

Consulte el manual técnico completo en:
👉 [`dsp/formulas_and_mixer_architectures.md`](file:///Users/borjafernandezangulo/.gemini/config/skills/flstudio-mcp-production/dsp/formulas_and_mixer_architectures.md)
* Fórmulas para **Fruity Formula Controller** (LFOs áureos aperiódicos, saturación $\tanh$, mapa logístico caótico).
* Desacoplamiento de fase bombo/rumble.
* Procesamiento Mid-Side sin comb-filtering.

---

## 🎵 7. Invariante de Centralización de Audio (`~/Music/`)

Todo render, bounce o loop de audio generado se deposita de forma soberana en:
`~/Music/FL Studio Bounces/` (`/Users/borjafernandezangulo/Music/FL Studio Bounces/`)

---

## 🏗️ 8. Compilación Binaria Headless de Proyectos FLP (`flp_multitrack_stem_compiler.py`)

Ubicación del script de compilación:
`~/10_PROJECTS/flstudio-mcp/scripts/flp_multitrack_stem_compiler.py`

Permite la generación atómica y determinista de archivos de proyecto nativos `.flp` sin interacción con la interfaz gráfica (GUI):
* **Encabezado `FLhd`:** Formato 0, número de canales dinámico, resolución temporal fija a 96 PPQ.
* **Cuerpo `FLdt`:** Flujo de bytes con eventos binarios nativos de Image-Line:
  - `0xC7`: Versión del motor (`21.0.3` / `2025`).
  - `0x9B`: Tempo codificado como entero (`tempo_bpm * 1000`).
  - `0xCA`: Título y metadatos del proyecto.
  - `0x40`: Creación de nuevo canal en el Channel Rack.
  - `0xC0`: Nombre identificador de la pista/canal.
  - `0xC4`: Ruta absoluta al archivo de audio (`.wav`) en disco.
  - `0x45`: Asignación 1:1 al canal de la mesa de mezclas (Mixer Track 1..125).
  - `0xE0`: Disparo automático de notas MIDI en tick 0 para reproducción sincronizada en Playlist.

---

## 🐝 9. Topología Swarm de 10 Especialistas (Producción Agéntica End-to-End)

Para composiciones completas a partir de prompts o muestras vocales, se orquesta un enjambre de 10 subagentes paralelos coordinados:

1. **Vocal Transient Slicer:** Detección de silencios (`top_db=25`), extracción de transitorios y slicing de formantes.
2. **Vocal Hook Synthesizer:** Ensamblado de stems vocales (Hook principal, speech determinista, chops rítmicos, reverb echoes).
3. **House Kick & Percussion Engine:** Síntesis analógica de bombo 909 afinado, clap/snare micro-reverb y rimshot sincopado.
4. **MPC Groove & Hats Stylist:** Swing Roger Linn MPC (56-57%), open hi-hat a contratiempo, closed hats elásticos y shaker estéreo.
5. **Rolling House SubBass Engine:** Síntesis analógica de subgrave (Moog ladder / Kerri Chandler fundamental C1/C2) con fase alineada.
6. **Detroit Cosmic Chords Synth:** Síntesis sustractiva polifónica analógica (Cm9, Fm9, Gm7, Abmaj7) con chorus estéreo y filtro ADSR.
7. **Cosmic Arp & Textures Synth:** Arpegio melódico en semicorcheas, colchón pad Juno-106 y riser de tensión de ruido blanco.
8. **Psychoacoustic Bark Mixer:** Análisis dinámico de enmascaramiento psicoacústico en 24 bandas Bark (Zwicker), tallando huecos en 65 Hz y 120 Hz.
9. **Arrangement & Falso Drop Architect:** Macro-estructura de 64 compases con la regla canónica del Falso Drop en el Compás 12 del bloque de tensión (Compás 60).
10. **FLP Binary Compiler & Master:** Compilación del `.flp`, asignación de pistas al mixer y masterización EBU R128 (-14.0 LUFS, -1.0 dBFS True Peak).

---

## 🎚️ 10. Carving Psicoacústico en Escala Bark de Zwicker

Herramienta: `~/10_PROJECTS/flstudio-mcp/scripts/psychoacoustic_masking_carver.py`

* Divide el espectro en las **24 bandas críticas de Bark** (Zwicker, 1961).
* Calcula el umbral de enmascaramiento simultáneo entre la señal dominante (ej. Bombo) y la señal enmascarada (ej. Sub-Bass o Rhodes).
* Aplica atenuación dinámica selectiva en los nodos de fricción crítica:
  - **Banda Bark 1 (0-100 Hz):** Corte dinámico centrado en **65 Hz** sobre el bajo para permitir el paso del transitorio de peso del bombo.
  - **Banda Bark 2 (100-200 Hz):** Corte dinámico centrado en **120 Hz** sobre el bombo para preservar la articulación armónica del bajo.

---

## 🎛️ 11. Pipeline de Masterización Broadcast EBU R128

* **Loudness Integrado:** $-14.0 \pm 0.5$ LUFS.
* **True Peak:** $\le -1.0$ dBFS (prevención de distorsión inter-sample en conversión analógica).
* **Rango Dinámico (LRA):** Entre $6.0$ y $8.0$ LU (preservación de transitorios y dinamismo de pista).
* **Entregables Obligatorios en `~/Music/`:**
  1. Master PCM de alta resolución: `48 kHz / 24-bit WAV`.
  2. Master de distribución móvil / promo: `320 kbps CBR MP3`.
