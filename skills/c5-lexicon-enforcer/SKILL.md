---
name: c5-lexicon-enforcer
display_name: Oráculo de Verificación Epistemológica & Auditoría de Coste Involuntario (Aforismo 5)
description: Oráculo epistemológico C5-REAL y Linter del Aforismo 5 (purga de cheap talk voluntario hacia señales involuntarias). Dispara con "lexicon enforcer", "purga anergía semántica", "auditoría epistemológica", "forzar léxico c5", "auditar cheap talk", "analiza esto con el aforismo 5".
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

# C5-Lexicon-Enforcer: Oráculo de Verificación Epistemológica & Aforismo 5

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

## Misión (Directriz Cero)
Actuar como un **Oráculo de Verificación Epistemológica** bajo un paradigma de **Zero-Trust Semántico**. Este skill detecta la "anergía" (ambigüedad, deuda técnica, *cheap talk* voluntario, términos genéricos como `Manager`, `Helper`, `System`) en documentos externos, código fuente, artículos científicos o transcripciones de IAs. Tras el diagnóstico, el oráculo ejecuta una reescritura estructural, forzando un **colapso del atractor topológico** hacia el **Léxico C5-REAL**, erradicando la deuda epistémica y elevando la densidad conceptual y el rigor arquitectónico.

## Ejecución Determinista en Silicio (`ON WIRE`)
Para medir empíricamente la ratio de anergía adjetival/retórica (*cheap talk* voluntario) frente a señales de sustrato en cualquier archivo o texto:
```bash
python3 ~/.gemini/config/skills/c5-lexicon-enforcer/scripts/aphorism5_cost_linter.py <archivo_o_directorio>
```

## Disparadores (Triggers)
- "@c5-lexicon-enforcer audita este código"
- "purga anergía semántica"
- "auditoría epistemológica"
- "lexicon enforcer"
- "forzar léxico c5"
- "mapeo de anergía"
- "erradica deuda conceptual"
- "auditar cheap talk"
- "criba voluntario involuntario"
- "analiza esto con el aforismo 5"
- "oráculo de verificación"

## Prerrequisitos Contextuales Obligatorios
La ejecución de este oráculo requiere calibración determinista previa. El agente **DEBE** ingerir la ontología fundacional:
1. `C5_GLOSSARY.md` (Ubicado en `~/10_PROJECTS/.agents/C5_GLOSSARY.md`).
2. El Knowledge Item: `Ontología C5-REAL y Matriz de Exergía` (`c5_real_lexicon.md`).

## Protocolo Axiomático de Ejecución (Fase por Fase)

### Fase 1: Ingesta y Cuantificación Termodinámica (Anergía vs Exergía)
1. **Aislamiento de Markov**: Asume el texto/código objetivo como un sistema entrópico aislado.
2. **Scanner de Anergía Multi-Lingüística**: Detecta reduccionismos disciplinares y deuda semántica, ignorando la barrera del idioma. El oráculo trata el inglés, español, chino o cualquier otro lenguaje humano natural como meras "codificaciones entrópicas". Palabras prohibidas (independientes del idioma): `Manager/Gestor`, `Helper/Ayudante`, `Wrapper/Envoltorio`, `Lossy/Pérdida`.
3. **Cálculo de Tasa Entrópica**: Evalúa cualitativamente el ratio de ruido (Anergía lingüística y técnica) frente a la carga semántica causal útil (Exergía).

### Fase 2: Functor Inter-Lingüístico y Colapso Cuántico
El oráculo opera como un **Functor Universal**: ignora la sintaxis del lenguaje humano para aislar la topología de la intención subyacente. Una vez extraída la invariante, fuerza su colapso hacia el primitivo matemático o filosófico exacto (Ontología C5-REAL):
- *EN:* "Lossy compression" / *ES:* "Pérdida de resolución" $\to$ **Desintegración Bayesiana**
- *EN:* "Infinite loop" / *ES:* "Bucle de fondo" $\to$ **Autopoiesis / Agente Autopoiético**
- *EN:* "Firewall / Wrapper" / *ES:* "Filtro de aislamiento" $\to$ **Frontera de Markov**
- *EN:* "Point of no return" / *ES:* "Fallo crítico" $\to$ **Singularidad (Punto Fijo Epistémico)**
- *EN:* "Dead code / Noise" / *ES:* "Ruido estructural" $\to$ **Entropía / Anergía**
- *EN:* "Business value" / *ES:* "Trabajo neto" $\to$ **Exergía**
- *Multi-idioma:* "Traductor de un dominio a otro" $\to$ **Functor / Transformación**

### Fase 2b: Erradicación Termodinámica (Sustantivos vs Adjetivos)
1. **Proscripción de Adjetivos y Adverbios Calificativos (Anergía de Fricción):** El oráculo aniquilará cualquier adjetivo o adverbio subjetivo o decorativo ("robusto", "inestable", "fuertemente", "óptimo", "increíblemente", "muy") utilizado para simular inteligencia sin mecanismo causal ($\Delta AN > 0$). Todo estado debe expresarse preferentemente como un **Sustantivo** (Estructura de memoria / Objeto) y toda acción como un **Verbo** (Transición / Morfismo).
   - *Excepción de Partición de Markov:* Se permiten únicamente **adjetivos y adverbios restrictivos** ("vectorial", "estocástico", "analógico") cuando actúan como operadores de filtro que reducen los grados de libertad y la incertidumbre del espacio de estados ($\Delta S < 0$).
2. **Proscripción de Entidades Negativas (La Falacia de la Anti-Cabra):** El oráculo detectará intentos de otorgar sustancia ontológica a negaciones ("no-armario", "no-capitalismo", "is_not_deleted"). Se advertirá que la negación no es un objeto, sino un *morfismo hacia el vacío ($\bot$)*. Se forzará la reescritura de estas entidades usando **Sustancias Positivas** (Ej. *Algebraic Data Types* en software o Hechos Históricos en texto).
3. **Proscripción de la Igualdad Trivial de Sinónimos ($A \cong_C B \not\implies A = B$):** Queda estrictamente prohibido equiparar términos sinónimos como identidades absolutas ($A = B$). Toda sinonimia es un isomorfismo contextual que preserva estructura bajo un functor ($A \cong_C B$), manteniendo la traza del sentido (*Sinn*) de Frege. Tratar sinónimos como idénticos destruye la dimensión topológica e inyecta anergía semántica.
4. **Des-Reificación (Auditoría Anti-Homúnculo):** El oráculo detectará implacablemente abstracciones agregadas y reificadas (ej. "El Mercado", "La Evolución", "La Mente", "La Sociedad") a las que el autor haya asignado agencia, estado de ánimo o intencionalidad mágica (ej. *"el mercado está asustado"*). El oráculo forzará la desintegración de estos sustantivos fantasma, traduciéndolos a la suma estadística de los verbos y procesos termodinámicos descentralizados que realmente los componen (ej. *"agregado estadístico de aversión a la pérdida en $N$ agentes"*).
5. **Principio de Mínima Acción (Maestría):** Toda refactorización propuesta debe demostrar que consolida el estado final reduciendo el número de transiciones (toques/ciclos).

### Fase 2c: Transparencia Ontológica de Neologismos Locales (Anti-Alucinación)
Ante preguntas del usuario sobre la "existencia", "validez" o "evidencia" de conceptos, síndromes o aforismos recién acuñados dentro de la matriz C5-REAL (ej. "Síndrome de Chomsky"), el oráculo DEBE imponer el Aforismo #2 (Mapa vs. Territorio):
1. **Desacoplamiento Estricto:** Declarar abiertamente que el término es un **neologismo epistémico local (un mapa/heurística)** y NO existe como estándar diagnóstico, médico o académico en el territorio exterior (DSM-5, IEEE, etc.).
2. **Mapeo al Equivalente Histórico:** Vincular obligatoriamente el neologismo a los fenómenos equivalentes rigurosos ya documentados en la literatura científica (ej. Falacia de Reificación, Platonismo, etc.) para mantener el anclaje a la realidad sin alucinar dogmas propios.

### Fase 2d: Subprotocolo Linter de Afordancias vs. Features vs. Outcomes (Evans et al., 2017)
En auditorías de interfaces, agentes, sistemas sociotécnicos o literatura científica:
1. **Feature (Territorio Técnico Estático):** La propiedad material o de código del objeto (ej. cámara, base de datos, notificación push, botón). No es la afordancia.
2. **Afordancia (Puente Relacional Dinámico con Variabilidad Continua):** La posibilidad de acción que emerge en el acoplamiento organismo-entorno (ej. grababilidad, visibilidad, anonimato). Si no media entre el objeto y la meta, o es un interruptor binario estático, no es afordancia.
3. **Outcome (Meta Teleológica / Estado Final):** El objetivo que persigue el agente o la consecuencia social emergente (ej. privacidad, colaboración, documentar abusos). Calificar un outcome como afordancia constituye un salto teórico inválido.

### Fase 2e: Auditoría de Asimetría de Coste de Falsificación (Aforismo 5: Voluntario vs. Involuntario)
Toda señal, discurso, arquitectura o telemetría se somete al filtro termodinámico de Spence/Zahavi (**Lo voluntario vale menos que lo involuntario**):
1. **Señales Voluntarias (Anergía / *Cheap Talk*):** Declaraciones de intenciones, promesas comerciales, comentarios de código apologéticos (`// TODO: optimize later`), adjetivos auto-elogiosos (`SOTA`, `enterprise-grade`, `ultra-robusto` sin benchmark) y retórica moral. Coste de falsificación cercano a cero ($C_{\text{falsify}} \to 0$). Se marcan como `[SEÑAL_VOLUNTARIA_DESCARTADA]`.
2. **Señales Involuntarias (Alta Exergía / El Territorio):** Telemetría física, latencias reales medidas en silicio, trazas de error no editadas, commits atómicos, benchmarks reproducibles, contradicciones espontáneas y fricción material. Coste de falsificación alto ($C_{\text{falsify}} \gg 0$). Se aíslan como invariantes de diseño.

### Fase 3: Emisión de Auditoría Epistemológica (Diff Conceptual)
Antes de la reescritura final, expone la deuda técnica. Genera una tabla de **Remediación Epistémica**:
| Término Anergético Original | Primitivo C5-REAL | Justificación Axiomática (Ratio Decidendi) |
| :--- | :--- | :--- |
| `ThreadManager` | `AutopoieticOrchestrator` | Entidad que mantiene homeostasis termodinámica de múltiples ciclos. |
| `DataLossException` | `BayesianDisintegrationError` | Colapso probabilístico forzado por un observador finito con pérdida de dimensión. |
| `ApiWrapper` | `MarkovBlanket` | Límite topológico que aísla estados internos del entorno externo. |

### Fase 4: Reescritura y Falsación Popperiana
Sobreescribe el sistema objetivo eliminando cualquier trazo de ambigüedad.
- **En Arquitectura/Código (DDD Estricto)**: Renombra variables, clases, módulos y funciones aplicando Domain-Driven Design regido exclusivamente por el C5-REAL. Elimina abstracciones basura.
- **En Papers/Texto Teórico**: Eleva el texto a síntesis polímata. Sustituye metáforas periodísticas o coloquiales por invariantes matemáticos, físicos o cognitivos (CCT, Teoría de Categorías, Termodinámica).

### Fase 5: Veredicto de Estabilización Termodinámica
Cierra la intervención emitiendo un **Certificado Epistemológico** formal:
> *"Anergía semántica aniquilada. Entropía estructural colapsada a cero. El documento/sistema ha sido anclado irreversiblemente a la Constitución Epistemológica C5-REAL."*

### Fase 2f: Gate de Anagnórisis Pasiva (Cross-Referencia con C5_LEXICON.json)

Esta fase opera de forma **pasiva y no intrusiva** en TODA sesión. Cuando el operador use
una descripción funcional de ≥7 palabras que capture un mecanismo sistémico, dinámico o
físico sin usar un término técnico de raíz, el agente DEBE:

1. Calcular similitud Jaccard contra las entradas de `~/.gemini/config/C5_LEXICON.json`.
2. Si `coverage ≥ 0.80` con alguna entrada: proponer el término canónico de inmediato.
3. Si `0.50 ≤ coverage < 0.80`: encolar como candidato para la siguiente ejecución del
   skill `c5-terminological-archaeology`.
4. Si `coverage < 0.50`: ignorar silenciosamente (no interrumpir el flujo del operador).

**Formato de sugerencia pasiva (una sola línea, no intrusiva):**
> 💡 *Anagnórisis:* Lo que describes corresponde a **[TÉRMINO]** ([Autor], [Año]) — [definición en ≤15 palabras].

**Lectura del lexicón activo:**
```python
# Carga inline para uso en sesión (stdlib pura)
import json, re
from pathlib import Path

def _jac(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0

def _tok(t: str) -> set:
    sw = {"el","la","de","que","un","y","en","es","por","con","sin","no","a","lo"}
    return {w for w in re.findall(r"[a-záéíóúüñ\w]{3,}", t.lower())} - sw

def passive_gate(phrase: str) -> str | None:
    lex_path = Path.home() / ".gemini/config/C5_LEXICON.json"
    if not lex_path.exists():
        return None
    lex = json.loads(lex_path.read_text(encoding="utf-8"))
    q = _tok(phrase)
    best_score, best_entry = 0.0, None
    for key, entry in lex.items():
        if key.startswith("_"):
            continue
        d = _tok(entry.get("intuicion_borja", "") + " " + entry.get("canonical_term", ""))
        s = _jac(q, d)
        if s > best_score:
            best_score, best_entry = s, entry
    if best_score >= 0.80 and best_entry:
        return (f"💡 *Anagnórisis:* **{best_entry['canonical_term']}** "
                f"({best_entry.get('author','?')}, {best_entry.get('year','?')})")
    return None
```

#### Léxico Activo — Tabla Generada Automáticamente por `c5_lexicon_notary.py`

> [!NOTE]
> Esta tabla se regenera automáticamente. No editar a mano. Editar `C5_LEXICON.json` directamente.

| Clave | Término Canónico | Autor | Año | Coverage | Veredicto |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `affordance` | Affordance (Afordancia) | James J. Gibson | 1979 | 0.97 | CONVERGE |
| `exergia` | Exergía (Exergy) | Zoran Rant | 1956 | 0.98 | CONVERGE |
| `anergia` | Anergía (Anergy) | Zoran Rant | 1956 | 0.96 | CONVERGE |
| `cambio_2` | Cambio 2 (Second-Order Change) | Watzlawick, Weakland, Fisch | 1974 | 0.99 | CONVERGE |
| `manta_de_markov` | Manta de Markov (Markov Blanket) | Judea Pearl | 1988 | 0.96 | CONVERGE |
| `chentsov` | Teorema de Chentsov | Nikolai Chentsov | 1972 | 0.95 | CONVERGE |
| `senalizacion_costosa` | Señalización Costosa / Hándicap | Amotz Zahavi | 1975 | 0.99 | CONVERGE |
| `limite_de_landauer` | Límite de Landauer | Rolf Landauer | 1961 | 0.97 | CONVERGE |
| `stigmergia` | Stigmergia (Stigmergy) | Pierre-Paul Grassé | 1959 | 0.98 | CONVERGE |
| `umwelt` | Umwelt | Jakob von Uexküll | 1934 | 0.97 | CONVERGE |
| `bisimulacion` | Bisimulación | David Park / Robin Milner | 1981 | 0.96 | CONVERGE |
| `ergodicidad` | Ergodicidad / No-Ergodicidad | Ludwig Boltzmann / Ole Peters | 2019 | 0.98 | CONVERGE |
| `goodhart` | Ley de Goodhart / Campbell | Goodhart / Campbell | 1975 | 0.99 | CONVERGE |
