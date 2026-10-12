---
name: soulseek-p2p-audio-acquisition
description: Protocolo autónomo de adquisición de audio de alta exergía, orquestación P2P en Soulseek (evasión de conflictos de puertos Errno 48, gestión de rate-limits y aislamiento de sockets) y auditoría espectral STFT/FFT para detección forense de fake FLACs upscales. Dispara con "descargar musica", "descargar cancion", "soulseek download", "adquisicion audio p2p", "auditoria espectral flac", "bajar flac soulseek", "fake flac".
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

# Protocolo de Adquisición de Audio y Orquestación P2P Soulseek (C5-REAL)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este protocolo rige la captura, verificación y upgrade de activos musicales hacia la máxima fidelidad acústica (FLAC/WAV máster) centralizada en `~/Music/`.

---

## Arquitectura de 5 Fases

### Fase 1: Normalización de Búsqueda y Deconstrucción de Tokens
Antes de consultar la red Soulseek o pasarelas de audio:
1. **Normalización ASCII-7:** Purgar tildes, diacríticos y caracteres especiales (`NFKD` -> ASCII).
2. **Deconstrucción de N-gramas:** Separar `[Artista]`, `[Título Núcleo]` y `[Remixer]`.
   - *Ejemplo:* `"Golden bug- sans le soléil - asa moto remix"` -> Probar sucesivamente:
     1. `"Golden Bug Sans Soleil Asa Moto"`
     2. `"Sans Soleil Asa Moto"`
     3. `"Golden Bug Sans Soleil"`
3. **Purga de Artículos / Ruido Sintáctico:** Eliminar partículas gramaticales que los rippers no indexan ("le", "la", "the", "official audio", "clip").

### Fase 2: Orquestación P2P Resiliente en Soulseek
Al interactuar programáticamente con la red Soulseek (`aioslsk`):

1. **Evasión de Colisión de Puertos (`Errno 48`):**
   - NUNCA usar los puertos por defecto `60000/60001` sin verificar previamente si están libres con `lsof -i :60000`.
   - Asignar siempre dinámicamente puertos en rango superior libre (ej. `60150/60151` a `60220/60221`):
     ```python
     network = NetworkSettings(listening=ListeningSettings(port=port_a, obfuscated_port=port_b))
     ```

2. **Invariante de Sesión Única (Serialización Estricta):**
   - Queda estrictamente prohibido ejecutar múltiples clientes concurrentes bajo la misma cuenta `SOULSEEK_USER`. Provoca congestión de colas, reseteo de sockets y baneos temporales.
   - Si se descargan lotes o colecciones, ejecutar las descargas secuencialmente dentro del mismo bucle de sesión asíncrona.

3. **Ranking Determinista de Fuentes:**
   - Priorizar peers con:
     1. `has_free_slots == True`
     2. `queue_size == 0`
     3. `avg_speed > 1024 KB/s`
     4. Formato de archivo: `.flac` o `.wav` con tamaño > 15 MB.

4. **Transferencia Directa:**
   - Encolar vía `Transfer` con `TransferDirection.DOWNLOAD`.
   - Monitorear `bytes_transfered` con detector de estancamiento (abortar si la velocidad es 0 por > 15 s).

### Fase 3: Fallback a Master Stream (Transcodificación Opus 48 kHz)
Si la red Soulseek devuelve 0 peers compartiendo máster sin pérdidas (común en lanzamientos recientes o tiradas de vinilo ultra-limitadas):
1. **Adquisición Inmediata vía Stream Oficial:**
   - Descargar el stream de mayor resolución disponible (Opus 48 kHz, formato 251):
     ```bash
     yt-dlp -f 251 --audio-quality 0 -x --audio-format flac -o "~/Music/<Subcarpeta>/%(title)s.%(ext)s" "<URL>"
     ```
   - Este formato garantiza respuesta en frecuencia plana hasta 20,0 kHz, evitando la distorsión del codificador MP3.

### Fase 4: Auditoría Espectral Forense STFT/FFT
1. Ejecutar el auditor espectral sobre el archivo obtenido:
   ```bash
   python -m soulseek.cli audit "~/Music/<Ruta>/<archivo>"
   ```
2. **Taxonomía de Calidad y Criterio de Exergía:**
   - `S_TIER_LOSSLESS` (`Cutoff >= 21.5 kHz` y Exergía > 95/100): Máster de estudio / vinilo genuino sin compresión destructiva.
   - `LOSSLESS_CONTAINER` (`Cutoff ~20.0 kHz`): Stream Opus 48 kHz transcodificado a contenedor FLAC o master digital web con brickwall en 20 kHz.
   - `VINTAGE_LOFI_BANDWIDTH` (`Cutoff 14.0 - 18.0 kHz` con densidad analógica): Filtrado paso-bajo deliberado por instrumentación analógica (sintetizadores vintage, estética lo-fi). Se preserva si la fuente es fidedigna.
   - `FAKE_FLAC_UPSCALE_320K/192K/128K` (`Cutoff < 19.5 kHz` con caída abrupta y dispersión digital): Fraude de contenedor. **Disparar re-búsqueda P2P de versión alternativa**.

### Fase 5: Consolidación y Centralización Soberana (`RULE[music_assets_centralization_invariant]`)
1. **Estructura de Directorios:**
   - Piezas sueltas: `~/Music/DOWNLOADED_AUDIO/` o carpeta por artista (`~/Music/<Artista>/`).
   - Lotes o colecciones temáticas: subcarpeta temática (ej. `~/Music/10_PERLAS_DARK_DISCO/`).
2. **Creación Inmediata de Enlaces Canónicos:**
   - Todo activo debe ser enlazado de forma inmediata en la raíz de `~/Music/`:
     ```bash
     ln -sf "/Users/borjafernandezangulo/Music/<Subcarpeta>/<archivo>.flac" "/Users/borjafernandezangulo/Music/<archivo>.flac"
     ```
