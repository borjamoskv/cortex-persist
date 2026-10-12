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
