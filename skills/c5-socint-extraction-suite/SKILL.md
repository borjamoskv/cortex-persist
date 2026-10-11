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

Esta suite unifica los tres vectores principales de extracción, normalización, detección de astroturfing e ingestión de telemetría discursiva en plataformas públicas (**X / Twitter**, **Substack** y **Reddit**), eludiendo muros de registro, JavaScript reactivo forzado y APIs corporativas cerradas mediante acceso directo a silicio y endpoints estáticos en Python stdlib pura.

---

## 🏛️ 1. Axiomas Cibernéticos SOCINT (Aforismo 5)

En redes públicas, la señal está sumergida en un océano de *cheap talk*, bots de astroturfing y cárteles de recomendación mutua. La suite aplica el **Aforismo 5 de C5-REAL** (*Lo voluntario vale menos que lo involuntario*):
1. **Señales Voluntarias (Baja Exergía / Alto Ruido):** Declaraciones de intenciones, hilos promocionales, retórica moral, hypes de 100x y testimonios no reproducibles.
2. **Señales Involuntarias (Alta Exergía / Evidencia Dura):** Hashes de commit (`git`), referencias legales vinculantes (`BOE/BORME`), benchmarks empíricos con métricas reproducibles ($p_{99}$, $ms$, $tokens/s$), timestamps inmutables, ratio de controversia en Reddit, similitud léxica Jaccard entre cuentas bot y grafos topológicos de recomendación cruzada.

---

## ⚙️ 2. Motor CLI en Silicio (`scripts/socint_extract.py`)

La suite dispone de una herramienta de línea de comandos en **stdlib pura** (cero dependencias externas como Selenium, Playwright o wrappers hinchados) con soporte para almacenamiento SQLite WAL:

```bash
# Desenrollar hilo completo en X (Twitter) hasta la raíz
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://x.com/username/status/1844000000000000000" \
  --unfold --format markdown --save-vault

# Peritaje forense de usuario en Reddit con cálculo de entropía H(sub)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "u/username" --limit 50 --format markdown

# Búsqueda contextual dentro de un subreddit
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "r/LocalLLaMA" --search "quantization" --limit 20 --format markdown

# Extracción de vídeo y transcripción en YouTube (Zero-Auth)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format markdown

# Consultar estadísticas agregadas y telemetría de la Bóveda SQLite WAL
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py --vault-stats

# Ejecutar consulta SQL de lectura sobre el histórico archivado
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --vault-query "SELECT platform, author, snr_score FROM socint_vault WHERE snr_score > 0.60 LIMIT 10"

# Ejecución de la Suite de Verificación Determinista Offline (12/12)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/test_socint.py
```

---

## 🛰️ 3. Adaptador X (Twitter): Hilos, Perfiles y Desacople de Auth

### Pipeline de Resolución Multicapa (Fail-Closed)
1. **Capa 1 (FixTweet / FxTwitter API):**
   - Invocación directa a `https://api.fxtwitter.com/{user}/status/{id}` o `/status/{id}`.
   - Retorna payload JSON sin cookies ni sesión: texto íntegro, fecha ISO, autor (`followers`, `following`, `screen_name`), media (fotos/vídeos), tweet citado (*quoted tweet*) y métricas (`likes`, `retweets`, `replies`, `views`).
   - Endpoint de perfil: `https://api.fxtwitter.com/{username}` para telemetría forense de cuentas (fecha de creación, badges de verificación, ratios).
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
1. **Lectura de Artículo y Comentarios:**
   - Invocación a `https://{domain}/api/v1/posts/{slug}` y `https://{domain}/api/v1/posts/{post_id}/comments`.
   - Retorna el HTML semántico limpio del artículo y las reacciones de suscriptores, eliminando popups de suscripción y paywalls blandos.
2. **Archivo Cronológico Completo:**
   - Invocación paginada a `https://{domain}/api/v1/archive?sort=new&limit=50&offset=0`.
   - Indexa títulos, fechas, número de palabras, comentarios y recuento de likes.
3. **Auditoría Forense de PODs (Cárteles de Recomendación):**
   - Endpoint: `https://{domain}/api/v1/recommendations`.
   - Detecta si la publicación forma parte de un círculo de auto-promoción inflada (*reciprocal backscratching*) analizando si $>15$ newsletters se recomiendan circularmente sin base técnica.
4. **Fallback RSS:** `https://{domain}/feed` para publicaciones con DNS personalizado o WAF activado.

---

## 👾 5. Adaptador Reddit: Minería de Hilos, Árboles y Controversia

### Extracción Determinista con Degradación a Atom RSS
1. **Barrido de Subreddit:**
   - Endpoint primario: `https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}`.
   - Fallback de silicio: `https://www.reddit.com/r/{subreddit}/{sort}.rss` (Atom XML) si Reddit responde con HTTP 403 o 429 por límite de IP sin sesión.
4. **Dossier Forense de Usuario y Entropía Shannon:**
   - Analiza `/user/{username}/submitted` y calcula la entropía de Shannon sobre la distribución de subreddits:
     $$H_{\text{sub}} = -\sum p_i \log_2(p_i)$$
   - $H_{\text{sub}} < 0.85$ bits con $>5$ posts señala una cuenta monotemática utilizada para spam, shill o astroturfing.

---

## 📺 6. Adaptador YouTube: Metadatos y Transcripciones Zero-Auth

- **Extracción de Metadatos:** Invocación a `https://www.youtube.com/oembed?url={video_url}&format=json` (título, creador, miniatura).
- **Rescate de Transcripción:** Recuperación de subtítulos y audio transcrito mediante proxy autónomo Jina Reader sin requerir Google Cloud Console ni API keys.
- **Auditoría Epistemológica Integrada:** El texto del vídeo se somete a la matriz cuádruple C5-REAL para medir el ratio de afirmaciones fundamentadas frente a clickbait.

---

## 🤖 7. Detector Forense de Astroturfing (Similitud Jaccard N-Grams)

Para desenmascarar granjas de bots, cuentas títere (*sockpuppets*) y ataques Sybil:
1. **Extracción y Tokenización:** Descompone los comentarios en 3-gramas de palabras consecutivas.
2. **Similitud Jaccard por Pares:**
   $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
   Pares con $J(A, B) > 0.60$ se marcan como duplicados sintéticos.
3. **Score Ponderado de Riesgo Astroturf:**
   $$\text{Risk Score} = \min\left(1.0, 0.35 \cdot \text{ConcentraciónAutor} + 1.30 \cdot \frac{N_{\text{pares\_duplicados}}}{N_{\text{pares\_posibles}}}\right)$$
   - $\ge 55\%$: Campaña artificial / Granja de bots confirmada.
   - $25\% - 54\%$: Repetición léxica moderada o saturación de autor.
   - $< 25\%$: Discusión comunitaria orgánica.

---

## ⚖️ 8. Matriz de Clasificación Epistemológica (Las 4 Categorías C5-REAL)

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

## 🏛️ 8. Bóveda Local SQLite WAL (`socint_vault.db`)

Con la bandera `--save-vault`, toda investigación se archiva en una base de datos local SQLite bajo modo WAL (`PRAGMA journal_mode = WAL;`) en `~/.gemini/antigravity/socint_vault.db`:
- Registra `record_id`, `platform`, `target_type`, `url`, `author`, `title`, `raw_content`, `metrics_json`, `epistemic_counts_json`, `snr_score` y `captured_at`.
- Operación idempotente (`INSERT OR REPLACE`), protegiendo la evidencia histórica frente a eliminación de tweets o borrado de posts.

---

## 🔒 9. Contrato de Autonomía Fail-Closed (Ω10 / Ω11 / Ω12)

- **Ω10 (Zero Pause Transition):** El agente no debe detener la ejecución ni solicitar autorización al operador para saltar de la API primaria al fallback de sindicación o lector Markdown ante un error HTTP (403, 429).
- **Ω11 (Degradación Determinista):**
  $$\text{API Directa JSON} \xrightarrow{\text{error}} \text{Sindicación/RSS} \xrightarrow{\text{error}} \text{Proxy Lector Markdown} \xrightarrow{\text{error}} \text{Subagente Browser}$$
- **Ω12 (Atestación Limpia):** Los datos extraídos deben exportarse limpios de scripts o trackers, respetando la Manta de Markov y almacenándose en `/tmp/` o en el artefacto de la conversación.
