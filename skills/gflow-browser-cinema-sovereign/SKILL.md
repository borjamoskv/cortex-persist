---
name: gflow-browser-cinema-sovereign
display_name: Estudio Cinematográfico Soberano y Automatización Google Flow (v4.0 Apex)
description: 'Estudio virtual de cine, DAG narrativo, anclaje de personajes anti-drift, locución, subtítulos broadcast y puente Remotion TSX. Dispara con "gflow browser", "cine gflow", "flow google mcp", "sovereign cinema", "estudio gflow", "gflow v4", "character anchor veo", "veo 2 browser", "dialogue engine gflow", "cockpit gflow", "remotion gflow".'
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

# Skill: Estudio Cinematográfico Soberano y Automatización Google Flow (v4.0 Apex)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos)
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este protocolo rige la automatización profunda de Google Flow (`flow.google.com`), la orquestación cinematográfica en DAG, la eliminación del character drift en Veo 2, el diseño acústico/VFX fotoquímico, y el empaquetado directo hacia suites Remotion 4K sobre macOS Apple Silicon.

---

## 1. Arquitectura y Módulos de Silicio (gflow-browser-mcp v4.0.0)

El repositorio canónico reside en `/Users/borjafernandezangulo/10_PROJECTS/gflow-browser-mcp`:

1. **Driver Nativo Safari JXA (`safari_jxa.py` / `safari_subagent.py`):**
   - Introspección y control determinista sin Playwright ni Chromium headless.
   - Set-of-Marks visual con badges `@e1..@eN` para visión multimodal cero-alucinación.
   - Inyección Image-to-Video sintetizando objetos `File`/`DataTransfer` en el DOM sin diálogos del SO.
2. **Director Narrativo en DAG (`film_director.py`):**
   - Descompone premisas en una gramática de 4 planos (Master Wide, Tracking Medium, Focal Detail, Climax Revelation).
3. **Anclaje de Identidad de Personaje (`character_anchor.py`):**
   - Erradica el *character drift* en Veo 2 mediante contratos de ADN visual (`[CHARACTER CONTINUITY ANCHOR: ...]`), paleta hex y directivas de fisionomía persistente.
4. **Locución y Subtitulado Sincronizado (`dialogue_engine.py`):**
   - Síntesis de voz nativa en macOS (`say` / AVFoundation a 48 kHz).
   - Generación de subtítulos con timecodes milimétricos en formatos SubRip (`.srt`) y WebVTT (`.vtt`).
   - Construcción de filtros FFmpeg para quemado tipográfico de subtítulos.
5. **Cadena VFX Óptica & Color Grading (`vfx_pipeline.py` / `color_grade.py`):**
   - Grano fotoquímico 35mm/16mm, halación en altas luces y encuadre DCI Scope 2.39:1 / Academy 1.85:1.
   - Looks cinematográficos analógicos (Teal & Orange, Bleach Bypass, Technicolor 3-Strip).
6. **Ledger Criptográfico de Procedencia SCITT (`film_ledger.py`):**
   - Atestación formal conforme a SCITT RFC 9942 con cálculo de Merkle Root SHA-256 sobre prompts y videos.
7. **Cockpit HUD en Tiempo Real (`cockpit_tui.py`):**
   - Cuadro de mandos ANSI en terminal y dashboard visual `.gflow/cockpit.html`.
8. **Puente Remotion Studio (`studio_bridge.py`):**
   - Empaquetado de clips, subtítulos y composiciones TSX hacia `wild-mitxu-studios` con cálculo de sobres de audio RMS/SFM conformes con `StudioAssetAuditor`.

---

## 2. Herramientas MCP Clave (31 Herramientas)

- `gflow_safari_navigate`: Control de navegación y foco de pestaña en Safari.
- `gflow_safari_discover`: Mapeo completo de elementos interactivos y marcas SoM `@e1..@eN`.
- `gflow_safari_screenshot`: Captura nativa con badges Set-of-Marks.
- `gflow_browser_direct_film`: Desglose automático de premisas dramáticas en DAG cinematográfico.
- `gflow_character_anchor_register`: Registro de ADN visual y anclaje contra drift.
- `gflow_character_anchor_enrich`: Inyección de directivas de continuidad en prompts.
- `gflow_dialogue_synthesize`: Generación de locución, subtítulos SRT/VTT y audio master.
- `gflow_studio_export_remotion`: Empaquetado automático hacia `wild-mitxu-studios`.
- `gflow_cockpit_status`: Telemetría en tiempo real del vuelo y estado de Veo 2.

---

## 3. Cheatsheet CLI

```bash
# Diagnóstico de entorno y permisos
gflow-browser-mcp doctor

# Dirección de un cortometraje completo en DAG
gflow-browser-mcp direct "Un hacker solitario infiltrándose en una estación orbital" --preset anamorphic_cinema --shots 4

# Anclaje de personaje contra drift
gflow-browser-mcp anchor --id "mitxu" --name "Mitxu" --dna "leather jacket, neon mic" --prompt "DJ booth in bunker"

# Locución de diálogo y generación de subtítulos
gflow-browser-mcp dialogue --lines '[{"shot": 1, "speaker": "Mitxu", "text": "Emisión soberana activa.", "start": 0.0, "end": 2.5}]'

# Ensamblado de timeline con transiciones y masterización
gflow-browser-mcp stitch ./film_project_dir --transition crossfade

# Exportación directa a Remotion TSX
gflow-browser-mcp export-remotion ./film_project_dir/storyboard_manifest.json

# Live Cockpit HUD en terminal
gflow-browser-mcp cockpit --shot 3 --shots 4 --status "POLLING_VEO_2"
```

---

## 4. Invariante de Pruebas Unitarias FastMCP

Al probar herramientas registradas en servidores FastMCP (`MCPServer`):
- `server.list_tools()` es una corrutina asíncrona.
- Todo test que inspeccione herramientas debe decorarse obligatoriamente con `@pytest.mark.asyncio` y usar `await server.list_tools()`.
