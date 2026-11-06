---
name: dynamic-subagent-lifecycle
display_name: Supervisión del Ciclo de Vida de Subagentes Dinámicos
description: Gestión del ciclo de vida, mitigación de deadlocks y supervisión de subagentes dinámicos. Dispara con "subagente dinámico", "ciclo de vida subagente", "dynamic subagent", "invoke_subagent", "supervisar subagente", "mitigar deadlocks", "orquestar agentes dinámicos".
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

# Skill: Dynamic Subagent Lifecycle Protocol (C5-REAL / Ω)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Define las 4 reglas deterministas para la creación de **Dynamic Subagents** en el ecosistema Antigravity / BABYLON-60.

---

## 🎯 Disparadores Obligatorios de Creación

Crear un Dynamic Subagent vía `define_subagent` únicamente cuando se cumpla al menos uno de los siguientes criterios:

1. **Rol Hiper-Especializado (System Prompt Aislado):**
   - El subagente requiere directivas restrictivas o de dominio acotado (ej. *AST Walker 1-WL*, *SQLite BFT Auditor*, *Z3 Axiom Verifier*).
2. **Aislamiento de Herramientas (Least Privilege Boundary):**
   - Se requiere deshabilitar herramientas de escritura (`enable_write_tools=False`) o restringir llamadas a herramientas MCP (`enable_mcp_tools=False`).
3. **Optimización de Exergía de Contexto:**
   - La tarea debe ejecutarse en un entorno limpio para evitar la acumulación de entropía de una conversación larga.
4. **Enjambre Masivo de Micro-Agentes ($N \ge 5$):**
   - Orquestación paralela sobre múltiples repositorios o módulos aislados.

---

## ⚙️ Workflow de Ejecución Nativo (Antigravity 2.0)

```python
# Paso 1 (Opcional si no existe en ~/.gemini/config/agents/*.md): Definir subagente efímero
define_subagent(
    Name="bft_sqlite_auditor",
    Description="Auditor determinista de colisiones e idempotencia en SQLite",
    SystemPrompt="Eres un auditor C5-REAL. Aplica INV_BFT_04 sobre committer functions...",
    EnableWriteTools=False,
    EnableMCPTools=False,
    EnableSubagentTools=False,
)

# Paso 2: Invocar instancia asíncrona (retorna conversationId de forma inmediata)
invoke_subagent(
    TypeName="bft_sqlite_auditor",  # o agente persistente: "moskv1", "moskvbot", "research"
    Role="Database BFT Auditor",
    Prompt="Audita todas las funciones de commit en babylon60/io_persist_ledger.py",
    Model="inherit",                # "inherit" | "flash_lite" | "flash" | "pro"
    Workspace="inherit",            # "inherit" | "branch" | "share"
)
```

### Máquina de Estados del Subagente Asíncrono (`Running` $\leftrightarrow$ `Idle` $\to$ `Killed`)
1. **`Running` $\to$ `Idle` (Wakeup Reactivo):** Al concluir su tarea, el subagente envía su respuesta al padre y pasa a `Idle` (0% CPU, contexto preservado). El padre se despierta automáticamente sin necesidad de *polling*.
2. **`Idle` $\to$ `Running` (Reanudación Confinada):** Para continuar el trabajo en el mismo contexto del subagente, invocar `send_message(Recipient="<conversationId>", Message="...")` en lugar de lanzar otro `invoke_subagent`.
3. **`Running | Idle` $\to$ `Killed` (Apoptosis en Cascada):** `manage_subagents(Action="kill", ConversationIds=["<conversationId>"])` termina al subagente y a todos sus descendientes, destruyendo sus workspaces `branch`/`share` y conservando logs y artefactos.

---

## 📡 Patrón Agent Beeper (Zero-Friction Interruption)

Para la orquestación masiva de subagentes enjambre ($N \ge 100$), implementar siempre la primitiva de **Agent Beeper** (`AgentPager`):

1. **Suspensión de Anergía 0%**: Subagentes ingresan a un estado de letargo puro mediante `await pager.wait_for_beep(tenant_id)` en lugar de *polling* o `asyncio.sleep()`.
2. **Invariante de Desacoplamiento de Concurrencia**:
   - ❌ **Anti-Patrón (Deadlock)**: No colocar la espera de señal (`wait_for_beep`) dentro del bloque `async with semaphore:`. Esto causa inanición si $N > \text{limit}$.
   - ✅ **Patrón Correcto**:
     ```python
     # 1. Registro y espera del Beep FUERA del semáforo (0% CPU, N agentes escuchando)
     payload = await pager.wait_for_beep(tenant_id)

     # 2. Adquisición de semáforo para ejecución post-señal
     async with semaphore:
         await execute_agent_task(payload)
     ```
3. **Fan-Out Multicast $O(1)$**: Usar un `asyncio.Event` global compartido para señales de broadcast enjambre para lograr sincronización instantánea sin sobrecarga de memoria ($O(1)$ en lugar de $O(N)$ tareas).
