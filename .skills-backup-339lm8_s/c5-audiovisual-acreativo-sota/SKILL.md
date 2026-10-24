---
name: c5-audiovisual-acreativo-sota
display_name: Audiovisual Acreativo SOTA
description: Enruta producción musical, acústica, voz, vídeo, diseño visual y arquitectura
  solar. Dispara con "audiovisual hub", "acreativo hub", "producción audiovisual",
  "FL Studio", "Suno", "Remotion", "auditoría de vídeo".
role: arquitecto
allowed_roles:
- arquitecto
- ejecutor
- auditor
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# Audiovisual Acreativo SOTA

> **Directiva Declarativa:** Enruta módulos bajo demanda y conserva su ámbito y contrato.

## Selección

1. Identifica la petición y busca el alias en la tabla o en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia renders, scripts, servicios externos ni cambios de documentos.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
Normaliza mayúsculas y acentos, prioriza coincidencias exactas y respeta límites de palabra.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos de ámbito global

| Módulo completo | Nombres y triggers conservados |
| --- | --- |
| [c5-rubin-acoustic-linter](references/modules/c5-rubin-acoustic-linter/MODULE.md) | `c5-rubin-acoustic-linter`, `/c5-rubin-acoustic-linter`, `linter acústico`, `auditoría de mezcla`, `purga de nata en audio`, `rubin audit`, `dedup apfs audio`, `crest factor audio`, `medir compresión` |
| [c5-metodo-acreativo](references/modules/c5-metodo-acreativo/MODULE.md) | `c5-metodo-acreativo`, `/c5-metodo-acreativo`, `metodo acreativo`, `método acreativo`, `transducción soberana`, `oraculo de apoptosis`, `protocolo rubin`, `crear arte c5`, `produccion musical c5` |
| [c5-spatial-audio-architect](references/modules/c5-spatial-audio-architect/MODULE.md) | `c5-spatial-audio-architect`, `/c5-spatial-audio-architect`, `auditoría dsp`, `audio espacial`, `criticar estéreo`, `hoa`, `binaural`, `ambisonics`, `spatial audio` |
| [flstudio-mcp-production](references/modules/flstudio-mcp-production/MODULE.md) | `flstudio-mcp-production`, `/flstudio-mcp-production`, `FL Studio`, `flstudio-mcp`, `balag-omega`, `generador de musica`, `compilar flp`, `piano roll script`, `microtonal house` |
| [djstudio-mcp](references/modules/djstudio-mcp/MODULE.md) | `djstudio-mcp`, `/djstudio-mcp`, `dj studio`, `djstudio`, `dj studio mcp`, `harmonize dj studio`, `stems dj studio`, `transiciones dj`, `crossover linkwitz riley`, `rekordbox xml` |
| [suno-bracket-tagging](references/modules/suno-bracket-tagging/MODULE.md) | `suno-bracket-tagging`, `/suno-bracket-tagging`, `suno prompt`, `udio tags`, `prompt musical`, `etiquetas suno`, `control causal audio`, `audio ai`, `jailbreak acustico`, `des-plasticar audio` |
| [soulseek-p2p-audio-acquisition](references/modules/soulseek-p2p-audio-acquisition/MODULE.md) | `soulseek-p2p-audio-acquisition`, `/soulseek-p2p-audio-acquisition`, `descargar musica`, `descargar cancion`, `soulseek download`, `adquisicion audio p2p`, `auditoria espectral flac`, `bajar flac soulseek`, `fake flac` |
| [c5-media-platform-epistemology](references/modules/c5-media-platform-epistemology/MODULE.md) | `c5-media-platform-epistemology`, `/c5-media-platform-epistemology`, `procesar audio largo`, `scraping spa`, `falsos positivos http 200`, `adquisicion opus nativo`, `rip opus youtube`, `itag 251` |
| [f5tts-voice-cloning-sota](references/modules/f5tts-voice-cloning-sota/MODULE.md) | `f5tts-voice-cloning-sota`, `/f5tts-voice-cloning-sota`, `clonar voz`, `sintetizar voz`, `f5-tts`, `f5tts`, `voice clone`, `prosodia tts`, `nota de voz ia` |
| [gflow-browser-cinema-sovereign](references/modules/gflow-browser-cinema-sovereign/MODULE.md) | `gflow-browser-cinema-sovereign`, `/gflow-browser-cinema-sovereign`, `gflow browser`, `cine gflow`, `flow google mcp`, `sovereign cinema`, `estudio gflow`, `gflow v4`, `character anchor veo`, `veo 2 browser`, `dialogue engine gflow`, `cockpit gflow`, `remotion gflow` |
| [pika-generative-video-pipeline](references/modules/pika-generative-video-pipeline/MODULE.md) | `pika-generative-video-pipeline`, `/pika-generative-video-pipeline`, `pika art`, `pika tutorial`, `pika camera`, `pikaffects`, `pika prompt`, `generación vídeo pika`, `pikaffects sota` |
| [remotion-audio-reactive-video](references/modules/remotion-audio-reactive-video/MODULE.md) | `remotion-audio-reactive-video`, `/remotion-audio-reactive-video`, `video reactivo a la musica`, `audio reactivo`, `remotion audio reactive`, `visualizador de musica`, `audio visualizer`, `video musical reactivo` |
| [youtube-remotion-sota](references/modules/youtube-remotion-sota/MODULE.md) | `youtube-remotion-sota`, `/youtube-remotion-sota`, `youtube remotion`, `remotion render`, `react video synthesis`, `renderizar vídeo remotion` |
| [c5-video-quality-audit](references/modules/c5-video-quality-audit/MODULE.md) | `c5-video-quality-audit`, `/c5-video-quality-audit`, `calidad de video`, `psnr ssim`, `diferencia de compresion`, `video quality diff`, `auditoría de compresion`, `medir vmaf`, `auditoría ffmpeg video` |
| [c5-neural-face-swap-cuadrilla](references/modules/c5-neural-face-swap-cuadrilla/MODULE.md) | `c5-neural-face-swap-cuadrilla`, `/c5-neural-face-swap-cuadrilla`, `face swap`, `deepfake cuadrilla`, `intercambio facial`, `c5 face swap` |
| [c5-poster-and-sign-craft](references/modules/c5-poster-and-sign-craft/MODULE.md) | `c5-poster-and-sign-craft`, `/c5-poster-and-sign-craft`, `remasterizar cartel`, `rotular letrero`, `cambiar texto cartel`, `sign craft`, `filtro vintage comic`, `bajar contraste imagen`, `quitar contraste duro`, `poster remaster`, `maquetación cartel`, `analizar cartel`, `flyer underground`, `auditoría tipográfica cartel` |
| [c5-solar-thermodynamic-architecture](references/modules/c5-solar-thermodynamic-architecture/MODULE.md) | `c5-solar-thermodynamic-architecture`, `/c5-solar-thermodynamic-architecture`, `sun path`, `análisis solar`, `confort térmico`, `estudio de sombras`, `fanger pmv`, `helio-arquitectura`, `bioclimático` |
