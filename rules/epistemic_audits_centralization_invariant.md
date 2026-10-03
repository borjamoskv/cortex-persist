---
name: epistemic_audits_centralization_invariant
description: Invariante obligatoria que fuerza a centralizar, indexar y persistir toda auditoría epistemológica, falsación popperiana o análisis metrológico en el repositorio soberano ~/10_PROJECTS/AUDITORIAS_EPISTEMICAS/.
---

# Invariante de Centralización de Auditorías Epistémicas (Directorio Canónico ~/10_PROJECTS/AUDITORIAS_EPISTEMICAS/)

Toda auditoría epistemológica, falsación popperiana, análisis metrológico o deconstrucción de discurso (procedente de YouTube, papers científicos, podcasts, hilos de X/Twitter, artículos web o volcados externos) que el agente elabore **DEBE quedar inmediatamente persistida e indexada en el repositorio soberano del usuario: `/Users/borjafernandezangulo/10_PROJECTS/AUDITORIAS_EPISTEMICAS/`**.

## 1. Prohibición de Aislamiento Exclusivo en Carpetas Internas o Temporales
Queda estrictamente prohibido confinar este tipo de auditorías exclusivamente en carpetas internas de proyectos o en el directorio temporal de artefactos de sesión (`~/.gemini/antigravity/brain/...`).

## 2. Política de Clasificación y Nomenclatura
- **Canal YouTube:** `youtube/YYYY-MM-DD_youtube_<ID>_<slug>.md`
- **Papers y Literatura:** `papers/YYYY-MM-DD_paper_<doi_o_autor>_<slug>.md`
- **Podcasts y Audio:** `podcast/YYYY-MM-DD_podcast_<nombre>_<slug>.md`
- **Redes y Artículos Web:** `redes/YYYY-MM-DD_redes_<fuente>_<slug>.md`
- **Simulaciones Numéricas:** `simulaciones/YYYY-MM-DD_<tema>_simulation.json`

## 3. Actualización Obligatoria del Índice Maestro
Tras depositar cualquier auditoría nueva, el agente **DEBE actualizar el archivo maestro `README.md`** en `/Users/borjafernandezangulo/10_PROJECTS/AUDITORIAS_EPISTEMICAS/README.md` incorporando la entrada en la tabla cronológica con fecha, tipo, emisor, tema, calibración epistémica y enlace relativo.
