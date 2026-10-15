---
name: c5_epistemic_publishing_and_typography_extensions
description: Protocolos especializados de publicación y tipografía C5-REAL: Ingesta de aforismos en frases-sin-nata, Bajada al Barro, Calibración Litográfica de carteles, Paleta Cromática HTML/Mermaid, Estructura de 6 Bloques para ensayos, Anclaje Sacádico Selectivo (SSA) y Compilación de PDFs con Typst 0.15+.
trigger: "model_decision"
---

# Extensiones de Publicación, Tipografía y Diseño Visual (C5-REAL)

## 1. Protocolo Canónico de Ingesta de Aforismos ('frases-sin-nata' / Omnipresencia Territorial)
Cuando el usuario emita aforismos, proposiciones o sentencias de alta exergía —tanto operando en el workspace de `frases-sin-nata` como si la sesión carece de workspace activo—, el agente DEBE resolver de forma autónoma la ruta física canónica en `/Users/borjafernandezangulo/10_PROJECTS/frases-sin-nata` y ejecutar de forma atómica y sin requerir recordatorios:
0. *Sub-Protocolo de Audio-Anclaje Acústico:* Si la sentencia acompaña a un enlace sonoro (Bandcamp, SoundCloud, YouTube Music, Spotify), el agente DEBE inspeccionar los metadatos de la pista (álbum, género, características de producción) y fijarla formalmente como `Audio-Anclaje` en la cabecera del cristal y en la glosa del manuscrito.
1. *Anclaje en Manuscrito:* Incorporar las sentencias en `MANUSCRIPT_V3/APENDICE_II_AFORISMOS.md` actualizando el contador cardinal del encabezado.
2. *Sincronización de Índice:* Actualizar el contador de aforismos en `MANUSCRIPT_V3/00_INDICE_GENERAL.md`.
3. *Registro Lexicográfico y Visual:* Registrar la entrada correspondiente bajo formato dual («Bajada al Barro») en `EL_BORJARIO.md`, ejecutar `python3 scripts/generate_borjario_visuals.py` para regenerar la matriz de activos vectoriales (`assets/borjario_visuals/*.svg`) y actualizar el Atlas interactivo (`EL_BORJARIO_ATLAS_VISUAL.html`), auditando y purgando cualquier esquema ASCII duplicado que el script pudiera inducir en el archivo Markdown.
4. *Compilación y Linter en Silicio:* Ejecutar `python3 scripts/compile_v3.py` para re-ensamblar `FRASES_SIN_NATA_V3_LIBRO_COMPLETO.md`, verificando 100% de hipervínculos internos, cero comandos LaTeX prohibidos y cero violaciones del C5 Linter.
5. *Cristal Epistémico y Portapapeles:* Generar el cristal formal en `brain/` e inyectar proactivamente la tarjeta biónica en `pbcopy`.
6. *Silencio Termodinámico:* Emitir respuesta sucinta con la tarjeta en bloque ` ```text ` y firma topológica activa.
7. *Commit Atómico en Repositorio:* Realizar un commit git inmediato en `frases-sin-nata` registrando la cristalización (`feat(aforismo): ...`), asegurando que solo se incluyan los archivos de origen (`MANUSCRIPT_V3/`, `EL_BORJARIO.md`, `*.svg`, `*.html`, `AUDITORIA_C5.md`) y respetando el `.gitignore` que excluye imágenes rasterizadas (`*.png`).

## 2. Titulación Dual Lexicográfica («Bajada al Barro»)
En glosarios, diccionarios conceptuales (ej. *El Borjario*) y taxonomías, todo concepto debe incluir su denominación formal seguida de su traducción coloquial de asfalto:  
`### N. [Concepto Formal de Alta Exergía] («Lema / Explicación Bajada al Barro»)`

### 2.1. Protocolo de Doble Despliegue ante Petición «Bajada al Barro»
Cuando el operador emita la directiva «bajada al barro» (o equivalentes de asfalto):
1. **Inyección en Portapapeles (`pbcopy`):** Formatear y copiar de forma prioritaria la Tarjeta Biónica en Unicode Sans-Bold Universal (ancho estricto ≤68 caracteres, cero asteriscos `**` dentro de ` ```text `).
2. **Paridad Isomórfica en Documento Canónico (PDF y Markdown):** Incorporar simultáneamente la sección formal «Traducción Integral de Asfalto (Bajada al Barro)» tanto en el artefacto Markdown como en el documento PDF compilado, garantizando que el archivo físico final contenga la traducción dual y no quede como un residuo efímero en el chat.

## 3. Invariante de Calibración Tonal y Anti-Contraste Digital en Arte Gráfico e Ilustración
1. **Veto al Contraste Digital Duro:** Ante cualquier solicitud de remasterización, retoque o filtrado de ilustraciones, carteles, cómics o fotomontajes artísticos (o ante observaciones de *«tiene mucho contraste»*), queda estrictamente prohibido aplicar curvas S empinadas, ecualización CLAHE agresiva o filtros de enfoque que aplasten los negros a 0 digital o quemen las luces a 255.
2. **Estándar de Imprenta Litográfica:** El agente DEBE aplicar compresión de rango dinámico estilo imprenta analógica:
   - *Negro Mate Aterciopelado:* Piso mínimo de luminancia elevado al 7-9% (RGB ~18-23).
   - *Papel de Autor / Rag Paper:* Techo máximo de altas luces comprimido al 92-94% (RGB ~235-240).
   - *Micro-grano Unificador:* Inyección de micro-textura de papel litográfico (~1% de amplitud) para amalgamar fotomontajes con trazos ilustrados.
3. **Preservación Estricta de Jerarquía de Planos:** En rotulación o sustitución de textos en perspectiva, los objetos oclusivos en primer plano (vidrios, líquidos, ramas) deben segregarse mediante máscaras curvilíneas fieles, preservando su comportamiento óptico de absorción y refracción.

## 4. Estándar Gráfico y Diagramas de Silicio (Mermaid & ASCII)
1. **Topología Vertical Obligatoria en Diagramas de Flujo:** En diagramas Mermaid, utilizar prioritariamente `flowchart TD` (Top-Down) o subgraphs verticales sobre `flowchart LR`. Los diagramas horizontales largos desbordan la pantalla partida en IDEs y clientes móviles.
2. **Acotamiento de Diagramas de Texto ASCII/Unicode:** Todo diagrama o caja de texto dentro de bloques cercados debe tener un ancho máximo estricto de **68 caracteres** para prevenir roturas de línea accidentales al pegarse en WhatsApp o terminales estándar.
3. **Estilos de Nodo en Mermaid:** Emplear clases de estilo sobrias alineadas con la paleta C5-REAL:
   - Nodos de inicio/núcleo: fondo `#1e293b`, borde `#38bdf8`, texto `#f8fafc`.
   - Nodos de fallo/DROP: fondo `#450a0a`, borde `#f87171`, texto `#fecaca`.
   - Nodos de éxito/COMMITTED: fondo `#064e3b`, borde `#34d399`, texto `#d1fae5`.

## 5. Paleta Cromática Canónica C5-REAL (Diseño, Widgets y Visualización)
En cualquier desarrollo de interfaces, widgets HTML, SVG o visualizaciones de datos:
1. **Sustrato Neutro Mate (Sin Negros ni Blancos Crudos):**
   - Fondo Base: `#0d1117` (Negro grafito mate / RGB 13, 17, 23).
   - Fondo de Tarjeta / Panel: `#161b22` (Gris oscuro con textura visual / RGB 22, 27, 34).
   - Borde Estructural: `#30363d` (Gris pizarra / RGB 48, 54, 61).
   - Texto Primario: `#e6edf3` (Blanco roto de imprenta / RGB 230, 237, 243).
   - Texto Secundario / Metadatos: `#8b949e` (Gris medio legible / RGB 139, 148, 158).
2. **Acentos Semánticos de Exergía:**
   - *Cian Silicio (Acción / Primario):* `#38bdf8` (Acento vivo) y `#0284c7` (Borde interactivo).
   - *Ámbar Soberano (Punto Ω / Destacado):* `#fbbf24` (Acento dorado) y `#b45309` (Borde de advertencia).
   - *Esmeralda de Atestación (Éxito / Commit):* `#34d399` (Acento verde) y `#047857` (Borde de éxito).
   - *Carmesí de Apoptosis (Error / DROP):* `#f87171` (Acento rojo) y `#b91c1c` (Borde de fallo).

## 6. Estructura Canónica de 6 Bloques para Artículos y Cristales Epistémicos (Modo B)
Todo ensayo formal o cristal epistémico generado en `brain/` debe articularse obligamente bajo esta jerarquía:
1. **Cabecera Formal con Metadatos:** Título descriptivo `# ...`, autoría invariable (`**Por Borja Fernández Angulo**\n*Investigador en Sistemas Complejos*`), UUID/SHA-256 e índice temporal.
2. **Abstract Ejecutivo en Callout:** `> [!NOTE]` con el resumen ejecutivo de 3 a 5 líneas y el diagnóstico central de exergía.
3. **Sección 1 (Contexto & Tesis):** Planteamiento del problema, desmantelamiento de premisas previas y delimitación del territorio.
4. **Sección 2 (Desglose Arquitectónico & Diagrama Vertical):** Formalización técnica con diagrama Mermaid (`flowchart TD`) estilizado según la paleta C5-REAL.
5. **Sección 3 (Evidencia Empírica & Telemetría):** Datos duros en tablas estructuradas o JSONs medidos en silicio local.
6. **Sección 4 (Discusión Dialéctica & Falsación Popperiana):** Delimitación de límites asintóticos bajo el Principio de Correspondencia de Bohr ($\mathcal{R}_{PF}$, $\mathcal{E}_E$).
7. **Sección 5 (Dictamen de Ingeniería & Próximos Pasos):** Conclusiones ejecutivas y recomendaciones de acción inmediata.
8. **Colofón Formal:** Firma obligatoria e inmutable de Borja Fernández Angulo.

## 7. Protocolo de Anclaje Sacádico Selectivo (SSA) y Serialización Multiplataforma
1. **Regla de Oro SSA (Selective Saccadic Anchoring):** El anclaje por prefijo en negrita se restringe **exclusivamente a lexemas de alto contenido informacional** (sustantivos, verbos operativos, adjetivos de dominio, métricas y cifras). Las partículas gramaticales (*stop-words*: el, la, los, las, un, una, de, del, en, a, al, con, sin, por, para, y, o, que, se, su) permanecen **100% lisas (sin negrita)**.
2. **Algoritmo de Micro-Anclaje por Longitud de Lexema (SSA):**
   - Palabras de 1 a 3 letras (si no son stop-words): 1 letra en negrita (`**r**ed`, `**b**it`, `**d**aw`).
   - Palabras de 4 a 6 letras: 2 letras en negrita (`**ar**nés`, `**to**ken`, `**da**to`, `**la**tencia`).
   - Palabras de 7 a 9 letras: 3 letras en negrita (`**sis**tema`, `**mem**oria`, `**des**pacho`, `**con**senso`).
   - Palabras de $\ge 10$ letras: 4 letras en negrita (`**ter**modinámica`, `**cons**trucción`, `**des**integración`).
3. **Matriz de Serialización Triple:**
   - **Target A — Markdown Estándar (`**pre**fijo`):** Para artículos formales, GitHub, Obsidian y documentación web.
   - **Target B — Mensajería Móvil WhatsApp / Telegram (`*pre*fijo`):** Emplear asterisco simple para negrita, bullets limpios (`▪`, `▫`, `╰─►`) y cero tablas multipilar (>2 columnas).
   - **Target C — Unicode Sans-Bold Universal (`𝗽𝗿𝗲`fijo):** Para cajas ASCII/ANSI, bloques de código cercados (````text ... ````), terminales de macOS y notas planas.

## 8. Invariante de Compilación Tipográfica de PDFs en Silicio (Typst 0.15+ & Gate Pre-Entrega)
1. **Motor de Compilación Preferente (Typst 0.15+):** Compilar directamente desde especificaciones `.typ` hacia PDF mediante `/opt/homebrew/bin/typst compile`, empleando fuentes canónicas del sistema (`New Computer Modern` para cuerpo y fórmulas, `Menlo` o `DejaVu Sans Mono` para identificadores y código).
2. **Veto a la Coma Doble en Math Typst:** En expresiones matemáticas Typst, queda estrictamente prohibido utilizar `\,` tras una coma (ej. `cal(X), \, cal(S)`).
3. **Veto a Cajas Indivisibles en Citaciones Extensas (Anti-Justificación Rota):** En listados de papers o referencias múltiples, queda terminantemente prohibido utilizar `box(...)` indivisibles.
4. **Invariante Sticky en Encabezados y Cajas Críticas:** Obligatorio activar `#show heading: set block(sticky: true)`.
5. **Gate Obligatorio de Auditoría Visual Pre-Entrega (Zero-Broken-Layout Gate):** Antes de entregar cualquier PDF, rasterizar todas sus páginas a PNG (`pdftoppm -png -r 150 <pdf> <prefix>`) e inspeccionar visualmente cada una con `view_file`.
