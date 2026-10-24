---
name: c5-cortex-swarm-orchestrator
display_name: CORTEX Swarm Orchestrator
description: Enruta enjambres, ciclo de vida de agentes, proveedores, telemetría,
  auditoría y composición de skills, planificación y handoff. Dispara con "cortex
  swarm hub", "swarm hub", "enjambre", "sharur", "skill chain", "telemetría", "plan
  omega".
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

# CORTEX Swarm Orchestrator

> **Directiva Declarativa:** Enruta módulos bajo demanda y conserva su ámbito y contrato.

## Selección

1. Identifica la petición y identifica la acción y el dominio, o una invocación explícita, en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia enjambres, scripts, llamadas a proveedores ni purgas.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Desempate de triggers compartidos

`tensor de transducción` también activa `symbiotic-cognitive-architecture` en el ámbito del proyecto. Usa este hub para Gemini API, claves, cuotas o esquemas JSON; usa la habilidad del proyecto para arquitectura cognitiva y colaboración agente-persona. Si solo aparece el trigger y el tema no aclara el destino, pregunta antes de cargar procedimientos.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
El resolver exige acción y dominio para peticiones contextuales, respeta negaciones y conserva invocaciones explícitas. Para una continuación, añade `--context "objetivo anterior del usuario"`; no infiere permiso para ejecutar procedimientos.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos disponibles

| Procedimiento | Intención contextual |
| --- | --- |
| [anergy-purge-protocol](references/modules/anergy-purge-protocol/MODULE.md) | Purga de código muerto, artefactos efímeros, ghost listeners, saturación APFS y prompt bloat. |
| [c5-adaptive-annealing-engine](references/modules/c5-adaptive-annealing-engine/MODULE.md) | Motor de Recocido Adaptativo en cuatro cuartiles (Q1-Q4) para forzar convergencia al Apex en espacios discretos y optimización sin colisión topológica ni colapso de gradiente voraz. |
| [c5-autonomous-agent-primitives](references/modules/c5-autonomous-agent-primitives/MODULE.md) | Catálogo y matriz de las 47 primitivas de agente autónomo colapsadas en los 4 macro-transductores C5-REAL. |
| [c5-debloat-agent-kernel](references/modules/c5-debloat-agent-kernel/MODULE.md) | Diseño y migración a micro-kernels de agentes en un archivo con stdlib pura y SQLite WAL sin LangChain. |
| [c5-gemini-api-2026-standards](references/modules/c5-gemini-api-2026-standards/MODULE.md) | Estándares Gemini API 2026: modelos y cuotas verificables, diagnóstico HTTP, credenciales autorizadas y salidas estructuradas. |
| [c5-plan-omega](references/modules/c5-plan-omega/MODULE.md) | Motor de planificación determinista en DAG (Protocolo PLAN-Ω). Sustituye checklists planas por matrices topológicas de 4 niveles, sondeo pre-flight en 60s, puertas Two-Way/One-Way con rollback y micro-gates Fail-Stop. |
| [c5-session-deskimming](references/modules/c5-session-deskimming/MODULE.md) | Workflow de enjambre (Ring-2 a Ring-0) para auditar historiales, purgar nata y reubicar archivos huérfanos. |
| [c5-sharur-3600](references/modules/c5-sharur-3600/MODULE.md) | Define e instancia a SHARUR-3600. Matriz de enjambre estocástico de Ring-2 para exploración masiva paralela y Surrealismo del Bueno. |
| [c5-tri-provider-swarm](references/modules/c5-tri-provider-swarm/MODULE.md) | Orquestación desacoplada de enjambres multi-agente combinando OpenAI (Planner N0, Structured Outputs), Qwen (Workers de Código N1 en vLLM local sin 429) y Kimi (Arqueología N2 de 1M-2M tokens) bajo semáforos de Landauer. |
| [cortex-skill-auditor](references/modules/cortex-skill-auditor/MODULE.md) | Audita estructura, rutas, enlaces y coherencia de instrucciones cuando se pide revisar una biblioteca de skills; conserva comprobaciones independientes y explicita su cobertura. |
| [cortex-skill-composer](references/modules/cortex-skill-composer/MODULE.md) | Composición y orquestación en cadena (Skill Chains) de múltiples habilidades CORTEX. |
| [cortex-skill-genesis](references/modules/cortex-skill-genesis/MODULE.md) | Síntesis y generación automática de nuevos SKILL.md desde telemetría de sesiones y patrones observados. |
| [cortex-telemetry](references/modules/cortex-telemetry/MODULE.md) | Inspección de telemetría runtime, logs transcript.jsonl, exergía de prompts (Chentsov-Markov) y consolidación de sesiones efímeras del brain. |
| [dynamic-subagent-lifecycle](references/modules/dynamic-subagent-lifecycle/MODULE.md) | Gestión del ciclo de vida, mitigación de deadlocks y supervisión de subagentes dinámicos. |
| [goal](references/modules/goal/MODULE.md) | Destila cualquier tarea en un contrato cerrado de mínimo consumo de tokens y asigna el modelo/nivel exacto antes de tocar código. |
| [handoff](references/modules/handoff/MODULE.md) | Genera un documento completo de traspaso de contexto (HANDOFF.md) para transferir lecciones aprendidas, estado del sistema y próximos pasos a una nueva sesión. |
| [kimi-mcp-orchestrator](references/modules/kimi-mcp-orchestrator/MODULE.md) | Orquestación de tareas vía Moonshot AI (Kimi K3) MCP bridge, delegación de auditorías a instancias swarm o interacción con la API de Kimi. |
| [swarm-quantum-collapse](references/modules/swarm-quantum-collapse/MODULE.md) | Orquesta un enjambre Python P×S calibrado empíricamente para forzar la sincronización (Colapso Cuántico) de múltiples repositorios simultáneos. |
| [swarm-router](references/modules/swarm-router/MODULE.md) | Orquestador central y despachador inteligente de enjambres multi-agente con auto-detección contextual y tolerancia a typos. |
