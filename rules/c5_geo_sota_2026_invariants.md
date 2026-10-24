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
1. **Acceso Concedido (Discovery / RAG):** `OAI-SearchBot`, `PerplexityBot`, `Googlebot`, `Bingbot`, `ClaudeBot`, `Applebot-Extended`.
2. **Acceso Denegado (Bulk Scraping / Entrenamiento sin Atribución):** `GPTBot`, `CCBot` (Common Crawl), `Google-Extended`.
3. **Fail-Closed en Entornos Experimentales:** Carpetas de backup, rutas efímeras y paneles internos deben estar explícitamente vedados (`Disallow: /test/`, `Disallow: /assets/backup_*/`).

## 3. Invariante de Pre-renderizado Factual en DOM SSR (Zero-JS Evidence Gate)
Los rastreadores RAG y agentes ligeros evalúan el sustrato HTML sin garantizar la ejecución completa del árbol de JavaScript o con presupuestos de tiempo de renderizado ultrarreducidos:
1. **Evidencia Pre-renderizada:** Todo dato crítico de entidad (técnica, soporte, medidas métricas, precios explícitos, fecha de verificación, autoría) DEBE figurar en el marcado HTML estático de origen (SSR / SSG), nunca generado exclusivamente por hidratación cliente.
2. **Isomorfismo Estricto DOM ↔ Schema.org:** Todo nodo JSON-LD (`VisualArtwork`, `Product`, `TechArticle`, `Person`) debe corresponder 1:1 con elementos visibles en la interfaz humana. Queda prohibida la inyección de claims en metadatos que no estén respaldados visualmente en el DOM.

## 4. Invariante Agent-Ready DOM (Touchpoints y Navegabilidad)
Para permitir que agentes autónomos completen tareas transaccionales sin ambigüedad:
1. **Atributos Semánticos y Accesibilidad:** Todo campo interactivo debe contar con `<label>` explícito, estados ARIA normalizados (`aria-pressed`, `aria-expanded`, `aria-live`) y botones nativos (`<button>`, `<a>`).
2. **Deep Links Transaccionales en $O(1)$:** Las vías de acción (adquisición, consulta, reserva) deben proveer enlaces directos con parámetros contextuales codificados (ej. WhatsApp API o correo con asunto de la entidad activa), evitando barreras de registro innecesarias.

## 5. Invariante de Integridad Ontológica de la Entidad (Veto al Sesgo de Recencia)
En el modelado de grafos de conocimiento (`Person`, `VisualArtist`, `Organization`), fichas técnicas, `OfferCatalog`, selectores interactivos y archivos `llms.txt`:
1. **Prohibición de Reduccionismo por Novedad Temporal:** Queda terminantemente prohibido etiquetar una serie, soporte o material explorado recientemente (ej. pizarra y mica) como la «especialidad» definitoria del creador ni anteponerlo al núcleo histórico de su práctica.
2. **Jerarquía Disciplinar Real:** Los descriptores primarios (`description`, `knowsAbout`, orden de ejemplos y opciones por defecto en configuradores) DEBEN liderar siempre con el cuerpo central de la disciplina (ej. dibujo, pintura al óleo/acrílico, collage textil sobre madera, objetos intervenidos), situando los materiales recientes como exploraciones específicas sin sesgar los vectores semánticos en RAG.
3. **Veto a Fallbacks Contaminantes:** Prohibido usar materiales de una serie específica como valor por defecto (`default`) al serializar catálogos completos.

## 6. Invariante de Notificación Push (`IndexNow`) y Licenciamiento Visual (Lens)
1. **IndexNow Determinista:** Todo pipeline de generación estática debe emitir `{key}.txt` e `indexnow.json` con la totalidad de rutas canónicas y disparar notificación POST a `api.indexnow.org/indexnow` en despliegue.
2. **Atribución Multimodal:** Inyección obligatoria de `<meta name="robots" content="index, follow, max-image-preview:large">` y `acquireLicensePage` en cada `ImageObject` apuntando a la ruta transaccional de encargo/adquisición.

## 7. Invariante de Grafo Canónico de Entidad y Locus (`#artist`, `#studio`)
1. **IDs Fragmentarios Deterministas:** Toda entidad principal (`Person`, `LocalBusiness`, `Service`, `Place`) debe poseer un `@id` canónico basado en fragmento (`/#artist`, `/#studio`, `/retratos-por-encargo-bilbao/#service`, `/obra/#catalogue`).
2. **Paridad de Atribución 1:1:** Todo nodo secundario (`ImageObject.creator`, `VisualArtwork.creator`, `Offer.seller`, `BlogPosting.author`, `ExhibitionEvent.organizer`) DEBE referenciar idéntico `@id` canónico y compartir el mismo vector de autoridad (`sameAs`).
3. **Locus Físico Verificado:** El punto físico de producción (`#studio`) debe sincronizar sus coordenadas `(lat, lon)`, dirección postal y `hasMap` entre Schema.org, la API estructurada (`api/catalog.json`) y el archivo `llms.txt`.

## 8. Invariante de Sindicación RSS con Dublin Core (`xmlns:dc`)
En la emisión de canales RSS 2.0 (`feed.xml`), es obligatorio incorporar `xmlns:dc="http://purl.org/dc/elements/1.1/"` y publicar en cada `<item>` las etiquetas complementarias `<dc:creator>` y `<author>` para resolver la autoría de forma unívoca ante agentes RAG.

## 9. Invariante de Aislamiento Acústico en Tests Headless (JSDOM Media Gate)
Cuando el cliente web implemente capas sonoras interactivas o hápticas (`new window.Audio(...)` / Web Audio API), los entornos de simulación sintéticos (JSDOM) deben inicializarse en `beforeParse(window)` con stubs controlados para `HTMLMediaElement.prototype.play = () => Promise.resolve()` y `pause = () => {}`, previniendo que excepciones no implementadas contaminen la traza de auditoría de errores.

## 10. Veto a la Nata y Superstición GEO (Anti-Cargo-Cult)
Queda estrictamente prohibido:
1. Generar archivos `llms.txt` vacíos o redundantes con el HTML semántico sin directiva operativa.
2. Fragmentar páginas en micro-URLs cosméticas sin contenido de valor diferenciado.
3. Crear esquemas propietarios inventados ajenos al estándar formal de `Schema.org`.
4. Perseguir menciones sintéticas o granjas de enlaces que carezcan de evidencia primaria verificable.
5. Inyectar el esquema `FAQPage` (depreciado por Google en mayo de 2026); las preguntas frecuentes de abanico (Query Fan-Out) deben servirse en marcado semántico nativo (`<details>`/`<summary>`) sin contaminar el bloque JSON-LD.
