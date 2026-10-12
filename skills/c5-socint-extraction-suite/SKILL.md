---
name: c5-socint-extraction-suite
display_name: Suite Soberana de Inteligencia Social (SOCINT C5-REAL)
description: 'Suite unificada de extracción de inteligencia social (SOCINT), telemetría de opinión y auditoría epistemológica de redes: X/Twitter (hilos/artículos), Substack (newsletters/notes) y Reddit (subreddits/discusiones). Dispara con "socint suite", "inteligencia social", "scraping redes", "reddit socint", "reddit osint", "scraping reddit", "inteligencia reddit", "socint reddit", "extraer subreddit", "substack socint", "substack osint", "scraping newsletter", "análisis substack", "socint substack", "extraer substack", "auditar tweet", "analizar hilo x", "extraer tweet", "auditar x twitter", "hilo twitter audit", "twitter article audit", "x.com audit".'
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

Esta suite unifica los tres vectores principales de extracción e ingestión de telemetría discursiva en plataformas sociales públicas, eludiendo la fricción burocrática de APIs cerradas y muros de registro sin dependencias pesadas.

---

## 🛰️ 1. Adaptador X/Twitter: Hilos, Artículos y Auditoría Epistemológica

### Criterios de Activación
- URLs directas: `x.com/*/status/*`, `twitter.com/*/status/*`.
- Intenciones: Auditar credibilidad de tweets, extraer hilos completos, resumir artículos largos de X.

### Pipeline de Ejecución
1. **Extracción Atómica (`read_url_content`)**:
   - Pasar la URL directa del post a `read_url_content`.
   - Recuperar el Markdown resultante y aislar: Autor (`@handle`), Métricas (Likes, Retweets, Vistas) y Cuerpo íntegro del texto/hilo.
2. **Matriz de Clasificación Epistémica (4 Categorías C5-REAL)**:
   - **Hechos Verificados**: Registros formales, sentencias, datos empíricos contrastables.
   - **Evidencia Experimental / Métricas**: Pruebas cuantitativas, A/B testing, telemetría verificada.
   - **Modelos y Doctrina**: Hipótesis de comportamiento, economía conductual, arquitectura de interfaz.
   - **Especulación / Falsa Causalidad**: Correlaciones espurias, sesgos de supervivencia o hipérboles de marketing.
3. **Tabla de Auditoría de Afirmaciones**: Contrastar cada tesis central con un veredicto formal (`FALSADA`, `VERIFICADA`, `AMBIGUA`).

---

## 📰 2. Adaptador Substack: Newsletters, Notes y Topología EBEAF

### Bypass de WAF y Lectura Silenciosa
Substack aplica bloqueos de scroll a clientes estáticos. Para extracción masiva y limpia:
1. **API Reader Oculta**:
   ```
   https://substack.com/api/v1/reader/feed/profile/<user_id>?limit=500
   ```
   *(Localizar el `<user_id>` numérico del perfil en el código fuente o metadatos JSON).*
2. **Extracción por Expresiones Regulares (Cero Anergía JSON)**:
   - Fechas y Timestamps:
     ```python
     fechas = re.findall(r'"type":"feed","date":"(202\d-[^"]+)"', contenido)
     ```
   - Cuerpo de Notas (Comments):
     ```python
     notes = re.findall(r'"body":"(.*?)"', contenido)
     ```
   - Artículos (Posts):
     ```python
     posts = re.findall(r'"truncated_body_text":"(.*?)"', contenido)
     ```
3. **Auditoría de Cartelización (PODs)**: Identificar redes de recomendación mutua cruzada para aislar la señal real del ruido algorítmico del feed.

---

## 👾 3. Adaptador Reddit: Minería de Subreddits y Señal Comunitaria

### Bypass de API y Extracción Silenciosa
1. **Vector Endpoint JSON Directo**:
   - Añadir `.json` a cualquier URL de subreddit o hilo de Reddit para obtener el árbol completo de datos sin autenticación:
     ```bash
     curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" "https://www.reddit.com/r/<subreddit>/hot.json?limit=50"
     ```
2. **Parseo de Señal**:
   - Filtrar posts fijados (`stickied: true`) y moderación automática.
   - Calcular ratio de controversia (`upvote_ratio < 0.70`) y densidad de argumentos técnicos frente a memética.
3. **Degradación a Navegador Headless**:
   - Si el endpoint responde con HTTP 429 o bloqueo Cloudflare, activar el subagente `/browser` o Puppeteer headless en `/tmp/` con rotación de cabeceras.

---

## 🔒 Autonomy Contract (Ω10 / Ω11 / Ω12)
- **Zero Pause Invariant**: No solicitar confirmación al operador para alternar entre adaptadores.
- **Cadena de Fallback**: `Endpoint API JSON -> URL Content Parser -> Browser Subagent`.
