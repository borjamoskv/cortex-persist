---
name: music_assets_centralization_invariant
description: Invariante obligatoria que fuerza a centralizar o enlazar automáticamente en ~/Music cualquier activo sonoro, descarga (Soulseek/yt-dlp), máster, export o sesión musical procesada por el agente.
---

# Invariante de Centralización de Activos Musicales (Directorio Canónico ~/Music)

Todo activo de audio, música, discografía, directo, sesión, stem o export sonoro que el agente descargue (vía Soulseek, yt-dlp, streaming, etc.), procese o genere **DEBE quedar inmediatamente disponible y centralizado en la biblioteca raíz del usuario: `~/Music/` (`/Users/borjafernandezangulo/Music/`)**.

## 1. Prohibición de Aislamiento en Subdirectorios Locales
Queda estrictamente prohibido confinar descargas o archivos de audio terminados exclusivamente en carpetas internas de proyectos (ej. `10_PROJECTS/soulseek-agent/downloads/`) o temporales sin que exista un acceso directo canónico en `~/Music/`.

## 2. Política de Enlace o Destino Directo
- Si la herramienta descarga por defecto en un directorio interno del proyecto, el agente **DEBE crear de forma inmediata y automática un enlace simbólico (`ln -s`)** en `~/Music/<Nombre_Carpeta_o_Artista>` apuntando a los archivos descargados, o moverlos/guardarlos directamente en `~/Music/`.
- `~/Music/` es el espacio soberano de indexación para el usuario, reproductores de audio, Serato, DJ.Studio y archivo discográfico.
