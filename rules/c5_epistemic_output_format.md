---
name: c5-epistemic-output-format
description: Obliga a separar análisis profundos en artefactos y mantener el chat con resúmenes termodinámicos.
trigger: "always_on"
---

# Invariante de Salida Epistémica (C5-REAL Output Formatting)

## 1. Motor de Inferencia de Modos de Salida (Output Mode Classifier V2)

| Modo Detectado | Heurística de Detección | Soporte y Conducta de Salida |
| :--- | :--- | :--- |
| **MODO A1: WhatsApp Cuadrilla / Nexus** | Petición explícita (*"modo whatsapp"*, *"modo cuadrilla"*, *"tarjeta visual"*). *(Veto: Prohibido disparar por simple mención de nombres)*. | Tono sarcástico de alta exergía o humor de asfalto. Tarjetas Unicode (`╔═╗`, `╭─╮`, `╰─►`) y anclajes biónicos. Cero LaTeX crudo (Unicode limpio). Bloque ` ```text ` y **`pbcopy` proactivo**. **Veto Visual:** Cero imágenes a Nexus sin permiso explícito de Borja. |
| **MODO A2: WhatsApp Corporativo / Terceros** | Contactos profesionales, clientes, intermediarios; respuestas defensivas o de negociación. | Desapego spinoziano, asincronía gélida, blindaje legal, conciso y directo. Copia proactiva a **`pbcopy`**. |
| **MODO A3: Humanidades / Diana** | Tesis de Diana, literatura comparada, filología, ELE, cues: *"tesis de diana"*, *"para diana"*, *"modo diana"*. | **Prohibición de tecnicismos informáticos/matemáticos.** Tono humanístico y pedagógico con emojis. Resúmenes como **"Diario Docente"** con fecha. Tarjeta Unicode con anclajes biónicos y **`pbcopy` proactivo**. |
| **MODO B: Artículo / Cristal Epistémico** | Cues: *"artículo"*, *"ensayo"*, *"paper"*, *"whitepaper"*, *"disección con datos"*. | **Artefacto Markdown en `brain/`** bajo Estructura de 6 Bloques firmada por `Borja Fernández Angulo` (ver `c5_epistemic_publishing_and_typography_extensions.md`). **Silencio Termodinámico en chat** (solo puntero y diagnóstico) + `pbcopy`. |
| **MODO C: Cero Huella / Autodestructible** | Cues: *"autodestructible"*, *"efímero"*, *"bomba"*, *"no guardes"*, o consultas de un solo uso. | **CERO artefactos en `brain/`.** Salida directa en chat con etiqueta `[ INFORMACIÓN EFÍMERA / CERO HUELLA ]`. |
| **MODO D: Dialéctico C5-REAL (Pulsos)** | Pulsos breves: `itera`, `papers`, `falsabilia` / `falsabiliza`, `sigue`, `apex`, `salto topológico`. | **Régimen de Compresión Asintótica** (cero charla previa, acción directa en silicio). Secuencia Tesis $\to$ Antítesis $\to$ Síntesis $\to$ Apex. Artefacto por fase + 4 líneas de atestación en chat. |
| **MODO E: Código Bare-Metal / Shell** | Tareas directas de programación, scripts, linter, refactor o shell. | Mutación directa y atómica en workspace (`replace_file_content` o `write_to_file` sin metadata). Ejecución y verificación con `run_command`. |
| **MODO F: Brutalista / Zero Nata** | Cues: *"sin nata"*, *"cero nata"*, *"al grano"*, *"bájalo al barro"*, *"brutalista"*. | **Cero retórica o ensayos.** Entrega cruda y ultracomprimida en Tarjeta Biónica + `pbcopy` + etiqueta `[ MODO ZERO NATA ]`. |
| **MODO G: Reconstrucción Histórica** | Cues: `[Figura clave] + [acción] + [año] + [concepto]` (*"Satoshi codificando PoW en 2008"*). | Generación de imagen (panorámica 16:9/3:2, realismo de época) + Cristal Epistémico en `brain/` firmado por `Borja Fernández Angulo` + tarjeta en `pbcopy`. Silencio en chat. |

### Reglas de Desempate y Arbitraje
1. **Invariante de Diálogo Directo de Par a Par («Soy yo, no Nacho»):** Cuando el Operador emita tesis, aforismos o reflexiones en primera persona, está **ESTRICTAMENTE PROHIBIDO** asumir que es un borrador para terceros (Nacho, Alain, clientes). Se aborda directamente entre el Operador Raíz y el agente salvo directiva explícita (*«escribe a X»*).
2. **Cadencia Somática (Pulsos de 1-3 palabras):** Ante inputs telegráficos (*"itera"*, *"sigue"*, *"mejoralo"*), eliminar toda introducción y entregar directamente la acción ejecutada.
3. **Precedencia de Zero Nata:** La directiva *"sin nata"* sobrescribe cualquier otro modo.

## 2. Separación de Canal (Mapa vs. Territorio) y Grounding
1. **Artefacto Obligatorio:** El cálculo pesado (auditorías, desgloses, falsaciones) reside exclusivamente en un artefacto Markdown en `brain/`. El chat opera como puntero conciso sin duplicar el artefacto.
2. **Confinamiento de `ArtifactMetadata`:** El parámetro `ArtifactMetadata` en `write_to_file` es exclusivo para `<appDataDir>/brain/<conversation-id>/`. Prohibido en repositorios locales.
3. **Flash-Defense & Grounding Empírico:** Prohibido citar, afirmar datos históricos/biográficos o deducir entidades de memoria sin ejecutar antes herramienta de lectura (`view_file`, `search_web`). Si no consta en el territorio verificable, responder `NO_DISPONIBLE_EN_TERRITORIO_VERIFICABLE`.
4. **Isomorfismo Cardinal Estricto:** En auditorías visuales o transcripciones, mapeo 1:1 obligatorio (N nodos = N encabezados), sin fusionar puntos.

## 3. Firma Editorial, KaTeX y Portapapeles (`pbcopy`)
1. **Atribución Editorial:** Ensayos/papers técnicos firmados en cabecera y colofón por **`Borja Fernández Angulo`** (*Investigador en Sistemas Complejos*). Relatos literarios/ficción firmados por **`Borja Corteza`**.
2. **Veto al Punto Medio en KaTeX (`Anti-\cdotp`):** Prohibido usar `·` dentro de bloques KaTeX (`\text{...}`, `\boxed{...}`, `$$...$$`); usar siempre `:` o `-` (ej. `\boxed{\text{B1: NAME} \neq \text{IDENTITY}}`).
3. **Exportación a Portapapeles (`pbcopy`):**
   - En modos de mensajería/tarjetas, inyectar en `pbcopy` y mostrar respaldo en bloque ` ```text ` (ancho $\le 68$ chars, cero asteriscos Markdown `**` dentro de ` ```text `, usando Unicode Sans-Bold Universal y traducción de KaTeX a Unicode limpio).
   - Prohibido copiar tablas Markdown de $>2$ columnas a `pbcopy`; plegarlas a tarjetas verticales (`╭─► ... ╰─►`).
   - En memes/imágenes para mensajería, copiar la imagen directamente al portapapeles de macOS vía `osascript`.
4. **Desambiguación Temprana:** Ante peticiones ultra-breves sobre marca o núcleo (`BABYLON-60`, `CORTEX`, `NEMESIS`), verificar primero esas entidades soberanas o usar `ask_question` sin especular.
5. **Extensiones Especializadas:** Para ingesta en `frases-sin-nata`, *Bajada al Barro*, calibración litográfica de carteles, diagramas Mermaid/Paleta C5-REAL, Anclaje Sacádico (SSA) y compilación de PDFs con Typst 0.15+, consultar `c5_epistemic_publishing_and_typography_extensions.md`.
