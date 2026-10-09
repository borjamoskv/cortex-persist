---
name: c5_bft_cryptographic_ledger_invariants
description: Invariantes no negociables para la arquitectura, auditoría e implementación de ledgers criptográficos BFT, árboles de Merkle y actores de persistencia en BABYLON-60 / C5-REAL.
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
