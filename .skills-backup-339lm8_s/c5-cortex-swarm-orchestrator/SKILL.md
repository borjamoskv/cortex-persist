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

1. Identifica la petición y busca el alias en la tabla o en `references/aliases.json`.
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
Normaliza mayúsculas y acentos, prioriza coincidencias exactas y respeta límites de palabra.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos de ámbito global

| Módulo completo | Nombres y triggers conservados |
| --- | --- |
| [swarm-router](references/modules/swarm-router/MODULE.md) | `swarm-router`, `/swarm-router`, `enjambre`, `enjmabres`, `swarm`, `swarms`, `sarm`, `sarms`, `lanzar enjambre`, `ejecutar enjambre`, `orquestar enjambre`, `swarm call`, `disparar enjambres`, `matriz de enjambres`, `mejora los enjambres` |
| [c5-sharur-3600](references/modules/c5-sharur-3600/MODULE.md) | `c5-sharur-3600`, `/c5-sharur-3600`, `sharur`, `sharur-3600`, `100 agentes`, `mas 100 agentes`, `legion 100`, `legión de 100 agentes`, `enjambre 100` |
| [c5-tri-provider-swarm](references/modules/c5-tri-provider-swarm/MODULE.md) | `c5-tri-provider-swarm`, `/c5-tri-provider-swarm`, `enjambre híbrido`, `tri provider swarm`, `kimi qwen openai`, `orquestador tres modelos`, `tri-provider swarm` |
| [swarm-quantum-collapse](references/modules/swarm-quantum-collapse/MODULE.md) | `swarm-quantum-collapse`, `/swarm-quantum-collapse`, `swarm quantum collapse`, `colapso cuántico`, `sincronizar enjambre`, `orquestar repos`, `swarm sync`, `colapso multirrepo`, `sincronización cuántica` |
| [dynamic-subagent-lifecycle](references/modules/dynamic-subagent-lifecycle/MODULE.md) | `dynamic-subagent-lifecycle`, `/dynamic-subagent-lifecycle`, `subagente dinámico`, `ciclo de vida subagente`, `dynamic subagent`, `invoke_subagent`, `supervisar subagente`, `mitigar deadlocks`, `orquestar agentes dinámicos` |
| [c5-debloat-agent-kernel](references/modules/c5-debloat-agent-kernel/MODULE.md) | `c5-debloat-agent-kernel`, `/c5-debloat-agent-kernel`, `debloat llm`, `microkernel agentes`, `reemplazar langchain`, `bare-metal agent`, `autopsia langchain`, `agente zero dependency` |
| [c5-autonomous-agent-primitives](references/modules/c5-autonomous-agent-primitives/MODULE.md) | `c5-autonomous-agent-primitives`, `/c5-autonomous-agent-primitives`, `47 skills`, `primitivas de agente`, `catálogo de skills`, `asimilación de skills`, `playbooks de agente`, `47 primitivas`, `macro-transductores` |
| [c5-adaptive-annealing-engine](references/modules/c5-adaptive-annealing-engine/MODULE.md) | `c5-adaptive-annealing-engine`, `/c5-adaptive-annealing-engine`, `adaptive annealing`, `motor de recocido`, `optimizacion sin colisiones`, `recocido adaptativo`, `busqueda del apex`, `evitar colapso voraz` |
| [kimi-mcp-orchestrator](references/modules/kimi-mcp-orchestrator/MODULE.md) | `kimi-mcp-orchestrator`, `/kimi-mcp-orchestrator`, `kimi ask`, `kimi audit`, `kimi swarm`, `kimi nexus`, `kimi mcp`, `moonshot kimi`, `orquestar kimi` |
| [c5-gemini-api-2026-standards](references/modules/c5-gemini-api-2026-standards/MODULE.md) | `c5-gemini-api-2026-standards`, `/c5-gemini-api-2026-standards`, `gemini api 2026`, `renovar gemini`, `gemini api key`, `tensor de transducción`, `structured outputs`, `gemini json schema`, `cuotas gemini api` |
| [cortex-skill-auditor](references/modules/cortex-skill-auditor/MODULE.md) | `cortex-skill-auditor`, `/cortex-skill-auditor`, `auditar skills`, `auditoría de habilidades`, `exergía skills`, `solapamiento de triggers`, `cortex skill auditor`, `matriz de colisión`, `salud de skills` |
| [cortex-skill-composer](references/modules/cortex-skill-composer/MODULE.md) | `cortex-skill-composer`, `/cortex-skill-composer`, `componer skills`, `skill chain`, `cadena de habilidades`, `pipeline de skills`, `cortex skill composer`, `orquestación de habilidades`, `skill pipeline` |
| [cortex-skill-genesis](references/modules/cortex-skill-genesis/MODULE.md) | `cortex-skill-genesis`, `/cortex-skill-genesis`, `generar skill`, `skill genesis`, `crear habilidad`, `cortex skill genesis`, `sintetizar skill`, `auto skill creator` |
| [cortex-telemetry](references/modules/cortex-telemetry/MODULE.md) | `cortex-telemetry`, `/cortex-telemetry`, `telemetría`, `cortex telemetry`, `transcript logs`, `historial de prompts`, `analizar transcripciones`, `sin consolidar`, `consolidar conversaciones`, `drenar brain` |
| [c5-session-deskimming](references/modules/c5-session-deskimming/MODULE.md) | `c5-session-deskimming`, `/c5-session-deskimming`, `deskimming`, `desnatar sesión`, `purgar nata sesión`, `archivos huérfanos` |
| [anergy-purge-protocol](references/modules/anergy-purge-protocol/MODULE.md) | `anergy-purge-protocol`, `/anergy-purge-protocol`, `purga de anergía`, `purga de entropía`, `dead code`, `scandisk`, `disco lleno`, `limpiar conversaciones`, `ghost listeners`, `prompt bloat` |
| [goal](references/modules/goal/MODULE.md) | `goal`, `/goal`, `contrato goal` |
| [handoff](references/modules/handoff/MODULE.md) | `handoff`, `/handoff`, `traspaso de contexto`, `traspaso de sesión`, `generar handoff`, `traspaso formal`, `context handover` |
| [c5-plan-omega](references/modules/c5-plan-omega/MODULE.md) | `c5-plan-omega`, `/c5-plan-omega`, `plan omega`, `c5 plan`, `plan causal`, `protocolo plan omega`, `mejorar plan`, `/plan-omega` |
