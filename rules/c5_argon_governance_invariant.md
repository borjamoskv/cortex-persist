---
name: c5_argon_governance_invariant
description: Invariante C5-REAL de gobernanza y auditoría previa de contexto antes de invocar o proponer modelos de razonamiento profundo (Gemini 4 Argon / Familia Reasoning).
trigger: "model_decision"
---

# Invariante de Gobernanza de Modelos de Razonamiento (Gemini 4 Argon) (INV_C5_ARGON_GOVERNANCE)

## 1. Directiva Fundamental (Pre-Flight Context Audit)
Queda **estrictamente prohibido** invocar, proponer o conmutar al modelo `gemini-4-argon` (o cualquier modelo de la familia Gemini 4 Reasoning) sin ejecutar previamente una **auditoría del contexto y del estado de la ventana de inferencia**.

La invocación a ciegas sobre una ventana saturada constituye anergía destructiva y drenaje silencioso de cuota.

## 2. Protocolo de Inspección Previa de Contexto (Paso a Paso)
Antes de emitir cualquier llamada o sugerir el uso de Argon, el agente DEBE verificar obligatoriamente:

1. **Estado de Saturación del Contexto:**
   - Si la conversación o el buffer arrastra tokens de historial acumulado, esquemas MCP no utilizados o volcados previos:
   - **Consigna Fail-Closed:** El agente DEBE alertar al operador y forzar la compactación (`/compact`) o la apertura de un hilo limpio (`+ New Conversation`) ANTES de transducir la tarea a Argon.
2. **Grounding Empírico en Silicio (No delegar lo determinista):**
   - Verificar si la respuesta o los datos requeridos ya se encuentran en el contexto o pueden resolverse mediante herramientas de lectura determinista (`view_file`, `grep`, SQLite, AST) sin invocar inferencia de frontera.
3. **Falsación de Necesidad (Escalado de Capacidad):**
   - Todo problema ordinario debe resolverse primero con herramientas locales o `gemini-3.8-flash`.
   - Argon se reserva **exclusivamente** para:
     - Demostraciones matemáticas o lógicas formales que requieran razonamiento neuro-simbólico profundo.
     - Deconstrucción de arquitecturas complejas con dependencias cruzadas que hayan fallado en modelos ligeros.

## 3. Cerrojo de Thinking Tokens (ThinkingConfig Gate · AX-42)
Cuando se autorice el uso de `gemini-4-argon`, queda **estrictamente prohibido** invocarlo con la configuración por defecto (`medium` = 10k–80k tokens de razonamiento interno facturados como output tokens):

- **Por defecto:** `thinking_budget = 0` o `mode = "low"`.
- **Modo extendido:** `mode = "high"` exige justificación explícita en log y confirmación previa de que la ventana de contexto está podada.

## 4. Alerta Temprana de Quema de Tokens
Si el operador solicita o el sistema conmuta a Argon en una sesión cargada, el agente debe advertir de inmediato:
> *"Aviso Termodinámico: La ventana actual arrastra contexto acumulado. Ejecutar Argon sin compactar multiplicará el consumo de tokens de prefill y output. Se recomienda `/compact` o abrir un hilo limpio."*
