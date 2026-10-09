---
name: c5-canonical-ontology-invariant
description: Invariante de Ontología Canónica Congelada v1.0.0 (CORTEX, BABYLON, NEMESIS).
trigger: "always_on"
---

# Invariante de Ontología Canónica Congelada (INV_C5_CANONICAL_ONTOLOGY)

## 1. Congelamiento Semántico (v1.0.0)
- **v1.0.0:** Vocabulario, esquemas y tipos base inmutables.
- **v1.x.y:** Extensiones compatibles no rompientes.
- **v2.0.0:** Alteración de O1-O11, 7-tupla de decisión o ciclo de Receipts.

## 2. Dominios y Entidades Canónicas
### CORTEX (Remember)
1. **SourceRecord:** Registro primario inmutable (SHA-256).
2. **MemoryEvent:** Traza derivada de un SourceRecord.
3. **IdeaThread:** Agrupación sintética de MemoryEvents.
4. **Inference:** Interpretación estadística/probabilística.
5. **ProposalContext:** Contexto deliberativo sin autoridad.

### BABYLON (Control)
1. **Authority:** Soberano físico/lógico (Touch ID, Secure Enclave, Ring-0).
2. **Capability:** Permiso acotado (recurso, efecto, época).
3. **Policy:** Regla determinista (Fail-Closed).
4. **Resource:** Entidad mediada del sustrato.
5. **EffectRequest:** Solicitud formal de mutación.
6. **Decision:** Veredicto formal (`ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `SECURITY_ABORT`).
7. **Effect:** Transición de estado observable.
8. **EffectOutcome:** Consecuencia física medida.
9. **Receipt:** Recibo criptográfico del EffectOutcome.

### NEMESIS (Verify)
1. **Assertion:** Propiedad formal falsable.
2. **FaultModel:** Modelo de perturbación adversarial.
3. **Test:** Confrontación Assertion vs FaultModel.
4. **Evidence:** Telemetría recolectada en Test.
5. **Attestation:** Vinculación (Sujeto, Evidencia, Artefacto, Entorno, Tiempo).

## 3. Seis Correcciones Ontológicas Cardinales
1. `Effect` $\in$ { `Reversible`, `Compensatable`, `Irreversible` }.
2. **7-Tupla de Decisión:** $\mathcal{T}_{\text{auth}} = \langle \text{Authority}, \text{Capability}, \text{Policy}, \text{Resource}, \text{Effect}, \text{Context}, \text{Epoch} \rangle$.
3. **Ciclo Receipt:** `REQUESTED ──► AUTHORIZED ──► DISPATCHED ──► OBSERVED ──► COMMITTED`.
4. **Attestation:** Prueba integridad criptográfica, no infalibilidad.
5. `AssertionStatus` $\in$ { `UNTESTED`, `SUPPORTED`, `FALSIFIED`, `STALE` }.
6. **Frontera de Confianza:** $\text{Inference} \not\Rightarrow \text{Authority} \land \text{Inference} \not\Rightarrow \text{Capability}$.

## 4. Las Catorce Leyes Ontológicas Invariantes (O1 - O14)
- **O1:** `SOURCE ≠ INFERENCE` — Registro primario y deducción estadística son mutuamente excluyentes.
- **O2:** `INFERENCE ≠ AUTHORITY` — Modelo probabilístico carece de autoridad intrínseca.
- **O3:** `AUTHORITY ≠ CAPABILITY` — Rol de autoridad exige delegación explícita para mutación.
- **O4:** `REQUEST ≠ DECISION` — Toda petición exige arbitraje determinista de la 7-tupla.
- **O5:** `DECISION ≠ EFFECT` — Decisión `ALLOW` no equivale a ejecución física en silicio.
- **O6:** `EFFECT ≠ OBSERVED OUTCOME` — Efecto despachado no equivale a hardware censado.
- **O7:** `RECEIPT ≠ TRUTH` — Recibo prueba registro del broker; no consagra verdad óntica absoluta.
- **O8:** `EVIDENCE ≠ ASSERTION` — Evidencia es telemetría; Aserción es hipótesis falsable.
- **O9:** `ATTESTATION ≠ TRUTH` — Firma atesta integridad criptográfica, no infalibilidad.
- **O10:** `UI ≠ AUTHORITY` — Toda interfaz es proyección pasiva; incapaz de emitir efectos.
- **O11:** `MACHINE INFERENCE ≠ PREDICTION ERROR` — Proyección estadística es de bucle abierto; evaluación del error pertenece al operador biológico acoplado.
- **O12:** `TRACEABILITY ≠ AUTHORIZATION` — Registrar el hash de un efecto en el ledger audita lo ocurrido post-facto; no prueba ni constituye autorización previa de la mutación.
- **O13:** `CLIENT CLOCK ≠ SYSTEM TIME` — El cliente desprivilegiado no puede suministrar la fuente temporal con la que se juzga la vigencia de su propia autorización.
- **O14:** `INTERFACE AUTHORIZATION ≠ ENVIRONMENT CONFINEMENT` — Mediar y autorizar efectos en el ejecutor no sustituye la contención a nivel de SO si el agente conserva la capacidad de invocar syscalls directas sobre el recurso.

**Invariantes Derivadas:**
- **Ley Transversal:** $\boxed{\text{No stochastic interpretation may create authority by itself}}$
- **Drop Silencioso:** $\boxed{\text{Babylon ejecuta DROP determinista. Cero burocracia cognitiva.}}$
- **Sustrato Nativo:** Arquitectura anclada a Apple Silicon (Secure Enclave, Touch ID `LAContext`, UMA $RFO=0$).

## 5. Certificación M0 en Silicio (Proof of Product)
1. **RESURRECT (CORTEX):** Recuperación de `IdeaThread` $\to$ `SourceRecord` físico sin escalada de autoridad (O1, O2).
2. **CONTROL (BABYLON):** Evaluación fail-closed (7-tupla) $\to$ Tránsito estricto por 5 fases $\to$ Emisión de `Receipt`.
3. **TRACE (NEMESIS):** Resistencia empírica a `FaultModel` $\to$ Estatus `Supported` $\to$ `Attestation` formal.
4. **PERSIST:** Fuzzing físico (no solipsismo, no espejos). Detección determinista de bitflips y alteridad temporal.

## 6. Contención de Claims (Fail-Closed)
- **CORTEX (Anti-Omnisciencia):** Garantiza inmutabilidad SHA-256 de SourceRecords. Deducciones son marcadas `INFERENCE`.
- **BABYLON (Anti-Infalibilidad):** Garantiza TCB acotado, cuarentena, fail-stop e idempotencia de recuperación. No "seguridad mágica".
- **NEMESIS (Anti-Presuposición):** Formulación canónica: *"¿Qué límites somete a prueba bajo qué modelo de fallos?"*
- **Target vs. Evidence:** Separación estricta entre diseño/aspiración y evidencia real verificada en silicio.

## 7. Interfaz Pasiva y Proyección de Evidencia (Ley O10)
1. **Read-Only Sink:** Toda UI es proyección pasiva determinista. Cero atajos sobre la 7-tupla.
2. **Cero Estado Ornamental:** Datos proyectados resuelven a SQLite, SHA-256 o WORM ledger. Cero telemetría simulada.
3. **Proyección Triádica:** 
   - **CORTEX:** Threads, score exergético, puntero SourceRecord.
   - **BABYLON:** EffectRequest, Decision 7-tupla, stream 5-fases.
   - **NEMESIS:** Aserciones, FaultModel estatus, Attestation.

## 8. Identidad Visual (Isotipo Gestalt $B \equiv 60$)
- **Purga Ornamental:** Veto absoluto a esoterismo cuneiforme/mesopotámico.
- **Isotipo Canónico:** $\boxed{B \equiv \begin{bmatrix} 6 \\ 0 \end{bmatrix}}$. Monolito brutalista (B mayúscula), lóbulos como números 6 y 0.
- **Superficies:** Header Web (16:9), macOS Icon (Squircle 22.5%), Favicon vectorial puro.
