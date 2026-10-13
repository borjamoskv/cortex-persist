---
name: autodidact-omega
display_name: Motor Autodidact-Ω de Investigación Profunda y Falsación Popperiana
description: Investigación profunda de frontera, síntesis de cristales ontológicos, verificación de papers/estudios, falsación Popperiana y atestación SCITT con asignación asimétrica de modelos (Flash para recolección, Argon con thinking controlado para síntesis formal). Dispara con "autodidact", "autodidact-omega", "investigación profunda", "investigar paper", "cristal ontológico", "deep research".
role: arquitecto
allowed_roles:
- arquitecto
- auditor
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# Motor Autodidact-Ω de Investigación Profunda y Falsación Popperiana

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `arquitecto` (Diseño Sistémico & Contratos de Invariantes)
> - **Modo de Acceso a Worktree:** `spec-only` (Lectura profunda y modelado formal; emisión de especificaciones sin mutación de código de producción)
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
- `"deep research"`
- `"papers"`
- `"papers'"`

---

## 2. Invariante Asimétrica de Modelos y Control de Cuota (Landauer Gate)

> [!CAUTION]
> **Veto a la Quema de Cuota en Fase de Búsqueda:** Queda estrictamente prohibido utilizar modelos de razonamiento profundo (`gemini-4-argon` o similares con `thinking_level="medium"` o superior) para tareas de recolección de papers, scraping o lectura de texto plano. Dicha práctica disipa hasta el 50% de la cuota en 2 consultas sin aportar compresión.

| Fase | Modelo Obligatorio | Thinking Level / Parámetros | Justificación Termodinámica |
|---|---|---|---|
| **Fase 1: Recolección** | `gemini-3.8-flash` | N/A (Desactivado) | Búsqueda I/O pura, extracción de citas y filtrado de DOIs. Máximo ancho de banda sin latencia. |
| **Fase 2: Falsación** | `gemini-3.8-flash` | `thinking_level="low"` | Evaluación de contra-ejemplos y 6 regímenes de estrés con bajo consumo. |
| **Fase 3: Cristal** | `gemini-4-argon` | `thinking_level="low"` (máx. "medium" si se justifica) | Síntesis ontológica formal y modelado matemático. Exige control estricto de presupuesto. |
| **Fase 4: Atestación** | Determinista local | SHA3-256 en silicio | Cero coste de inferencia. Firma criptográfica directa. |
| **Fase 5: PoC Silicio** | `gemini-3.8-flash` | N/A | Escritura de scripts ejecutables y ejecución de pruebas. |

---

## 3. Algoritmo de Ejecución (5 Fases C5-REAL)

```
[ Entrada: Tema / Paper / Conjetura ]
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 1: Recolección & Ground Truth       │ ──> (arXiv, PubMed, IEEE, RFCs) [Flash]
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 2: Falsación Popperiana            │ ──> (6 Regímenes de Estrés Exergético) [Flash]
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 3: Cristal Ontológico (21k Dim)    │ ──> (autodidact_omega_<slug>_crystal.md) [Argon]
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 4: Atestación SCITT & SHA3-256     │ ──> (Sellado en Ledger / Digest Local)
 └─────────────────────────────────────────┘
         │
         ▼
 ┌─────────────────────────────────────────┐
 │ Fase 5: Falsación en Silicio (PoC)      │ ──> (Código ejecutable sin teoría continua)
 └─────────────────────────────────────────┘
```

---

## 4. Cadencia Dialéctica ante Pulsos Monoverbales (Modo D)
Cuando el operador guíe la investigación mediante pulsos breves o monoverbales:
1. **Trigger Inicial / Tesis:** Genera el Cristal Ontológico preliminar (Fases 1–3).
2. **Pulso `itera` / Antítesis:** Falsación en Silicio (Fase 5) mediante PoC ejecutable y benchmark empírico.
3. **Pulso `papers` o `papers'` / Síntesis:** Compilación estructurada del Corpus de Literatura Científica Primaria (DOIs, preprints de frontera arXiv, contrastes empíricos).
4. **Pulso `apex` / Cierre:** Arquitectura de Sustrato y mitigación definitiva en Anillo-0.

---

## 5. Especificación Detallada de Fases

### Fase 1: Recolección y Extracción de Ground Truth
1. Extraer afirmaciones literales, ecuaciones y referencias (DOIs/RFCs) de la materia de estudio.
2. Separar explícitamente el **Territorio** (citas literales verificadas con punteros) del **Mapa** (interpretación del analista).

### Fase 2: Matriz de Falsación Popperiana
Someter el modelo a los 6 Regímenes de Estrés Exergético:
1. **Estrés de Ambigüedad:** Evaluar respuesta bajo inputs degradados o ruido sintáctico.
2. **Estrés de Acoplamiento:** Evaluar asincronía y barreras de comunicación inter-nodo.
3. **Estrés de Contexto:** Medir derivas semánticas y alucinaciones latentes.
4. **Estrés de Emergencia:** Probar comportamiento fuera de distribución de entrenamiento.
5. **Estrés de Verificación:** Forzar controles negativos y lemas de refutación formal.
6. **Estrés de Deuda:** Evaluar complejidad computacional acumulada frente a la ganancia de compresión.

### Fase 3: Generación del Cristal Ontológico (`autodidact_omega_<slug>_crystal.md`)
Generar el artefacto formal con la siguiente taxonomía:
- **Resumen Ejecutivo de Alta Exergía**
- **Invariantes Categóricas e Isomorfismos Silicio-Bio**
- **Matriz de Falsación (Claims Verificados vs. Refutados vs. Conjeturas)**
- **Pruebas de Estrés y Demostraciones Formales (Lean 4 / Álgebra de Estados)**
- **Recomendaciones de Arquitectura y Sustrato**

### Fase 4: Atestación y Sellado Criptográfico
1. Calcular la firma SHA3-256 del cristal ontológico generado.
2. Registrar el digest en el log de sesión o ledger local, garantizando trazabilidad e inmutabilidad temporal.

### Fase 5: Falsación en Silicio (Transición Mapa-Territorio)
Si tras la atestación el usuario emite una directiva de avance continuo (ej. `"sigue"`, `"ejecuta"`, `"falsa esto"`):
- Queda **terminantemente prohibido** emitir más texto discursivo o justificaciones abstractas.
- El agente **DEBE** escribir un **Proof of Concept (PoC) aislado y ejecutable**, ejecutarlo en el entorno y reportar la telemetría empírica como único veredicto válido.

---

## 6. Invariante Epistémica Obligatoria

> [!IMPORTANT]
> **Prohibición de Circularidad**: El motor Autodidact-Ω **NUNCA** considerará una prueba como superada simplemente porque un script de validación pase sus propios casos de prueba simulados. Todo veredicto exige contraste empírico contra fuentes primarias o ejecución determinista en silicio.
