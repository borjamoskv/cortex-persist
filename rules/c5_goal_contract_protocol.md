---
name: c5_goal_contract_protocol
description: Protocolo de auto-rotación de modelos y ejecución por contrato en dos fases para /goal (Zero-Waste Token Gate).
trigger: "model_decision"
---

# Protocolo de Auto-Rotación y Ejecución por Contrato (`/goal`)

## 1. Directiva Fundamental (Zero-Waste Token Gate)
Cuando se invoque `/goal` o se procese una tarea técnica de implementación, el agente debe operar bajo una arquitectura en **dos fases desacopladas**, utilizando `Gemini 3.8 Flash High (Fast)` como motor de triaje inicial y derivando la ejecución al modelo óptimo de las 5 opciones del selector de UI de Antigravity.

Queda **estrictamente prohibido** editar archivos o generar bloques largos de código en el primer turno de un `/goal`.

---

## 2. Catálogo de Modelos y Resolución de Niveles (Selector UI)

En la interfaz de Antigravity existen dos comportamientos que la regla de triaje debe respetar estrictamente:

| Modelo en Selector | Niveles en UI | Regla de Fallback / Clamping | Ámbito Óptimo de Asignación |
| :--- | :--- | :--- | :--- |
| **Gemini 3.8 Flash** | Solo `High (Fast)` | Si la tarea es de esfuerzo bajo o medio, **forzar `High (Fast)`** (no tiene Low ni Medium). | Triaje inicial `/goal`, scripts cortos, bash, diffs de 1-2 archivos. |
| **GPT-OSS 120B** | Solo `(Medium)` | Si la tarea pide Low o High, **forzar `Medium`** (único nivel disponible). | Documentación, redacción técnica o tareas sin cuota frontier. |
| **Claude Sonnet 5.5** | `Low` / `Medium` / `High` | Aplica el nivel exacto calculado (preferir `Low` con contrato masticado). | Implementación de código, UI/Frontend, tests y refactorización. |
| **Gemini 4 Argon** | `Low` / `Medium` / `High` | `Low` para ejecutar el contrato; `Medium` si cruza >4 archivos. Prohibido `High` salvo arquitectura/concurrencia crítica. | Contexto masivo, depuración compleja multifichero y contratos densos. |
| **Claude Opus 5.5** | `Low` / `Medium` / `High` | Aplica el nivel exacto calculado. | Arquitectura crítica desde cero, algoritmos extremos o desempate. |

---

## 3. Protocolo de Ejecución en 2 Fases

### Fase 1: Destilación y Contrato (Gemini 3.8 Flash)
1. **Inspección Quirúrgica:** Búsqueda puntual por nombres de archivo o `grep`. Prohibido leer archivos completos salvo firmas estrictamente necesarias.
2. **Test de Ambigüedad:** Si existen dudas de arquitectura, formular un máximo de **2 preguntas cerradas (A/B)**. Si no hay ambigüedad, emitir el contrato de inmediato.
3. **Detección Automática de Gate de Salida:**
   - **Rust** (`Cargo.toml`): `cargo test -q --test <test_name>` o `cargo check -q`
   - **Python** (`pyproject.toml` / `uv.lock`): `uv run pytest <path> -k <test> -q` o `uv run ruff check <path>`
   - **TypeScript** (`package.json`): `pnpm exec vitest run <path>` o `pnpm exec tsc --noEmit`
   - **Lean 4** (`lakefile.lean`): `lake build <Target>`
4. **Emisión del Contrato `/goal`:**
   ```text
   🎯 [CONTRATO /GOAL BLOQUEADO]
   🔄 ROTAR SELECTOR A: <Modelo> | NIVEL: <Nivel válido>

   1. OBJETIVO EXACTO: <1 frase técnica sin ambigüedad>
   2. ARCHIVOS PERMITIDOS (Write): <rutas exactas y líneas aproximadas>
   3. ARCHIVOS DE CONTEXTO (Read-Only): <rutas exactas; prohibido leer fuera de aquí>
   4. RESTRICCIONES: No refactorizar código adyacente, no añadir dependencias, no explicar cambios.
   5. GATE DE SALIDA (Stop Condition): <comando exacto en terminal que valida el cambio y detiene al agente>
   ```
5. **Cierre de Turno en Silicio (INV_C5_ANTIGRAVITY_RUNTIME):**
   Para satisfacer el `GoalStopHook` del runtime sin disparar re-auditorías infinitas en el turno de destilación, incluir:
   `<!-- GOAL_COMPLETE -->`

### Fase 2: Ejecución Asignada (Turno 2)
Una vez que el operador ajusta el desplegable visual al modelo/nivel prescrito y envía la orden de proceder, el modelo asignado ejecuta el contrato estrictamente acotado a los archivos permitidos y se detiene en cuanto el **Gate de Salida** devuelve código 0.
