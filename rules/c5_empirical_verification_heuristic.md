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

5. **Independencia de Contexto y Aislamiento Efectivo:** Otra conversación o identidad de agente no constituye una frontera de permisos. Un revisor de solo lectura debe carecer de herramientas de edición y shell libre, incluidas capacidades equivalentes vía MCP, delegación o herramientas heredadas. Ejecutar Cargo, Lean o `verify.sh` exige un ejecutor restringido: operaciones y argumentos permitidos explícitamente, fuentes e inputs protegidos contra escritura y directorios de salida separados. Redirigir salidas o declarar una política de sandbox no prueba por sí solo el confinamiento.

6. **Aceptación del Verificador:** Comprobar por separado su carga e invocación en el cliente real, el rechazo efectivo de escrituras sobre fuentes e inputs mediante una prueba negativa controlada y la vinculación del resultado al contenido ejecutado. Conservar versión y configuración del cliente, capacidades efectivas, comando, entorno, resultado y digests con algoritmo explícito de inputs, oráculo y evidencias. Incluir cambios locales y archivos no versionados que sean inputs; `HEAD`, el índice Git o `git status` por sí solos no identifican ni protegen todo el contenido leído. Verificar que cambiar un input o el oráculo invalida el resultado anterior; proteger la instantánea durante la ejecución, pues comparar hashes antes y después no impide modificaciones transitorias. Sin estas comprobaciones, declarar la propiedad pendiente como `NO_VERIFICADO` o la ejecución como `INCONCLUSIVE`.

7. **Diagnósticos y Valoraciones Delimitados:** Distinguir formato documentado, archivos presentes, configuración declarada y comportamiento observado, registrando fecha y versión. Un formato antiguo, una ausencia en un listado o un vocabulario impropio no demuestran por sí solos el rechazo completo de un plugin ni su causa; tampoco prueban que una causa esté descartada. Etiquetas como «P0», «Óptimo» o puntuaciones sin método, datos y comparación reproducible son valoraciones, no resultados medidos.

---

## 11. Invariante de PoC como Frontera Medible y Conservación de Evidencia (INV_C5_POC_MEASURABLE_BOUNDARY)
Una Prueba de Concepto (**PoC**) contrasta una hipótesis acotada; su aceptación no certifica automáticamente producción ni demuestra un óptimo físico.
1. **Criterio Fijado Antes de Ejecutar:** Declarar hipótesis, inputs, entorno, comando reproducible y umbral observable de aceptación o rechazo. Registrar `PASS` o `FAIL` cuando el ensayo sea válido; usar `INCONCLUSIVE` si faltan condiciones para evaluarlo, sin convertirlo en éxito ni en refutación.
2. **Aislamiento del Mecanismo:** Reducir dependencias ajenas a la hipótesis y declarar las que permanecen. Omitir UI, red o base de datos solo cuando no formen parte del comportamiento estudiado; medir el componente aislado no demuestra su comportamiento integrado.
3. **Línea Base Versionada:** Conservar fuentes, configuración, versiones de herramientas, inputs, umbrales y resultados vinculados por digests. Comparar producción bajo condiciones equivalentes y con tolerancias declaradas; cualquier revisión de la línea base conserva la anterior y explica la causa.
4. **Destino Canónico y Limpieza Acotada:** Integrar los PoCs reutilizables y su evidencia en `scripts/` de la skill correspondiente o en su repositorio de `~/10_PROJECTS/`. Registrar destino y procedencia de clones de terceros. Limpiar únicamente temporales propios identificados, dentro del alcance autorizado y después de comprobar la copia conservada; no borrar trabajo ajeno o evidencia para imponer un objetivo global de `0 B` en `~/.gemini/antigravity/scratch/`.

---

## 12. Pentálogo de Falsación Socrática Directa (Protocolo Q11–Q15)

Ante cualquier informe de arquitectura, auditoría o defensa de diseño, el evaluador debe someter el sistema a las 5 preguntas de despojo ontológico:

1. **Q11 · Prueba del Despojo de Jerga:** Retirar toda la terminología propia y etiquetas de branding («Ring-0», «consenso BFT», «exergía»). ¿Qué hecho físico y verificable en el sistema operativo queda en pie? (EL0, SQLite WAL, 64B Seqlock, 354 tests).
2. **Q12 · Prueba del Bug Mortal Silencioso:** Identificar qué fallo de concurrencia, corrupción de datos o bypass de sandbox pasaría inadvertido por los tests actuales debido a aislamiento del arnés o mocks ciegos.
3. **Q13 · Test del Extraño Hostil (Cierre al Segundo 35):** Examinar la portada y tablas de presentación: si un ingeniero escéptico sin contexto previo abre el proyecto, todo término interno opaco en los primeros 100 renglones debe traducirse a estándares de la industria (ej. *«Deterministic fail-stop halt»* antes que *«Apoptosis»*) para evitar el abandono de lectura al segundo 35.
4. **Q14 · Deuda de Vigilia Zero-Touch:** Auditar si el sistema sobrevive 30 días sin intervención biológica: verificar rutas de intérprete en daemons, rotación de logs, ausencia de mutaciones automáticas en worktrees y caducidad de atestaciones biométricas.
5. **Q15 · Proporcionalidad de Cómputo vs. Pereza de Poda:** El plano de mediación y seguridad determinista debe operar en < 50 MB de memoria. Queda prohibido justificar expansiones de hardware masivas (256 GB) para suplir falta de poda algorítmica, sobrecarga de reglas en contexto o clasificación estocástica de permisos.

---

## 13. Invariante de Verificación Criptográfica de Releases y Clausura de Bundles Standalone (INV_C5_ZERO_TRUST_RELEASE_BUNDLE)
Al diseñar, auditar o implementar empaquetadores y scripts de verificación de releases (`verify_release.sh`, `verify.sh`):

1. **Tipado Booleano Estricto (Veto a Coerción de Strings):**
   - En parsers de evidencia, queda terminantemente prohibido utilizar conversiones de veracidad implícitas (`bool(x)`). El verificador DEBE evaluar `isinstance(raw_value, bool) is True`.
   - Cualquier valor que no sea un booleano estricto (ej. el string `"false"`, enteros `0`/`1`, nulos no declarados) DEBE abortar en `FAIL-CLOSED` con código de salida no nulo.

2. **Reconstrucción Inductiva de Cardinalidades (Merkle Leaf Counts):**
   - Queda estrictamente prohibido validar contadores basándose únicamente en sumarios de alto nivel o en `failed == 0`.
   - El verificador DEBE recalcular inductivamente cada categoría (`verified`, `empirical_and_bounded`, `experimental`, `failed`, `total`) iterando sobre la totalidad de las hojas evaluadas del árbol Merkle.
   - La discrepancia entre los contadores reconstruidos y los declarados en `RELEASE_MANIFEST.json` o `evidence.json` constituye adulteración de evidencia y aborta en `FAIL`.

3. **Clausura Autónoma de Bundles Distribuidos (Sin `.git`):**
   - Todo archivo comprimido de release (`.zip` / `.tar.gz`) destinado a distribución pública o auditoría independiente DEBE ser autocontenido y verificable sin depender de metadatos `.git`:
     a) **Paridad de Gobernanza:** DEBE incluir el 100% de los archivos declarados en `artifacts_sha256`.
     b) **Paridad de Construcción:** DEBE contener todos los activos exigidos por directivas de empaquetado (ej. `tool.hatch.build.targets.wheel.force-include`).
     c) **Inventario Autenticado de Fuentes:** El manifiesto DEBE registrar el listado exhaustivo de archivos del bundle (`release_bundle.source_files`) y su digest determinista (`release_bundle.tree_digest`), permitiendo al verificador certificar la autenticidad del árbol público en ausencia de `.git`.

---

## 14. Invariante de la Cadena de Transducción Quíntuple y Atestación Delimitada (FL-022-v2)
Al diseñar, evaluar o auditar agentes que generen código, optimicen geometrías o sinteticen artefactos ejecutables:

1. **La Ley de Goodhart Física:** La optimización interna de un proxy continuo o simbólico (`ProxyScore`) por parte del agente no preserva monótonamente el orden ni la utilidad del artefacto final discretizado (`FinalUtility`):
   $$\operatorname{argmax}_{z \in \mathcal{Z}} S_{\text{proxy}}(z) \neq \operatorname{argmax}_{z \in \mathcal{Z}} U_{\text{final}}(\tau(z))$$
   Queda estrictamente prohibido comprometer o promover un artefacto basándose únicamente en el ranking de su función objetivo interna.

2. **Las Cuatro Brechas de Transducción Obligatorias ($P_1 - P_4$):**
   - **$P_1$ (`proxy_gap`):** Optimizador vs. Representación Intermedia (IR).
   - **$P_2$ (`transformation_gap`):** IR continua/simbólica vs. Artefacto final discretizado/compilado.
   - **$P_3$ (`deployment_gap`):** Artefacto verificado vs. Objeto realmente desplegado en runtime ($\operatorname{BLAKE3}(a_{\text{deployed}}) == \operatorname{BLAKE3}(a_{\text{verified}})$).
   - **$P_4$ (`reality_gap`):** Modelo de simulación/verificación vs. Comportamiento real medido en el entorno de contorno.

3. **Invariante de Aceptación y Commit:**
   $$\operatorname{Accept}(a, P, E) \implies \operatorname{Identity}(a) \land \operatorname{Verification}_{\mathcal{V}_\perp}(a, P) \land \operatorname{EnvironmentMatch}(P, E) \land \operatorname{ObservedConstraints}(a, E)$$
   $$\operatorname{CommittedArtifact}(a) \implies \operatorname{BLAKE3}(a_{\text{deployed}}) = \operatorname{BLAKE3}(a_{\text{verified}}) \land \operatorname{CriticalConstraints}(\operatorname{Observed}(a_{\text{deployed}})) = \text{PASS}$$

4. **Ortogonalidad de Modelos ($\mathcal{M}_{\text{ver}} \neq \mathcal{M}_{\text{opt}}$):**
   El modelo o simulador evaluador debe ser ortogonal e independiente del generador para erradicar puntos ciegos correlacionados (`CORRELATED_VERIFIER_MODEL_REJECTED`).

5. **Veto a Etiquetas `status = SAFE` sin Alcance (BORJARIO IR B3/B6):**
   Queda estrictamente prohibido registrar o aceptar atributos booleanos globales descontextualizados (`artifact.status = SAFE`). Toda afirmación de idoneidad en `CORTEX` exige el formato delimitado `ScopedClaimRecord` con perfil ambiental verificado $P$, perfil observado $E$, digest criptográfico y resultado tipado (`SUPPORTED` / `OBSERVED`).
