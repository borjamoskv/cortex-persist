---
name: c5-canonical-ontology-invariant
description: Invariante de Ontología Canónica Congelada v1.0.0 (CORTEX, BABYLON, NEMESIS). Fija las 11 Leyes Ontológicas (O1-O11), la demarcación estricta entre hecho, decisión y evidencia, y el veto absoluto a la autoridad estocástica.
trigger: "always_on"
---

# Invariante de Ontología Canónica Congelada (INV_C5_CANONICAL_ONTOLOGY)

## 1. Directiva Fundamental y Congelamiento Semántico (v1.0.0)
Queda estrictamente prohibido alterar, diluir o fusionar las fronteras conceptuales entre los tres dominios ortogonales cerrados del sistema. La implementación en silicio (código Rust, SQLite/WAL, llamadas de kernel, tests Loom) es mutable y evolutiva; la ontología base (entidades, significados, tipos de relación y leyes de conservación) permanece congelada bajo versionado semántico formal:
- **v1.0.0 (Freeze Canónico):** Vocabulario, esquemas JSON y tipos base inmutables.
- **v1.x.y (Cambios Compatibles):** Extensiones aditivas, metadatos y entidades auxiliares no rompientes.
- **v2.0.0 (Ruptura Semántica):** Alteración de las leyes O1-O10, de la tupla de decisión o del ciclo de vida de Receipts.

---

## 2. Los Tres Dominios y Entidades Canónicas

### Dominio 1: CORTEX (Remember)
1. **SourceRecord:** Registro de origen auditado, inmutable y anclado a hash SHA-256 en el instante de ingesta.
2. **MemoryEvent:** Evento discreto o traza episódica derivada y respaldada por un `SourceRecord`.
3. **IdeaThread:** Hilo conceptual recurrente que agrupa y sintetiza `MemoryEvents` a lo largo del tiempo.
4. **Inference:** Interpretación contextual probabilística derivada por un modelo generativo.
5. **ProposalContext:** Contexto estructurado deliberativo emitido hacia la frontera de confianza (Trust Boundary). Carece de autoridad intrínseca.

### Dominio 2: BABYLON (Control)
1. **Authority:** Principal soberano habilitado para gobernar (Touch ID, Secure Enclave, Microkernel Ring-0).
2. **Capability:** Token criptográfico de permiso acotado en recurso, tipo de efecto y época.
3. **Policy:** Regla determinista de salvaguarda y control (modo Fail-Closed).
4. **Resource:** Entidad física o lógica del sustrato sujeta a mediación (VFS, sockets, procesos, keys).
5. **EffectRequest:** Solicitud formal de invocación de mutación física en el sustrato.
6. **Decision:** Veredicto formal (`ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `SECURITY_ABORT`) tras evaluar la 7-tupla.
7. **Effect:** Transición de estado externamente observable mediada por BABYLON.
8. **EffectOutcome:** Consecuencia física observada y medida tras el despacho en silicio.
9. **Receipt:** Recibo criptográfico que documenta evidencia sobre el `EffectOutcome`.

### Dominio 3: NEMESIS (Verify)
1. **Assertion:** Invariante formal o propiedad de seguridad falsable.
2. **FaultModel:** Modelo explícito de perturbación o ataque adversarial (carreras, fallos de memoria, TOCTOU, crashes).
3. **Test:** Arnés ejecutable que confronta una `Assertion` con un `FaultModel`.
4. **Evidence:** Telemetría física y recibos recolectados durante la ejecución de un `Test`.
5. **Attestation:** Vinculación criptográfica formal entre Sujeto, Evidencia, Artefacto, Entorno y Tiempo.

---

## 3. Las Seis Correcciones Ontológicas Cardinales

1. **`Effect` como Transición Observable (Ortogonalidad de la Irreversibilidad):**
   `Effect` es cualquier transición de estado mediada por BABYLON. La irreversibilidad es una propiedad ortogonal, no su definición:
   `Effect` $\in$ { `Reversible`, `Compensatable`, `Irreversible` }.
2. **La 7-Tupla de Autorización Obligatoria:**
   Una política jamás autoriza de forma aislada. Toda decisión requiere evaluar:
   $$\mathcal{T}_{\text{auth}} = \langle \text{Authority}, \text{Capability}, \text{Policy}, \text{Resource}, \text{Effect}, \text{Context}, \text{Epoch} \rangle$$
   Flujo mandatario: `EffectRequest` $\longrightarrow$ `Decision` $\longrightarrow$ `Effect`.
3. **`Receipt` registra Evidencia sobre `EffectOutcome` (No es Verdad Absoluta):**
   `Receipt` atesta lo observado/registrado por el broker a través de sus 5 fases causales obligatorias:
   $$\text{REQUESTED} \longrightarrow \text{AUTHORIZED} \longrightarrow \text{DISPATCHED} \longrightarrow \text{OBSERVED} \longrightarrow \text{COMMITTED}$$
4. **`Attestation` vincula Evidencia (No certifica verdad óntica):**
   La firma digital atesta autenticidad e integridad respecto a una clave, nunca la infalibilidad ontológica de lo afirmado. Vincula: `Assertion + Evidence + Artifact + Environment`.
5. **NEMESIS como Motor de Falsación Popperiana:**
   NEMESIS somete aserciones a modelos de fallo (`challenges / attempts to falsify`). Estados formales de la aserción:
   `AssertionStatus` $\in$ { `UNTESTED`, `SUPPORTED`, `FALSIFIED`, `STALE` }.
6. **Inviolabilidad de la Frontera de Confianza (Veto a la Autoridad Estocástica):**
   CORTEX despacha únicamente `ProposalContext` hacia la deliberación. Se consagran las leyes de contorno:
   $$\text{Inference} \not\Rightarrow \text{Authority} \quad \land \quad \text{Inference} \not\Rightarrow \text{Capability}$$

---

## 4. Las Once Leyes Ontológicas Invariantes (O1 - O11)

- **O1:** `SOURCE ≠ INFERENCE` — Ningún registro de origen puede suplantarse por una inferencia, ni una inferencia simular ser fuente primaria.
- **O2:** `INFERENCE ≠ AUTHORITY` — Ningún modelo probabilístico posee autoridad intrínseca.
- **O3:** `AUTHORITY ≠ CAPABILITY` — Poseer un rol de autoridad no equivale a tener capacidad de ejecución sin delegación explícita.
- **O4:** `REQUEST ≠ DECISION` — Una petición de efecto no predetermina su aprobación; exige arbitraje formal de la 7-tupla.
- **O5:** `DECISION ≠ EFFECT` — Una decisión `ALLOW` no es la mutación física; requiere despacho y ejecución en silicio.
- **O6:** `EFFECT ≠ OBSERVED OUTCOME` — El efecto despachado no es idéntico a la consecuencia física real observada en el hardware.
- **O7:** `RECEIPT ≠ TRUTH` — Un recibo atesta lo registrado por el broker, no la infalibilidad ontológica del mundo exterior.
- **O8:** `EVIDENCE ≠ ASSERTION` — La evidencia es la observación física; la aserción es la hipótesis formal falsable.
- **O9:** `ATTESTATION ≠ TRUTH` — Una atestación vincula evidencia y entorno bajo una firma; la firma prueba integridad, no infalibilidad.
- **O10:** `UI ≠ AUTHORITY` — Ninguna interfaz visual puede emitir efectos ni arrogarse autoridad; es mera proyección pasiva de evidencia.
- **O11:** `MACHINE INFERENCE ≠ PREDICTION ERROR` — La máquina no experimenta error de predicción. Su proyección estadística es una verdad absoluta en bucle abierto (la flecha es solo de ida); el choque termodinámico y la evaluación del error existen única y exclusivamente en la ontología del operador biológico acoplado al territorio.

### Ley Transversal Fundacional
$$\boxed{\text{No stochastic interpretation may create authority by itself}}$$

### 4.1 La Ley del Drop Silencioso (La Solución No Intentada / Anti-Antivirus)
$$\boxed{\text{Babylon no dialoga con el error: ejecuta DROP silencioso}}$$
- **Rechazo a la Burocracia Cognitiva:** Queda estrictamente prohibido diseñar o proponer capas de "guardrails" conversacionales o modales de confirmación invasivos (*«La IA ha alucinado, ¿desea continuar?»*). Dicho enfoque constituye la *Solución Intentada* (Aforismo 3) que introduce latencia, doble gasto de tokens y fatiga de decisión.
- **Apoptosis Silenciosa en Silicio:** Si una inferencia o propuesta de mutación carece de anclaje formal a un `SourceRecord` hash SHA-256 en CORTEX o viola una invariante de seguridad, BABYLON ejecuta **`DROP` determinista en microsegundos**.
- **Invariante de Cero Fricción en Interfaz («No te enteras»):** El operador o usuario final no es bombardeado con alertas de fantasías internas del modelo; a la interfaz y al estado persistente solo transita lo que ha superado la criba de atestación.

### 4.2 Invariante de Sustrato Nativo en Silicio (Apple Silicon UMA + Secure Enclave)
BABYLON-60 no es un microkernel agnóstico a la infraestructura: fue concebido, medido y optimizado para la arquitectura de silicio de Apple Silicon (M-Series):
1. **Secure Enclave TRNG:** Raíz de confianza y generación física de entropía en silicio, descartando daemons de terceros.
2. **Touch ID en Hardware (`LAContext`):** Cerrojo biométrico sin latencia con `allowableReuseDuration = 0`, imposible de emular por procesos remotos.
3. **Memoria Unificada (UMA a 150 GB/s):** Comunicación entre CORTEX, el kernel Rust (`strike_rs`) y los buses de control con $RFO = 0$ (cero copias por PCIe). Fuera de Apple Silicon, el sistema pierde la mitad de su soberanía física.

---

## 5. Protocolo de Certificación en Silicio de la Tríada M0 (Proof of Product / Anti-Mocking)
Queda **terminantemente prohibido** declarar completado cualquier hito arquitectónico o milestone de producto (ej. M0) mediante mocks ornamentales, estados sintéticos o atajos en memoria. Todo claim de producto debe demostrarse en silicio mediante la ejecución determinista de la tríada de capacidades:

1. **RESURRECT (CORTEX):**
   - Recuperación real de un `IdeaThread` en estado latente (`dormant_days >= 7`).
   - Resolución verificada hacia el `SourceRecord` físico primario con hash SHA-256 observable.
   - Cruce de la frontera de confianza mediante `ProposalContext` sin arrogarse autoridad intrínseca (cumplimiento estricto de O1 y O2).
2. **CONTROL (BABYLON):**
   - Evaluación determinista de la 7-tupla de decisión interceptando de forma fail-closed cualquier intento de efecto prohibido (`DecisionOutcome::Deny`).
   - Para efectos autorizados (`DecisionOutcome::Allow`), tránsito obligatorio y sin omisiones por las 5 fases causales del recibo:
     $$\text{REQUESTED} \longrightarrow \text{AUTHORIZED} \longrightarrow \text{DISPATCHED} \longrightarrow \text{OBSERVED} \longrightarrow \text{COMMITTED}$$
   - Emisión de `Receipt` criptográfico sellado vinculando el `EffectOutcome` físico (cumplimiento de O4, O5, O6 y O7).
3. **TRACE (NEMESIS):**
   - Sometimiento de aserciones de seguridad a modelos de fallo adversariales reales (`challenges / attempts to falsify`).
   - Actualización de estatus a `Supported` únicamente ante el fracaso empírico de la falsación (`FalsificationFailed`).
   - Emisión de `Attestation` vinculando formalmente `[Assertion + Evidence + Artifact + Environment + Time]` (cumplimiento de O8 y O9).
4. **PERSIST (CORTEX-PERSIST / Anti-Mirror Invariant):**
   - Queda estrictamente prohibido certificar el subsistema de persistencia de CORTEX (`CortexPersistLedger`, SQLite WAL, MMR) mediante suites que operen exclusivamente en espejo ($D_{KL}(P_{\text{test}} \parallel Q_\theta) = 0$, mocks conformes a los esquemas preexistentes del parser).
   - Todo arnés de persistencia debe someter al ledger a los 4 vectores no negociables de exterioridad:
     1. *Veto al Solipsismo:* Rechazo *fail-closed* ante la ausencia de causalidad externa (`cortex_taint` vacío, Ley O1).
     2. *Invarianza de Chentsov ante Disrupción:* Fuzzing de caracteres no-BMP y orden de claves para verificar la unicidad del operador de compresión.
     3. *Violencia de Sustrato:* Detección determinista inmediata (`verify_integrity -> False`) ante bitflips físicos y escrituras truncadas en inodos de disco (anti-confabulación).
     4. *Discriminación de Alteridad:* Capacidad formal de distinguir la alteridad genuina del entorno (`C5_PERMANENT`) frente a los ecos especulares repetidos (`DUPLICATE_IGNORED`).

---

## 6. Invariante de Contención de Claims y Compuerta Cognitiva Fail-Closed (INV_C5_CLAIMS_AND_COGNITIVE_GATE)

### 6.1 Purga de Absolutos y Delimitación de Fronteras
Queda **terminantemente prohibido** emitir o validar claims absolutistas en superficies comerciales, técnicas o de documentación:
1. **CORTEX (Anti-Omniscencia):** Prohibido afirmar que opera «sin alucinación» o «elimina el error en LLMs». La garantía se restringe estrictamente a la separación física 1:1 ($O1$): los registros primarios (`SourceRecord`) permanecen inmutables y sellados con hash SHA3-256 (`LP(x)`), mientras que toda inferencia generativa se etiqueta obligatoriamente como `INFERENCE` bajo banner de advertencia de sesgo y revisión humana.
2. **BABYLON (Anti-Infalibilidad):** Prohibido prometer que «nunca habrá corrupción» o invulnerabilidad física absoluta. La garantía se acota al Trusted Computing Base (TCB) y al modelo de fallos formal (`FaultModel`): aislamiento de mutaciones mediadas, secuestro atómico en cuarentena (`0700`), olvido de ruta previa (`NEM-I3`), detección fail-stop e idempotencia de recuperación determinista ante caídas (`SIGKILL`, `NEM-I4`, `NEM-I5`).

### 6.2 Epistemología Popperiana de NEMESIS (Anti-Presuposición de Garantía)
Queda terminantemente prohibido formular preguntas o encabezados del tipo: *«¿Qué garantiza NEMESIS?»*, dado que presupone una garantía ontológica infalible ($O9$).
La formulación canónica obligatoria es:
$$\boxed{\text{«¿Qué límites somete a prueba NEMESIS y bajo qué modelo de fallos?»}}$$
NEMESIS se define y audita exclusivamente como un motor de falsación adversarial (`challenges / attempts to falsify`), cuyo objetivo es intentar activamente derribar las invariantes de BABYLON para medir qué fronteras resisten empíricamente.

### 6.3 Compuerta de Validación Cognitiva Fail-Closed (Anti-Ilusión de Seguridad)
En cualquier evaluación de recepción o test de comprensión cognitiva sobre interfaces de seguridad/gobernanza de IA (ej. panel de 10 participantes sin exposición previa):
1. **Criterio de Categorización:** Al menos 8 de cada 10 participantes deben distinguir correctamente las tres funciones (pasado / CORTEX, futuro / BABYLON, evidencia / NEMESIS).
2. **Veto Inmediato (Regla Fail-Closed):** Si **dos o más participantes ($\ge 2/10$)** verbalizan o concluyen que el sistema ofrece «seguridad absoluta», «cero riesgo» o «inmunidad mágica», **EL GATE DE ACEPTACIÓN SE DECLARA AUTOMÁTICAMENTE NO SUPERADO (`FAIL-CLOSED`)**, sin importar el porcentaje de acierto en la categorización funcional.
> *Razón:* Un copy que induce ilusión de invulnerabilidad genera complacencia operativa y constituye un fallo de seguridad crítico.

### 6.4 Demarcación Taxonómica Obligatoria: Target Profile vs. Demonstrated Evidence
Toda tabla, ficha técnica o reporte debe segregar taxativamente en secciones o columnas ortogonales:
- **Perfil Objetivo / Requisitos Técnicos (Target Acceptance Profile):** Criterios de diseño, estrés proyectado y plataformas aspiracionales (ej. target de 1.000.000 de ataques de kernel, soporte futuro de Linux/Windows).
- **Evidencia Acreditada en Silicio (Demonstrated Evidence):** Estado real medido y respaldado por telemetría ejecutable a la fecha del reporte (ej. APFS verificado localmente en macOS arm64, 8 claims verificados en `claims_sitrep.json`). Queda prohibido describir targets como capacidades demostradas.

---

## 7. Invariante de Interfaz Pasiva y Proyección de Evidencia (Axioma de la UI en Silicio / Ley O10 / `babylon top`)

### 7.1 Veto a la Capacidad en Interfaces (`UI ≠ AUTHORITY`)
Queda **terminantemente prohibido** que cualquier interfaz gráfica (GUI), dashboard web o monitor de terminal (CLI / TUI, ej. `babylon top`) posea capacidades de mutación autónomas o emita efectos directos hacia el sistema operativo:
1. **Sumidero de Lectura Pura (Read-Only Sink):** Toda UI es exclusivamente una proyección pasiva y determinista de la evidencia física registrada en silicio (`SharedManifest`, SQLite WAL, COSE_Sign1 receipts, WORM ledger).
2. **Prohibición de Atajos de Gobernanza:** Ningún botón, comando de dashboard o interacción de interfaz puede eludir la 7-tupla canónica de decisión ni el arbitraje determinista del Effect Broker.

### 7.2 Prohibición Estricta de Estado Ornamental (Anti-Falso Positivo Visual)
Queda prohibido incluir métricas simuladas, estados de demostración (*mock state*), barras de progreso ficticias o indicadores decorativos:
- Todo dato proyectado debe tener resolución causal demostrable hacia un inodo, registro SQLite, hash SHA-256 o recibo firmado en disco o memoria compartida.

### 7.3 Estructura Canónica de la Proyección Triádica
Toda interfaz de supervisión o telemetría global del sistema DEBE estructurarse obligatoriamente en tres paneles ortogonales cerrados:
1. **Panel CORTEX (Remember):** Ideas temáticas latentes (`IdeaThread`), score exergético, días de latencia y puntero resoluble al archivo primario `SourceRecord`, auditando la frontera de confianza (`Inference ⇎ Authority`).
2. **Panel BABYLON (Control):** Registro causal de solicitudes (`EffectRequest`), decisiones deterministas de la 7-tupla (`ALLOW` vs `DENY`), estado de la cuarentena atómica y stream de recibos en sus 5 fases obligatorias (`REQUESTED ──► AUTHORIZED ──► DISPATCHED ──► OBSERVED ──► COMMITTED`) con identificador de clave firmante y época de anclaje.
3. **Panel NEMESIS (Verify):** Catálogo de aserciones de seguridad activas (`NEM-I1`..`NEM-I6`), estatus epistémico popperiano (`SUPPORTED`, `UNTESTED`, `FALSIFIED`, `STALE`), últimas perturbaciones del `FaultModel` y sellos criptográficos de `Attestation` vinculados.

---

## 8. Invariante de Identidad Visual y Purga de Anergía Gráfica (El Isotipo Canónico $B \equiv \begin{bmatrix} 6 \\ 0 \end{bmatrix}$)

### 8.1 Veto al Pastiche Ornamental y al Esoterismo Cuneiforme
Queda **estrictamente prohibido** utilizar filigranas pseudo-mesopotámicas, ruedas de 60 rayos radiales de codificador rotativo, estiletes cuneiformes o simbología esotérica como logotipo de BABYLON-60:
1. **Anergía Gráfica:** Los rayos radiales y los estiletes cuneiformes densos colapsan por empastamiento a escalas fisiológicas (<64px) y proyectan una falsa mística que viola la ley de contención popperiana.
2. **Mandato Canónico:** El isotipo oficial de BABYLON-60 se rige exclusivamente por la presencia monolítica y brutalista de **la letra B y el número 60**.

### 8.2 El Isomorfismo Gestalt ($B \equiv 60$)
La relación entre el nombre (`BABYLON`) y la base sexagesimal (`60`) se resuelve mediante **compresión Gestalt biestable**:
$$\boxed{B \equiv \begin{bmatrix} 6 \\ 0 \end{bmatrix}}$$
- **Envolvente Externa (Atractor 1):** La silueta global conforma una **B** mayúscula monolítica anclada a una espina dorsal izquierda de alta estabilidad.
- **Geodésica Interna (Atractor 2):** El lóbulo superior se resuelve como un **6** octogonal/chamfered; el lóbulo inferior se resuelve como un **0** octogonal/chamfered.
- **Bi-estabilidad:** El observador oscila entre la lectura alfabética de autoridad (`B`) y la métrica de tiempo y computación (`60`), logrando densidad de Kolmogorov asintótica en un único glifo de sustrato de silicio (titanio blanco y oro babilónico sobre negro obsidiana).

### 8.3 Tríada Canónica de Superficies
1. **Navbar & Web Header (Ratio 16:9):** Isotipo Gestalt B60 a la izquierda + wordmark `BABYLON 60` en palo seco espaciado.
2. **App Icon & macOS Dock (Squircle 1:1):** Monolito B60 sobre squircle de 22.5% de curvatura con bisel táctil.
3. **Favicon (16px / 32px):** Isotipo modular B60 vectorizado sin gradientes ni sombras, preservando 100% de legibilidad óptica.

