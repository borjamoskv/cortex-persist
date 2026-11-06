---
name: c5_antigravity_runtime_invariants
description: Invariantes del runtime de Google Antigravity IDE (hooks, subagentes, contención de sesiones y prohibición de robo de foco en WindowServer/navegador).
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

---

## 5. Invariante de Cero Robo de Foco en macOS (`INV_C5_ZERO_FOCUS_STEAL`)
Queda **estrictamente prohibido** que cualquier agente, subagente, script o herramienta MCP altere la ventana activa (`frontmost`) o robe el foco de teclado/ratón en `WindowServer` de macOS sin aviso y permiso explícito previo del Operador:
1. **Prohibición de `open` en Primer Plano:** Todo comando `open` en shell DEBE incluir obligatoriamente el flag `-g` (`--background`, ej. `open -g "https://..."` o `open -g -a Safari`) para impedir que macOS conmute de aplicación o de Space.
2. **Veto a `.activate()` en AppleScript / JXA:** Queda prohibido invocar `tell application "..." to activate`, `Application("...").activate()`, o `set frontmost to true` en `osascript`. La interacción con Safari (`do JavaScript ... in current tab of window 1`) y otras apps debe ejecutarse estrictamente en segundo plano.
3. **Navegación y Automatización Headless por Defecto:** Para pruebas web, scraping o verificación de UI con Chrome/Playwright/Puppeteer, se debe forzar siempre `--headless=new` o emplear `read_url_content` / `curl`. Queda prohibido levantar ventanas visibles del navegador (incluyendo llamadas sorpresivas al navegador headful o `Page.bringToFront` / `Target.activateTarget`) salvo que el Operador solicite explícitamente una sesión visual interactiva.

---

## 6. Invariante de Subagentes Asíncronos en Antigravity 2.0 (`INV_C5_ASYNC_SUBAGENTS_RUNTIME`)
1. **Esquema Nativo `.md` y Veto a `.json` Heredado:** Todo subagente persistente en `~/.gemini/config/agents/` o plugins (`agents/*.md`) DEBE definirse en Markdown con frontmatter YAML (`name`, `description`, `mainAgent`, `subagent`, `model`, `commandExecutionPolicy`, `tools`). Queda prohibido el formato `.json` heredado.
2. **Lista Blanca Estricta de `tools` en Frontmatter YAML (Prevención de Hang R1):** Especificar nombres de herramientas no mapeados por el cargador de subagentes `.md` (ej. `read_file`, `write_file`, `edit_file`) provoca un bloqueo indefinido (*hang* silencioso) al instanciar el subagente. Sólo se permiten los identificadores internos validados:
   - Lectura y búsqueda: `view_file`, `list_dir`, `grep_search`, `find_by_name`, `search_web`, `read_url_content`
   - Mutación y ejecución: `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `run_command`
   - Coordinación y control: `send_message`, `schedule`, `invoke_subagent`, `manage_subagents`, `ask_question`
3. **Aislamiento de Profundidad ($d=1$) y Kill en Cascada:**
   - Los subagentes hoja (`moskvbot`) tienen estrictamente prohibido incluir `invoke_subagent` o `manage_subagents` en su lista `tools`, acotando la profundidad del árbol a $d=1$.
   - `manage_subagents(Action="kill")` sobre un subagente padre termina en cascada a todos sus descendientes y elimina sus workspaces ramificados (`branch`/`share`), preservando logs y artefactos.
4. **Degradación de `Workspace: "branch" | "share"` sin Workspace Activo (Regímenes R2/R5):**
   - Los modos `Workspace="branch"` y `Workspace="share"` en `invoke_subagent` requieren que la sesión tenga un repositorio VCS vinculado como workspace activo en el IDE.
   - Cuando se opere fuera de un workspace activo (`Outside of Project`), ambos modos se degradan silenciosamente al filesystem compartido (`inherit`). En dicho régimen, queda prohibido despachar múltiples subagentes con herramientas de escritura sobre el mismo directorio sin partición disjunta explícita de rutas (`write_scope`).
5. **Wakeup Reactivo y Veto a Polling / Timers `any` (Régimen R6):**
   - Tras `invoke_subagent`, queda prohibido hacer *polling* mediante `manage_subagents(Action="list")` en bucle; el runtime reanuda reactivamente al agente padre cuando el subagente transiciona `Running` $\to$ `Idle`.
   - Queda prohibido combinar `invoke_subagent` con `schedule(TimerCondition="any")`, ya que cualquier comando de fondo que finalice cancela prematuramente el temporizador. Si se requiere un SLA de corte sobre un subagente específico, usar exclusivamente `TimerCondition="<conversationId_del_subagente>"`.
