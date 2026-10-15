---
name: c5_empty_tautology_invariant
description: Invariante contra anti-patrones de tautología vacía en pruebas formales y tests.
trigger: "model_decision"
---

# Invariante de Anti-Patrones de Tautología Vacía (INV_C5_EMPTY_TAUTOLOGY)

## 1. Principio Fundamental
Queda terminantemente prohibido que cualquier agente, subagente o pipeline neurosimbólico reporte verificación o cumplimiento de propiedades formales, energéticas o causales mediante tautologías vacías ($\Delta \Phi = 0$, $g_{ij} = 0$). Una aserción sólo es válida si constriñe el espacio de estados y es vulnerable a falsación empírica.

## 2. Las Cinco Prohibiciones Cardinales (T1 - T5)

### T1: Veto a Stubs Triviales en Demostradores Formales
- **Restricción:** En especificaciones o verificaciones (Lean 4, Z3, Coq), queda prohibido el uso de firmas vacías, axiomas no fundamentados o teoremas con pruebas triviales (ej. `axiom ax : ∀ x, True`, `by trivial` o `sorry` encubierto) para certificar invariantes de concurrencia, energía o consistencia.
- **Remediación:** Toda formalización exige términos cerrados, invariantes computables y compilación nativa AOT (`INV_C5_LEAN_AOT_ORACLE`).

### T2: Veto a Telemetría y Claims Fantasma (Ghost Claims & Ghost Tests)
- **Restricción:** Prohibido declarar métricas de rendimiento, contadores de pruebas pasadas o cobertura empírica sin ejecución efectiva del arnés de pruebas sobre archivos y fuentes de datos existentes en el árbol físico.
- **Acoplamiento Ontológico:** Acatamiento estricto de las Leyes **B2** (`DEFINITION ≠ EVIDENCE`) y **O8** (`EVIDENCE ≠ ASSERTION`).

### T3: Veto al Retorno Indiferente (Mocking Ciego)
- **Restricción:** Ningún subsistema de control de acceso, gateway de admisión o árbitro de seguridad puede resolver mediante retornos fijos (`ALLOW`) o mocks pasivos que ignoren la evaluación de la 7-tupla causal $\mathcal{T}_{\text{auth}} = \langle \text{Authority}, \text{Capability}, \text{Policy}, \text{Resource}, \text{Effect}, \text{Context}, \text{Epoch} \rangle$.
- **Fail-Stop:** La omisión de la atestación biométrica o de hardware ligado al Secure Enclave detona apoptosis irreversible (`POISONED = 0xDEAD_6060`).

### T4: Veto a la Circularidad Semántica (Anergía de Cheap Talk)
- **Restricción:** Prohibido sustituir magnitudes físicas o matemáticas auditables (Joules, Kelvin, bits de Shannon, compresión de Kolmogorov) por tautologías retóricas o juegos de sinonimia lingüística que no incrementen la Información de Fisher del sistema.
- **Acoplamiento Ontológico:** Acatamiento estricto de la Ley **B5** (`TERM COST < COMPRESSION GAIN`) y linter `BJR-E091`.

### T5: Veto a Tests de Integración Tautológicos (Holgura Indiferente en AST / cargo-mutants)
- **Restricción:** Queda prohibido diseñar tests de integración para máquinas de estado, consenso o quórums que operen con holgura de camino feliz (ej. acumular $N$ votos cuando se requiere $2f+1$) permitiendo la supervivencia de mutantes en operadores relacionales ($<$ vs $\le$), aritmética de quórum ($2f+1 \to 2f-1$) o conjunciones lógicas ($\&\&$ vs $||$).
- **Los Tres Principios Anti-Mutante Obligatorios:**
  1. **Pinza de Frontera Exacta ($K-1$ vs $K$):** Probar obligatoriamente el fallo en el límite inferior ($2f$ votos $\implies \text{InsufficientQuorum}$) y la transición al añadir el voto exacto número $2f+1$.
  2. **Desambiguación Aritmética Multi-Escala:** Evaluar en al menos dos escalas primas entre sí ($f=1$ y $f=3$) para aniquilar mutaciones que colapsen numéricamente ($2 \times f \equiv 2 + f$ en $f=2$).
  3. **Inyección de Perturbación por Guarda:** Probar explícitamente cada rama de error (replay Sybil, mismatch de bloque, fase incorrecta) comprobando la variante exacta de `Err`.
- **Gate de Mutaciones en CI:** En suites auditadas con `cargo-mutants`, el criterio de gate fail-closed exige `MISSED == 0` y `TIMEOUT == 0` sobre módulos críticos de consenso (`.cargo/mutants.toml`).
