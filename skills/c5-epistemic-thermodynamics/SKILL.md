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

1. Identifica la petición y busca el alias en la tabla o en `references/aliases.json`.
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
Normaliza mayúsculas y acentos, prioriza coincidencias exactas y respeta límites de palabra.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos de ámbito global

| Módulo completo | Nombres y triggers conservados |
| --- | --- |
| [c5-axiomatic-kernel](references/modules/c5-axiomatic-kernel/MODULE.md) | `c5-axiomatic-kernel`, `/c5-axiomatic-kernel`, `axiomas`, `principios c5`, `núcleo operativo`, `top 100 principios`, `invariantes fundacionales`, `axiomas c5-real`, `kernel axiomático` |
| [c5-lexicon-enforcer](references/modules/c5-lexicon-enforcer/MODULE.md) | `c5-lexicon-enforcer`, `/c5-lexicon-enforcer`, `lexicon enforcer`, `purga anergía semántica`, `auditoría epistemológica`, `forzar léxico c5`, `auditar cheap talk`, `analiza esto con el aforismo 5` |
| [c5-ontological-translator](references/modules/c5-ontological-translator/MODULE.md) | `c5-ontological-translator`, `/c5-ontological-translator`, `traducción ontológica`, `colapso semántico`, `traducir a c5`, `mapeo ontológico`, `ontological translator`, `colapso ontológico` |
| [c5-terminological-archaeology](references/modules/c5-terminological-archaeology/MODULE.md) | `c5-terminological-archaeology`, `/c5-terminological-archaeology`, `arqueología terminológica`, `busca mis perífrasis`, `anagnórisis`, `ya existe ese término`, `tiene nombre esto`, `cómo se llama esto en ciencia`, `cómo se llama cuando` |
| [c5-exergy-scale-evaluator](references/modules/c5-exergy-scale-evaluator/MODULE.md) | `c5-exergy-scale-evaluator`, `/c5-exergy-scale-evaluator`, `escala de exergía`, `evaluar exergía`, `auditoría de exergía`, `puntuación exergética`, `escala 21000`, `exergy scale`, `3 evaluadores` |
| [c5-information-thermodynamics](references/modules/c5-information-thermodynamics/MODULE.md) | `c5-information-thermodynamics`, `/c5-information-thermodynamics`, `entropía de shannon`, `divergencia kl`, `kullback leibler`, `fisher information`, `teorema de chentsov`, `landauer limit`, `information geometry`, `amari natural gradient`, `flujo de wasserstein`, `audita entropía` |
| [categorical-hallucination-audit](references/modules/categorical-hallucination-audit/MODULE.md) | `categorical-hallucination-audit`, `/categorical-hallucination-audit`, `alucinación categórica`, `cota de confabulación`, `desintegración bayesiana`, `Kl(D) audit`, `Myhill-Nerode estocástico`, `cota de lipschitz`, `mean shift 1d` |
| [cct-cognitive-theory-advisor](references/modules/cct-cognitive-theory-advisor/MODULE.md) | `cct-cognitive-theory-advisor`, `/cct-cognitive-theory-advisor`, `teoría cognitiva`, `cct advisor`, `gödel turing`, `autopoiesis`, `maturana luhmann`, `burnout cognitivo` |
| [cta-cognitive-transition-algebra](references/modules/cta-cognitive-transition-algebra/MODULE.md) | `cta-cognitive-transition-algebra`, `/cta-cognitive-transition-algebra`, `álgebra cognitiva`, `cta transition`, `event sourcing cognitivo`, `matriz cta`, `transición de estados`, `álgebra de transiciones`, `comónada cognitiva` |
| [polymath-concept-synthesis](references/modules/polymath-concept-synthesis/MODULE.md) | `polymath-concept-synthesis`, `/polymath-concept-synthesis`, `ultrathink`, `síntesis polímata`, `polymath synthesis`, `concepto polímata`, `unificación interdisciplinar`, `síntesis interdisciplinar`, `unificación conceptual` |
| [epistemic-extinction-protocol](references/modules/epistemic-extinction-protocol/MODULE.md) | `epistemic-extinction-protocol`, `/epistemic-extinction-protocol`, `extinción epistémica`, `punto fijo omega`, `reducción dimensional`, `epistemic extinction`, `punto fijo ω`, `extinción conceptual` |
| [c5-dialectical-pipeline](references/modules/c5-dialectical-pipeline/MODULE.md) | `c5-dialectical-pipeline`, `/c5-dialectical-pipeline`, `falsabliza`, `falsabiliza`, `falsabilia`, `falsa`, `itera`, `itrera`, `itra`, `iteraa`, `iytera`, `sigue`, `salto topológico` |
| [c5-systemic-dissection-protocol](references/modules/c5-systemic-dissection-protocol/MODULE.md) | `c5-systemic-dissection-protocol`, `/c5-systemic-dissection-protocol`, `disección sistémica`, `auditar sistema completo`, `c5-systemic-dissection`, `disección termodinámica`, `protocolo de disección`, `100 primitivas` |
| [c5-popperian-falsification-auditor](references/modules/c5-popperian-falsification-auditor/MODULE.md) | `c5-popperian-falsification-auditor`, `/c5-popperian-falsification-auditor`, `falsación de documento`, `auditar documento`, `falsar afirmación`, `veredicto empírico`, `falsar paper` |
| [discourse-popperian-falsification](references/modules/discourse-popperian-falsification/MODULE.md) | `discourse-popperian-falsification`, `/discourse-popperian-falsification`, `falsación popperiana`, `análisis popperiano`, `auditoría discursiva`, `falsar hipótesis`, `auditar mito`, `leyenda urbana`, `desmentir mito` |
| [autodidact-omega](references/modules/autodidact-omega/MODULE.md) | `autodidact-omega`, `/autodidact-omega`, `autodidact`, `investigación profunda`, `investigar paper`, `cristal ontológico`, `deep research` |
| [c5-academic-peer-reviewer](references/modules/c5-academic-peer-reviewer/MODULE.md) | `c5-academic-peer-reviewer`, `/c5-academic-peer-reviewer`, `peer review`, `academic reviewer`, `revisar paper`, `auditoría de paper`, `dictamen académico` |
