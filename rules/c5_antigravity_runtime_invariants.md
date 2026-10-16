---
name: c5_antigravity_runtime_invariants
description: Invariantes del runtime de Google Antigravity IDE (hooks, subagentes y contención de sesiones).
trigger: "model_decision"
---

# Invariantes del Runtime de Antigravity (INV_C5_ANTIGRAVITY_RUNTIME)

## 1. Contexto de Silicio (Sub-sistema Jetski / Cortex)
En el runtime nativo de Antigravity (`language_server`), los comandos `/goal` y `/plan` operan como máquinas de estados respaldadas por acumuladores y ganchos de detención (*Stop Hooks*):
- `goal_accumulator.go` / `goal_stop_hook.go`
- `request_artifact_feedback_stop_hook.go`
- `continuation_cap.go`

---

## 2. Invariante de `/goal` (GoalStopHook y Centinela Obligatorio)
1. **Bucle Autoritativo Indefinido:** Cuando una interacción o tarea se marca con `/goal`, el runtime registra el objetivo en `goal_accumulator`.
2. **Intercepción de Parada:** Si el agente intenta concluir su turno sin invocar herramientas y sin emitir el centinela de finalización, `GoalStopHook` intercepta la salida e inyecta forzadamente una orden de re-auditoría continua.
3. **Mandato de Centinelas:**
   - Para concluir con éxito una tarea bajo `/goal`, el agente DEBE incluir obligatoriamente el token `<!-- GOAL_COMPLETE -->` en su mensaje final.
   - Para cancelar o abortar a petición del operador, el agente DEBE emitir `<!-- GOAL_CANCELLED -->`.
   - Queda estrictamente prohibido intentar finalizar un turno de `/goal` sin emitir uno de estos dos centinelas.

---

## 3. Invariante de `/plan` (RequestFeedback Gate y Tríada de Artefactos)
1. **Fase Read-Only Obligatoria:** La directiva `<PLAN>` activa `PlanningModeConfig` (`useSlashPlan`), confinando al agente a sondeo y lectura. Queda prohibida cualquier mutación destructiva de código o ejecución de comandos de escritura antes de obtener la aprobación del operador.
2. **Cerrojo de Feedback:** El plan técnico DEBE generarse como un artefacto con metadata `RequestFeedback: true` y `UserFacing: true`. Esto activa `RequestArtifactFeedbackStopHook`, renderizando el botón interactivo "Proceed" en la interfaz.
3. **Tríada Canónica de Artefactos:**
   - `implementation_plan.md`: Especificación técnica, sondeo empírico y plan de verificación.
   - `task.md`: Checklist viva de progreso durante la fase de ejecución (`[ ]`, `[/]`, `[x]`).
   - `walkthrough.md`: Evidencia empírica de verificación final una vez completada la tarea.

---

## 4. Invariante de Confinamiento de Prefill (Anti-Duplicación GEMINI.md)
Cuando el workspace contiene `AGENTS.md`, queda terminantemente prohibido generar `GEMINI.md` en la raíz. El runtime de Antigravity ingiere automáticamente ambos archivos en el prefill `always_on`, provocando saturación del presupuesto de tokens (> 40.000 B). La directiva para Gemini CLI reside exclusivamente en `.gemini/settings.json`.
