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

1. Identifica la petición y identifica la acción y el dominio, o una invocación explícita, en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia renders, scripts, servicios externos ni cambios de documentos.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
El resolver exige acción y dominio para peticiones contextuales, respeta negaciones y conserva invocaciones explícitas. Para una continuación, añade `--context "objetivo anterior del usuario"`; no infiere permiso para ejecutar procedimientos.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos disponibles

| Procedimiento | Intención contextual |
| --- | --- |
| [c5-media-platform-epistemology](references/modules/c5-media-platform-epistemology/MODULE.md) | Heurísticas para audio largo, evasión de falsos positivos SPA y adquisición directa Opus (itag 251) sin MP3. |
| [c5-metodo-acreativo](references/modules/c5-metodo-acreativo/MODULE.md) | Metodología formal del Método Acreativo, Oráculo de Apoptosis O(1), sustracción Rubin-Chentsov y Punto Fijo Ω. |
| [c5-neural-face-swap-cuadrilla](references/modules/c5-neural-face-swap-cuadrilla/MODULE.md) | Pipeline V5 SOTA de intercambio facial neuronal (InsightFace/BiSeNet CoreML + VideoToolbox) sobre Apple Silicon. |
| [c5-poster-and-sign-craft](references/modules/c5-poster-and-sign-craft/MODULE.md) | Remasterización y rotulación 4K de cartelería. |
| [c5-rubin-acoustic-linter](references/modules/c5-rubin-acoustic-linter/MODULE.md) | Auditoría determinista de exergía acústica (WCF, SFM, TSI, LPC), purga de nata sónica y dedup APFS clonefile. |
| [c5-solar-thermodynamic-architecture](references/modules/c5-solar-thermodynamic-architecture/MODULE.md) | Generación de diagramas de trayectoria solar (Sun Path), análisis vectorial de sombras y cartas psicrométricas de confort térmico (Fanger PMV/PPD, ISO 7730/ASHRAE 55). |
| [c5-spatial-audio-architect](references/modules/c5-spatial-audio-architect/MODULE.md) | Auditoría epistemológica y refactorización termodinámica de pipelines DSP de audio. Falsación de técnicas estéreo planar y diseño de arquitecturas Ambisonics (HOA) / Binaural. |
| [c5-video-quality-audit](references/modules/c5-video-quality-audit/MODULE.md) | Auditoría cuantitativa de compresión y fidelidad de video comparando secuencias cuadro a cuadro mediante PSNR, SSIM y VMAF. |
| [djstudio-mcp](references/modules/djstudio-mcp/MODULE.md) | Protocolo MCP, automatización de mezclas, stems y DSP Linkwitz-Riley para DJ.Studio y Rekordbox XML. |
| [f5tts-voice-cloning-sota](references/modules/f5tts-voice-cloning-sota/MODULE.md) | Clonación y síntesis de voz con F5-TTS en Apple Silicon MPS, prosodia orgánica y masterización Opus VOIP. |
| [flstudio-mcp-production](references/modules/flstudio-mcp-production/MODULE.md) | Integración MCP con FL Studio 2025, compilación .flp headless, BALAG-OMEGA a 48 kHz, microtonalidad Scala y carving Bark. |
| [gflow-browser-cinema-sovereign](references/modules/gflow-browser-cinema-sovereign/MODULE.md) | Estudio virtual de cine, DAG narrativo, WebSocket bridge, encadenamiento I2V y audio EBU R128. |
| [pika-generative-video-pipeline](references/modules/pika-generative-video-pipeline/MODULE.md) | Generación de vídeo e integración de audio en Pika Art con control de física (-motion, -fps), Pikaffects y Pika Audio Models. |
| [remotion-audio-reactive-video](references/modules/remotion-audio-reactive-video/MODULE.md) | Diseño y renderizado de vídeos reactivos al audio con Remotion, análisis FFT espectral y shaders WebGL/Canvas. |
| [soulseek-p2p-audio-acquisition](references/modules/soulseek-p2p-audio-acquisition/MODULE.md) | Adquisición P2P de audio en Soulseek y auditoría espectral STFT/FFT para detección forense de fake FLACs. |
| [suno-bracket-tagging](references/modules/suno-bracket-tagging/MODULE.md) | Ingeniería acústica forense, etiquetado estructurado [...] y rescate espectral en DAW para Suno, Udio y YuE. |
| [youtube-remotion-sota](references/modules/youtube-remotion-sota/MODULE.md) | Renderizado programático de vídeo SOTA utilizando React y Remotion engine. |
