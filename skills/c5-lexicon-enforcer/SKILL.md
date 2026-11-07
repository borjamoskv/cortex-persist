---
name: c5-lexicon-enforcer
display_name: Oráculo de Verificación Epistemológica & Auditoría de Coste Involuntario
  (Aforismo 5)
description: Oráculo epistemológico C5-REAL y Linter del Aforismo 5 (purga de cheap
  talk voluntario hacia señales involuntarias).
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

# c5-lexicon-enforcer

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-epistemic-thermodynamics/references/modules/c5-lexicon-enforcer/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.

### Fase 2f: Gate de Anagnórisis Pasiva (Cross-Referencia con C5_LEXICON.json v1.1)
Cuando el operador use una descripción funcional en sesión, comparar contra `~/.gemini/config/C5_LEXICON.json`. Sugerir el término canónico distinguiendo siempre qué establece la literatura primaria (`canonical_claim`) y cuál es el salto o extensión propia (`unproven_leap`):

> 💡 **Detección pasiva de anagnórisis:** Lo que describes se relaciona con **[TÉRMINO]** ([Autor], [año]) [Relación: `CONVERGE | PARTIAL | ANALOGY | EXTENSION | DIVERGE`]. Literatura: [canonical_claim]. Límite/Salto: [unproven_leap].

#### Léxico Auditado v1.1 (generado automáticamente — no editar a mano)

| Clave | Término Canónico | Autor (Año) | Relación (`mapping.type`) | Estatus Epistémico | Prioridad Temporal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `affordance` | Affordance (Afordancia) y Signifier (Significante) | James J. Gibson / Donald A. Norman (1979) | `PARTIAL` | `SUPPORTED` | No verificada |
| `exergia` | Exergía (Exergy) | Zoran Rant (1956) | `ANALOGY` | `PROVISIONAL` | No verificada |
| `anergia` | Anergía (Anergy) | Zoran Rant (1956) | `ANALOGY` | `PROVISIONAL` | No verificada |
| `cambio_2` | Cambio 2 (Second-Order Change) | Paul Watzlawick, John H. Weakland, Richard Fisch (1974) | `CONVERGE` | `SUPPORTED` | No verificada |
| `manta_de_markov` | Manta de Markov (Markov Blanket) | Judea Pearl / Karl Friston (1988) | `ANALOGY` | `PROVISIONAL` | No verificada |
| `chentsov` | Teorema de Chentsov (Fisher-Rao Metric Uniqueness) | Nikolai N. Chentsov (Čencov) / L. L. Campbell (1972) | `ANALOGY` | `PROVISIONAL` | No verificada |
| `senalizacion_costosa` | Señalización Costosa / Principio del Hándicap (Costly Signaling / Handicap Principle) | Amotz Zahavi / Alan Grafen / Michael Spence (1975) | `PARTIAL` | `SUPPORTED` | No verificada |
| `limite_de_landauer` | Principio / Límite de Landauer (Landauer's Principle) | Rolf Landauer (1961) | `DIVERGE` | `SCOPE_REDUCED` | Verificada (SHA-256) |
| `stigmergia` | Stigmergia (Stigmergy) | Pierre-Paul Grassé / Francis Heylighen (1959) | `CONVERGE` | `SUPPORTED` | No verificada |
| `umwelt` | Umwelt (Mundo Perceptual Subjetivo) | Jakob von Uexküll (1934) | `ANALOGY` | `PROVISIONAL` | No verificada |
| `bisimulacion` | Bisimulación (Bisimulation) | David Park / Robin Milner (1981) | `DIVERGE` | `SCOPE_REDUCED` | No verificada |
| `ergodicidad` | Ergodicidad y Ruptura de Ergodicidad (Non-Ergodicity) | Ludwig Boltzmann / George D. Birkhoff / Ole Peters (2019) | `EXTENSION` | `SUPPORTED` | No verificada |
| `goodhart` | Ley de Goodhart / Ley de Campbell / Paráfrasis de Strathern | Charles Goodhart / Donald T. Campbell / Marilyn Strathern (1975) | `CONVERGE` | `SUPPORTED` | No verificada |
| `direct_manipulation` | Manipulación Directa (Direct Manipulation) | Ben Shneiderman / Edwin L. Hutchins, James D. Hollan, Donald A. Norman (1982) | `PARTIAL` | `SUPPORTED` | No verificada |
| `deep_modules` | Módulos Profundos (Deep Modules vs. Shallow Modules) | John Ousterhout (2018) | `EXTENSION` | `SUPPORTED` | No verificada |
| `gender_equality_paradox` | Paradoja de la Igualdad de Género (Gender-Equality Paradox) | Gijsbert Stoet, David C. Geary / Armin Falk, Johannes Hermle / Sarah S. Richardson et al. (2018) | `DIVERGE` | `CHALLENGED` | No verificada |
| `lemons_problem` | Problema de los Limones (Akerlof) vs. El Marketing de los Limones (BJR-ATLAS-0158) | George A. Akerlof / Phillip Nelson / Michael R. Darby & Edi Karni (1970) | `DIVERGE` | `PROVISIONAL` | No verificada |
| `psychological_reactance` | Reactancia Psicológica (Psychological Reactance) y Efecto Cobra | Jack W. Brehm / Robert K. Merton / Horst Siebert (1966) | `PARTIAL` | `SUPPORTED` | No verificada |
| `transient_hypofrontality` | Hipótesis de Hipofrontalidad Transitoria, Estado de Flujo y Wu Wei | Arne Dietrich / Mihaly Csikszentmihalyi (2003) | `DIVERGE` | `SCOPE_REDUCED` | No verificada |
| `galls_law` | Ley de Gall (Gall's Law / Systemantics) | John Gall (1975) | `CONVERGE` | `SUPPORTED` | No verificada |
| `dunning_kruger` | Efecto Dunning-Kruger (Dunning-Kruger Effect) | Justin Kruger, David Dunning / Joachim I. Krueger, Ross A. Mueller (1999) | `DIVERGE` | `CHALLENGED` | Verificada (SHA-256) |
| `simulacra_hyperreality` | Simulacro e Hiperrealidad (Simulacra and Hyperreality) | Jean Baudrillard (1981) | `ANALOGY` | `PROVISIONAL` | Verificada (SHA-256) |
| `sovereign_interrogation_decalogue` | Variedad Requerida y Sorpresa Informacional vs. El Decálogo de Interrogación Soberana (BJR-ATLAS-0155) | W. Ross Ashby / Claude E. Shannon (1956) | `EXTENSION` | `PROVISIONAL` | Verificada (SHA-256) |
| `question_extinction_theorem` | Estados Inválidos Irrepresentables (Make Illegal States Unrepresentable) y Ley de Goodhart vs. El Teorema de Extinción de la Pregunta (BJR-ATLAS-0159) | C. A. R. Hoare / Charles Goodhart / Yaron Minsky (1969) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
