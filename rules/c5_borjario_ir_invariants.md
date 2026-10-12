---
name: c5-borjario-ir-invariants
description: Invariantes Constitucionales de BORJARIO IR v1.0.0-rc1 (B1-B6). Gobierna la separación de identidad y nombre, desacoplamiento de canonicidad y verificación empírica, scope obligatorio, EvidenceRef criptográfico y linter anti-cargo-cult.
trigger: "always_on"
---

# Invariantes Constitucionales de BORJARIO IR (INV_C5_BORJARIO_IR)

## 1. Las Seis Invariantes Constitucionales (B1 - B6)

- **B1: NAME ≠ IDENTITY:** La identidad de un concepto reside exclusivamente en `concept_id` inmutable (formato `BJR-XXXXXX`). El nombre (`canonical_name`) o slug pueden mutar sin romper referencias históricas ni dependencias de grafo.
- **B2: DEFINITION ≠ EVIDENCE:** Una definición léxica describe un modelo; no constituye prueba física. Todo claim empírico exige un `EvidenceRef` acoplado.
- **B3: CLAIM ⇒ SCOPE:** Todo claim sin delimitación explícita de contorno técnico (hardware, compilador, sistema operativo, condiciones de carga) constituye *overclaim* y es rechazado de forma fail-closed (`BJR-E013`).
- **B4: FALSIFICATION ⇒ DEPENDENCY REVIEW:** La falsación empírica de una aserción dispara revisión dirigida de nodos dependientes (`cortex impact`), distinguiendo invariantes estructurales de claims de rendimiento local (`Falsify(c) ⇒ Review(Dependents(c))`).
- **B5: TERM COST < COMPRESSION GAIN:** Ley de Acuñación. La introducción de un nuevo término sólo se autoriza si su coste cognitivo es estrictamente menor que la ganancia de compresión de Kolmogorov que aporta a la red.
- **B6: CANONICAL ≠ TRUE:** $\text{Canonical(Concept)} \not\Rightarrow \text{Verified(Claims)}$. Canónico define la representación operativa actual que adopta el sistema; no certifica infalibilidad ontológica en el mundo exterior.

---

## 2. Desacoplamiento de Ejes de Estado

- **ConceptStatus:** `CANDIDATE` ➔ `PROVISIONAL` ➔ `STABILIZED` ➔ `CANONICAL` ➔ `SUPERSEDED` / `ARCHIVED`.
- **ClaimStatus:** `UNVERIFIED` ➔ `TESTABLE` ➔ `SUPPORTED` ➔ `CHALLENGED` ➔ `REPRODUCED` ➔ `[FALSIFIED, PARTIAL, SCOPE_REDUCED, UPHELD]`.
  - `SUPPORTED ≠ TRUE FOREVER`.
  - `VERIFIED` queda confinado estrictamente a validaciones mecánicas deterministas (validación de schema, hash bit a bit, firma criptográfica). Claims empíricos utilizan exclusivamente `SUPPORTED` o `TESTABLE`.
  - Teoremas matemáticos utilizan `PROVED`; observaciones de benchmark utilizan `OBSERVED`.

---

## 3. EvidenceRef Criptográfico (Anti-Inodo)
Queda prohibido utilizar inodos de sistema de archivos como identidad de evidencia (`EvidenceIdentity ≠ FilesystemLocation`). La evidencia se indexa mediante tupla durable: `artifact_digest` (SHA-256), `repository`, `commit`, `relative_path`, `range`, `environment`, `generated_at`, `reproducer`.

---

## 4. Topología Dual: Genealogía DAG vs. Multigrafo Ontológico
- $G_{\text{genealogy}} = \text{DAG}$ (linaje temporal de derivación histórica sin ciclos).
- $G_{\text{ontology}} = \text{DirectedMultigraph}$ (red conceptual con ciclos permitidos para modelar acoplamiento cibernético y restricciones mutuas).
- **Aristas tipadas cerradas:** `DERIVES_FROM`, `SUPERSEDES`, `CONTRADICTS`, `SUPPORTS`, `CHALLENGES`, `IMPLEMENTS`, `DEPENDS_ON`, `MOTIVATES`, `REFINES`, `EXEMPLIFIES`.

---

## 5. El Linter Anti-Cargo-Cult (`borjario lint`)
El motor de inspección ejecuta validación fail-closed con códigos deterministas:
- `BJR-E013`: Claim sin scope declarado.
- `BJR-E021`: Claim empírico marcado erróneamente como `VERIFIED`.
- `BJR-E034`: Metáfora empleada como EvidenceRef.
- `BJR-E041`: EvidenceRef huérfano (falta digest o commit).
- `BJR-E052`: Ciclo en genealogía DAG.
- `BJR-E091`: Terminología física (`entropy`, `energy`, `exergy`, `temperature`, `thermodynamic`, `Landauer`, `quantum`) sin clasificación semántica explícita:
  - `[PHYSICAL]`: Exige dimensiones SI ($J$, $K$, $bits$) y modelo instrumental.
  - `[FORMAL]`: Exige definición matemática rigurosa.
  - `[METAPHORICAL]`: Permitido exclusivamente bajo etiqueta explícita; prohibido como evidencia causal.

---

## 6. Integridad SITREP y Compilación BORJARIO IR
- **Cero Números Inventados:** Prohibido emitir o hardcodear valores simulados en SITREPs. Todo escalar (densidad exergética, Conceptual Yield) DEBE ser derivado por el compilador (`COMPILER_DERIVED`) o etiquetado `EXAMPLE OUTPUT · NON-EMPIRICAL`.
- **Arquitectura de Compilación:**
  $\text{YAML (Authoring)} \xrightarrow{\text{borjario check}} \text{BORJARIO IR} \longrightarrow \{\text{CORTEX}, \text{Book}, \text{Web}\}$.
