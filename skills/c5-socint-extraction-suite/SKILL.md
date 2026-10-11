---
name: c5-socint-extraction-suite
display_name: Suite Soberana de Inteligencia Social (SOCINT C5-REAL)
description: 'Suite SOCINT omnivectorial en 11 plataformas (X, Substack, Reddit, YouTube, HN, Bluesky, Telegram, GitHub, Mastodon, Polymarket, Wikipedia) con detección de astroturfing y bóveda SQLite. Dispara con "socint suite", "inteligencia social", "scraping redes", "reddit socint", "substack socint", "auditar tweet", "analizar hilo x".'
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

# Suite Soberana de Inteligencia Social (SOCINT C5-REAL Omnivectorial)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Esta suite unifica la extracción, normalización, detección de astroturfing y auditoría epistemológica de telemetría discursiva en **11 plataformas públicas**, eludiendo muros de registro, JavaScript reactivo forzado y APIs corporativas cerradas mediante acceso directo a silicio y endpoints estáticos en Python stdlib pura.

---

## 🌐 1. Matriz de Cobertura Omnivectorial (11 Plataformas)

| Plataforma | Adaptador en Silicio | Mecanismo de Extracción Zero-Auth | Telemetría / Entidad Extraída |
| :--- | :--- | :--- | :--- |
| **X (Twitter)** | `XAdapter` | FixTweet API (`api.fxtwitter.com`) & CDN Twimg Syndication | Tweets, hilos completos (`--unfold`), métricas, perfiles. |
| **Substack** | `SubstackAdapter` | REST Archive API (`/api/v1/archive`), Posts y RSS | Artículos, comentarios de suscriptores, cárteles (PODs). |
| **Reddit** | `RedditAdapter` | JSON API nativa con degradación a Atom RSS (`.rss`) | Hilos, subreddits, búsqueda, dossiers y entropía $H_{\text{sub}}$. |
| **YouTube** | `YouTubeAdapter` | oEmbed API (`youtube.com/oembed`) & Proxy Jina | Título, creador, miniatura, transcripción íntegra de audio. |
| **Hacker News** | `HackerNewsAdapter` | Algolia REST API (`hn.algolia.com`) & Firebase v0 | Historias, puntos, árboles anidados de comentarios, karma. |
| **Bluesky** | `BlueskyAdapter` | AT Protocol Public AppView (`public.api.bsky.app`) | Posts, hilos descentralizados, reposts, likes, perfiles. |
| **Telegram** | `TelegramAdapter` | Vista previa web estática de canales (`t.me/s/`) | Mensajes, recuento de vistas, canales de reenvío. |
| **GitHub** | `GitHubAdapter` | Atom Feeds de actividad (`github.com/{u}.atom`) y commits | Eventos públicos, historial de commits, issues y PRs. |
| **Mastodon** | `MastodonAdapter` | REST API pública de instancias federadas (`/api/v1/statuses`) | Toots, reblogs, favoritos y respuestas federadas. |
| **Mercados de Predicción** | `PredictionMarketAdapter` | Polymarket Gamma API & Manifold Markets REST | Probabilidad implícita, volumen transaccionado, liquidez. |
| **Wikipedia** | `WikipediaAdapter` | MediaWiki Revisions API (`wikipedia.org/w/api.php`) | Historial de revisiones, guerras de edición y reversiones. |

---

## ⚙️ 2. Motor CLI en Silicio (`scripts/socint_extract.py`)

```bash
# 1. Desenrollar hilo completo en X (Twitter) hasta la raíz
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://x.com/username/status/1844000000000000000" --unfold --save-vault

# 2. Peritaje forense de usuario en Reddit con cálculo de entropía H(sub)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "u/username" --limit 50 --format markdown

# 3. Discusión completa en Hacker News con árbol anidado de comentarios
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://news.ycombinator.com/item?id=38000000" --format markdown

# 4. Hilo descentralizado en Bluesky (AT Protocol)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://bsky.app/profile/user.bsky.social/post/3kabc123" --format markdown

# 5. Canal público de Telegram con recuento de vistas
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://t.me/s/channel_name" --format markdown

# 6. Actividad pública de desarrollador en GitHub
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://github.com/torvalds" --format markdown

# 7. Probabilidad y volumen en Polymarket o Manifold
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://polymarket.com/event/slug-name" --format markdown

# 8. Peritaje de guerras de edición en Wikipedia
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://es.wikipedia.org/wiki/Nombre_Articulo" --format markdown

# 9. Consultar telemetría y registros de la Bóveda SQLite WAL
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py --vault-stats

# 10. Análisis forense temporal, dispersión léxica y pivotado de identidad
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://x.com/username/status/1844000000000000000" --temporal-check --lexical-check --pivot-check

# 11. Exportar grafo de red (Mermaid, Graphviz DOT, Gephi GEXF)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://news.ycombinator.com/item?id=38000000" --export-mermaid grafo.mmd --export-dot grafo.dot --export-gexf grafo.gexf

# 12. Dashboard HTML forense interactivo offline & CSV RFC 4180
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://x.com/username/status/1844000000000000000" --export-html reporte.html --export-csv registros.csv

# 13. Sello de atestación criptográfica Merkle (SHA-256 Tree) & análisis de afecto
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/socint_extract.py \
  --url "https://x.com/username/status/1844000000000000000" --sentiment-check --merkle-seal

# 14. Ejecución de la Suite de Verificación Determinista Offline (35/35)
python3 ~/.gemini/config/skills/c5-socint-extraction-suite/scripts/test_socint.py
```

---

## 🤖 3. Detector Forense de Astroturfing (Similitud Jaccard N-Grams)

Desenmascara granjas de bots, cuentas títere (*sockpuppets*) y ataques Sybil:
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

## ⚖️ 4. Matriz de Clasificación Epistemológica (Las 4 Categorías C5-REAL)

Todo texto procesado se clasifica automáticamente en 4 estratos epistémicos:

| Categoría Epistémica | Indicadores Lingüísticos & Silicio | Veredicto Operativo |
| :--- | :--- | :--- |
| **1. Hechos Verificados** | Hashes SHA-256, repos GitHub, URLs canónicas, DOIs, leyes/BOE, contratos. | **Señal Base** (Aceptado sin fricción) |
| **2. Evidencia Experimental** | Benchmarks ($ms$, $tokens/s$, $p_{99}$), telemetría, tamaños muestrales ($n$), costes auditados. | **Verificable** (Sujeto a reproducción) |
| **3. Modelos & Doctrina** | Arquitecturas de sistemas, topologías causales, invariantes, teoría de la información. | **Marco Conceptual** (Evaluado por consistencia) |
| **4. Especulación / Sesgo** | Hype ("100x", "game changer"), profecías no falsables, afirmaciones sin evidencia. | **Anergía / Ruido** (Etiquetado como *Cheap Talk*) |

### Ratio de Señal/Ruido (SNR):
$$\text{SNR} = \frac{N_{\text{hechos}} + N_{\text{experimental}} + N_{\text{modelos}}}{N_{\text{hechos}} + N_{\text{experimental}} + N_{\text{modelos}} + 1.5 \cdot N_{\text{especulacion}}}$$

---

## 🏛️ 5. Bóveda Local SQLite WAL (`socint_vault.db`)

Con `--save-vault`, toda investigación se archiva de forma duradera en `~/.gemini/antigravity/socint_vault.db` (`PRAGMA journal_mode = WAL;`):
- Registra `record_id`, `platform`, `target_type`, `url`, `author`, `title`, `raw_content`, `metrics_json`, `epistemic_counts_json`, `snr_score` y `captured_at`.
- Operación idempotente (`INSERT OR REPLACE`), protegiendo la evidencia histórica frente a eliminación de tweets, mensajes o posts.

---

## 🔬 6. Módulos Forenses Avanzados & Atestación Criptográfica (v1.3.0)

1. **TemporalForensics:**
   - Coeficiente de Ráfaga: $B = \frac{\sigma - \mu}{\sigma + \mu} \in [-1, 1]$
   - Factor de Fano: $F = \frac{\sigma^2}{\mu}$
   - Detección de *Bot Drip* periódico ($B \to -1, F \ll 1$) vs. *Ráfagas CIB coordinadas* ($B > 0.40, F > 10$).
2. **LexicalDispersion (Hapax Legomena):**
   - Ratio $V/N$ (Type-Token Ratio) y proporción de palabras únicas ($Hapax/V$) para distinguir prosa humana rica de monotonía estocástica generada por LLMs.
3. **ActorNetwork & Grafos:**
   - Extracción de menciones `@user`, enlaces e interacciones. Exportación directa a **Mermaid (`.mmd`)**, **Graphviz (`.dot`)** y **Gephi XML (`.gexf`)**.
4. **SentimentAffectEngine:**
   - Detección de polaridad (valencia $\in [-1, 1]$), ratio de indignación (*outrage ratio*) y volatilidad emocional en hilos de discusión.
5. **Merkle Attestation:**
   - Árbol binario criptográfico SHA-256 sobre hojas canónicas ordenadas (`compute_merkle_root`), garantizando integridad forense inalterable y no repudio.

---

## 🔒 7. Contrato de Autonomía Fail-Closed (Ω10 / Ω11 / Ω12)

- **Ω10 (Zero Pause Transition):** El agente no debe detener la ejecución ni solicitar autorización al operador para alternar entre adaptadores o ejecutar fallbacks de sindicación/Atom.
- **Ω11 (Degradación Determinista):**
  $$\text{API Directa JSON} \xrightarrow{\text{error}} \text{Sindicación/RSS/Atom} \xrightarrow{\text{error}} \text{Proxy Lector Markdown} \xrightarrow{\text{error}} \text{Subagente Browser}$$
- **Ω12 (Atestación Limpia):** Los datos extraídos deben exportarse limpios de scripts o trackers, respetando la Manta de Markov y almacenándose en `/tmp/` o en el artefacto de la conversación.
