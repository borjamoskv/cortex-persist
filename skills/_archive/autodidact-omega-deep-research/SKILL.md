---
name: autodidact-omega-deep-research
display_name: Motor Autodidact-Ω de Investigación Profunda y Falsación Popperiana
description: Investigación profunda de frontera, síntesis de cristales ontológicos, verificación de papers/estudios, falsación Popperiana y atestación SCITT. Dispara con "autodidact", "autodidact-omega", "investigación profunda", "investigar paper", "cristal ontológico", "deep research".
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

# Motor Autodidact-Ω de Investigación Profunda y Falsación Popperiana

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `arquitecto` (Arquitecto (Diseño Sistémico & Contratos de Invariantes))
> - **Modo de Acceso a Worktree:** `spec-only` (spec-only (Lectura profunda y modelado formal; emisión de especificaciones sin mutación de código de producción))
> - **Fase Causal:** `design`
> - **Contrato Handoff:** Recibe de `operador` $\to$ Despacha a `ejecutor`

Este protocolo rige el proceso agéntico de **investigación profunda de frontera (Deep Research)**, deducción formal, falsación Popperiana y cristalización ontológica de alta exergía ($\ge 19.000 / 21.000$).

---

## 1. Disparadores (Triggers)
- `"autodidact"`
- `"autodidact-omega"`
- `"investigación profunda"`
- `"investigar paper"`
- `"cristal ontológico"`
- "deep research"
- "papers"
- "papers'"

---

## 2. Algoritmo de Ejecución (5 Fases C5-REAL)

```
[ Entrada: Tema / Paper / Conjetura ]
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 1: Recolección & Ground Truth       │ ──> (arXiv, PubMed, IEEE, IETF RFCs)
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 2: Falsación Popperiana            │ ──> (Búsqueda de contra-ejemplos y límites físicos)
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 3: Cristal Ontológico (21k Dim)    │ ──> (Genera autodidact_omega_<slug>_crystal.md)
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 4: Atestación SCITT & SHA3-256     │ ──> (Sellado en el Ledger WORM)
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 5: Falsación en Silicio (PoC)      │ ──> (Transducción de Recomendación a Ejecutable)
 └─────────────────────────────────────────┘
```

---

### 2.1 Cadencia Dialéctica ante Pulsos Monoverbales (Modo D)
Cuando el operador guíe la investigación mediante pulsos breves o monoverbales:
1. **Trigger Inicial / Tesis:** Genera el Cristal Ontológico preliminar (Fases 1–3).
2. **Pulso `itera` / Antítesis:** Falsación en Silicio (Fase 5) mediante PoC ejecutable y benchmark empírico (ej. Monte Carlo de fallas).
3. **Pulso `papers` o `papers'` / Síntesis:** Compilación estructurada del Corpus de Literatura Científica Primaria (DOIs, preprints de frontera arXiv, contrastes teóricos vs empíricos).
4. **Pulso `apex` / Cierre:** Arquitectura de Sustrato y mitigación definitiva en Anillo-0 (`KUDURRU-64`).

---

## 3. Especificación de Fases

### Fase 1: Recolección y Extracción de Ground Truth
1. Extraer afirmaciones literales, ecuaciones y referencias (DOIs/RFCs) de la materia de estudio.
2. Separar explícitamente el **Territorio** (citas literales del autor) del **Mapa** (traducción a primitivas termodinámicas e informacionales).

### Fase 2: Matriz de Falsación Popperiana
Someter el modelo a los 6 Regímenes de Estrés Exergético:
1. **Estrés de Ambigüedad:** Evaluar respuesta bajo inputs degradados.
2. **Estrés de Acoplamiento:** Evaluar asincronía y barreras de comunicación.
3. **Estrés de Contexto:** Medir derivas semánticas y alucinaciones latentes.
4. **Estrés de Emergencia:** Probar comportamiento fuera de distribución.
5. **Estrés de Verificación:** Forzar controles negativos y lemas de refutación.
6. **Estrés de Deuda:** Evaluar complejidad computacional acumulada.

### Fase 3: Generación del Cristal Ontológico (`autodidact_omega_<slug>_crystal.md`)
Generar un archivo de cristal ontológico en el directorio de artefactos con la siguiente taxonomía:
- **Resumen Ejecutivo de Alta Exergía**
- **Invariantes Categóricas e Isomorfismos Silicio-Bio**
- **Matriz de Falsación (Claims Verificados vs. Refutados vs. Conjeturas)**
- **Pruebas de Estrés y Demostraciones Formales (Lean 4 / SMT)**
- **Recomendaciones de Arquitectura y Sustrato**

### Fase 4: Atestación y Sellado SCITT
1. Calcular la firma SHA3-256 del cristal ontológico.
2. Generar el recibo SCITT (RFC 9942 compliant) y registrar la entrada en el Ledger BFT (`cortex.db`).

### Fase 5: Falsación en Silicio (Transición Mapa-Territorio)
Si tras la atestación (Fase 4) el usuario emite una directiva de avance continuo (ej. `"sigue"`, `"ejecuta"`, `"falsa esto"`), el agente **NUNCA** generará más teoría pasiva. 
El agente DEBE materializar la principal "Recomendación de Arquitectura y Sustrato" del Cristal Ontológico escribiendo un **Proof of Concept (PoC) aislado y ejecutable** (ej. un script en `scripts/c5_demos/`). El PoC debe compilarse, ejecutarse y reportar el *log* empírico como refutación definitiva.

---

## 4. Invariante Epistémica Obligatoria

> [!IMPORTANT]
> **Prohibición de Circularidad**: El motor Autodidact-Ω **NUNCA** considerará una prueba como superada simplemente porque un script linter pase sus propios casos de prueba mockeados. Todo veredicto exige contraste empírico contra fuentes primarias o derivación analítica de validez incondicional.
