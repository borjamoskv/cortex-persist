---
name: c5-geo-sota-2026
display_name: Protocolo GEO SOTA 2026 y Evidence Graph
description: 'Arquitectura y auditoría GEO SOTA 2026: Evidence Graph, Query Fan-Out, bots RAG y UX para agentes. Dispara con "geo sota", "evidence graph", "agent-ready seo", "auditoría geo".'
role: arquitecto
allowed_roles:
  - arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

<!-- DIRECTIVA DE EXERGÍA: ARQUITECTURA GEO SOTA 2026 (C5-REAL) -->
<!-- Propósito: Diseñar y auditar arquitecturas de recuperación generativa, evidencia citable y UX para agentes autónomos. -->

# Protocolo GEO SOTA 2026 (Generative Engine Optimization)

## 1. El Embudo de Recuperación Generativa
Toda optimización moderna debe modelar el tránsito de la información en tres estratos:
1. **Discovery (Descubrimiento):** Indexación por rastreadores de búsqueda y bots RAG (`OAI-SearchBot`, `PerplexityBot`, `Googlebot`, `Bingbot`).
2. **Selection (Selección):** Relevancia semántica, densidad factual y citabilidad de la fuente frente a competidores en la ventana de contexto del LLM.
3. **Action (Acción):** Transacción, conversión, click profundo o interacción autónoma vía DOM/WebMCP.

---

## 2. Arquitectura de Datos «Evidence Graph»
En lugar de tratar las páginas como artículos genéricos, cada activo se estructura como una unidad de conocimiento con procedencia:

| Propiedad | Definición Operativa |
| :--- | :--- |
| `entity` | Identificador unívoco y canónico (ej. `https://dominio.com/obra/slug/#artwork`). |
| `intent` | Problema o consulta específica que resuelve en el grafo temático. |
| `answer` | Respuesta concisa y factual sin relleno retórico. |
| `claims` | Afirmaciones comprobables (medidas, fechas, técnicas, benchmarks). |
| `evidence` | Fuentes primarias: fotografías macro/detalle, código reproducible, papers o registros físicos. |
| `limitations` | Restricciones conocidas o condiciones de aplicación (transparencia que fideliza la selección en RAG). |
| `verified_at`| Marca temporal explícita de verificación empírica. |
| `action` | Deep link o función de siguiente paso disponible (reserva, compra, contacto directo). |

---

## 3. Las 7 Estrategias Avanzadas SOTA

1. **Query Fan-Out Mapping:** Mapear el grafo multidimensional de subconsultas que un LLM formula al investigar una intención raíz (precios, técnicas, plazos, comparativas, ejemplos reales).
2. **Evidence-First Publishing:** Publicar datos duros, imágenes originales con metadatos técnicos y metodologías antes de redactar prosa narrativa.
3. **Entity Consistency:** Unificar perfiles de creador/empresa (`sameAs`), direcciones canónicas, autoría y referencias cruzadas.
4. **Citation Gap Analysis:** Auditar consultas temáticas en Bing Topics Portfolio y rastreos donde los competidores son citados y nuestro dominio no.
5. **Cross-Engine Testing:** Evaluar disparidad de citación comparando Google AI Overviews, ChatGPT Search y Perplexity.
6. **Agent-Ready UX:** Diseñar para agentes de navegación: DOM semántico, `<label>` explícitos, compatibilidad con árbol de accesibilidad y endpoints WebMCP.
7. **First-Party Conversion Data:** Medir la atribución real entre citación generativa, tráfico asistido, leads cualificados y ventas cerradas.

---

## 4. GEO Observatory (Protocolo Experimental de Medición)

### Métrica Canónica
$$\text{Citation Rate} = \frac{\text{Respuestas que citan el dominio}}{\text{Total de respuestas evaluadas en el panel}}$$

### Parámetros del Panel de Evaluación
- **Muestra:** Mínimo 50–100 consultas de abanico (Fan-Out).
- **Motores:** Google (AI Mode / Overviews), OpenAI (ChatGPT Search), Perplexity, Bing Copilot.
- **Repeticiones:** 5 rondas por consulta para absorber la estocasticidad del muestreo de temperatura.
- **Registro:** Fecha, modelo/versión, fuentes citadas, orden ordinal de la cita y precisión de las afirmaciones atribuidas.

---

## 5. Handoff y Cadenas de Ejecución
- **Hacia Implementación:** Handoff a `EJECUTOR` (generadores estáticos, scripts Python/Vite, mutación de templates).
- **Hacia Auditoría:** Handoff a `cortex-skill-auditor` y validadores DOM locales (`test_immersive_dom.cjs` o suites Puppeteer/Playwright).
