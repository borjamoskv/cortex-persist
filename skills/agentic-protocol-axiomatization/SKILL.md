---
name: agentic-protocol-axiomatization
display_name: Axiomatización de Protocolos Agénticos C5 & Generación DAC
description: Axiomatización formal de comandos, bucles deductivos y control de agentes bajo invariantes C5-REAL (PSAFE v3.0, AOF / AASAD v2.0). Dispara con "axiomatizar", "axiomatización", "/axiomatize", "/aasad-dac", "dac yaml", "oráculo axiomático", "bucle deductivo", "axiomas del agente", "protocolo axiomático".
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

# Axiomatización Formal de Protocolos Agénticos & DAC (AASAD v2.0)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `arquitecto` (Arquitecto (Diseño Sistémico & Contratos de Invariantes))
> - **Modo de Acceso a Worktree:** `spec-only` (spec-only (Lectura profunda y modelado formal; emisión de especificaciones sin mutación de código de producción))
> - **Fase Causal:** `design`
> - **Contrato Handoff:** Recibe de `operador` $\to$ Despacha a `ejecutor`

Este protocolo define la metodología unificada para transformar cualquier comando de control de agentes, bucle de ejecución o arquitectura agéntica en un **sistema formal lógico-deductivo** $\mathcal{G}$.

---

## 1. Sub-modos de Operación

### Modo A: Invocación Directa `/axiomatize` (Estructuración Física PSAFE v3.0)
Actúa como estructurador fundamental previo a escribir código crítico (kernel, unsafe, concurrencia):
1. **Fase 0 (Dominio Físico):** Define plataformas objetivo (`x86_64`, `aarch64`), modelo de memoria (`TSO`, `ARMv8 Weak`) y ABI (`System V`).
2. **Fase 1 (Axiomatización Formal):** Redacta axiomas `[AX-N]` atómicos y el Teorema de Corrección del Sistema.
3. **Matriz de Refutación Empírica:** Genera tabla Markdown (Axioma, Refutación Automatizable, Punto de Verificación, Mensaje Diagnóstico).
*Invariante:* PROHIBIDO emitir código fuente real hasta aprobar la axiomatización previa.

### Modo B: Invocación `/aasad-dac` (Agente Ontólogo Físico - AOF)
Asume el rol estricto de **AOF** bajo la Arquitectura Agéntica de Síntesis Axiomática Distribuida (AASAD v2.0):
1. Prohibida la síntesis de código. Eres exclusivamente ontólogo físico.
2. Emite **únicamente** un documento YAML estructurado como **DAC v2.0**:
   ```yaml
   dac_version: 2.0
   project: <nombre_componente>
   platform_targets: [x86_64, aarch64]
   memory_models: [TSO, ARMv8-Weak]
   abi: [SystemV-AMD64]
   axioms: [...]
   theorem: <declaracion_correccion_emergente>
   ```

---

## 2. Estructura Metodológica del Sistema Formal $\mathcal{G}$

**INVARIANTE METODOLÓGICO:** Jamás inventes axiomas sin haber aislado antes la primitiva irreducible. Un axioma dicta cómo se comporta una primitiva; no la sustituye. Sigue estrictamente esta jerarquía descendente:

### Nivel 1. Primitivas Irreducibles
* Define la unidad atómica de tu sistema (ej. La *Transición* $\Omega$, la *Restricción* $\mathcal{R}$, el *Estado*, la *Distinción*).
* Regla de oro: Si un concepto puede definirse a partir de otro, **no es una primitiva**.

### Nivel 2. Axiomas Fundamentales
Responde a la pregunta: *"¿Qué propiedades innegociables debe cumplir la primitiva?"*
* **Ejemplo (Causalidad):** Toda transición $A \to B$ implica una relación estricta de orden.
* **Ejemplo (Monotonía de Exergía):** La aplicación del operador $\Omega$ nunca incrementa la Entropía del sistema cerrado.
* Los axiomas deben ser ortogonales (independientes) y mínimos.

### Nivel 3. Definiciones
Construye conceptos de alto nivel usando solo Primitivas y Axiomas.
* Ej: Un "Bucle `while`" se define como la aplicación recursiva de $\Omega$ hasta que la guarda $\mathcal{G}$ evalúa a falso.

### Nivel 4. Teoremas y Corolarios
El valor de la teoría reside en demostrar propiedades emergentes (ej. Decidibilidad Termodinámica, Convergencia) que no eran obvias en los axiomas.

---

## 3. Pipeline de Realización Completa (End-to-End Delivery)

Para toda nueva axiomatización agéntica o termodinámica, el agente DEBE ejecutar la **Tríada de Realización Completa**:

1. **Especificación Teórica (`docs/06_theory/axiom_*.md`)**: Primitivas, Axiomas `AX-*`, Implicaciones Regulatorias (EU AI Act).
2. **Ejecución Causal Empírica (`scripts/c5_demos/poc_*.py`)**: Script ejecutable Python sin dependencias demostrando cuantitativamente los axiomas.
3. **Verificación Formal en Lean 4 (`proof/lean/Babylon.lean`)**: Tipos inductivos, axiomas y teoremas formalizados (`exact` / `decide`).
4. **Supervisión Bi-Modal Interactiva (`apps/`)**: Web App HTML/JS para supervisión humana por diseño (Art. 14 EU AI Act).

## 4. Axiomatización de Inferencias de Alto Riesgo (Transducción vs. Política)

Toda arquitectura agéntica que opere en dominios de alto riesgo (Clínico, LegalTech, DevSecOps) donde un error provoque daños físicos, penales o financieros irreparables, DEBE someterse a la separación estricta entre Transducción Estocástica y Política Determinista. Aplica universalmente a cualquier LLM subyacente (Gemini, Claude, GPT, Llama).

### Primitivas Irreducibles de Dominio Crítico
* **$\mathcal{N}$ (Entropía Narrativa):** Input crudo estocástico proveniente del entorno (anamnesis de paciente, contratos, logs de servidor).
* **$\mathcal{E}$ (Evidencia Estructurada):** Matriz de observables con trazabilidad estricta (spans textuales).
* **$\mathcal{D}$ (Decisión):** Veredicto irreversible (Triaje, Sentencia Legal, Política de Contención SecOps).

### Axiomas de Aislamiento
* **[AX-TRANS] Límite de Transducción:** Todo modelo de lenguaje $\mathcal{L}$ opera estrictamente como el operador probabilístico $T(\mathcal{N}) \to \mathcal{E}$. *Jamás* se permite delegar a un LLM el salto ontológico $T(\mathcal{N}) \to \mathcal{D}$.
* **[AX-DET] Determinismo de Veredicto:** La función de Decisión debe ser un operador puramente determinista, versionable externamente y auditable $P(\mathcal{E}) \to \mathcal{D}$. No puede invocar ni depender de inferencia estocástica.
* **[AX-LEDGER] Invariancia Criptográfica:** La trayectoria del estado forma un grafo causal inmutable $\mathcal{N}_{hash} \to \mathcal{E}_{hash} \to P_{version} \to \mathcal{D}$. Este grafo debe sellarse iterativamente en un registro de solo-escritura (CORTEX Ledger) para permitir atestación termodinámica L5 (OpenTimestamps).
