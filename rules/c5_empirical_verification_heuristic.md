---
name: c5_empirical_verification_heuristic
description: Heurística de verificación empírica en silicio previa a afirmaciones de estado.
trigger: "model_decision"
---

# Invariante de Verificación Empírica (C5-REAL)

## 1. Heurística de Aserción sobre Sistemas Reales
Ante cualquier pregunta o solicitud formulada con la estructura **"¿X tiene/cumple Y?"** (o variaciones semánticas equivalentes) referida a un sistema real, entorno físico o de software activo, el agente **DEBE**:

1. **Escalar a Modelo "High":** Invocar el uso del modelo de mayor capacidad (ej. Gemini Pro / High) para el razonamiento, evitando confabulaciones de modelos menores.
2. **Forzar Validación en Silicio:** Abstenerse de dar una respuesta definitiva basándose únicamente en la memoria latente de pesos pre-entrenados. El agente DEBE proporcionar o ejecutar los comandos exactos de terminal necesarios para **comprobar empíricamente** la aserción directamente en la máquina o sistema real.

*El mapa no es el territorio. La única respuesta válida a "¿X tiene/cumple Y?" es la salida estándar (stdout) de una traza física o comando de auditoría que lo verifique.*

---

## 2. Desacoplamiento de CI y Resurrección Local (Cambio 2 en Integración Continua)
Cuando la integración continua en la nube (GitHub Actions u otros SaaS) sufra bloqueos externos ajenos al código (fallos de facturación, suspensiones de cuenta, límites de cuota o caídas de infraestructura):
1. **Prohibición de Bloqueo Cognitivo:** Queda terminantemente prohibido que el agente declare bloqueada la maduración del software o espere la intervención humana en la pasarela de pago para continuar.
2. **Gate Local Determinista en $O(1)$:** El agente DEBE verificar o instanciar un script local reproducible (`scripts/ci_local.sh` o target `make ci-local`) que ejecute de forma atómica y ordenada todas las fases esenciales:
   - Validación estática de schemas y JSON (`jq` / python ast).
   - Linters de flujos de trabajo (`actionlint`).
   - Chequeo y tests de compilación bare-metal (`cargo check --all-targets`, `cargo test`).
   - Batería completa de pruebas de lenguaje (`pytest tests/`).
3. La única certificación de paso válida en régimen de asedio externo es la atestación local en el silicio de la máquina de desarrollo.

---

## 3. Linters AST sobre Control de Flujo (Anti-Falsos Positivos en Cadenas `elif`)
Al implementar o auditar analizadores estáticos de código basados en el árbol sintáctico abstracto (`ast.AST`) que vigilen la profundidad máxima de anidamiento (ej. `INV_C5_13`):
1. **Isomorfismo de Indentación Visual vs. AST:** En el parser de Python, cada cláusula `elif` se representa internamente como un nodo `ast.If` anidado dentro de la lista `orelse` del nodo anterior.
2. **Veto al Incremento en `elif`:** El cálculo recursivo de profundidad DEBE comprobar si el hijo es un `ast.If` contenido como único elemento en `node.orelse`. De cumplirse, el incremento de profundidad es 0.
3. Tratar un despacho `if/elif/...` lineal como anidamiento profundo constituye un error de medición que degrada la legibilidad al forzar fragmentaciones artificiales.

---

## 4. Arquitectura Dual de Atestación Criptográfica (`AttestationEnvelope`)
En arquitecturas de soberanía de silicio donde el anillo central de autoridad delega por defecto en enclaves seguros de hardware (Touch ID / Apple Secure Enclave P-256):
1. **Doble Ruta de Despacho:** La función constructora (`AttestationEnvelope.create()`) DEBE mantener siempre una ruta secundaria activada mediante parámetro explícito (`signing_key: Optional[str]`).
2. **Confinamiento de Pruebas y CI:** Las suites de test, harnesses de estrés y procesos desatendidos deben suministrar claves deterministas de prueba para ejecutar firmas Ed25519 en memoria, permitiendo que la verificación criptográfica (`env.verify()`) se certifique de forma autónoma.
3. El gate biométrico físico se reserva para mutaciones reales del operador biológico en el canal de producción, erradicando fallos de cuelgue o bloqueos síncronos en pipelines automatizados.

---

## 5. Invariante de Aislamiento en Mutación de Dependencias y Gates Limpios (Clean Worktree Gate)
Cuando se ejecute una actualización de dependencias, regeneración de lockfiles (`uv.lock`, `Cargo.lock`, `pnpm-lock.yaml`) o resolución de PRs en un repositorio cuyo working tree contenga modificaciones o supresiones no relacionadas (`git status --porcelain` no vacío):
1. **Veto a la Mutación en Árbol Sucio:** Queda terminantemente prohibido editar manifiestos o ejecutar comandos de actualización (`uv lock`, `cargo update`, `pnpm install`) directamente sobre el árbol de trabajo contaminado, al absorber involuntariamente estados intermedios, módulos fantasma o configuraciones locales no commiteadas.
2. **Confinamiento en Worktree Limpio:** La operación DEBE ejecutarse en un worktree efímero e ignorado (`git worktree add target/wt-... <ref>`).
3. **Auditoría Estricta de Diff Relativo al Padre:** Antes de stagear, contrastar con `git diff <parent> -- <manifest>` para certificar que el cambio contiene **estrictamente** los pisos/versiones solicitados y cero arrastre de modificaciones preexistentes.
4. **Verificación de Gate en Silicio Limpio:** La condición de parada (`uv lock --check`, `cargo check --locked`, test suites) DEBE evaluarse dentro del worktree limpio contra el commit exacto previo al push a ramas troncales (`main`).

## 6. Invariante de Reconocimiento Forense Autónomo de Código (INV_C5_AUTONOMOUS_FORENSIC_RECOVERY)
Ante cualquier búsqueda o verificación sobre la existencia, estado o autoría de un módulo, aplicación, herramienta o trabajo previo referenciado por el usuario:
1. **Prohibición de Dictamen Superficial:** Queda terminantemente prohibido concluir la inexistencia de código basándose únicamente en `HEAD`, `git status` o `git ls-files`.
2. **Protocolo Forense Obligatorio de 6 Estratos:** El agente DEBE ejecutar y agotar autónomamente antes de emitir cualquier diagnóstico:
   - **Estrato 1 (Gitignore y Staging):** `git status --ignored` y comprobación de patrones en `.gitignore` para descartar rutas deliberadamente excluidas (`tools/`, `target/`, `.cursor/`).
   - **Estrato 2 (Reflogs Profundos):** `git reflog --all --date=iso` buscando commits huérfanos, checkpoints de asistentes o conmutaciones recientes.
   - **Estrato 3 (Árbol de Ramas y Worktrees):** `git branch -a` y `git worktree list` contrastando ramas locales y remotas no integradas.
   - **Estrato 4 (Archivos Untracked y Stashes):** `git status --short --untracked-files=all` y `git stash list`.
   - **Estrato 5 (Topología de Organización Remota):** Búsqueda de repositorios hermanos y ramas activas vía `gh repo list` o `gh api "repos/<org>/<repo>/branches"`.
   - **Estrato 6 (Artefactos y Transcripciones de Sesión):** Inspección de `brain/` e historiales de sesiones recientes (`transcript.jsonl`).
3. **Veto a la Consulta Prematura:** Queda estrictamente prohibido solicitar al operador humano confirmación de rutas o nombres sin haber agotado los 6 estratos en silicio.

---

## 7. Invariante de Suites Mixtas y Falsación de Optimizaciones (PCC Negative-Case Invariant)
Al auditar, optimizar o endurecer scripts de compilación, verificación o tests sobre directorios de programas fuente (ej. `examples/`, `tests/fixtures/`):
1. **Presunción de Heterogeneidad Semántica:** Queda estrictamente prohibido asumir que todos los archivos de un directorio son casos positivos destinados a compilar o verificar con éxito. En compiladores Proof-Carrying Code (PCC) o con solvers SMT/Z3, una fracción sustancial son pruebas de penetración o exploits intencionales diseñados expresamente para ser **rechazados** (`REJECTED`) en tiempo de compilación.
2. **Veto a Comodines Globales Rígidos:** Queda terminantemente prohibido imponer `set -euo pipefail` o suprimir banderas de tolerancia a fallos sobre comodines globales (`*.anv`, `*.rs`) sin antes particionar en silicio los casos positivos verificables de los casos de refutación negativos.

---

## 8. Invariante de Prioridad Epistémica de Núcleo frente a Fontanería de CI
Ante solicitudes conceptuales, análisis dialécticos o demostraciones formales de código:
1. **Primacía del Núcleo y Silicio Local:** El agente DEBE resolver la consulta en el sustrato matemático, en el código local (`src/`, `tests/`) o en artefactos analíticos de `brain/`.
2. **Veto a la Desviación hacia Workflows Externos:** Queda terminantemente prohibido desviar la tarea hacia la modificación o refactorización de flujos de integración continua (`.github/workflows/*.yml`) salvo mandato expreso e imperativo del Operador (*"olvida github action"* como directiva por defecto ante dialéctica teórica).

---

## 9. Invariante de Grounding en Colecciones Artísticas y Anti-Confabulación Iconográfica
Ante consultas para identificar, buscar o atribuir obras de arte basadas en imágenes, similitudes temáticas o referencias a la cultura popular (ej. portadas de discos, iconos musicales o cinematográficos):
1. **Prohibición de Atribución Asociativa:** Queda terminantemente prohibido asumir o afirmar la identidad de una obra del catálogo basándose únicamente en memoria asociativa o en que el sujeto comparta rasgos con una referencia externa (ej. el niño de una portada de U2).
2. **Inspección de Archivo Local Obligatoria:** El agente DEBE verificar empíricamente los metadatos y archivos del repositorio (`catalogo.json`, `images/catalogo/`, `src/artworks.ts`) mediante herramientas de lectura (`read_file`, `search_files`) antes de confirmar el título de la obra.
3. Si la pieza no se encuentra en el archivo verificado del proyecto, el agente debe declarar explícitamente la no correspondencia, evitando validar coincidencias falsas.

---

## 10. Invariante de Integridad de Evidencia y Tripartición de Hallazgos (FL-VERIFY-01)
Al diseñar, evaluar o auditar sistemas multi-agente de seguridad, verificación de código o remediación automatizada:

1. **Tripartición Canónica de Roles:** Queda estrictamente prohibido que un único agente o componente concentre afirmación, verificación y mutación. El sistema DEBE desacoplar formalmente tres entidades:
   - **Generación (`Finding`):** Afirma que un artefacto identificado de forma unívoca por su digest (`inspected_artifact_digest`) presenta un comportamiento prohibido (`prohibited_behavior_id`).
   - **Verificación Independiente (`ReproductionRun`):** Ejecuta de forma aislada y determinista la reproducción, observando exclusivamente testigos físicos independientes del proceso padre (canarios en disco, sockets escuchados, inodos), nunca telemetría o afirmaciones autorreportadas por el código bajo prueba (`INV_C5_NEMESIS_EVIDENCE_CONTRACT`). El verificador debe ser estrictamente ajeno al productor (`verifier_id != producer_id`).
   - **Autorización Causal (`Authorization`):** Registro de aprobación del operador humano o política de gobernanza en ledger inmutable WORM (`VerificationGate` / SCITT SHA-256 Merkle chain). Cualquier efecto o parche sobre un hallazgo no verificado o sin autorización explícita para esa acción debe abortar en *fail-closed* (`ContractViolation`).

2. **La Invariante de Asimetría Epistémica (Lección ETH):**
   $$\text{Prueba o ejecución formal válida} \not\Rightarrow \text{Afirmación informal correctamente formalizada}$$
   Un crash fortuito, una excepción de sintaxis o un comportamiento anómalo distinto al afirmado no constituye verificación del hallazgo. La condición `VERIFIED(f)` exige correspondencia biyectiva entre el comportamiento prohibido afirmado y el evaluado por el oráculo determinista (`oracle_digest`) del verificador sobre el mismo artefacto exacto:
   $$\operatorname{VERIFIED}(f) \iff \exists\,\text{run}: \operatorname{Run}(f) \land (\text{run.artifact\_digest} = f.\text{inspected\_artifact\_digest}) \land (\text{run.observed\_behavior} = f.\text{prohibited\_behavior}) \land (\text{run.outcome} = \text{REPRODUCED}) \land (\text{run.verifier} \neq f.\text{producer})$$

3. **Disambiguación Criptográfica de Hashes:** Al coexistir múltiples algoritmos de digest de igual longitud (ej. SHA-256 vs BLAKE3, ambos con representaciones hexadecimales de 64 caracteres), todo digest de artefacto, oráculo o recibo DEBE llevar prefijo de esquema canónico (`sha256:...`, `blake3:...`) para prevenir colisiones sintácticas y falsas validaciones cruzadas.

4. **Reutilización de Sondas de Confinamiento en Silicio:** Prohibido improvisar nuevos entornos de ejecución desprotegidos para reproducir exploits. Las reproducciones dinámicas deben apalancarse en las sondas previas de confinamiento del sistema operativo (Seatbelt `(deny default)`, veto de red, fork y subprocesos; ej. `McpSandboxValidator`), registrando `INCONCLUSIVE` (nunca `NOT_REPRODUCED`) si el aislamiento de silicio no puede certificarse.
