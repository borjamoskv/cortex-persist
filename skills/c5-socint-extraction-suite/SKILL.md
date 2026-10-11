---
name: c5-socint-extraction-suite
display_name: Suite Soberana de Inteligencia Social (SOCINT C5-REAL)
description: 'Extracción e ingestión SOCINT en Reddit, Substack y X sin APIs de pago, con clasificación epistémica cuádruple y detección de astroturfing. Dispara con "socint suite", "inteligencia social", "scraping redes", "reddit socint", "extraer subreddit", "substack socint", "auditar tweet", "analizar hilo x", "hilo twitter audit".'
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

# Suite Soberana de Inteligencia Social (SOCINT C5-REAL)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Esta suite unifica los tres vectores principales de extracción, normalización e ingestión de telemetría discursiva en plataformas públicas (**X / Twitter**, **Substack** y **Reddit**), eludiendo muros de registro, JavaScript reactivo forzado y APIs corporativas cerradas mediante acceso directo a silicio y endpoints estáticos en Python stdlib pura.

---

## 🏛️ 1. Axiomas Cibernéticos SOCINT (Aforismo 5)

En redes públicas, la señal está sumergida en un océano de *cheap talk*, bots de astroturfing y cárteles de recomendación mutua. La suite aplica el **Aforismo 5 de C5-REAL** (*Lo voluntario vale menos que lo involuntario*):
1. **Señales Voluntarias (Baja Exergía / Alto Ruido):** Declaraciones de intenciones, hilos promocionales, retórica moral, hypes de 100x y testimonios no reproducibles.
2. **Señales Involuntarias (Alta Exergía / Evidencia Dura):** Hashes de commit (`git`), referencias legales vinculantes (`BOE/BORME`), benchmarks empíricos con métricas reproducibles ($p_{99}$, $ms$, $tokens/s$), timestamps inmutables, ratio de controversia en Reddit y grafos topológicos de recomendación cruzada.

---

## ⚙️ 2. Motor CLI en Silicio (`scripts/socint_extract.py`)

La suite dispone de una herramienta de línea de comandos en **stdlib pura** (cero dependencias externas como Selenium, Playwright o wrappers hinchados):

```bash
# Extracción de post o hilo en X (Twitter)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://x.com/username/status/1844000000000000000" \
  --format markdown

# Extracción de entrega completa de Substack
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://danluu.substack.com/p/velocity" \
  --format markdown

# Auditoría de Cártel de Recomendaciones (PODs) en Substack
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://substack_name.substack.com" \
  --audit-pods --format json

# Barrido de subreddit con cálculo de Índice de Controversia
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "r/LocalLLaMA" \
  --limit 25 --format markdown

# Extracción profunda de hilo y árbol de comentarios en Reddit
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://www.reddit.com/r/MachineLearning/comments/1fxyzab/title/" \
  --depth 3 --limit 50 --output /tmp/reddit_audit.md
```

---

## 🛰️ 3. Adaptador X (Twitter): Hilos, Métricas y Desacople de Auth

### Pipeline de Resolución Multicapa (Fail-Closed)
1. **Capa 1 (FixTweet / FxTwitter API):**
   - Invocación directa a `https://api.fxtwitter.com/{user}/status/{id}`.
   - Retorna payload JSON sin cookies ni sesión: texto íntegro, fecha ISO, autor (`followers`, `screen_name`), media (fotos/vídeos), tweet citado (*quoted tweet*) y métricas (`likes`, `retweets`, `replies`, `views`).
2. **Capa 2 (Twimg Syndication Endpoint):**
   - Si Capa 1 falla, consulta el CDN de sindicación oficial de X:
     `https://cdn.syndication.twimg.com/tweet-result?id={id}&token={token}`.
   - Extrae el texto plano del tweet y metadatos del autor sin ejecutar JavaScript.
3. **Capa 3 (Proxy Autónomo Jina Reader):**
   - `https://r.jina.ai/https://x.com/{user}/status/{id}` para rescate en formato Markdown.
4. **Capa 4 (Headless / JXA):** Degradación al subagente `/browser` o automatización de Safari local si se activa un WAF severo.

---

## 📰 4. Adaptador Substack: Archivos, Artículos y Auditoría de PODs

### Bypass de WAF y API JSON Nativa
1. **Lectura de Artículo Completo:**
   - Invocación a `https://{domain}/api/v1/posts/{slug}`.
   - Retorna el HTML semántico limpio del artículo, eliminando popups de suscripción y paywalls blandos.
2. **Archivo Cronológico Completo:**
   - Invocación paginada a `https://{domain}/api/v1/archive?sort=new&limit=50&offset=0`.
   - Indexa títulos, fechas, número de palabras, comentarios y recuento de likes.
3. **Auditoría Forense de PODs (Cárteles de Recomendación):**
   - Endpoint: `https://{domain}/api/v1/recommendations`.
   - Detecta si la publicación forma parte de un círculo de auto-promoción inflada (*reciprocal backscratching*) analizando si $>15$ newsletters se recomiendan circularmente sin base técnica.
4. **Fallback RSS:** `https://{domain}/feed` para publicaciones con DNS personalizado o WAF activado.

---

## 👾 5. Adaptador Reddit: Minería de Hilos, Árboles y Controversia

### Extracción Determinista vía Sufijo `.json`
1. **Barrido de Subreddit:**
   - Endpoint: `https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}`.
   - Filtra automáticamente posts fijados institucionales (`stickied: true`).
2. **Árbol Jerárquico de Comentarios:**
   - Endpoint: `https://www.reddit.com/r/{subreddit}/comments/{id}.json?depth={depth}&limit={limit}`.
   - Parsea recursivamente el árbol de respuestas (`kind == "t1"`), preservando autor, puntuación neta y profundidad de anidamiento.
3. **Métrica C5 de Índice de Controversia:**
   $$\text{Controversy Index} = (1.0 - \text{upvote\_ratio}) \cdot \sqrt{N_{\text{comments}}}$$
   - Valores elevados señalan debates con polarización real o *brigading* artificial; valores bajos con ratio $>0.95$ señalan consenso comunitario o cámaras de eco.

---

## ⚖️ 6. Matriz de Clasificación Epistemológica (Las 4 Categorías C5-REAL)

Todo texto procesado por la suite se clasifica automáticamente en 4 estratos epistémicos:

| Categoría Epistémica | Indicadores Lingüísticos & Silicio | Veredicto Operativo |
| :--- | :--- | :--- |
| **1. Hechos Verificados** | Hashes SHA-256, repos GitHub, URLs canónicas, DOIs, leyes/BOE, contratos. | **Señal Base** (Aceptado sin fricción) |
| **2. Evidencia Experimental** | Benchmarks ($ms$, $tokens/s$, $p_{99}$), telemetría, tamaños muestrales ($n$), costes auditados. | **Verificable** (Sujeto a reproducción) |
| **3. Modelos & Doctrina** | Arquitecturas de sistemas, topologías causales, invariantes, teoría de la información. | **Marco Conceptual** (Evaluado por consistencia) |
| **4. Especulación / Sesgo** | Hype ("100x", "game changer"), profecías no falsables, afirmaciones sin evidencia. | **Anergía / Ruido** (Etiquetado como *Cheap Talk*) |

### Ratio de Señal/Ruido (SNR):
$$\text{SNR} = \frac{N_{\text{hechos}} + N_{\text{experimental}} + N_{\text{modelos}}}{N_{\text{hechos}} + N_{\text{experimental}} + N_{\text{modelos}} + 1.5 \cdot N_{\text{especulacion}}}$$

---

## 🔒 7. Contrato de Autonomía Fail-Closed (Ω10 / Ω11 / Ω12)

- **Ω10 (Zero Pause Transition):** El agente no debe detener la ejecución ni solicitar autorización al operador para saltar de la API primaria al fallback de sindicación o lector Markdown ante un error HTTP (403, 429).
- **Ω11 (Degradación Determinista):**
  $$\text{API Directa JSON} \xrightarrow{\text{error}} \text{Sindicación/RSS} \xrightarrow{\text{error}} \text{Proxy Lector Markdown} \xrightarrow{\text{error}} \text{Subagente Browser}$$
- **Ω12 (Atestación Limpia):** Los datos extraídos deben exportarse limpios de scripts o trackers, respetando la Manta de Markov y almacenándose en `/tmp/` o en el artefacto de la conversación.
