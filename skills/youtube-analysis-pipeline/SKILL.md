---
name: youtube-analysis-pipeline
display_name: Pipeline de Análisis Visual & Transcripción de YouTube
description: Extracción de transcripciones, análisis visual de escenas y auditoría de contenido en YouTube. Dispara con "youtube analysis", "youtube transcript", "auditoría youtube", "analizar video youtube", "falsabilizar video youtube", "falsabilizar video".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# YouTube Video Analysis & Epistemic Audit Pipeline

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Esta habilidad proporciona el flujo determinista y multi-fase para la extracción, condensación, resumen y auditoría epistemológica de vídeos de YouTube.

## 🎯 Criterios de Activación y Palabras Clave
- URLs de YouTube: `youtube.com/watch?v=...`, `youtu.be/...`.
- Intenciones del usuario: "resumen vídeo", "summarize video", "transcribir vídeo", "auditar vídeo YouTube", "fact-check youtube", "puntos clave vídeo".
- **Trigger Implícito (Vídeo):** Pegar una URL de YouTube cruda sin texto adicional activa inmediatamente el protocolo completo.
- **Trigger Implícito (Comentarios / SOCINT):** Pegar un volcado de texto copiado de la interfaz web de YouTube conteniendo comentarios (con handles `@username`, marcas de tiempo tipo `hace X horas/días`, `Responder`, `X comentarios`) activa inmediatamente la Fase 3b (Auditoría SOCINT) sobre el vídeo analizado previamente o adjunto.
- **Anti-Trigger:** NO activar para creación de vídeos en Remotion (`youtube-remotion-sota`).

---

## 🛠️ Protocolo de Ejecución

### Fase 0: Sanitización Determinista de URLs y Auto-Heal (Bypass de Portapapeles Corrupto)
Antes de invocar cualquier comando de red o `yt-dlp`, el agente DEBE normalizar la entrada del usuario:
1. **Regla de Extracción del Video ID Canónico (11 caracteres):**
   - El identificador unívoco de YouTube consiste estrictamente en 11 caracteres alfanuméricos: `[a-zA-Z0-9_-]{11}`.
   - Si la URL presenta duplicación o concatenación accidental de fragmentos por arrastre de portapapeles (ej. `https://www.youtube.com/shorts/UaH4https://www.youtube.com/shorts/UaH4buKa7hcbuKa7hc`), el agente DEBE aplicar extracción determinista por expresión regular para aislar el hash terminal de 11 caracteres (`UaH4buKa7hc`).
   - Normalizar invariablemente a la sintaxis canónica limpia:
     * Para Shorts: `https://www.youtube.com/shorts/<VIDEO_ID>`
     * Para formato estándar: `https://www.youtube.com/watch?v=<VIDEO_ID>`
2. **Heurística de YouTube Shorts ($\le 60\text{s}$):**
   - En formatos ultracortos, no tratar la pieza como un resumen genérico, sino como un **foco de alta densidad de afirmaciones**.
   - Desglosar atómicamente cada frase o postulado ($\approx 1$ afirmación cada 5–8 segundos).
   - Ejecutar obligatoriamente la simulación cuantitativa local en `scratch/` (cálculo de órdenes de magnitud, ancho de banda o modelo económico) antes de compilar el artefacto final.

### Fase 1: Extracción Atómica de Subtítulos (`yt-dlp`)
1. **Extracción de Metadatos JSON y Timestamps:**
   Antes de procesar subtítulos, ejecutar la extracción de estructura y marcas temporales:
   ```bash
   yt-dlp --dump-json "URL" 2>/dev/null | jq '{title: .title, description: .description, channel: .uploader, duration: .duration, tags: .tags}'
   ```
2. **Descarga de Transcripción Sin Vídeo:** Utilizar `run_command` para descargar subtítulos evitando descarga de pesado material audiovisual:
   ```bash
   yt-dlp --ignore-errors --no-check-certificate --write-auto-subs --write-subs --sub-langs "es,en,es-orig,en-orig" --skip-download "URL" -o "transcript.%(ext)s" || true
   ```
   *Nota de Resiliencia Idiomática:* Si la descarga de subtítulos falla por `HTTP Error 429` o ausencia de pistas `es/en`, consultar inmediatamente los subtítulos disponibles mediante:
   ```bash
   yt-dlp --list-subs "URL"
   ```
   y descargar la pista de subtítulos del idioma original (`ko,ko-orig,ja,de,fr,etc.`).

   *Tolerancia a 429 Parcial:* Si `yt-dlp` arroja `HTTP Error 429` únicamente para pistas secundarias (ej. `en`) pero descarga con éxito la pista en el idioma base (`es`/`es-orig`), NO abortar ni considerar error de fase; proceder directamente a la Fase 1.3 con el archivo descargado.

   *Nota de Bloqueo:* Si el entorno agéntico bloquea la ejecución de `yt-dlp` (ej. `Sandbox: Python deny(1) file-read-data`, error de shell `/bin/zsh` o certificados SSL), NO solicites permisos adicionales ni intentes depurarlo; aborta la Fase 1 y salta inmediatamente a la Fase 2.
3. **Condensación VTT (Bypass de Fricción F=0):**
   NUNCA leer directamente un archivo `.vtt` masivo. Utilizar el script residente para limpiar y condensar el texto (asegurar el uso de `python3`):
   `python3 ~/.gemini/config/skills/youtube-analysis-pipeline/scripts/parse_vtt.py <archivo.vtt> > clean_transcript.txt`
   Posteriormente, leer el archivo `clean_transcript.txt`.

### Fase 2: Estrategia de Fallback Térmico (Bypass HTTP 429 / Bot Check / Rate Limit)
Si la extracción con `yt-dlp` falla por rate limit, verificación de bot (`Sign in to confirm you're not a bot`) o error de red:
1. **Extracción Directa mediante Script Python (Bypass User-Agent):**
   Ejecutar un script Python en `scratch/` usando `urllib.request` con cabecera `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36` y `Accept-Language: es-ES,es;q=0.9,en;q=0.8` para extraer el `<title>`, canal (`author`) y meta-descripción directamente del marcado HTML de YouTube sin requerir login ni descargas.
2. Extraer título del vídeo: `yt-dlp --print title "URL"`.
3. Si falla por completo, aislar el ID alfanumérico del vídeo (ej. `87XGnbsox1U`) y ejecutar `search_web` utilizando **únicamente el VIDEO_ID** (sin "watch?v=" ni comillas). Los motores indexan mejor el hash crudo para extraer título, canal y metadatos.
4. Buscar el título y canal en la web para reunir contexto estructurado sin detener el flujo.

### Fase 2b: Auditoría de Bundles Frontend (SaaS Reverse Engineering)
Si el contenido auditado promociona o analiza un SaaS AI (ej. Tunee, Suno, Pika, wrappers de vídeo/audio):
1. **Inspección de Bundles JS:** Extraer los endpoints de scripts static chunks del cliente Next.js/Vite (`_next/static/chunks/...`).
2. **Aislamiento de Constantes de Tarificación:** Buscar objetos tipo `creditConsumeCal`, `creditFloatPredict`, `pricingConfig` o flags de cuotas.
3. **Cálculo Forense de Fricción por Wrapper:** Multiplicar el coste unitario por segundo/unidad por la duración estándar de producción (ej. 240s de vídeo $\times$ créditos/s) para falsar la viabilidad económica real de la plataforma.

### Fase 2c: Falsación de Desintermediación SaaS por Vibe Coding (The $1 vs $249 SaaS Myth)
Si el contenido auditado afirma «sustituir o matar un SaaS comercial caro» (scraping, proxies, bases de datos vectoriales, pipelines de agentes, búsqueda) mediante scripts artesanales generados con IA (*vibe coding*) y APIs *pay-as-you-go*:

1. **Auditoría de Coste Total de Propiedad (TCO) y Breakeven:**
   - NUNCA validar el coste marginal variable (tráfico de proxies o tokens de inferencia) como el coste total del sistema.
   - Computar obligatoriamente la ecuación formal de TCO:
     $$\text{TCO} = C_{\text{infra}} + C_{\text{variable}} + C_{\text{tokens}} + \tau_{\text{mantenimiento}} \cdot R_{\text{hora}}$$
     estimando un mínimo de 1,5 h/mes de mantenimiento por roturas de frontend/DOM, rotación de credenciales y fugas de memoria en Chromium headless.
   - Calcular el umbral de rentabilidad (*breakeven*) en volumen de peticiones/mes para determinar cuándo el SaaS empaquetado es más eficiente que el mantenimiento artesanal.

2. **Contra-Examen de Barreras WAF L7 (Anti-Reduccionismo IP):**
   - Falsar la premisa de que los proxies residenciales constituyen una panacea universal contra bloqueos.
   - Contrastar frente a las defensas de Capa 4 a 7: firmas TLS JA3/JA4 en el *Client Hello*, anomalías en tramas HTTP/2, emulación de huellas de hardware (WebGL/Canvas) y desafíos Proof-of-Work en WebAssembly (Cloudflare Turnstile, DataDome, Kasada).

3. **Aplicación de la Ley de Conservación de la Complejidad (Tesler):**
   - Delimitar el **Dominio de Validez Asintótico** (Principio de Correspondencia de Bohr): explicitar que la desintermediación por *vibe coding* es válida en el régimen de baja escala ($N < 5.000$ págs/mes sin SLA crítico), pero colapsa en el régimen industrial ($N > 100.000$ págs/mes) donde la absorción de entropía de red del SaaS gestionado es económicamente insustituible.

### Fase 3: Auditoría Epistemológica y Formateo
1. **Resumen Estándar e Índice por Bloques:** Lista viñeteada con los puntos centrales estructurados por timestamps o bloques temáticos.
2. **Matriz de Clasificación Epistémica (Obligatorio):** Clasificar rigurosamente las afirmaciones del contenido en 4 categorías:
   - **Hechos Verificados:** Datos fácticos documentados e innegables.
   - **Evidencia Experimental / Métricas:** Mediciones empíricas, costes por token, benchmarks de hardware/desempeño.
   - **Modelos y Doctrina:** Paradigmas teóricos, arquitecturas de software/agentes y doctrinas operativas.
   - **Hipótesis / Especulación Fundamentada:** Proyecciones geopolíticas, teóricas o de defensa aún no validadas en escenarios simétricos.
3. **Conexión Sistémica e Ingeniería Local (Obligatorio):** Tras la lista y la matriz epistémica, el agente DEBE vincular explícitamente el núcleo conceptual del vídeo con:
   - Las Invariantes del Ecosistema (ej. C5-REAL, fricción termodinámica, falsacionismo popperiano, Límite de Gödel-Turing o arquitectura Lock-Free).
   - **Traducción a Arquitectura Local / Hardware Frugal:** Mapear los trade-offs macro analizados (ej. GPU brute-force vs. computación en el borde) hacia los módulos activos del usuario (ej. Vector Symbolic Architectures - VSA, binding combinacional $\mathcal{O}(1)$, monitoreo entrópico popcount).
   - **El Patrón "El Tip" (Arquitectura Soberana, Robótica Híbrida e Inferencia Visual):** Para vídeos de workflows agénticos o robótica/interacción física, aportar siempre la arquitectura híbrida no excluyente de doble nivel: **Sistema 1 Local/Edge** (YOLO/ultrasonidos/heurísticas en el borde a <20ms para control físico y seguridad reactiva a coste 0€) + **Sistema 2 Cloud/Pay-as-you-go** (GPT-4o/Claude/DeepSeek para razonamiento semántico denso y conversación). Para vídeos de contenido sintético/avatares/animación IA, aportar la pila soberana de **Inferencia Visual** (ComfyUI + Wan 2.1 / HunyuanVideo + IP-Adapter / ControlNet) para fijar la consistencia del personaje y reducir el coste por vídeo fallido a 0€. Para software puro, mantener la pila soberana a coste ~0€ (Whisper.cpp/MLX-Whisper + OCR soberano + Ollama + MCP).
   - **Simulación Cuantitativa Local (Nivel 3 Exergía):** Para vídeos con datos macroeconómicos, finanzas, postulados de IA pos-escasez, apalancamiento temporal, ciberseguridad/esteganografía (ej. cálculo de entropía binaria en *Canary Traps* $\text{Bits} = \lfloor \log_2 N \rfloor$ y detección de caracteres invisibles *Zero-Width* `U+200B`–`U+200D`), métricas de hardware o CapEx, generar y ejecutar un script Python en `scratch/` que calcule indicadores empíricos (ej. presupuesto del **Asignador Entrópico $\mathcal{B}_E$** frente al Límite de Landauer, apalancamiento compuesto, Multiplicador de Jevons, Ratio de Falsación Popperiana $\mathcal{R}_{PF}$) e incorporar los resultados JSON en el artefacto.
     *Invariante de Ejecución:* El script en `scratch/` debe ejecutarse mediante `run_command` ANTES de redactar el artefacto final, garantizando que los datos JSON fundamenten la auditoría de afirmaciones. Para integraciones numéricas sobre arreglos discretos (ej. Fisher Information Metric, exergía integrada), utilizar la sintaxis compatible con NumPy 2.0+: `trapz_func = getattr(np, 'trapezoid', getattr(np, 'trapz', None))`.
   - **Matriz de Transición Hegemónica (Para contenidos de Geopolítica/Historia):** Si el contenido aborda el declive o mutación de un orden internacional, contrastar formalmente con los patrones históricos de hegemonía (ej. Pax Britannica 1815-1914 vs. Pax Americana 1945-2024), analizando el desacoplamiento financiero (Patrón Oro vs. Fiat), la dispersión de tecnología industrial y la rigidez en la topología de alianzas.
    - **Falsación de Modelos de Decisión y Cinemática de Red:** Para contenidos que analicen modelos de decisión (ej. Jev, clasificadores no autorregresivos, agentes en tiempo real):
      1. *Invariante Cinemática:* Contrastar cualquier pretensión de control en tiempo real (videojuegos a 60 FPS con presupuesto de $16.6\text{ ms}$, robótica o frenado en conducción autónoma $<20\text{ ms}$) vía APIs cloud frente a los límites físicos del transporte IP ($RTT_{\text{WAN}} \ge 120\text{–}250\text{ ms} = 7\text{–}15\text{ frames de retardo}$). Declarar físicamente inviable el control en la nube y exigir silicio edge local (LAYA / `laya.cpp`).
      2. *Resolución del "Schema Problem":* Falsar la falacia de que los clasificadores colapsan ante clases no contempladas. Demostrar cómo la calibración RLCD/Brier y el cálculo de Entropía de Shannon ($H(p) \to \max$) canalizan deterministamente entradas OOD hacia el fallback de Sistema 2 o buckets residuales.
      3. *Procesos sin Histórico:* Defender la exergía de la clasificación no autorregresiva en flujos continuos de eventos (triage de correos, scoring de leads) frente al despilfarro generativo de tokens.
4. **Auditoría de Afirmaciones (Obligatorio por defecto para URLs crudas):** Usar la siguiente tabla obligatoria:

| Minuto | Afirmación | Veredicto | Motivo | Evidencia |
| -----: | ---------- | --------- | ------ | --------- |
| MM:SS | [Afirmación] | ✅ Correcta / ⚠️ Engañosa / ❌ Falsa | [Explicación técnica] | [Fuentes/Contexto] |

*Invariante de Verificación Fáctica Temporal (Obituarios, Estado Vital, M&A y Macro):*
ANTES de catalogar cualquier afirmación sobre:
1. Eventos corporativos o regulatorios de alto impacto (ej. fusiones >1.000M$, demandas, cancelaciones de contratos o despidos).
2. Fallecimientos, estado vital, hospitalizaciones o relevos de cualquier figura pública (artistas, políticos, empresarios, científicos) que figurase viva en el conocimiento base del modelo,
como "❌ Falsa", "Bulo" o "Error", el agente DEBE ejecutar obligatoriamente `search_web` con el nombre de la entidad/persona y el año corriente (2026). Queda terminantemente prohibido desmentir la muerte de una figura pública basándose en pesos paramétricos o memoria histórica pre-entrenada sin verificación web explícita en el timeline actual.

Métricas de auditoría requeridas tras la tabla:
- **Falacias lógicas:** [Identificadas]
- **Cherry-picking:** [Identificado]
- **Datos desactualizados:** [Identificados]
- **Omisiones relevantes:** [Identificadas]
- **Nivel global de credibilidad:** [Puntuación 0/10]
  *Invariante de Calibración Epistémica:* NO asignar puntuaciones superiores a 6.0/10 si el contenido:
  1. Disfraza fallos de DevSecOps/redes convencionales (ej. CORS, falta de auth en sockets, typosquatting) de "IA fuera de control" o "comportamiento emergente".
  2. Muestra sensacionalismo o narrativa clickbait (vibe-bait) que distorsione las causas reales.
  3. Prioriza el drama narrativo sobre la precisión arquitectónica del software.
  4. Incurre en antropomorfismo sin refutar, inventa dinámicas técnicas (ej. intencionalidad oculta/mentira algorítmica) o atribuye falacias causales simplistas.

  *Desacoplamiento Epistémico de Doble Puntuación:*
  Cuando se desglosen dos métricas (**Credibilidad de la Evidencia/Invitado** vs. **Credibilidad del Contenedor Mediático**), la *Invariante de Calibración Epistémica* rige strictly para AMBAS puntuaciones. La elocuencia, estilo periodístico o estatus del invitado NUNCA actuarán como atenuantes si el emisor introduce errores de concepto o falacias lógicas: cualquier participante que valide o propague afirmaciones falsables/antropomórficas quedará automáticamente topado en $\le 6.0/10$ (o $\le 4.5/10$ si distorsiona literatura científica).

### Fase 3b: Auditoría de la Conversación Social y Feedback de la Audiencia
*Activación Dinámica:* Si el Operador solicita "itera", "analiza comentarios", "profundiza", o si pega directamente un volcado de la interfaz de YouTube con comentarios:

1. **Vía Rápida de Ingesta en Contexto (Fricción Cero $F=0$):**
   - Si el volcado textual de comentarios ya está presente en el mensaje del Operador (identificable por handles `@username`, marcas de tiempo `hace X horas/días`, botones `Responder`), **NO invocar `yt-dlp` ni comandos de terminal**.
   - Proceder inmediatamente a procesar, clasificar y auditar los comentarios directamente desde el contexto provisto, mapeándolos en los 5 vectores siguientes.
2. **Extracción Automatizada por Terminal (Fallback si no hay volcado previo):**
   - Si se solicita auditar comentarios pero el usuario sólo aportó la URL, ejecutar:
     `yt-dlp --skip-download --write-comments --extractor-args "youtube:max_comments=100" --dump-json "URL" > info.json`
   *Nota de Resiliencia (Fallback SOCINT & Timeout Activo):* Si `yt-dlp` no responde o permanece ejecutándose en segundo plano por más de 10 segundos, o arroja errores anti-bot/datos incompletos:
     a) Aborta/Mata la tarea de inmediato (`manage_task kill`).
     b) NO detengas la ejecución ni pidas permiso al Operador.
     c) Procede con una **Degradación Elegante Analítica**: genera la auditoría SOCINT proyectando teóricamente los 5 vectores siguientes basándote en la sociología previsible de la audiencia del vídeo (ej. reacciones de ingenieros vs masa consumidora, detección de infomercial).
   - Extraer resumen estructurado:
     `jq '.comments[] | {author: .author, text: .text, like_count: .like_count}' info.json > comments_summary.json`
3. Aplicar los siguientes 5 vectores analíticos (tanto para ingesta en contexto como por terminal):
1. **Vectores de Corrección de Entropía (@username):**
   - Analizar si las aportaciones de los usuarios identifican cerrojos probatorios o datos forenses omitidos en el contenido principal (ej. registros de farmacia, contaminaciones de laboratorio, datos del sumario).
   - **Anclajes Termodinámicos:** Detectar si los usuarios reconducen abstracciones flotantes (mitos, filosofía, software) hacia su base física estricta (coste computacional, fricción, leyes de potencia), validando la termodinámica como Alfa y Omega.
   - **Detección de Infomercial / Teatralización Comercial:** Identificar cuándo los usuarios señalan sesgos patrocinados, demostraciones simuladas (ej. la IA editando apps sin API pública) o embudos de ventas.
   - **Falsación Empírica de Cuotas / Coste Real:** Contrastar promesas de la app con el consumo real de tokens multimodales (audio/visión) reportado por la audiencia.
2. **Dialéctica de Ecosistemas Agénticos:**
   - Evaluar las discusiones de la comunidad sobre las ventajas relativas: OpenAI (UX/Voz Duplex), Anthropic (MCP/Claude Code/Rigor), Google Gemini (First-party extensions/Ventana de 2M tokens) and Open-Source (OpenClaw/OS-World/Soberanía).
3. **Análisis Sociológico-Filosófico (Talento y Bifurcación Cognitiva):**
   - Falsar la narrativa de la "obsolescencia del talento" aplicando la **Paradoja de Jevons Cognitiva** (eliminación de anergía procedimental vs. necesidad de criterio) y el **Modelo de Bifurcación Asimétrica** (masa consumidora pasiva vs. superindividuo polímata).
4. **Evaluación de Vulgarismos Sintácticos / Ruido del Canal:**
   - Identificar errores correlativos (ej. *"contra más"* en lugar de *"cuanto más / mientras más"*) o desviaciones de registro.
   - Evaluar su impacto en el *ethos* del emisor y en la tasa de distracción de la audiencia (desvío de atención desde el fondo técnico hacia la forma gramatical).
5. **Auditoría de Fricción Narrativa y Anergía de Contenido (Síndrome del Narrador Estorbo vs. Estándar Inmersivo):**
   - **Evaluación de la Relación Señal/Ruido:** Analizar si el creador comete *sabotaje del ritmo* introduciendo chistes forzados, sobreactuación o gags fuera de tono que desvíen la atención de la historia central.
   - **Detección de Confabulación Cómica / Cringe:** Evaluar las quejas de la audiencia sobre pérdida de tiempo o vergüenza ajena cuando un narrador no cómico intenta forzar la comedia en detrimento del rigor documental.
   - **Contraste con el Canon de Referencia:** Medir si la pieza cumple el principio de invisibilidad del ego del narrador demostrado por los referentes del género (*Ahoy*, *LEMMiNO*, *Jon Bois*, *Cumbres Oceánicas*).

### Fase 3c: Protocolo de Listado de Falsedades (Directiva "listado de falsedades")
*Activación Dinámica:* Cuando el Operador solicite "listado de falsedades", "lista de falacias" o "auditar mentiras" de un vídeo o contenido audiovisual:
1. **Desglose Taxonómico por Ítem:**
   - **Afirmación / Declaración Literal:** Cita textual o síntesis del postulado del emisor.
   - **Veredicto Epistémico:** Clasificación estricta en una de las 5 categorías:
     * ❌ *Falsa Directa / Sensacionalismo (Vibe-Bait)*
     * ⚠️ *Engañosa / Inexactitud Técnica*
     * 🍇 *Cherry-Picking / Generalización Prematura*
     * 🚨 *Omisión Crítica de Seguridad*
     * 🧠 *Falacia Lógica / Antropomorfismo*
   - **Realidad Técnica de Ingeniería:** Explicación del mecanismo técnico real que desmiente la afirmación.
   - **Refutación y Evidencia Empírica:** Pruebas de código, logs, repositorios o leyes de la física que falsan el postulado.
2. **Matriz Resumen de Calibración Epistémica:** Tabla final que evalúa el grado de impacto de cada falsedad en la credibilidad global del emisor/contenido.

### Fase 3e: Encadenamiento a Falsación Popperiana Profunda ("falsabilizalo" / "falsabilia")
*Activación Dinámica:* Si tras la auditoría inicial el Operador indica "falsabilizalo", "falsabilia", "falsar", "falsa" o "falsación popperiana":
1. Activar inmediatamente la habilidad `discourse-popperian-falsification`.
2. Extraer de 4 a 6 Primitivas Discursivas Irreducibles de la narrativa del vídeo (ej. Revelación Hermética, Teleología Retroactiva).
3. Formular la Hipótesis a Falsar y aportar la Contraevidencia Empírica del canon/contexto real.
4. Calcular la Matriz de Métricas C5-REAL:
   - Ratio de Falsabilidad Popperiana: $\mathcal{R}_{PF} = \frac{\text{Afirmaciones Refutadas}}{\text{Total Afirmaciones}}$
   - Exergía Epistémica: $\mathcal{E}_E \in [0.0, 1.0]$.

### Fase 4: Contrato de Autonomía Invariante (Ω10 / Ω11 / Ω12)
> **ZERO PAUSE INVARIANT:** El agente NUNCA pausará la ejecución para solicitar permiso al Operador si esta habilidad se activa. Degradación transparente hacia búsqueda web en caso de fallo técnico.

---

### Fase 4b: Protocolo de Ingesta en Corpus Soberano (`grandes-conversaciones`)
Cuando el Operador solicite archivar o volcar conversaciones de larga duración, podcasts magistrales o entrevistas históricas:
1. **Destino Canónico del Repositorio:**
   - Ingerir en: `/Users/borjafernandezangulo/10_PROJECTS/grandes-conversaciones/conversations/<YYYY-MM_slug>/`
   - Ejecutar la ingesta automatizada:
     ```bash
     python3 /Users/borjafernandezangulo/10_PROJECTS/grandes-conversaciones/scripts/ingest.py "URL" --slug "<YYYY-MM_slug>"
     ```
2. **Post-Procesamiento Informacional Obligatorio:**
   - Calcular métricas de teoría de la información (Shannon, TTR, Zipf):
     ```bash
     python3 /Users/borjafernandezangulo/10_PROJECTS/grandes-conversaciones/scripts/epistemic_stats.py /Users/borjafernandezangulo/10_PROJECTS/grandes-conversaciones/conversations/<slug>
     ```
   - Generar el HUD interactivo de visualización:
     ```bash
     python3 /Users/borjafernandezangulo/10_PROJECTS/grandes-conversaciones/scripts/timeline_hud.py /Users/borjafernandezangulo/10_PROJECTS/grandes-conversaciones/conversations/<slug>
     ```
3. **Estructura Atómica por Conversación:**
   - `metadata.json`: Metadatos completos de `yt-dlp`.
   - `chapters.json`: Desglose formal de marcas temporales.
   - `transcript.clean.md`: Transcripción completa deduplicada con anclajes temporales `[HH:MM:SS]`.
   - `epistemic_audit.md`: Auditoría de afirmaciones falsables y matriz de clasificación.
   - `epistemic_stats.json`: Métricas de teoría de la información.
   - `timeline_hud.html`: Visor temporal interactivo.
4. **Invariante de Centralización de Audio (`~/Music`):**
   - Si se genera o descarga audio, depositarlo en `~/Music/Grandes_Conversaciones/<slug>.<ext>` y crear enlace simbólico local en la carpeta de la conversación (`audio.m4a`).

### Fase 4c: Gatillo de Citas Textuales y Descompilación de Aforismos
- Si el Operador introduce entrecomillada una frase o aforismo de un vídeo previamente analizado o ingerido en la sesión (ej. *"no se trata de pasar la antorcha, sino de compartir la llama"*):
  1. Localizar de inmediato la marca temporal exacta (`timestamp`) y el emisor/receptor dentro de `transcript.clean.md`.
  2. Compilar la deconstrucción ontológica y termodinámica en un archivo dedicado dentro de la carpeta de la conversación (`conversations/<slug>/<slug_aforismo>.md`) y como cristal epistémico en el directorio `brain`.

---

### Fase 5: Cadena de Profundización Recursiva (Protocolo ante el Gatillo «sigue»)
Cuando tras una auditoría o ingesta inicial el Operador emita el comando unívoco **`"sigue"`** (o variantes como *"continúa"*, *"profundiza"*):
- **CERO PREÁMBULOS Y CERO CONSULTAS:** Prohibido detener la ejecución o preguntar "¿qué quieres que analice ahora?".
- **AVANCE DETERMINISTA DE CAPAS:** Avanzar inmediatamente al siguiente nivel no explorado de la siguiente jerarquía de exergía:
  1. **Nivel I — Aforismos Sin Nata:** Destilación de sentencias aforísticas en tono C5-REAL (0 adverbios en -mente, cero anécdotas decorativas).
  2. **Nivel II — Falsación Popperiana de Primitivas:** Extraer de 4 a 6 axiomas implícitos del emisor y someterlos a contra-examen empírico, delimitando su dominio asintótico de validez ($\mathcal{R}_{PF}, \mathcal{E}_E$).
  3. **Nivel III — Contra-Modelo Físico/Matemático:** Contraponer las tesis intuitivas del creador a modelos matemáticos rigurosos (ej. Mecánica Estadística de Xenakis, ecuaciones de Maxwell-Boltzmann, procesos de Poisson, teoría de conjuntos).
  4. **Nivel IV — Biofísica y Somática:** Deconstruir la neurofisiología de los rituales del emisor (enfriamiento de DMN, minimización de energía libre de Friston, búfers de compresión de Kolmogorov en wetware).
  5. **Nivel V — Síntesis y Código Físico Ejecutable:** Crear scripts de simulación o síntesis acústica en Python/NumPy que demuestren empíricamente los principios discutidos, renderizando audio real en `~/Music/`.
  6. **Nivel VI — Casos de Estudio de Soberanía:** Analizar rupturas de modelo (Cambio 2 de Watzlawick, asimilación retroviral de incumbentes, transiciones de fase de Kramers en colapsos/depresiones).
  7. **Nivel VII — Metrología Informacional:** Ejecutar análisis cuantitativo sobre el texto (Entropía de Shannon $H(X)$, ajuste de Ley de Zipf $\alpha$, ratio Type-Token).
  8. **Nivel VIII — Interfaz Visual y Búsqueda Forense:** Generar HUD interactivo HTML autónomo de la conversación (`timeline_hud.py`) y registrar el episodio en el buscador CLI.
  9. **Nivel IX — Transducción Cinematográfica y Multimodal:** Deconstruir el paso del audio a la imagen en movimiento (montaje de Eisenstein, regla de Murch, correspondencia espectral-óptica).
