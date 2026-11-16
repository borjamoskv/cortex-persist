---
name: c5-tri-provider-swarm
display_name: Orquestador de Enjambre Híbrido Tri-Provider (OpenAI ⊗ Ollama Local ⊗ Gemini / Kimi)
description: Orquestación desacoplada de enjambres multi-agente combinando OpenAI (Planner N0, JSON Schema strict), Ollama Local (Workers de Código N1 qwen2.5-coder:14b sin 429) y Gemini Interactions API / Kimi opcional (Contexto Largo N2) bajo triple semáforo y AgentPager. Dispara con "enjambre híbrido", "tri provider swarm", "kimi qwen openai", "orquestador tres modelos", "tri-provider swarm".
role: ejecutor
allowed_roles:
- ejecutor
- arquitecto
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# Skill: Orquestador de Enjambre Híbrido Tri-Provider (C5-REAL)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor`
> - **Modo de Acceso a Worktree:** `read-write`
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Despacha campañas multi-agente reales sobre HTTP asíncrono (`httpx.AsyncClient`) en el paquete canónico `~/10_PROJECTS/tri-swarm-dispatcher/`, gobernadas por triple semáforo (`L1`, `CLOUD`, `LOCAL`), suspensión `AgentPager` $O(1)$ fuera de los locks, circuit breakers por proveedor, backoff con jitter completo (`Retry-After`) y manejo `Fail-Closed` de errores de autenticación (`401`/`403` deshabilitan el backend sin reintentos ni fuga de secretos).

---

## 1. Rutas y Estratos Reales

1. **Nivel 0 (`plan`):** `openai` (`POST /v1/chat/completions`, `response_format` `json_schema` `strict: true`) $\to$ `gemini` (`POST /v1/interactions`, `response_format` JSON Schema) $\to$ `ollama`.
2. **Nivel 1 (`code_mutation`):** `ollama` (`POST /api/chat`, `qwen2.5-coder:14b` por defecto, `think=False` con fallback automático si el modelo no soporta `think`) $\to$ `openai` $\to$ `gemini`.
3. **Nivel 2 (`deep_context`):** `gemini` (`POST /v1/interactions`, `gemini-4-hydrogen`, `Api-Revision: 2026-05-20`, `store=False`) $\to$ `kimi` (activo solo si `MOONSHOT_API_KEY` y `TRI_KIMI_MODEL` están definidos) $\to$ `openai`.

---

## 2. Triple Semáforo Calibrado para Apple M3 Pro (`5P+6E` / `18 GB`)

- `TRI_MAX_L1=5`: escuadrones concurrentes activos (`squad_size=10` por defecto).
- `TRI_MAX_CLOUD=11`: peticiones HTTP cloud simultáneas en vuelo (se libera durante los sleeps de backoff).
- `TRI_MAX_LOCAL=2`: peticiones simultáneas contra `ollama` local.
- `AgentPager`: registro y espera `await pager.wait_for_beep()` fuera de `SEM_L1` / `SEM_CLOUD` / `SEM_LOCAL` para evitar inanición con $N \ge 100$ tareas.

---

## 3. Invocación Canónica

Paquete y suite de tests (`pytest` offline con `httpx.MockTransport`):
`/Users/borjafernandezangulo/10_PROJECTS/tri-swarm-dispatcher/`

El puntero del skill delega automáticamente al `.venv` del paquete:
```bash
python3 ~/.gemini/config/skills/c5-tri-provider-swarm/scripts/tri_swarm_dispatcher.py --probe
python3 ~/.gemini/config/skills/c5-tri-provider-swarm/scripts/tri_swarm_dispatcher.py --tasks tasks.json --out results.json
```
