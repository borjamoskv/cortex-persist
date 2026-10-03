---
name: safari-browser-agent
display_name: Agente Autónomo de Navegación Safari (MCP Dual-Engine v6.0 Sexagesimal Apex Sovereign)
description: 'Orquestación y control soberano de Safari mediante MCP v6.0 Apex Sovereign y puente nativo JXA/WindowServer (sin WebDriver). Suite sexagesimal completa de 60 herramientas: OCR local en silicio vía Apple Vision Framework, grabación/reproducción determinista de macros JSON, auditoría Core Web Vitals (TTFB, FCP, LCP, DOM), mocking de geolocalización HTML5, síntesis de voz somática con enrutamiento de audio a ~/Music, inspección WebGL/Canvas con volcado de frames, extracción de grafo semántico epistémico (JSON-LD, microdatos, H1-H6), organización higiénica y deduplicación de pestañas, exportación a PDF vectorial nativo, recolección de activos (PDFs, datasets, audio), monitoreo de WebSockets/SSE (streaming en vivo), captura full-page cosida, diffing estructural del DOM, inyección de estilos CSS (modo oscuro, paywall unblur), rellenado semántico multi-campo (fill-form), modo lectura destilado, control multimedia HTML5 (SoundCloud, YouTube), bloqueo de red/mocking, detección anti-bot
  (Turnstile, Cloudflare WAF, reCAPTCHA, DataDome), quiescencia dual, congelación/restauración de sesiones, Set-of-Marks neón, promesas CSP-safe, clics por coordenadas/Shadow DOM y exportación de cookies Netscape. Dispara con "safari agent", "navegar safari", "mcp safari", "controlar safari", "safari browser agent", "safari automation", "inspeccionar safari", "mac maestro", "automatizar safari jxa", "bypass webdriver", "mac maestro bridge", "control jxa macos", "windowserver automation".'
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

# Skill: Safari Browser Agent v6.0 Sexagesimal Apex Sovereign (BABYLON-60)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este protocolo rige la interacción, observabilidad profunda y navegación autónoma en **Safari** sobre macOS a través del servidor MCP `safari` (`safari-mcp v6.0 Apex Sovereign`) y su CLI binaria `safari-cli`.

---

## 1. Arquitectura y Capacidades Sexagesimales (60 Herramientas)

- **Identidad Base-60 (BABYLON-60):** La suite alcanza la cota sexagesimal exacta de **60 herramientas MCP nativas**, conformando la arquitectura más densa, rápida y resiliente de control de navegador en macOS.
- **OCR 100% Local en Silicio (`safari_ocr_screen_region`):** Micro-binario nativo Swift (`c5_vision_ocr`) acoplado directamente al framework `Vision` de Apple. Extrae texto impreso y manuscrito de cualquier captura de Safari en menos de 30 ms sin enviar datos a la nube.
- **Grabación y Reproducción Determinista de Macros (`safari_record_action_macro` / `safari_replay_macro`):** Captura en caliente secuencias de clics, inputs, scrolls y navegación del usuario o agente en JSON reproducible, permitiendo re-ejecución con cadencia controlada y verificación de estado.
- **Auditoría de Rendimiento Core Web Vitals (`safari_audit_performance_lighthouse`):** Diagnóstico en runtime de TTFB, First Paint, FCP, duración de ejecución de scripts, profundidad del árbol DOM y memoria del JS Heap.
- **Mocking de Geolocalización (`safari_intercept_geolocation`):** Simulación precisa de coordenadas GPS (`latitude`, `longitude`, `accuracy`) sobre la API HTML5 sin necesidad de proxies ni emuladores externos.
- **Transducción Somática de Texto a Voz (`safari_synthesize_text_to_speech`):** Síntesis de voz nativa en macOS sobre artículos o elementos DOM, con enrutamiento automático de audio generado a `~/Music/` según la invariante de centralización musical.
- **Inspección de Lienzos Gráficos & WebGL (`safari_canvas_webgl_inspector`):** Inspección de contextos 2D, WebGL y WebGPU, telemetría de GPUs y volcado de fotogramas renderizados a PNG.
- **Grafo Epistémico Semántico (`safari_extract_semantic_graph`):** Extracción unificada de esquemas JSON-LD (`schema.org`), meta-etiquetas OpenGraph/Twitter, y la jerarquía ontológica de encabezados `H1`-`H6`.
- **Higiene y Organización de Pestañas (`safari_tab_grid_organizer`):** Desglose analítico de dominios activos y deduplicación segura de pestañas redundantes.
- **Exportación Vectorial a PDF (`safari_export_pdf`):** Generación de documentos PDF limpios mediante el subsistema de exportación de Safari y fallback raster de alta densidad.

---

## 2. Catálogo Sexagesimal de 60 Herramientas MCP

| # | Categoría | Herramienta | Descripción y Uso |
| :- | :--- | :--- | :--- |
| 1 | **Pestañas** | `safari_list_tabs` | Lista ventanas y pestañas (ID, título, URL, activo). |
| 2 | | `safari_new_tab` | Abre nueva pestaña en la ventana indicada o frontal. |
| 3 | | `safari_navigate` | Navega con espera de ciclo de vida (`load`, `domcontentloaded`). |
| 4 | | `safari_switch_tab` | Enfoca pestaña por índice numérico. |
| 5 | | `safari_focus_tab` | Encuentra y enfoca reactivamente por coincidencia de texto. |
| 6 | | `safari_close_tab` | Cierra pestaña activa o especificada. |
| 7 | **Navegación** | `safari_go_back` | Retrocede en el historial. |
| 8 | | `safari_go_forward` | Avanza en el historial. |
| 9 | | `safari_reload` | Recarga con opción de omitir caché. |
| 10 | **Sincronización**| `safari_wait_for` | Espera reactiva a aparición/desaparición de selectores. |
| 11 | | `safari_wait_for_quiescence`| Espera inactividad simultánea en DOM y peticiones de red. |
| 12 | **Extracción** | `safari_get_page_content` | Markdown estructurado de alta fidelidad. |
| 13 | | `safari_get_interactive_elements` | Mapea interactivos indexados `[0..n]`. |
| 14 | | `safari_get_accessibility_tree` | Árbol semántico de accesibilidad. |
| 15 | **Interacción**| `safari_click` | Clic de alta fidelidad, soporte `x, y` y Shadow DOM. |
| 16 | | `safari_hover` | Simula cursor sobre menús desplegables. |
| 17 | | `safari_fill` | Rellena inputs con reactividad para React/Vue/Angular. |
| 18 | | `safari_fill_form` | Rellenado semántico inteligente multi-campo en una transacción. |
| 19 | | `safari_select_option` | Selecciona opciones en menús `<select>`. |
| 20 | | `safari_press_key` | Emite pulsaciones de teclado (`Enter`, `Tab`, `Escape`). |
| 21 | | `safari_scroll` | Desplaza página o enfoca un selector específico. |
| 22 | | `safari_drag_and_drop` | Arrastra y suelta entre selectores o coordenadas. |
| 23 | | `safari_upload_file` | Carga archivo local en input file vía DataTransfer. |
| 24 | | `safari_handle_dialog` | Intercepta y auto-responde a `alert`, `confirm` y `prompt`. |
| 25 | **Estilos & Marca**| `safari_inject_styles` | Inyecta modo oscuro, elimina banners fijos y paywalls. |
| 26 | | `safari_highlight_elements` | Superpone cajas delimitadoras neón Set-of-Marks. |
| 27 | **Multimedia** | `safari_extract_media` | Extrae flujos de audio/vídeo HTML5. |
| 28 | | `safari_media_control` | Control HTML5 de audio/vídeo (play, seek, volume, rate). |
| 29 | **Almacenamiento**| `safari_get_storage` | Inspecciona cookies, localStorage y sessionStorage. |
| 30 | | `safari_set_storage` | Inyecta datos en cookies o web storage. |
| 31 | | `safari_clear_storage` | Purga selectiva de cookies y almacenamiento web. |
| 32 | | `safari_export_cookies` | Exporta cookies en formato estándar Netscape. |
| 33 | **Telemetría** | `safari_get_console_logs` | Captura errores y advertencias de consola JS. |
| 34 | | `safari_get_page_metrics` | Tiempos de carga, recursos, viewport y scroll. |
| 35 | | `safari_get_network_activity` | Sniffing en tiempo real de peticiones fetch y XHR. |
| 36 | | `safari_monitor_events` | Monitoreo asíncrono de WebSockets y Server-Sent Events. |
| 37 | **Red & Defensa**| `safari_intercept_network` | Bloquea rastreadores o simula rutas con respuestas sintéticas. |
| 38 | | `safari_detect_anti_bot` | Diagnóstico de Cloudflare Turnstile, reCAPTCHA y WAF. |
| 39 | **Viewport** | `safari_set_viewport` | Redimensiona la ventana de Safari. |
| 40 | | `safari_emulate_device` | Presets de geometría y User-Agent (iPhone, iPad, Desktop). |
| 41 | **Motor & Scripts**| `safari_evaluate_script` | Evaluación JS con resolución nativa de Promesas. |
| 42 | **Visual** | `safari_take_screenshot` | Captura de pantalla nativa con Set-of-Mark opcional. |
| 43 | | `safari_capture_full_page` | Captura continua de página completa ensamblada verticalmente. |
| 44 | **Scraping** | `safari_scrape_batch` | Extracción por lotes estructurada en una pasada. |
| 45 | **Sesiones** | `safari_save_session` | Congela pestañas, scroll y storage a snapshot JSON en disco. |
| 46 | | `safari_restore_session` | Restaura pestañas y navegación desde snapshot JSON. |
| 47 | **Activos Web**| `safari_harvest_assets` | Recolecta PDFs, datasets, imágenes o audio a `~/Music`. |
| 48 | **DOM** | `safari_diff_dom` | Detección diferencial de mutaciones en el árbol del DOM. |
| 49 | **Lectura** | `safari_toggle_reader_mode` | Conmuta Reader Mode nativo o destila texto limpio. |
| 50 | **Documentos** | `safari_export_pdf` | Exporta pestaña a PDF vectorial nativo o de alta resolución. |
| 51 | **Macros** | `safari_record_action_macro` | Graba interacciones DOM en macro reproducible. |
| 52 | | `safari_replay_macro` | Reproduce secuencia de acciones con cadencia configurable. |
| 53 | **Rendimiento**| `safari_audit_performance_lighthouse` | Auditoría Core Web Vitals (TTFB, FCP, LCP, DOM Depth). |
| 54 | **Geolocalización**| `safari_intercept_geolocation` | Emula y sobrescribe geolocalización HTML5 (GPS mock). |
| 55 | **Voz** | `safari_synthesize_text_to_speech` | Síntesis de voz somática macOS (audio guardado en `~/Music`). |
| 56 | **Visión** | `safari_ocr_screen_region` | OCR local en Apple Silicon vía Apple Vision Framework. |
| 57 | **Memoria** | `safari_profile_memory_leaks` | Audita nodos huérfanos y retención en JS Heap. |
| 58 | **Gráficos** | `safari_canvas_webgl_inspector` | Inspecciona Canvas 2D/WebGL/WebGPU y vuelca fotogramas PNG. |
| 59 | **Semántica** | `safari_extract_semantic_graph` | Extrae grafos JSON-LD, microdatos Schema.org y árboles H1-H6. |
| 60 | **Organización**| `safari_tab_grid_organizer` | Analiza desglose de dominios y deduplica pestañas. |

---

## 3. Guía Rápida CLI (`safari-cli`)

```bash
# Exportación y Visión Local
safari-cli pdf ~/Desktop/informe_safari.pdf
safari-cli ocr
safari-cli tts "Análisis de exergía completado" --voice=Monica --save

# Macros de Acción y Reproducción
safari-cli macro start
safari-cli macro stop
safari-cli replay-macro /tmp/mi_macro.json --delay=300

# Diagnóstico, Rendimiento y Epistemología
safari-cli vitals
safari-cli memory-profile
safari-cli semantic-graph
safari-cli canvas --snapshot
safari-cli organize-tabs deduplicate --apply

# Geolocalización Soberana
safari-cli geolocation 43.2630 -2.9350 10.0
safari-cli geolocation --clear
```
