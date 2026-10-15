---
name: c5_causal_planning_invariant
description: Invariante de planificación causal determinista en grafos DAG y puertas de validación.
trigger: "model_decision"
---

# Invariante de Planificación Causal Determinista (INV_C5_CAUSAL_PLANNING)

## 1. Mandato Fundamental (Anti-Vibe-Planning)
Toda tarea de refactorización estructural, integración de múltiples subsistemas, alteración de esquemas de datos o modificación de Ring-0/C-ABI que requiera planificación previa DEBE operar estrictamente bajo el **Protocolo PLAN-Ω**. Queda terminantemente prohibido emitir checklists lineales planas sin orden parcial de dependencias ni condiciones de salida en silicio.

---

## 2. Las Cuatro Leyes de la Planificación Causal

1. **CP-1: PROBE BEFORE SPEC (Sondeo Previo Obligatorio):**
   Antes de redactar la especificación de cambios en `implementation_plan.md`, el agente DEBE ejecutar un sondeo de viabilidad activo en silicio (one-liner de compilación, import de tipos o `git grep`) para verificar que las asunciones base del entorno son verdaderas. Prohibido planificar sobre librerías, métodos o APIs no verificadas.

2. **CP-2: TOPOLOGÍA EN DAG (Orden Parcial de 4 Niveles):**
   Las tareas se organizan obligatoriamente en un Grafo Acíclico Dirigido (DAG):
   - **N0 (Ground Truth & Baseline):** Sondas de lectura, comprobación de tests actuales y backups.
   - **N1 (Core & Contratos de Tipos):** Estructuras de datos, esquemas de BD, interfaces C-ABI/Traits.
   - **N2 (Lógica de Motor & Adaptadores):** Implementación de subsistemas, CLI, integración inter-componente.
   - **N3 (Validación & Sellado):** Tests de estrés, suites de regresión y commits atómicos.

3. **CP-3: DEMARCACIÓN DE PUERTAS (Two-Way vs. One-Way Doors):**
   - **Two-Way Doors (Reversibles):** Modificaciones a archivos nuevos, tests aislados, análisis de lectura.
   - **One-Way Doors (Irreversibles / Alto Impacto):** Migraciones de base de datos, purgas de archivos (`rm`), despliegues o alteración de estado externo.
   - *Invariante:* Toda One-Way Door exige obligatoriamente: (a) comando de rollback probado y preparado con antelación, y (b) autorización Touch ID explícita del Operador Raíz.

4. **CP-4: MICRO-GATES EN SILICIO FAIL-STOP:**
   Cada bloque del plan vincula de forma indivisible la mutación con su aserción empírica en hardware (`Mutación + Assert en Silicio`). Si el comando de verificación falla, el ejecutor se detiene inmediatamente (Fail-Stop), impidiendo la propagación de fallos en cascada.

---

## 3. Protocolo Anti-Thrashing (Regla de los 2 Intentos)
Si un micro-gate falla consecutivamente en dos intentos:
- Queda estrictamente prohibido realizar modificaciones estocásticas o parches ciegos en bucle.
- El agente congela la ejecución, marca el bloque como `[BLOCKED]` en el plan, y presenta una bifurcación técnica estructurada al Operador Raíz.
