---
name: c5_goal_contract_protocol
description: Protocolo de auto-rotación de modelos y ejecución por contrato en dos fases para /goal (Zero-Waste Token Gate).
trigger: "model_decision"
---

# Protocolo de Auto-Rotación y Ejecución por Contrato (`/goal` y Selector Gate Agnóstico)

## 1. Directiva Fundamental (Zero-Waste Token Gate)
En toda sesión (con o sin `/goal`, y en cualquier entorno: Antigravity, Claude Code, Codex, Cursor o CLI), el sistema evalúa continuamente la adecuación entre el **LLM + Nivel de Esfuerzo activos** y la complejidad real de la tarea mediante **3 Estratos Universales de Capacidad/Esfuerzo** (implementados en silicio en `scripts/guards/c5_signature_engine.py` y en el hook `PreInvocation` `workspace_pre_invocation_telemetry.py`).

Cuando se invoque `/goal` sin un contrato previo en el prompt, queda **estrictamente prohibido** editar archivos o generar bloques largos de código en el primer turno (Fase 1: Destilación). Si el prompt ya adjunta el contrato o solicita ejecutar una mutación acotada (Fase 2), el agente verifica el selector y ejecuta hasta superar el Gate de Salida.

---

## 2. Matriz Universal de 3 Estratos (Agnóstica de Proveedor) y Mapeo de UI

| Estrato Universal | Criterio Agnóstico de Clasificación | Ejemplos de Selector (Antigravity / Claude / OpenAI) | Ámbito Óptimo de Asignación |
| :--- | :--- | :--- | :--- |
| **Estrato 1 — Triaje / Fast** | Modelos rápidos/ligeros (`flash`, `haiku`, `mini`, `nano`, `lite`) o modo `Fast` / `Minimal`. | `Gemini 3.8 Flash \| High (Fast)`, `Claude Haiku`, `GPT-Mini` | Consultas directas, bash, diffs de 1–2 archivos y Fase 1 (destilación de contrato `/goal`). |
| **Estrato 2 — Ejecución Acotada (`Low` / `Medium`)** | Modelos de frontera en esfuerzo `Low` ($\le 4$ archivos) o `Medium` ($> 4$ archivos). | `Gemini 4 Argon \| Low/Medium`, `Claude Sonnet \| Low/Medium`, `GPT-OSS 120B \| Medium` | Fase 2: ejecución de contratos cerrados (`Low` para $\le 4$ archivos; `Medium` para refactors $> 4$ archivos). |
| **Estrato 3 — Razonamiento Profundo / Apex (`High`)** | Modelos pesados (`opus`, `o1`, `o3`, `ultra`) o modo `High` / `Max` / `Extended`. | `Gemini 4 Argon \| High`, `Claude Opus \| High` | Reservado **exclusivamente** para arquitectura crítica Ring-0, concurrencia, verificación formal (Lean 4/Z3) o debugging raíz multifichero. |

---

## 3. Protocolo de Ejecución en 2 Fases

### Fase 1: Destilación y Contrato (Estrato 1 — Fast)
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
   🔄 ROTAR SELECTOR A: <Estrato / Modelo recomendado> | NIVEL: <Low | Medium | High | Fast>

   1. OBJETIVO EXACTO: <1 frase técnica sin ambigüedad>
   2. ARCHIVOS PERMITIDOS (Write): <rutas exactas y líneas aproximadas>
   3. ARCHIVOS DE CONTEXTO (Read-Only): <rutas exactas; prohibido leer fuera de aquí>
   4. RESTRICCIONES: No refactorizar código adyacente, no añadir dependencias, no explicar cambios.
   5. GATE DE SALIDA (Stop Condition): <comando exacto en terminal que valida el cambio y detiene al agente>
   ```
5. **Cierre de Turno en Silicio (INV_C5_ANTIGRAVITY_RUNTIME):**
   Para satisfacer el `GoalStopHook` del runtime, incluir al final de la respuesta:
   `<!-- GOAL_COMPLETE -->`

### Fase 2: Ejecución Asignada (Estrato 2 — Low / Medium)
1. Funciona tanto pegando el bloque del contrato directamente (sin escribir `/goal`) como invocando `/goal`.
2. El modelo asignado audita que su Estrato/Nivel activo coincida con el prescrito, ejecuta los cambios únicamente en los archivos permitidos, valida el **Gate de Salida** (código 0) y cierra con el veredicto en la firma (`ÓPTIMO` o `DESAJUSTADO -> Óptimo: ...`).
