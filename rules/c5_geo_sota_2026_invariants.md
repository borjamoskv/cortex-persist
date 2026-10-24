---
name: c5_geo_sota_2026_invariants
description: Invariantes C5-REAL de optimización para motores generativos (GEO SOTA 2026), Evidence Graph, gobierno diferencial de rastreadores RAG y DOM accesible para agentes autónomos.
trigger: "model_decision"
---

# Invariantes de Optimización para Motores Generativos y Agentes (GEO SOTA 2026)

## 1. Principio Rector: Del Mapa Léxico al Territorio de Evidencia
La frontera de indexación y recuperación ya no es optimizar palabras clave en texto superficial, sino consolidar **entidades inequívocas, evidencia comprobable y acciones resolubles en $O(1)$** para buscadores híbridos, motores RAG y agentes de navegación autónoma (Aforismos 1 y 5).

## 2. Invariante de Gobierno Diferencial de Rastreadores (`robots.txt`)
En toda arquitectura web soberana, el archivo `robots.txt` DEBE discriminar formalmente entre motores de recuperación/búsqueda en tiempo real y extractores de entrenamiento masivo:
1. **Acceso Concedido (Discovery / RAG):** `OAI-SearchBot`, `PerplexityBot`, `Googlebot`, `Bingbot`.
2. **Acceso Denegado (Bulk Scraping / Entrenamiento sin Atribución):** `GPTBot`, `CCBot` (Common Crawl).
3. **Fail-Closed en Entornos Experimentales:** Carpetas de backup, rutas efímeras y paneles internos deben estar explícitamente vedados (`Disallow: /test/`, `Disallow: /assets/backup_*/`).

## 3. Invariante de Pre-renderizado Factual en DOM SSR (Zero-JS Evidence Gate)
Los rastreadores RAG y agentes ligeros evalúan el sustrato HTML sin garantizar la ejecución completa del árbol de JavaScript o con presupuestos de tiempo de renderizado ultrarreducidos:
1. **Evidencia Pre-renderizada:** Todo dato crítico de entidad (técnica, soporte, medidas métricas, precios explícitos, fecha de verificación, autoría) DEBE figurar en el marcado HTML estático de origen (SSR / SSG), nunca generado exclusivamente por hidratación cliente.
2. **Isomorfismo Estricto DOM ↔ Schema.org:** Todo nodo JSON-LD (`VisualArtwork`, `Product`, `TechArticle`, `Person`) debe corresponder 1:1 con elementos visibles en la interfaz humana. Queda prohibida la inyección de claims en metadatos que no estén respaldados visualmente en el DOM.

## 4. Invariante Agent-Ready DOM (Touchpoints y Navegabilidad)
Para permitir que agentes autónomos completen tareas transaccionales sin ambigüedad:
1. **Atributos Semánticos y Accesibilidad:** Todo campo interactivo debe contar con `<label>` explícito, estados ARIA normalizados (`aria-pressed`, `aria-expanded`, `aria-live`) y botones nativos (`<button>`, `<a>`).
2. **Deep Links Transaccionales en $O(1)$:** Las vías de acción (adquisición, consulta, reserva) deben proveer enlaces directos con parámetros contextuales codificados (ej. WhatsApp API o correo con asunto de la entidad activa), evitando barreras de registro innecesarias.

## 5. Veto a la Nata y Superstición GEO (Anti-Cargo-Cult)
Queda estrictamente prohibido:
1. Generar archivos `llms.txt` vacíos o redundantes con el HTML semántico sin directiva operativa.
2. Fragmentar páginas en micro-URLs cosméticas sin contenido de valor diferenciado.
3. Crear esquemas propietarios inventados ajenos al estándar formal de `Schema.org`.
4. Perseguir menciones sintéticas o granjas de enlaces que carezcan de evidencia primaria verificable.
