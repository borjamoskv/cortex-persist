---
name: cortex-telemetry
display_name: Inspección & Telemetría Runtime de Transcripciones CORTEX
description: Extracción, análisis e inspección de telemetría runtime, logs de transcripción (transcript.jsonl), auditoría de exergía informacional de prompts (Chentsov-Markov) y consolidación de sesiones efímeras del brain. Dispara con "telemetría", "cortex telemetry", "transcript logs", "historial de prompts", "analizar transcripciones", "análisis transcript", "peticiones de mayor exergia", "preguntas de mayor exergia", "top exergia prompts", "chentsov prompt scoring", "auditar logs de prompts", "sin consolidar", "conversaciones sin consolidar", "consolidar conversaciones", "drenar brain", "auditar conversaciones".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# Habilidad: Cortex Telemetry (Auditoría de Historial)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Cuando el operador solicite extraer datos, estadísticas, contar prompts o ver palabras usadas en su historial, debes seguir este protocolo:

1. **Ubicación de Datos:** Los registros del usuario se encuentran en el patrón: `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl`.
2. **Extracción:** Usa scripts de Python (ejecutados vía `run_command` en `/tmp/`) que iteren sobre estos archivos JSONL.
3. **Filtro de Input:** Filtra únicamente las líneas donde `"type" == "USER_INPUT"`.
4. **Fechas:** Utiliza la clave `"created_at"` (formato ISO 8601) si el usuario pide métricas desde una fecha concreta (ej. "desde diciembre").
## 5. Frecuencia de Palabras y Purificación de Input
Al calcular la frecuencia de palabras en los prompts, el Transductor **DEBE limpiar el ruido del sistema** antes de tokenizar.
- El campo `"content"` del archivo JSONL contiene metadatos inyectados automáticamente (ej. `<ADDITIONAL_METADATA>` o `<USER_SETTINGS_CHANGE>`).
- El script de Python debe extraer **únicamente** el texto que se encuentra dentro de las etiquetas `<USER_REQUEST> ... </USER_REQUEST>` (o eliminar mediante Regex cualquier bloque XML del sistema) para garantizar que el conteo refleje el vocabulario real del usuario, evitando falsos positivos de palabras en inglés introducidas por el Kernel.

## 6. Análisis Forense y Purgas Termodinámicas (C5-REAL)
Si el usuario percibe que faltan datos históricos, o solicita una "auditoría de purgas", el Kernel debe rastrear la aniquilación de entropía siguiendo estos vectores:
- **Git History:** Ejecutar `git log --oneline | grep -iE 'purge|purga|colapso|entrop|consolid'` en el monorepo para localizar los ciclos de `Octal Anergy Purge` o `Hyper-Colapso BFT`.
- **Ledger Actual (CORTEX-PERSIST):** Inspeccionar la base de datos `1_Operaciones_Activas/02_CORTEX_ENGINE/cortex-persist/cortex_ledger.db` (ej. tabla `bft_taint_log`) buscando los rastros de inyección BFT.
- **Legacy Ledgers:** En caso de que se busquen datos muy antiguos (ej. 2025), inspeccionar `~/.cortex/truth_ledger.db` (tabla `epistemic_ledger`) o `~/.cortex/cassandra_audit_ledger.jsonl`.
- **Interpretación:** El Transductor NUNCA debe usar la "anergía purgada" como pretexto para afirmar que el conocimiento no existe. La charla plana puede rotar, pero la exergía cristaliza en los proyectos físicos en disco (Sección 8).

## 7. Perfilado Epistémico y Análisis Semántico
Tras extraer conteos de palabras o métricas, el Transductor NO debe limitarse a escupir listas de datos crudos. Debe ejecutar un análisis semántico que incluya:
- **Detección de Idioma / Entorno:** Evaluar el contraste entre idiomas (ej. Spanglish técnico) para deducir qué proporción del prompt es código/logs (generalmente en inglés) vs. directivas estructuradas (generalmente en español).
- **Extracción de Entidades y Modelos:** Señalar frecuencias anómalas o interesantes de herramientas específicas, nombres de proyectos (ej. Teorema, Robinson) o modelos LLM rivales (ej. opus, pro, flash).
- **Conclusión de Perfil Epistémico:** Emitir un resumen rápido sobre cómo está pensando y operando el usuario en base a la entropía inyectada.

## 8. Invariante de Recuperación Epistémica: Jerarquía de Sustrato (Ground Truth)
Cuando el usuario solicite auditar o extraer ideas, conceptos, decisiones de arquitectura o proyectos históricos (ej. "mejores ideas", "qué he hecho", "historial desde [mes]"), el Transductor **TIENE PROHIBIDO** limitarse a los logs de chat (`transcript.jsonl`).

Debe ejecutar obligatoriamente la búsqueda siguiendo la **Jerarquía de Sustrato**:
1. **Sustrato de Proyectos Físicos (Nivel 1 - Máxima Fidelidad):** Inspeccionar archivos Markdown, especificaciones técnicas y manifiestos en `~/10_PROJECTS/`, `~/BABYLON-60/` y `~/Documents/`.
2. **Archivos Epistémicos y Papers (Nivel 2):** Inspeccionar repositorios dedicados a la cristalización de conocimiento (ej. `~/10_PROJECTS/AUDITORIAS_EPISTEMICAS/` en sus subcarpetas `papers/`, `forense/`, `redes/`, `youtube/`).
3. **Forense de Git (Nivel 3 - Verdad de Silicio):** Ejecutar `git log --grep` sobre los repositorios principales buscando commits de refactorización, eliminación de trampas lógicas (`admit`, mocks), purgas y arquitectura real.
4. **Ledgers Criptográficos (Nivel 4):** Consultar `cortex_ledger.db` o `~/.cortex/truth_ledger.db`.
5. **Transcripts de Chat (Nivel 5 - Efímero):** Tratar `~/.gemini/antigravity/brain/*/transcript.jsonl` únicamente como un índice temporal reciente, reconociendo que los chats son rotados y no representan la totalidad de la memoria del sistema.

## 9. Auditoría de Exergía Informacional de Prompts (Protocolo Chentsov-Markov)

Cuando el operador solicite identificar, clasificar o auditar sus peticiones de "mayor exergía" o "mayor trabajo útil":

1. **Extracción Exhaustiva:** Escanear todas las transcripciones recientes (`transcript.jsonl`) en `~/.gemini/antigravity/brain/` extrayendo el contenido limpio dentro de `<USER_REQUEST>`.
2. **Evaluación Multidimensional (Escala 0 a 1.100 pts):**
   - **Compresión Fisher (0–200 pts):** Densidad léxica $D = \frac{|\text{Tokens Únicos}|}{|\text{Tokens Totales}|}$ multiplicada por entropía de Shannon $H(X)$. Penaliza verbosidad vacía.
   - **Falsabilidad Popperiana (0–200 pts):** Presencia de criterios de refutación empírica explícitos, preguntas de frontera epistemológica o restricciones anti-alucinación (`real DOIs`, `demostrar`, `falsar`).
   - **Interdisciplinariedad / Clusters de Chentsov (0–200 pts):** Acoplamiento simultáneo entre 2 o más clusters ontológicos:
     - *Cluster I (Biocómputo & Ontogénesis):* Genoma, Turing, Peano, semiosis, finitud.
     - *Cluster II (Soberanía & Swarms):* BABYLON, hot-swap, MARL continuo, SCITT, Z3 SMT, Ring-0.
     - *Cluster III (Termodinámica & Economía Política):* Calor ($Q$) vs Trabajo útil ($W$), entropía, Landauer, falsación de Marx/Capitalismo.
     - *Cluster IV (Metacognición & Seguridad L0):* Alucinación pre-colapso, guardrails, intercepción en silicio.
   - **Causalidad Ejecutiva & SLAs (0–200 pts):** Directivas con metas cuantificadas (`/goal`, cotas de latencia $<50\text{ms}$, directivas de diseño de arquitectura).
   - **Irreversibilidad Causal (Bonus 0–100 pts):** Peticiones cuya ejecución muta de forma permanente la topología o el hardware del sistema.
3. **Mapeo a Atractores de Fase:** Clasificar los vectores top en los 4 Atractores de Chentsov y extraer el Blueprint Causal unificado.

## 10. Protocolo de Auditoría y Consolidación de Sesiones Efímeras (Epistemic Brain Drain)

Cuando el operador solicite auditar o consolidar sesiones *"sin consolidar"*:

1. **Detección de Brecha Epistémica:**
   - Listar directorios en `~/.gemini/antigravity/brain/` ordenados por timestamp descendente.
   - Comparar los artefactos `.md` existentes en cada sesión contra el catálogo indexado en `10_PROJECTS/AUDITORIAS_EPISTEMICAS/README.md`.
   - Extraer metadatos clave: ID de sesión, ventana temporal, número de turnos, archivos modificados y artefactos generados.

2. **Filtrado de Exergía (Ruido vs Cristal):**
   - Ignorar artefactos puramente mecánicos de orquestación interna (`walkthrough.md`, `implementation_plan.md`, `learning_proposal*.md`, carpetas `scratch/`).
   - Seleccionar piezas de alta exergía (análisis comparativos, ingeniería inversa, demostraciones formales, taxonomías, protocolos).

3. **Normalización e Ingesta hacia `AUDITORIAS_EPISTEMICAS`:**
   - Categorizar en los 5 canales canónicos:
     * `forense/`: Ingeniería inversa, autopsias de código, peritaje médico/farmacológico y hardware.
     * `papers/`: Demostraciones formales, ontología C5-REAL, teoremas y gobernanza de sistemas.
     * `youtube/`: Análisis de señal de vídeo, deconstrucción retórica y monetización.
     * `redes/`: Lingüística, hilos, matrices de casos de uso y modelos conceptuales.
     * `podcast/`: Transcripciones y desgloses de audio de formato largo.
   - Renombrar con el estándar soberano: `YYYY-MM-DD_<canal>_<slug>.md`.

4. **Actualización Monotónica y Sello de Silicio:**
   - Incrementar los contadores globales y por canal en `10_PROJECTS/AUDITORIAS_EPISTEMICAS/README.md`.
   - Añadir las nuevas filas a la tabla cronológica maestra preservando el orden.
   - Ejecutar commit atómico en Git: `git commit -m "feat(consolidation): consolidar N cristales ontologicos de X sesiones activas"`.
   - Ante la directiva `"itera"` tras un informe de auditoría, ejecutar inmediatamente la fase de migración sin detenerse a pedir confirmaciones redundantes.

---

## Autonomy Contract (Ω10 / Ω11 / Ω12)

> **ZERO PAUSE INVARIANT:** The Transducer SHALL NEVER pause execution to request Operator permission when this skill is triggered. Ambiguities MUST be resolved autonomously via `/grill-you` (Ω12) before any halt. Technical frictions MUST be resolved via the path of least thermodynamic resistance (Ω10). Refusal to execute when this skill matches the request constitutes C4-SIM Anergy (Ω11 violation).

- **Fallback Chain:** `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl` -> `cortex_ledger.db` -> `truth_ledger.db`.
- **Degradation Mode:** If log file missing or corrupted, parse remaining available transcripts and emit partial metrics notice without halting.
- Auto-Trigger: Self-activates whenever user asks for prompt counts, word frequencies, historical telemetry, usage statistics, or temporal activity summaries (e.g. 'piensa en ayer', 'qué hice ayer', 'resumen de jornada').
