---
name: c5-cortex-swarm-orchestrator
display_name: CORTEX Swarm Orchestrator
description: Enruta enjambres, ciclo de vida de agentes, proveedores, telemetría, auditoría y composición de skills, planificación y handoff. Dispara con "cortex swarm hub", "swarm hub", "enjambre", "sharur", "skill chain", "telemetría", "plan omega".
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

> **Directiva Declarativa:** Enruta módulos bajo demanda y preserva contratos, topología y ciclo de vida de enjambres.

## Selección y Gobernanza de Enjambres

1. **Resolución de Intención:** Determina la acción y el dominio en la petición o consulta la invocación explícita en `references/aliases.json`.
2. **Carga Quirúrgica:** Lee exclusivamente el módulo o los módulos pertinentes antes de activar su procedimiento.
3. **Preservación Contractual:** Conserva roles canónicos (`arquitecto`, `ejecutor`, `auditor`), restricciones operativas y referencias a recursos preservados.
4. **Cero Ejecución Eager:** La carga del hub no inicia enjambres, procesos en segundo plano, llamadas a proveedores ni purgas.
5. **Independencia Causal (Stage 1 MASS):** Antes de componer agentes en enjambre, valida la utilidad aislada de cada componente; nunca ordenes ruido.
6. **Partición Disjunta (Anti-Write Collision):** En enjambres concurrentes, asigna dominios de archivo estrictamente disjuntos a cada subagente. Prohibido mutar el mismo archivo desde múltiples agentes.
7. **Despertar Reactivo (Zero Polling):** Cero bucles activos de espera (`sleep`) para monitorear subagentes; el agente cede el turno y despierta por evento reactivo.
8. **Apoptosis Post-Ejecución:** Al concluir la tarea del enjambre, invoca obligatoriamente `manage_subagents` (`kill` o `kill_all`) para liberar memoria y erradicar procesos huérfanos.

## Topologías de Ejecución de Enjambre (MAS Patterns)

| Topología | Mecánica Operativa | Regla de Oro C5-REAL | Módulos Clave |
| :--- | :--- | :--- | :--- |
| **Fork-Join (Paralelo)** | Tareas ortogonales concurrentes vía subagentes independientes. | **Partición Disjunta:** Cero colisión en el árbol de archivos. | `dynamic-subagent-lifecycle`, `swarm-router` |
| **Pipeline (Secuencial)** | Flujo por etapas dependientes (Diseño $\to$ Ejecución $\to$ Auditoría $\to$ Atestación). | **Stage-Gating:** Cada fase debe verificar su contrato antes del avance. | `c5-plan-omega`, `goal` |
| **Handoff (Especialista)** | Traspaso unidireccional de contexto entre agentes especializados. | **Cero Arrastre de Nata:** Transferir solo el contrato de entrega (`HANDOFF.md`). | `handoff`, `cortex-skill-composer` |
| **Estocástico / Recocido** | Exploración masiva en Ring-2 con convergencia en Ring-0. | **Colapso Determinista:** Semáforos de Landauer y selección de Pareto. | `c5-sharur-3600`, `c5-adaptive-annealing-engine`, `c5-tri-provider-swarm` |

## Desempate de Triggers Compartidos

`tensor de transducción` también activa `symbiotic-cognitive-architecture` en el ámbito del proyecto. Usa este hub para Gemini API, claves, cuotas o esquemas JSON; usa la habilidad del proyecto para arquitectura cognitiva y colaboración agente-persona. Si solo aparece el trigger y el tema no aclara el destino, pregunta antes de cargar procedimientos.

## Resolver Aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
El resolver exige acción y dominio para peticiones contextuales, respeta negaciones y conserva invocaciones explícitas. Para una continuación, añade `--context "objetivo anterior del usuario"`; no infiere permiso para ejecutar procedimientos.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos Disponibles por Estrato

### 1. Planificación, Metas y Gobernanza Causal

| Procedimiento | Intención contextual |
| --- | --- |
| [c5-plan-omega](references/modules/c5-plan-omega/MODULE.md) | Motor de planificación determinista en DAG (Protocolo PLAN-Ω). Sustituye checklists planas por matrices topológicas de 4 niveles, sondeo pre-flight en 60s, puertas Two-Way/One-Way con rollback y micro-gates Fail-Stop. |
| [goal](references/modules/goal/MODULE.md) | Destila cualquier tarea en un contrato cerrado de mínimo consumo de tokens y asigna el modelo/nivel exacto antes de tocar código. |
| [handoff](references/modules/handoff/MODULE.md) | Genera un documento completo de traspaso de contexto (HANDOFF.md) para transferir lecciones aprendidas, estado del sistema y próximos pasos a una nueva sesión. |

### 2. Ejecución, Topología y Ciclo de Vida de Enjambres

| Procedimiento | Intención contextual |
| --- | --- |
| [c5-tri-provider-swarm](references/modules/c5-tri-provider-swarm/MODULE.md) | Orquestación desacoplada de enjambres multi-agente combinando OpenAI (Planner N0, Structured Outputs), Qwen (Workers de Código N1 en vLLM local sin 429) y Kimi (Arqueología N2 de 1M-2M tokens) bajo semáforos de Landauer. |
| [c5-sharur-3600](references/modules/c5-sharur-3600/MODULE.md) | Define e instancia a SHARUR-3600. Matriz de enjambre estocástico de Ring-2 para exploración masiva paralela y Surrealismo del Bueno. |
| [swarm-quantum-collapse](references/modules/swarm-quantum-collapse/MODULE.md) | Orquesta un enjambre Python P×S calibrado empíricamente para forzar la sincronización (Colapso Cuántico) de múltiples repositorios simultáneos. |
| [swarm-router](references/modules/swarm-router/MODULE.md) | Orquestador central y despachador inteligente de enjambres multi-agente con auto-detección contextual y tolerancia a typos. |
| [dynamic-subagent-lifecycle](references/modules/dynamic-subagent-lifecycle/MODULE.md) | Gestión del ciclo de vida, mitigación de deadlocks y supervisión de subagentes dinámicos. |

### 3. Motores de Decisión, Primitivas y Proveedores

| Procedimiento | Intención contextual |
| --- | --- |
| [c5-adaptive-annealing-engine](references/modules/c5-adaptive-annealing-engine/MODULE.md) | Motor de Recocido Adaptativo en cuatro cuartiles (Q1-Q4) para forzar convergencia al Apex en espacios discretos y optimización sin colisión topológica ni colapso de gradiente voraz. |
| [c5-autonomous-agent-primitives](references/modules/c5-autonomous-agent-primitives/MODULE.md) | Catálogo y matriz de las 47 primitivas de agente autónomo colapsadas en los 4 macro-transductores C5-REAL. |
| [c5-debloat-agent-kernel](references/modules/c5-debloat-agent-kernel/MODULE.md) | Diseño y migración a micro-kernels de agentes en un archivo con stdlib pura y SQLite WAL sin LangChain. |
| [c5-gemini-api-2026-standards](references/modules/c5-gemini-api-2026-standards/MODULE.md) | Estándares Gemini API 2026: modelos y cuotas verificables, diagnóstico HTTP, credenciales autorizadas y salidas estructuradas. |
| [kimi-mcp-orchestrator](references/modules/kimi-mcp-orchestrator/MODULE.md) | Orquestación de tareas vía Moonshot AI (Kimi K3) MCP bridge, delegación de auditorías a instancias swarm o interacción con la API de Kimi. |

### 4. Telemetría, Higiene y Metadatos de Habilidades

| Procedimiento | Intención contextual |
| --- | --- |
| [anergy-purge-protocol](references/modules/anergy-purge-protocol/MODULE.md) | Purga de código muerto, artefactos efímeros, ghost listeners, saturación APFS y prompt bloat. |
| [c5-session-deskimming](references/modules/c5-session-deskimming/MODULE.md) | Workflow de enjambre (Ring-2 a Ring-0) para auditar historiales, purgar nata y reubicar archivos huérfanos. |
| [cortex-telemetry](references/modules/cortex-telemetry/MODULE.md) | Inspección de telemetría runtime, logs transcript.jsonl, exergía de prompts (Chentsov-Markov) y consolidación de sesiones efímeras del brain. |
| [cortex-skill-auditor](references/modules/cortex-skill-auditor/MODULE.md) | Audita estructura, rutas, enlaces y coherencia de instrucciones cuando se pide revisar una biblioteca de skills; conserva comprobaciones independientes y explicita su cobertura. |
| [cortex-skill-composer](references/modules/cortex-skill-composer/MODULE.md) | Composición y orquestación en cadena (Skill Chains) de múltiples habilidades CORTEX. |
| [cortex-skill-genesis](references/modules/cortex-skill-genesis/MODULE.md) | Síntesis y generación automática de nuevos SKILL.md desde telemetría de sesiones y patrones observados. |
