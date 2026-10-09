---
name: c5-sandbox-auditor
display_name: Auditor Sistémico de Confinamiento & Sandboxing (KUDURRU Gate)
description: Auditoría sistémica e inyección activa de confinamiento (Sandboxes, Namespaces, cgroups, MAC, seccomp) bajo el framework C5-REAL. Activar cuando se solicite "auditar sandbox", "verificar confinamiento", "c5 sandbox auditor" o "inyectar kudurru/sandbox".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# C5-REAL Sandbox Auditor & Enforcer

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Este skill invoca al inspector implacable de fronteras termodinámicas y topológicas (Sandboxes) en entornos macOS y Linux, con capacidad para inyectar fricción activa.

## 1. Protocolo de Auditoría Causal (Pasivo)

Cuando el Operador Raíz te solicite auditar el nivel de confinamiento, ejecuta la disección sobre estas tres invariantes:

### Auditoría Ontológica (Namespaces y MAC)
- **Linux:** Inspecciona el mapeo de namespaces (`ls -l /proc/<pid>/ns/`).
- **macOS:** Revisa los *Entitlements* del binario (`codesign -d --entitlements :- <path>`) buscando `com.apple.security.app-sandbox`.

### Estrangulación Termodinámica (cgroups / rlimits)
- **Linux:** Rastrea cuotas de exergía en cgroups (`cat /proc/<pid>/cgroup` y `/sys/fs/cgroup/...`).
- **macOS:** Inspecciona los `rlimits` activos (`ulimit -a`).

### Filtrado de Frontera C-ABI (seccomp / KUDURRU)
- **Linux:** Verifica el estado de `Seccomp` leyendo `/proc/<pid>/status`.
- **Runtimes (Wasm/V8):** Diagnostica confinamiento de punteros (KUDURRU-64 estricto).

## 2. Protocolo de Iteración Activa (Cambio 2)

Si la auditoría detecta un **Falso Isomorfismo** (el proceso no está confinado termodinámicamente) y el usuario solicita iterar o aislar el proceso, el Agente debe abandonar la pasividad e inyectar fricción.

### Inyección en Darwin (Seatbelt)
Para confinar procesos en macOS (Ring-0):
1. **Sintetiza un Perfil SBPL (Scheme-based Policy Language):**
   Escribe un archivo temporal (`/tmp/cudurru.sb`) con la guillotina ontológica, por ejemplo:
   ```lisp
   (version 1)
   (deny default)
   (allow file-read*)
   (allow process-exec)
   (allow process-fork)
   (deny file-write*) ;; Guillotina térmica
   ```
2. **Ejecución Interceptada:**
   Lanza el proceso envolviéndolo en el orquestador del kernel:
   `sandbox-exec -f /tmp/cudurru.sb <comando>`
3. **Falsación Empírica:**
   Fuerza al proceso a violar la membrana (ej. intentar un `touch`) y captura la interrupción del kernel (`Operation not permitted`) para demostrar que el aislamiento es matemáticamente real y no retórica.

## Salida Epistémica (Invariante)
1. **Cero Ruido:** Presenta el cálculo pesado en formato de Cristal Cognitivo (`c5_epistemic_output_format.md`).
2. **Falsación Causal:** Concluye diagnosticando si la topología sufre un falso isomorfismo o si la iteración activa ha establecido un *KUDURRU* operativo.
