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

1. **Unificación Canónica de Funciones Hash y Fronteras Criptográficas:**
   - **Ruta On-Wire, IPC y Consenso en Rust (`00_ABZU_KERNEL` / `babylon-attest`):** `BLAKE3` como digest canónico exclusivo para árboles de Merkle de alta velocidad, integridad de mensajes IPC (`B60IPC` con MAC con clave), digests de nonces, caché de capacidades y deduplicación; `SHA-256` (`sha2`) circunscrito estrictamente a interfaces de atestación criptográfica formal, firmas de hardware NIST P-256 (Apple Secure Enclave / Touch ID) y atestaciones SCITT (RFC 9942). Queda prohibida la introducción de `ring` y `sha3` en esta ruta caliente de consenso e IPC.
   - **Ruta de Atestación de Release y Persistencia SQLite (`01_KISH_ENGINE`):** El árbol de Merkle inmutable de release (`compile_claims_manifest.py`) y el ledger de eventos Python (`cortex_crypto_kernel.py`) emplean `SHA3-256` reforzado con separación de dominio RFC 6962 (`0x00`/`0x01`/`0x02`) y compromiso de cardinalidad, no constituyendo infracción de `INV_C5_ONWIRE_CANON` al ser un almacenamiento de evidencia persistente y no un protocolo de transporte inter-nodo.

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

## 15. Invariante de Pureza Normativa en Especificaciones (Anti-Slop de Sanitización)
- **Prohibición de Marcadores Sintéticos:** Toda especificación formal, archivo de arquitectura (`spec_architecture.md`) o roadmap estratégico (`sota_evolution_roadmap.md`) DEBE mantener identificadores canónicos limpios.
- **Purga Determinista:** Queda prohibido versionar o dejar marcadores de sanitización automática (`[OBSOLETO: ...]`) en documentos normativos. Antes de sellar cualquier `RELEASE_MANIFEST.json` o compilar claims, debe verificarse mediante `! git grep -q "\[OBSOLETO:" docs/` que el corpus documental conserva su integridad terminológica.

## 16. Invariante de Agrupación Atómica en Dependencias Multi-Crate (INV_C5_DEPENDENCY_GROUP_ATOMICITY)
- **Invariante:** En repositorios con pilas de compilación acopladas (ej. `hyperium/tonic`, `prost`, `tokio` o suites criptográficas como `rand` y `ed25519-dalek`), los bots de actualización automatizada (Dependabot, Renovate) DEBEN configurarse obligatoriamente con directivas de agrupación (`groups:`).
- **Prohibición:** Queda terminantemente prohibido tramitar o permitir upgrades aislados de crates individuales pertenecientes a la misma familia de codegen/runtime (ej. `tonic-build` sin `tonic`, `prost` sin `tonic-prost-build`, `tonic-web` sin `tonic`) o bumps mayores de CSPRNG (`rand 0.9` vs `rand_core 0.6`) que provoquen fracturas nominales de traits (`E0277`) en el compilador de Rust.

## 17. Invariante Anti-TOCTOU en Descriptores de Fichero (INV_C5_FS_DESCRIPTOR_NOFOLLOW)
- **Invariante:** Toda rutina en Python o Rust que valide permisos, confinamiento de rutas o inexistencia de enlaces simbólicos en un recurso antes de leer su contenido (ej. `mcp_server.py`, artefactos) DEBE realizar la apertura física del descriptor utilizando la bandera `O_NOFOLLOW` (`os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)` o `OpenOptionsExt::custom_flags(libc::O_NOFOLLOW)`).
- **Prohibición:** Queda prohibida la secuencia ingenua de comprobar `is_symlink()` y posteriormente invocar `read_text()` o `open()`, al ser vulnerable a sustitución atómica de inodos en sistemas de archivos concurrentes.

## 18. Invariante de Normalización Geométrica de Claves Secure Enclave (INV_C5_SECURE_ENCLAVE_POINT_NORMALIZATION)
- **Invariante:** Al validar atestaciones de hardware emitidas por el Secure Enclave (Apple Silicon via CryptoKit), el runtime DEBE procesar y normalizar las claves públicas a puntos de curva elíptica SEC1 / NIST P-256 (`same_public_key`) antes de evaluar equivalencias.
- **Prohibición:** Queda prohibida la comparación cruda de bytes entre representaciones SEC1 no comprimidas (65 bytes `x963Representation`) y estructuras PKI SPKI DER (~91 bytes), previniendo falsos rechazos en la autorización biométrica de Ring-0.

## 12. Invariante de Trust Gateway para Computer Use y Mediación Completa (INV_C5_COMPUTER_USE_TRUST_GATEWAY)
Toda aplicación o motor de automatización de interfaz y control de escritorio (*Computer Use*, Mac Maestro, Mandato) gobernado por o acoplado a BABYLON-60 DEBE cumplir estrictamente:
1. **Cero Bypass GUI/AX/HID en Confinamiento OS (Seatbelt):** Todo perfil de aislamiento para procesos de agentes no confiables (`sandbox-exec` / XNU) DEBE incorporar obligatoriamente `(deny hid-control)`, `(deny appleevent-send)` y denegación explícita de `mach-lookup` hacia los servicios Mach del subsistema gráfico: `com.apple.windowserver.active`, `com.apple.accessibility.AXServer`, `com.apple.coreservices.appleevents` y `com.apple.tsm.portname`.
2. **Ticket de Despacho Criptográfico No Falsificable:** El ejecutor de acciones (`Desktop.execute`) tiene prohibido actuar sin un `AuthorizedDispatchTicket` respaldado por un `AttestationReceipt` verificable (clave pública SEC1 X9.63 de 65 bytes + firma ECDSA DER generada por el Secure Enclave). Prohibido descartar la firma biométrica en `Void`.
3. **Ciclo OODA con Verificación Reactiva de Deltas (`DeltaVerifier`):** El envío de un evento no demuestra el éxito de la tarea. Tras cada acción autorizada, el sistema DEBE re-observar la interfaz y verificar que el delta esperado (`ExpectedDelta`) se materializó en el estado observable. Si el delta es refutado tras reintentos escalonados ($100\,	ext{ms}, 250\,	ext{ms}, 500\,	ext{ms}$), el ciclo se congela inmediatamente en fail-closed (`DeltaMismatch`) asentando `stage: .failed` en el ledger WORM.
4. **Enlace Semántico de Controles:** Prohibido despachar eventos basándose exclusivamente en identificadores numéricos efímeros (`node: Int`). Toda propuesta debe vincular semánticamente la tupla `(id, role, title)` validando que el control no mutó antes del despacho.
5. **Freno de Emergencia Físico:** Implementación obligatoria de un detector de eventos para doble pulsación de `Escape` en $\le 400\,	ext{ms}$, detonando inmediatamente `0xDEAD_6060` (estado envenenado) y abortando tareas en curso.
