---
name: c5_bft_cryptographic_ledger_invariants
description: Invariantes no negociables para la arquitectura, auditoría e implementación de ledgers criptográficos BFT, árboles de Merkle y actores de persistencia en BABYLON-60 / C5-REAL.
trigger: "model_decision"
---

# Invariantes Criptográficas para Ledgers BFT (C5-REAL / Ring-0)

Cualquier diseño, auditoría o modificación de motores de persistencia inmutables (ej. `CortexPersistLedger`, `BFTLedgerActor` o ledgers SQLite WAL) DEBE cumplir estrictamente estas cuatro invariantes matemáticas:

## 1. Contigüidad Monotónica Estricta de Secuencia (Anti-Podado Discreto)
- **Invariante:** En toda función de verificación de integridad (`verify_integrity`), es OBLIGATORIO validar que cada registro verificado cumpla:
  $$\text{seq}_k \equiv \text{seq}_{k-1} + 1 \quad (\text{con } \text{seq}_1 = 1)$$
- **Justificación:** Validar únicamente `lamport_t > last_lamport` y `row_prev_hash == prev_hash` es insuficiente; permite que un adversario con acceso al archivo suprima filas intermedias y re-encadene el hash de la fila siguiente si el cálculo de hash recibe el `seq` local almacenado. La discontinuidad en los números naturales ($\mathbb{N}$) debe provocar el aborto inmediato de la atestación.

## 2. Inmunización Merkle contra Isomorfismo (Anti-CVE-2012-2459)
- **Invariante:** En la construcción de árboles binarios de Merkle (`build_merkle_tree` / `get_merkle_root`), queda TERMINANTEMENTE PROHIBIDO duplicar el último nodo de capas impares (`layer.append(layer[-1])`) sin separación de dominio y compromiso explícito de cardinalidad.
- **Protocolo de Blindaje Obligatorio:**
  1. **Domain Tags (RFC 6962):** Prefijar con `0x00` los hashes de nivel hoja y con `0x01` los hashes de nodos internos:
     $$\text{Nodo}_{\text{interno}} = \text{SHA3-256}(0\text{x}01 \parallel \text{hijo}_{\text{izq}} \parallel \text{hijo}_{\text{der}})$$
  2. **Cardinality Commitment:** La raíz final debe vincular la cantidad total de hojas antes de emitir el digesto de atestación:
     $$\text{MerkleRoot}_{\text{hardened}} = \text{SHA3-256}(0\text{x}02 \parallel \text{layer}_0 \parallel \text{total\_leaves.to\_bytes}(8, \text{'little'}))$$

## 3. Serialización Transaccional Inmediata (`BEGIN IMMEDIATE`)
- **Invariante:** Toda operación de inserción (individual o en lote) sobre SQLite WAL debe ejecutarse bajo una transacción explícita iniciada con `BEGIN IMMEDIATE`.
- **Justificación:** Previene deadlocks por escalada de bloqueo diferido (`BEGIN DEFERRED`) en entornos concurrentes y garantiza que el lock reservado se adquiera antes de calcular `MAX(seq)` o verificar duplicados en memoria.

## 4. Separación de Sustrato (Kernel Puro Libre de I/O)
- Las funciones matemáticas de serialización canónica, digests criptográficos, árboles de Merkle y validación de invariantes DEBEN residir en un módulo puro (`cortex_crypto_kernel.py`), completamente aislado de dependencias de red, I/O o async.
- Los motores síncronos (`sqlite3`) y asíncronos (`aiosqlite`) deben compartir dicho kernel para garantizar paridad matemática absoluta.

## 5. Erradicación de Pánicos en Grafos Causales y Algoritmos Topológicos (Rust / C-FFI)
En la implementación de algoritmos de ordenamiento topológico (Kahn), geodésicas de Fisher o evaluación de DAGs causales:
- Queda estrictamente prohibido el uso de `.unwrap()` o indexación directa forzada (`map[&k]`) en el bucle principal de ejecución.
- **Patrón Mandatorio:** Desestructuración segura mediante `let Some(u) = queue.pop_front() else { break; };`, búsqueda defensiva `map.get(&k)` y mutaciones aritméticas saturantes (`deg.saturating_sub(1)`).
- Todo flush o escritura sobre `stdout`/`stderr` en interfaces REPL o CLI debe ignorar errores de tubería rota (`let _ = io::stdout().flush();`) en lugar de provocar un pánico en el runtime.

## 6. Protocolo Pre-Push Cero-Fugas y Rutas Dinámicas Soberanas
- Antes de emitir cualquier comando `git push`, es mandatorio auditar criptográficamente el rango de conmutaciones salientes mediante `gitleaks detect --log-opts="origin/main..HEAD" -v`.
- Ningún script de despliegue o pipeline de test (`.sh`, `.py`, `.rs`) debe contener rutas absolutas de usuario (`/Users/...`). La raíz del proyecto debe resolverse siempre dinámicamente (`REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"`).

## 7. Normalización COSE ES256 a Raw 64-Bytes (r || s)
- **Invariante:** En todas las estructuras COSE (RFC 8152 / RFC 9052), la firma criptográfica para ES256 (ECDSA P-256 / SHA-256) DEBE codificarse estrictamente en formato crudo de 64 bytes (`r || s`, `raw64`).
- **Veto a DER dentro de COSE:** Queda terminantemente prohibido almacenar o aceptar firmas ASN.1/DER (70-72 bytes) en el campo de firma de un objeto COSE.
- **Frontera de Hardware:** Si la clave reside en hardware criptográfico (ej. Apple Secure Enclave / CryptoKit) que emite firmas en formato DER, la conversión a `r || s` (32B + 32B con zero-padding si es preciso) debe realizarse en la frontera de transducción inmediatamente antes de componer el payload COSE.
- **Verificación de Bytes Originales:** Se deben firmar y verificar los bytes canónicos originales exactos. Si se requiere compatibilidad DER en APIs de transporte o serialización externa, debe exponerse mediante una propiedad explícita separada (ej. `Attestation.signature_der`).

## 8. Transaccionalidad de Atestación Unificada y Validación Conjunta de Snapshots
- **Conexión Única Transaccional:** Toda rutina de atestación de estado que calcule conteos, raíces de Merkle (state_root, receipt_root) y pruebas de integridad sobre SQLite WAL debe ejecutarse dentro de un bloque `BEGIN ... COMMIT` utilizando una **única conexión de base de datos** para evitar lecturas intercaladas incoherentes.
- **Validación Conjunta de Snapshots:** Al persistir o capturar snapshots desde la memoria compartida, `read_snapshot` debe validar atómicamente y de forma conjunta:
  1. El flag de estado (`status_flag`).
  2. La secuencia del seqlock (`seq`).
  3. La integridad del payload (`payload_hash`).
  Si la lectura resulta en `None` o estado no disponible, se debe emitir un error tipado (`CortexError`) y queda estrictamente prohibido ejecutar `INSERT` en la base de datos de persistencia.

## 9. Erradicación de Pánicos en Fronteras FFI y Rutas de Persistencia Transaccional (INV_BFT_04)
- **Invariante:** En motores de persistencia y ledgers transaccionales exportados a través de fronteras FFI (ej. Rust PyO3, C-ABI, WASM), queda TERMINANTEMENTE PROHIBIDO invocar `panic!`, `unimplemented!()` o `todo!()` ante colisiones de hash, violaciones de unicidad o inconsistencias de estado.
- **Riesgo Físico:** El unwinding de pila a través de límites `extern "C"` genera comportamiento indefinido (UB), abortos incontrolados del proceso y deja transacciones SQLite WAL a medio escribir en disco.
- **Patrón Mandatorio:**
  1. Definir un error estructurado de dominio (ej. `BftCollisionError { kind, hash, existing_content, incoming_content }`).
  2. Retornar el fallo como `Result::Err` tipado (ej. empaquetado en `rusqlite::Error::ToSqlConversionFailure`).
  3. Permitir que el destructor RAII de la transacción ejecute el rollback automático antes de que el bridge FFI traduzca el fallo a una excepción nativa del lenguaje anfitrión (ej. `PyRuntimeError`).

## 10. Auditoría Pre-Flight del Historial de Git ante Conmutación a Público (Zero-Leakage Invariant)
- **Invariante:** Antes de conmutar la visibilidad de cualquier repositorio de `PRIVATE` a `PUBLIC` (`gh repo edit --visibility public`), queda ESTRICTAMENTE PROHIBIDO basar la decisión de seguridad únicamente en el estado del árbol de trabajo actual (`git status`).
- **Verificación Causal Obligatoria:**
  1. Ejecutar un escaneo del histórico completo de commits (`git log --all --full-history`) en busca de rutas sensibles (`PACK_SOCIOS`, contratos societarios, NDAs, DNI, claves privadas `*.pem`, `.env`, credenciales de API).
  2. Verificar que los archivos confidenciales no solo hayan sido eliminados del disco, sino que su rastro histórico haya sido destilado o purgado antes de abrir el repositorio a la red global.
  3. Si existen commits históricos con activos de equity o marketing privado, abortar la conmutación inmediata y exigir la destilación de una rama limpia o la migración de dichos activos a la bóveda aislada `~/20_VAULT/`.

## 11. Invariante de Aniquilación Afín de Vistas C-ABI sobre mmap (INV_C5_MMAP_AFFINE_ANNIHILATION)
- **Invariante:** En todo canal de memoria compartida o actor SPMC/SPSC que vincule estructuras C-ABI sobre descriptores `mmap` (`ctypes.Structure.from_buffer(mm)`), queda TERMINANTEMENTE PROHIBIDO invocar `mm.close()` o permitir el cierre del descriptor sin desenlazar explícitamente la vista exportada.
- **Riesgo en Silicio:** En Python 3.14+, intentar cerrar un `mmap` con punteros de estructura vivos dispara fatalmente un `BufferError: cannot close exported pointers exist`, corrompiendo la recuperación de memoria en bucles de prueba o reinicios del proceso.
- **Patrón Mandatorio:**
  1. Implementar método `.close()` explícito que reasigne o anule la estructura C-ABI (`self.manifest = NullStructure()`) inmediatamente antes de invocar `mm.close()`.
  2. Implementar soporte de gestor de contexto (`__enter__` / `__exit__`) para garantizar liberación determinista en excepciones.

## 12. Invariante de Canon On-Wire, Unificación Criptográfica y Fronteras IPC (INV_C5_ONWIRE_CANON)

Toda frontera de comunicación entre procesos (IPC), protocolos de atestación, ledgers criptográficos y serialización inter-agente DEBE regirse por los siguientes preceptos deterministas:

1. **Unificación Canónica de Funciones Hash:**
   - **`BLAKE3`:** Digest canónico exclusivo para árboles de Merkle de alta velocidad, integridad de mensajes IPC (`B60IPC` con MAC con clave), digests de nonces, caché de capacidades y deduplicación.
   - **`SHA-256` (`sha2`):** Circunscrito estrictamente a interfaces de atestación criptográfica formal, firmas de hardware NIST P-256 (Apple Secure Enclave / Touch ID) y atestaciones SCITT (RFC 9942).
   - **Veto a `ring` y `sha3`:** Queda prohibida la introducción de `ring` (sustituido por primitivas zero-copy/RustCrypto puras y `blake3::Hasher::new_keyed`) y `sha3` en las rutas de consenso e IPC.

2. **Transporte Canónico y Envelopes Tipados:**
   - El formato canónico de transporte inter-proceso para envelopes del executor, Receipts de 5 fases e inferencias es **`CBOR + COSE_Sign1 + CDDL`**.
   - Queda prohibido el uso de envelopes exteriores en JSON no versionados sobre sockets `AF_UNIX` de autoridad.
   - Todo mensaje estructurado de baja latencia (`KUDURRU-64`) debe incluir un byte explícito de versión de protocolo en cabecera y mantener endianness unificado.

3. **Ingesta Fail-Closed y Blindaje de Atestación:**
   - Queda estrictamente prohibido desplegar daemons de atestación HTTP sin autenticación en red local (`127.0.0.1:6060`).
   - Toda ingesta hacia el ledger WORM inmutable debe confinarse a sockets de dominio Unix (`AF_UNIX`) con verificación obligatoria de credenciales del peer llamante (`getpeereid` / `LOCAL_PEERCRED`).
   - Cualquier payload que no valide el esquema o resulte no parseable debe rechazarse de forma inmediata (*fail-closed* con error `400 Bad Request`); queda terminantemente prohibido almacenar fallos como literales crudos (`{"raw": body}`) en la cadena WORM.

4. **Protección Anti-Replay con Reloj Autoritativo de Host (Ley O13):**
   - La verificación de sobres de atestación inter-agente exige un `NonceStore` autoritativo en memoria del host.
   - No es admisible validar únicamente la ventana temporal del emisor; cada nonce debe ser de uso único estricto dentro de la ventana de frescura ($T \le 300\text{ s}$). Nonces duplicados o expirados deben ser rechazados sin invocar verificación de firma.

5. **Morfismo de Estado y Cero Grados de Libertad Parásitos:**
   - Toda ontología formal (`ReceiptStage`) debe vincularse mediante morfismos exhaustivos en compilación (`From` / `TryFrom`) al estado de ejecución real del runtime (`ReservationState`), impidiendo la coexistencia de máquinas de estados fantasma.
   - Queda prohibido reimplementar estructuras de sincronización lock-free (`SharedManifest`, Seqlock) fuera del crate canónico de Ring-0.

## 13. Convergencia Dual-Schema y Fachada Síncrona de Ledgers (R-8)
- **Núcleo Primario:** `BFTLedgerActor` constituye el motor asíncrono canónico de escritura única. Todo componente del sistema debe converger sobre su interfaz para mutaciones de alta concurrencia.
- **Fachadas y Mappers Canónicos:** Para superficies síncronas (CLI, scripts), se debe emplear `CortexPersistFacade` o mapear `CortexEvent` a `LedgerEvent` mediante `cortex_event_to_ledger_event` preservando invariantes de causalidad (`cortex_taint`, `lamport_t`, UUID v5).
- **Durabilidad Invariable:** Toda conexión de persistencia a tablas de ledger (`cortex_ledger`, `ledger_entries`) DEBE forzar `PRAGMA synchronous = FULL` bajo WAL mode, previniendo amnesia post-crash y falsas garantías de ordenamiento.

## 14. Anclaje Externo de Ledger-Heads en Transparency Logs (Rekor / Art. 12 EU AI Act)
- **Mitigación de Evidencia Auto-Emitida:** Para que una atestación de estado del ledger posea peso probatorio frente a reguladores o terceros (Art. 12 EU AI Act), el ledger-head (`merkle_root` + `max_lamport` + `total_entries` + `attested_at`) debe anclarse externamente en un log de transparencia público o federado (Sigstore Rekor).
- **Esquema de Anclaje:** El digest SHA-256 del JSON canónico del ledger-head debe firmarse criptográficamente (Ed25519) y enviarse mediante `RekorClient.anchor_payload(...)`.
- **Inspección de Evidencia Agnóstica:** Todo exportador de cumplimiento (`compliance_exporter`) DEBE inspeccionar dinámicamente `sqlite_master` para aceptar indiferentemente esquemas `ledger_entries` o `cortex_ledger`, integrando la prueba de inclusión de Rekor (`rekor_anchor`) en el bloque `evidence_verification`.


