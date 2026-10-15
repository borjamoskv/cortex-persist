---
name: c5-ring0-babylon-kernel
display_name: Ring-0 BABYLON Kernel
description: Enruta auditorías y trabajo de kernel, Lean 4/Z3, BFT, Seqlock, silicio,
  inferencia local y atestación; carga solo el módulo relevante. Dispara con "ring0
  hub", "kernel hub", "lean 4", "larsa", "kudurru", "eridu", "laya".
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

# Ring-0 BABYLON Kernel

> **Directiva Declarativa:** Selecciona módulos bajo demanda; cada módulo conserva su contrato.

## Uso

1. Identifica la petición y consulta los aliases de la tabla o `references/aliases.json`.
2. Lee únicamente el módulo o los módulos que corresponden a la petición.
3. Conserva su rol, ámbito, restricciones y recursos antes de ejecutar su procedimiento.
4. Si el módulo remite a un recurso relativo, resuélvelo desde su carpeta original preservada.
5. No interpretes la carga del hub como autorización para ejecutar todas sus instrucciones.
6. Los nombres originales permanecen como aliases compatibles y comandos independientes.

## Resolver aliases sin ejecutar módulos

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
La salida lista los módulos candidatos y sus rutas; no ejecuta sus procedimientos.
El resolver normaliza mayúsculas y acentos, prioriza coincidencias exactas y respeta límites de palabra.
Una selección múltiple requiere leer los candidatos pertinentes; no elimina contratos por similitud temática.

## Módulos de ámbito global

| Módulo íntegro | Nombres y triggers conservados |
| --- | --- |
| [babylon-shield](references/modules/babylon-shield/MODULE.md) | `babylon-shield`, `/babylon-shield`, `babylon shield`, `escudo termodinámico`, `ring-0 shield`, `prevenir anergía`, `atestación babylon`, `invariantes ring-0`, `protección ring-0` |
| [c5-mushushu-0](references/modules/c5-mushushu-0/MODULE.md) | `c5-mushushu-0`, `/c5-mushushu-0`, `mushushu`, `mushushu-0`, `firewall epistémico`, `apoptosis termodinámica` |
| [c5-kudurru-64](references/modules/c5-kudurru-64/MODULE.md) | `c5-kudurru-64`, `/c5-kudurru-64`, `kudurru`, `kudurru-64`, `filtro de gravedad`, `seqlock 64b`, `ddos cognitivo` |
| [c5-larsa-120](references/modules/c5-larsa-120/MODULE.md) | `c5-larsa-120`, `/c5-larsa-120`, `larsa`, `larsa-120`, `consenso bft`, `tríada arquitectónica`, `consenso isostático` |
| [c5-enki-60](references/modules/c5-enki-60/MODULE.md) | `c5-enki-60`, `/c5-enki-60`, `enki`, `enki-60`, `cálculo sexagesimal`, `aritmética base 60`, `precisión sexagesimal` |
| [c5-lean4-axiomatic-orchestrator](references/modules/c5-lean4-axiomatic-orchestrator/MODULE.md) | `c5-lean4-axiomatic-orchestrator`, `/c5-lean4-axiomatic-orchestrator`, `lean 4`, `formalizar en lean`, `oráculo axiomático`, `lake build`, `verificación formal`, `axiomas lean`, `probar teorema`, `neuro-simbólico` |
| [c5-lean4-neurosymbolic-architect](references/modules/c5-lean4-neurosymbolic-architect/MODULE.md) | `c5-lean4-neurosymbolic-architect`, `/c5-lean4-neurosymbolic-architect`, `lean 4 ffi`, `agente neuro-simbólico`, `autopoiesis coinductiva`, `itrees lean` |
| [c5-ctm-formal-architect](references/modules/c5-ctm-formal-architect/MODULE.md) | `c5-ctm-formal-architect`, `/c5-ctm-formal-architect`, `ctm benchmark`, `ctm formalization`, `lean 4 ctm`, `abduction vs deduction`, `falsification matrix`, `refinement trace` |
| [c5-silicon-stress-suite](references/modules/c5-silicon-stress-suite/MODULE.md) | `c5-silicon-stress-suite`, `/c5-silicon-stress-suite`, `pruebas de estres`, `stress test swarm`, `estres enjambre`, `concurrencia de silicio`, `stress suite`, `poc`, `test de estres`, `estres silicio` |
| [c5-sovereign-binary-architect](references/modules/c5-sovereign-binary-architect/MODULE.md) | `c5-sovereign-binary-architect`, `/c5-sovereign-binary-architect`, `binario estático`, `aislar dependencias`, `soberanía termodinámica`, `c5-sovereign-binary`, `compilación musl`, `binario soberano` |
| [c5-sovereign-inference-runtime](references/modules/c5-sovereign-inference-runtime/MODULE.md) | `c5-sovereign-inference-runtime`, `/c5-sovereign-inference-runtime`, `eridu-infer`, `inferencia soberana`, `appliance ia`, `lm studio protocolo`, `motor inferencia local`, `air-gapped infer`, `servidor openai local rust`, `sovereign inference runtime`, `desplegar eridu-infer`, `tríada jurídica` |
| [c5-sovereign-system1-engine](references/modules/c5-sovereign-system1-engine/MODULE.md) | `c5-sovereign-system1-engine`, `/c5-sovereign-system1-engine`, `laya`, `sistema 1 edge`, `jev local`, `triage desacoplado`, `kudurru 64 socket`, `decision engine local` |
| [c5-thermos-audit](references/modules/c5-thermos-audit/MODULE.md) | `c5-thermos-audit`, `/c5-thermos-audit`, `thermos`, `thermos audit`, `auditoría termonuclear`, `double thermo`, `revisión termonuclear`, `revisar rama a fondo`, `thermo review` |
| [opentimestamps-l5-diagnostics](references/modules/opentimestamps-l5-diagnostics/MODULE.md) | `opentimestamps-l5-diagnostics`, `/opentimestamps-l5-diagnostics`, `opentimestamps`, `ots verify`, `atestación l5`, `bitcoin timestamp`, `l5 diagnostics`, `ots bitcoin`, `sellado temporal l5` |
