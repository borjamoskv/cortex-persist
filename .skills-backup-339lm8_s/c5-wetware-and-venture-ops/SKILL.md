---
name: c5-wetware-and-venture-ops
display_name: Wetware and Venture Ops
description: Enruta módulos de carga cognitiva, telemetría somática, aprendizaje,
  valoración, estrategia de negocio y divulgación. Dispara con "wetware hub", "venture
  ops hub", "wetware and venture", "operaciones venture", "carga cognitiva".
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

# Wetware and Venture Ops

> **Directiva Declarativa:** Enruta módulos bajo demanda y conserva su ámbito y contrato.

## Selección

1. Identifica la petición y busca el alias en la tabla o en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia procedimientos, scripts, servicios externos ni cambios de documentos.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
Normaliza mayúsculas y acentos, prioriza coincidencias exactas y respeta límites de palabra.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos de ámbito global

| Módulo completo | Nombres y triggers conservados |
| --- | --- |
| [c5-wetware-divergente](references/modules/c5-wetware-divergente/MODULE.md) | `c5-wetware-divergente`, `/c5-wetware-divergente`, `alto voltaje`, `mente divergente`, `wetware divergente`, `tdah 2e`, `altas capacidades tdah`, `hiperfoco`, `burnout divergente`, `bloqueo ejecutivo 2e` |
| [c5-2e-neuropharmacological-sovereignty](references/modules/c5-2e-neuropharmacological-sovereignty/MODULE.md) | `c5-2e-neuropharmacological-sovereignty`, `/c5-2e-neuropharmacological-sovereignty`, `desacoplamiento concerta`, `bucle de parches`, `farmacología 2e`, `sustrato dopaminérgico`, `mitigar crash concerta` |
| [c5-somatic-panic-deescalation](references/modules/c5-somatic-panic-deescalation/MODULE.md) | `c5-somatic-panic-deescalation`, `/c5-somatic-panic-deescalation`, `ataque de ansiedad`, `ataque de pánico`, `hiperfijación somática`, `no puedo dormir por la respiración`, `bucle de pánico`, `siento que me muero`, `desescalar pánico` |
| [somatic-ble-transduction](references/modules/somatic-ble-transduction/MODULE.md) | `somatic-ble-transduction`, `/somatic-ble-transduction`, `telemetria somatica`, `conectar apple watch`, `somatic daemon`, `ble heart rate`, `ring minus 3` |
| [c5-spaced-repetition-architect](references/modules/c5-spaced-repetition-architect/MODULE.md) | `c5-spaced-repetition-architect`, `/c5-spaced-repetition-architect`, `anki maker`, `tarjetas anki`, `anki flashcards`, `repetición espaciada`, `adhd assistant`, `descomposición de tareas`, `micro-tasking`, `spaced repetition` |
| [c5-tamkarum-60](references/modules/c5-tamkarum-60/MODULE.md) | `c5-tamkarum-60`, `/c5-tamkarum-60`, `tamkarum`, `tamkarum-60`, `/tamkarum`, `arbitraje publicitario`, `auditar roas`, `optimizar campañas`, `equipo marketing`, `enjambre marketing`, `11 agentes`, `scitt` |
| [c5-venture-pitch-architect](references/modules/c5-venture-pitch-architect/MODULE.md) | `c5-venture-pitch-architect`, `/c5-venture-pitch-architect`, `pitch deck`, `investor pitch planner`, `pitch deck creator`, `investor letter writer`, `vc deal memo`, `plan de negocio pptx`, `the ask pitch` |
| [c5-codebase-valuation-audit](references/modules/c5-codebase-valuation-audit/MODULE.md) | `c5-codebase-valuation-audit`, `/c5-codebase-valuation-audit`, `valorar software`, `valoración económica`, `audit codebase valuation`, `software ip valuation`, `acqui-hire valuation`, `due diligence técnica` |
| [c5-real-legaltech-analysis](references/modules/c5-real-legaltech-analysis/MODULE.md) | `c5-real-legaltech-analysis`, `/c5-real-legaltech-analysis`, `legaltech`, `auditoría legal`, `EU AI Act`, `cumplimiento regulatorio`, `contrato inteligente c5`, `whitepaper legal` |
| [c5-epistemic-dissemination-engine](references/modules/c5-epistemic-dissemination-engine/MODULE.md) | `c5-epistemic-dissemination-engine`, `/c5-epistemic-dissemination-engine`, `diseminación epistémica`, `divulgación multicanal`, `hilo de twitter`, `adaptar artículo`, `cross-platform`, `oratoria retórica`, `keynote speech` |
| [c5-weighted-decision-matrix](references/modules/c5-weighted-decision-matrix/MODULE.md) | `c5-weighted-decision-matrix`, `/c5-weighted-decision-matrix`, `weighted scorer`, `matriz de decisión`, `pert estimation`, `estimación de proyectos`, `evaluación tecnológica`, `matriz de pesos`, `evaluación de proveedores` |
