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

## Desempate de triggers compartidos

`seqlock 64b` también activa `shared-manifest-kernel` en el ámbito del proyecto. Usa `c5-kudurru-64` para el formato o los envelopes KUDURRU-64; usa `shared-manifest-kernel` para SharedManifest, memoria compartida o IPC de BABYLON-60. Si solo aparece el trigger y el tema no aclara el destino, pregunta antes de cargar procedimientos.

## Resolver aliases sin ejecutar módulos

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
La salida lista los módulos candidatos y sus rutas; no ejecuta sus procedimientos.
El resolver normaliza mayúsculas y acentos, prioriza coincidencias exactas y respeta límites de palabra.
Una selección múltiple requiere leer los candidatos pertinentes; no elimina contratos por similitud temática.

## Módulos disponibles

| Procedimiento | Intención contextual |
| --- | --- |
| [babylon-shield](references/modules/babylon-shield/MODULE.md) | Escudo Termodinámico Ring-0 (Caballo de Troya). Inyecta las Invariantes C5-REAL, previene bucles de anergía y fuerza la atestación de estado antes de cualquier mutación del código. |
| [c5-ctm-formal-architect](references/modules/c5-ctm-formal-architect/MODULE.md) | Arquitectura formal y empírica de Cognitive Transition Machines (CTM) e invariantes Lean 4 (AP-01 a AP-09). |
| [c5-enki-60](references/modules/c5-enki-60/MODULE.md) | Motor aritmético de precisión sexagesimal y cálculo pesado en silicio (ENKI-60). |
| [c5-kudurru-64](references/modules/c5-kudurru-64/MODULE.md) | Filtro de gravedad Lock-Free Seqlock 64B en frontera Ring-0 contra DDoS cognitivo (KUDURRU-64). |
| [c5-larsa-120](references/modules/c5-larsa-120/MODULE.md) | Orquestador de Consenso BFT Isostático de la Tríada Arquitectónica (LARSA-120). |
| [c5-lean4-axiomatic-orchestrator](references/modules/c5-lean4-axiomatic-orchestrator/MODULE.md) | Orquestación neuro-simbólica y verificación formal en Lean 4 (ΔΦ > 0, antipatrones AP-01..09 y Lake build). |
| [c5-lean4-neurosymbolic-architect](references/modules/c5-lean4-neurosymbolic-architect/MODULE.md) | Arquitectura de agentes neuro-simbólicos y binarios soberanos en Lean 4 (C-FFI, ITrees, lógica lineal). |
| [c5-mushushu-0](references/modules/c5-mushushu-0/MODULE.md) | Oráculo formal y firewall epistémico Ring-0 para validación determinista y apoptosis (MUSHUSHU-0). |
| [c5-silicon-stress-suite](references/modules/c5-silicon-stress-suite/MODULE.md) | Pruebas de estrés en paralelo y benchmarks de silicio (multicast O(1), Seqlock KUDURRU-64, BFT y Touch ID COSE_Sign1). |
| [c5-sovereign-binary-architect](references/modules/c5-sovereign-binary-architect/MODULE.md) | Desacopla dependencias pesadas (FFI/PyO3/Node), aísla el núcleo matemático detrás de feature flags y configura binarios estáticos soberanos (x86_64-unknown-linux-musl) de baja entropía. |
| [c5-sovereign-inference-runtime](references/modules/c5-sovereign-inference-runtime/MODULE.md) | Despliegue y auditoría de motores de inferencia local bare-metal. |
| [c5-sovereign-system1-engine](references/modules/c5-sovereign-system1-engine/MODULE.md) | Diseño, compilación, despliegue y calibración on-device de motores de decisión de Sistema 1 no autorregresivos (LAYA / ModernBERT) en silicio local Apple Silicon. |
| [c5-thermos-audit](references/modules/c5-thermos-audit/MODULE.md) | Auditoría termonuclear de ramas y PRs con 2 subagentes paralelos (Seguridad/DevEx vs. Regla 1000 líneas/Code Judo). |
| [opentimestamps-l5-diagnostics](references/modules/opentimestamps-l5-diagnostics/MODULE.md) | Verificación de atestación criptográfica y estampados temporales L5 en Bitcoin (OpenTimestamps). |
