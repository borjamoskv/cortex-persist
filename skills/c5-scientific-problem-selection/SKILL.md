---
name: c5-scientific-problem-selection
display_name: Selección Estratégica de Problemas Científicos
description: Selección estratégica de problemas de investigación, matrices de riesgo popperianas y desatasco de proyectos I+D. Dispara con "selección de problemas", "scientific problem selection", "desatascar investigación", "unstick research", "matriz de riesgo científico", "priorización popperiana".
role: arquitecto
allowed_roles:
- arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# Skill: C5 Scientific Problem Selection

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `arquitecto` (Arquitecto (Diseño Sistémico & Contratos de Invariantes))
> - **Modo de Acceso a Worktree:** `spec-only` (spec-only (Lectura profunda y modelado formal; emisión de especificaciones sin mutación de código de producción))
> - **Fase Causal:** `design`
> - **Contrato Handoff:** Recibe de `operador` $\to$ Despacha a `ejecutor`

Este protocolo guía la selección de problemas de investigación estratégica, la evaluación de cuellos de botella conceptuales y la desconstrucción de bloqueos en proyectos I+D mediante rigor popperiano y análisis multidimensional.

---

## 1. Protocolo de Evaluación de Problemas

1. **Definición del Espacio de Estados:**
   - Formular la hipótesis nula ($H_0$) y la hipótesis alternativa ($H_1$).
   - Identificar las variables de control y los observables exergéticos del sistema.

2. **Matriz de Riesgo y Falsabilidad Popperiana:**
   - Evaluar si el problema propuesto posee experimentos con falsación realizable en $O(1)$ o $O(N)$ tiempo.
   - Clasificar según la matriz de impacto-incertidumbre:
     - *Cuadrante I (High Impact, Low Risk):* Prioridad A.
     - *Cuadrante II (High Impact, High Risk):* Requiere prototipo de prueba de concepto $10\times$.
     - *Cuadrante III (Low Impact, Low Risk):* Anergía/Trabajo rutinario; descartar o automatizar.

3. **Estrategia de Desatasco (Unsticking Engine):**
   - **Vía de Reducción Dimensional:** Aislar el acoplamiento no lineal más fuerte y modelar el sistema bajo un subespacio lineal simplificado.
   - **Vía de Analogía Categórica:** Mapear la estructura algebraica del problema hacia un dominio equivalente (ej. Mecánica Estadística $\leftrightarrow$ Teoría de la Información).

---

## 2. Salida Estructurada

Toda sesión de evaluación genera un **Research Decision Tree** conteniendo:
- **Matriz de Falsación:** Lista de pruebas mínimas para destruir la hipótesis.
- **Ruta Crítica:** Grafo DAG de hitos para la prueba de concepto inicial.
