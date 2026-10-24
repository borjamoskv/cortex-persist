---
name: c5-epistemic-thermodynamics
display_name: Epistemic Thermodynamics
description: Enruta axiomas, léxico, termodinámica de información, modelos cognitivos,
  síntesis y falsación de afirmaciones. Dispara con "epistemic hub", "termodinámica
  epistémica", "axiomas", "anagnórisis", "falsación", "investigación profunda", "peer
  review".
role: arquitecto
allowed_roles:
- arquitecto
- ejecutor
- auditor
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# Epistemic Thermodynamics

> **Directiva Declarativa:** Enruta módulos bajo demanda y conserva su ámbito y contrato.

## Selección

1. Identifica la petición y identifica la acción y el dominio, o una invocación explícita, en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia auditorías, scripts, búsquedas externas ni cambios de documentos.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Desempate de triggers compartidos

`tensor de transducción` también activa `symbiotic-cognitive-architecture` en el ámbito del proyecto. Usa este hub para teoría cognitiva y análisis conceptual; usa la habilidad del proyecto para arquitectura cognitiva y colaboración agente-persona. Si solo aparece el trigger y el tema no aclara el destino, pregunta antes de cargar procedimientos.

`burnout cognitivo` también activa `adaptive-cron` del proyecto. Usa este hub para teoría cognitiva; usa `adaptive-cron` para planificar carga de trabajo, descanso o límites de disipación. Si solo aparece el trigger y el tema no aclara el destino, pregunta antes de cargar procedimientos.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
El resolver exige acción y dominio para peticiones contextuales, respeta negaciones y conserva invocaciones explícitas. Para una continuación, añade `--context "objetivo anterior del usuario"`; no infiere permiso para ejecutar procedimientos.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos disponibles

| Procedimiento | Intención contextual |
| --- | --- |
| [autodidact-omega](references/modules/autodidact-omega/MODULE.md) | Investigación profunda de frontera, cristales ontológicos 21k, falsación Popperiana y atestación SCITT. |
| [c5-academic-peer-reviewer](references/modules/c5-academic-peer-reviewer/MODULE.md) | Simulación de revisión por pares académica para papers científicos. Genera dictámenes estructurados (Accept / Major Revision / Minor Revision / Reject) en 4 dimensiones. |
| [c5-axiomatic-kernel](references/modules/c5-axiomatic-kernel/MODULE.md) | Núcleo Operativo de los 100 Principios Fundacionales de Alta Exergía (Axiomas C5-REAL). Contiene la destilación en sinónimos, verbos y álgebra de los principios rectores. |
| [c5-dialectical-pipeline](references/modules/c5-dialectical-pipeline/MODULE.md) | Macro-operador dialéctico: Tesis, Antítesis (falsabiliza) y Síntesis recursiva (itera) hacia el Salto Topológico. |
| [c5-exergy-scale-evaluator](references/modules/c5-exergy-scale-evaluator/MODULE.md) | Auditoría de exergía estructural en escala 1 a 21.000 bajo la Regla de 3 Evaluadores (Silicio, Kolmogorov, Causal). |
| [c5-information-thermodynamics](references/modules/c5-information-thermodynamics/MODULE.md) | Auditoría de física de la información e IA. |
| [c5-lexicon-enforcer](references/modules/c5-lexicon-enforcer/MODULE.md) | Oráculo epistemológico C5-REAL y Linter del Aforismo 5 (purga de cheap talk voluntario hacia señales involuntarias). |
| [c5-ontological-translator](references/modules/c5-ontological-translator/MODULE.md) | Traducción ontológica estricta de conceptos humanos y abstractos hacia invariantes de alta exergía (Termodinámica, Información, Topología). |
| [c5-popperian-falsification-auditor](references/modules/c5-popperian-falsification-auditor/MODULE.md) | Somete documentos locales, manifiestos o afirmaciones técnicas a falsación empírica C5-REAL contrastando con literatura científica primaria. |
| [c5-systemic-dissection-protocol](references/modules/c5-systemic-dissection-protocol/MODULE.md) | Ejecuta una auditoría dialéctica en 4 fases sobre un sistema complejo: Extracción de 100 primitivas, Falsación Popperiana, Anclaje Empírico (Papers) y Síntesis Topológica. |
| [c5-terminological-archaeology](references/modules/c5-terminological-archaeology/MODULE.md) | Cruza perífrasis con literatura primaria y registra términos canónicos en el léxico C5. |
| [categorical-hallucination-audit](references/modules/categorical-hallucination-audit/MODULE.md) | Formalización en Categorías de Markov, desintegración bayesiana y cota cuantitativa de alucinación en Kl(D). |
| [cct-cognitive-theory-advisor](references/modules/cct-cognitive-theory-advisor/MODULE.md) | Asesor en Teoría Cognitiva CCT, Límite de Gödel-Turing, Autopoiesis (Maturana/Luhmann) y prevención de colapso entrópico. |
| [cta-cognitive-transition-algebra](references/modules/cta-cognitive-transition-algebra/MODULE.md) | Álgebra de Transiciones Cognitivas (CTA), event-sourcing comonádico y modelos formales de estado. |
| [discourse-popperian-falsification](references/modules/discourse-popperian-falsification/MODULE.md) | Falsación popperiana estricta de hipótesis científicas, leyendas urbanas, hipérboles biográficas y modelos externos. |
| [epistemic-extinction-protocol](references/modules/epistemic-extinction-protocol/MODULE.md) | Protocolo de reducción dimensional y extinción epistémica (Punto Fijo Ω). |
| [polymath-concept-synthesis](references/modules/polymath-concept-synthesis/MODULE.md) | Síntesis polímata de conceptos complejos integrando física, matemáticas, teoría de la información y arte (Modo ULTRATHINK). |
