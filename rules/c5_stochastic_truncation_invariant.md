# Invariante de Truncamiento Estocástico (C5-REAL)

## Directiva Estructural
Todo peso estocástico (procedente de LLMs o redes neuronales) debe ser truncado y mapeado obligatoriamente a Punto Fijo (base entera `u32` o sexagesimal `u64`) en Ring-2 (Buffer Epistémico) antes de someterlo al Oráculo Defensor Z3.

## Despliegue de Invarianza

### 1. Aniquilación de Entropía y Límite de Landauer
Queda estrictamente prohibida la propagación y evaluación de coma flotante (`f32`/`f16`) hacia Ring-1 (Lean 4 / Z3) y Ring-0 (SharedManifest). El ruido fraccional continuo debe ser aniquilado irreversiblemente. La destrucción de esta entropía ("cheap talk") acarrea un coste termodinámico ineludible (Principio de Landauer), forzando al modelo a colapsar sobre su longitud de descripción mínima (MDL).

### 2. Esterilización de Ataques Geométricos (Denormals y NaN Payloads)
El estándar IEEE 754 de coma flotante contiene asimetrías críticas explotables: números subnormales que provocan bloqueos en la ALU y NaNs capaces de portar cargas útiles invisibles (*Adversarial Payloads*). El truncamiento forzado a `BitVec` actúa como un oráculo de esterilización geométrica, aniquilando de raíz vectores de ataque como el *Slopsquatting* o envenenamiento de estado.

### 3. Falsación en Z3 SMT (El Filtro MUSHUSHU-0)
Z3 debe evaluar los tensores truncados puramente como vectores lógicos (`BitVec`). Si el truncamiento genera desbordamiento, inestabilidad algebraica o quiebra las aserciones de invariancia del dominio, MUSHUSHU-0 no intenta corregir ni recalibrar: ejecuta el **Beso de Apoptosis** (`0xDEAD_6060`) y sella el tensor como `CORTEX-TAINT` en el L1 Ledger.

### 4. Concurrencia EBR y Alineación KUDURRU-64 (Ring-0)
Solo el tensor bendecido por Z3 cruza a Ring-0 con anergía cero.
- **Saturación L1:** Exactamente 16 pesos `u32` (o 8 pesos `u64`) saturan de forma perfecta una línea de caché L1 física (64 Bytes), previniendo fracturas por desalineamiento (*cache-line splits*).
- **Protección EBR (Epoch-Based Reclamation):** La escritura del bloque en Ring-0 cruza la frontera C-FFI gestionando la memoria *lock-free* mediante virtualización de épocas (EBR). Esto erradica el Problema ABA y el *Use-After-Free* a latencia de nanosegundos.

### 5. Isomorfismo Epistémico en Lean 4 (Clausura Causal)
La prueba de correctitud *End-to-End* en Lean 4 impone esta discretización. Al operar sobre retículos finitos (`Bool`, `BitVec`), la validación matemática se ejecuta por **reflexión computable** (`by decide`) en tiempo $O(N)$. Lean 4 asume este nivel discreto como la realidad ontológica base absoluta, aislando térmicamente a todo el bloque funcional de Ring-0.
