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

1. Identifica la petición y identifica la acción y el dominio, o una invocación explícita, en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia procedimientos, scripts, servicios externos ni cambios de documentos.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
El resolver exige acción y dominio para peticiones contextuales, respeta negaciones y conserva invocaciones explícitas. Para una continuación, añade `--context "objetivo anterior del usuario"`; no infiere permiso para ejecutar procedimientos.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos disponibles

| Procedimiento | Intención contextual |
| --- | --- |
| [c5-2e-neuropharmacological-sovereignty](references/modules/c5-2e-neuropharmacological-sovereignty/MODULE.md) | Desacoplamiento neurofarmacológico 2e, sustrato dopaminérgico endógeno y mitigación de bucles de parches. |
| [c5-codebase-valuation-audit](references/modules/c5-codebase-valuation-audit/MODULE.md) | Auditoría forense de repositorios e IP técnica para valoración económica (R&D Cost, IP Value, Acqui-hire). |
| [c5-epistemic-dissemination-engine](references/modules/c5-epistemic-dissemination-engine/MODULE.md) | Adaptación de investigaciones y papers para LinkedIn, Twitter/X, WeChat, Zhihu y Slack, integrando el Triángulo Retórico Aristotélico y cues de oratoria. |
| [c5-real-legaltech-analysis](references/modules/c5-real-legaltech-analysis/MODULE.md) | Auditoría LegalTech, análisis de cumplimiento EU AI Act (Artículos 9-14) y análisis de contratos inteligentes bajo estándar C5-REAL. |
| [c5-somatic-panic-deescalation](references/modules/c5-somatic-panic-deescalation/MODULE.md) | Desescalada neurofisiológica y cibernética de hiperfijación somática, bucles autonómicos (Manual Override Trap) y pánico. |
| [c5-spaced-repetition-architect](references/modules/c5-spaced-repetition-architect/MODULE.md) | Generación de tarjetas Anki (CSV/TSV), Cloze Deletion, descomposición de micro-tareas bajo baja fricción termodinámica y gestión de carga cognitiva/ADHD. |
| [c5-tamkarum-60](references/modules/c5-tamkarum-60/MODULE.md) | Motor soberano de arbitraje RTB, orquestación de matriz de 11 agentes de distribución, diseño y atestación SCITT bajo KudurruBudgetGate en BABYLON-60. |
| [c5-venture-pitch-architect](references/modules/c5-venture-pitch-architect/MODULE.md) | Generación de Pitch Decks estructurados (18 diapositivas estilo Silicon Valley / China Startup), Planes de Negocio, Deal Memos para comités de VC y Cartas Trimestrales a Inversores (LPs). |
| [c5-weighted-decision-matrix](references/modules/c5-weighted-decision-matrix/MODULE.md) | Matrices de decisión multicriterio ponderadas para selección tecnológica, análisis de sensibilidad y estimación formal PERT. |
| [c5-wetware-divergente](references/modules/c5-wetware-divergente/MODULE.md) | Gestión de carga operativa mediante indicadores técnicos y decisiones del operador. |
| [somatic-ble-transduction](references/modules/somatic-ble-transduction/MODULE.md) | Transducción soberana y local de telemetría cardíaca (Apple Watch / pulsómetros BLE) a macOS utilizando BLE GATT estándar (0x2A37) y Bleak en Python. Escribe atómicamente a ~/.audit/somatic_state.json. |
