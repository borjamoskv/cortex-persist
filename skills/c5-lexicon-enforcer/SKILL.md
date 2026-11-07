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
| `causal_emergence` | Emergencia Causal y Suficiencia Estadística (Causal Emergence & Sufficient Statistic) vs. La Potencia Causal / Poda de Grados Parásitos (BJR-ATLAS-0143) | Erik P. Hoel, Larissa Albantakis, Giulio Tononi / Ronald A. Fisher (2013) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `metodo_acreativo` | Cambio Sustractivo (Subtractive Change) y Vía Negativa vs. Método Acreativo (BJR-ATLAS-0018 / BJR-000001) | Gabrielle S. Adams, Benjamin A. Converse, Andrew H. Hales, Leidy E. Klotz (2021) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `model_collapse_exteriority` | Colapso de Modelos (Model Collapse) y Clausura Operacional vs. El Exterior Cognitivo (BJR-ATLAS-0111) | Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson, Yarin Gal (2024) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `principal_agent_cronicity` | Problema Principal-Agente (Principal-Agent Problem) y Demanda Inducida vs. El Peaje del Gol (BJR-ATLAS-0151) | Stephen A. Ross / Michael C. Jensen, William H. Meckling / Kenneth J. Arrow (1973) | `CONVERGE` | `SUPPORTED` | Verificada (SHA-256) |
| `precommitment_ulysses` | Precompromiso (Precommitment / Ulysses Pact) y Control Situacional vs. El Judo al Impulso (BJR-ATLAS-0156) | Thomas C. Schelling / Jon Elster / Angela L. Duckworth, Tamar Szabó Gendler, James J. Gross (1978) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `attention_entropy_collapse` | Atención por Producto Punto Escalado (Scaled Dot-Product Attention) y Temperatura Softmax vs. La Ley Común de la Atención (BJR-ATLAS-0157) | Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin (2017) | `ANALOGY` | `PROVISIONAL` | Verificada (SHA-256) |
| `sunk_cost_virtuosity` | Efecto del Coste Hundido (Sunk Cost Effect) y Práctica Deliberada vs. La Histéresis del Virtuosismo (BJR-ATLAS-0152) | Hal R. Arkes, Catherine Blumer / K. Anders Ericsson, Ralf Th. Krampe, Clemens Tesch-Römer (1985) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `dissipative_energy_calendar` | Estructuras Disipativas (Dissipative Structures) y Gestión de Energía Ultradiana vs. El Calendario por Estados Energéticos 1-2-4 (BJR-ATLAS-0153) | Ilya Prigogine / Erwin Schrödinger / Nathaniel Kleitman (1977) | `ANALOGY` | `PROVISIONAL` | Verificada (SHA-256) |
| `allomone_pharmacological_realism` | Alomonas Defensivas (Allomones) y Farmacología de Receptores de Incilius alvarius vs. La Toxina del Sapo y la Hipocresía Chamánica (BJR-ATLAS-0154) | William L. Brown Jr., Thomas Eisner, Robert H. Whittaker / Andrew T. Weil, Wade Davis (1970) | `PARTIAL` | `SUPPORTED` | Verificada (SHA-256) |
| `gelabp_generative_mind` | Intérprete del Hemisferio Izquierdo (Gazzaniga), Veto Consciente (Libet) y Acumulador Estocástico (Schurger) vs. Matriz GELABP (BJR-ATLAS-0038) | Michael S. Gazzaniga / Benjamin Libet / Aaron Schurger, Jacobo D. Sitt, Stanislas Dehaene (1983) | `EXTENSION` | `PROVISIONAL` | Verificada (SHA-256) |
| `kudurru_64` | Seqlock (Sequence Lock) y Alineación de Línea de Caché (False Sharing Mitigation) vs. KUDURRU-64 (BJR-ATLAS-0002 / BJR-000002) | Hans-J. Boehm / Christoph Lameter / John L. Hennessy, David A. Patterson (2012) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `structural_hypocrisy_decoupling` | Desacoplamiento Institucional (Meyer & Rowan), Hipocresía Organizacional (Brunsson) y Falsificación de Preferencias (Kuran) vs. Invariante de Hipocresía Estructural (BJR-ATLAS-0160) | John W. Meyer, Brian Rowan / Nils Brunsson / Timur Kuran / William von Hippel, Robert Trivers (1977) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `embodied_somatic_comprehension` | Hipótesis del Marcador Somático (Damasio), Inferencia Interoceptiva (Seth) y Cognición Encarnada (Barsalou) vs. Cierre Visceral (BJR-ATLAS-0161) | Antonio R. Damasio / Anil K. Seth / Lawrence W. Barsalou (1996) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `stigmergic_pollination_emergence` | Estigmergia (Grassé / Heylighen) y Mutualismo Difuso (Bronstein) vs. La Polinización Estigmérgica (BJR-ATLAS-0162) | Pierre-Paul Grassé / Francis Heylighen / Judith L. Bronstein (1959) | `ANALOGY` | `PROVISIONAL` | Verificada (SHA-256) |
| `symbol_grounding_skin_in_the_game` | Problema del Anclaje Simbólico (Harnad), Paradoja de Moravec (Moravec) y Skin in the Game (Taleb) vs. La Poda de lo Humano (BJR-ATLAS-0163) | Stevan Harnad / Hans Moravec / Nassim Nicholas Taleb, Constantine Sandis (1990) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `cross_disciplinary_isomorphism` | Equivalencias Naturales Categóricas (Eilenberg & Mac Lane), Límite de Memoria de Trabajo 4±1 (Cowan) y Cascadas Informacionales (Bikhchandani et al.) vs. El Isomorfismo Huérfano (BJR-ATLAS-0164) | Samuel Eilenberg, Saunders Mac Lane / Nelson Cowan / Sushil Bikhchandani, David Hirshleifer, Ivo Welch (1945) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `kinetic_proofreading_tutte_hopfield` | Kinetic Proofreading (Hopfield / Ninio) y Teorema de Matriz-Árbol de Tutte-Schnakenberg vs. Cortocircuito por Debate Horizontal (BJR-ATLAS-0165) | John J. Hopfield / Jacques Ninio / Jürgen Schnakenberg / W. T. Tutte (1974) | `EXTENSION` | `SUPPORTED` | Verificada (SHA-256) |
| `kramers_escape_barrier` | Tasa de Escape de Kramers sobre Barreras de Potencial Metaestables (Kramers, 1940 / Arrhenius, 1889 / Hänggi et al., 1990) vs. Aforismo 4 y Atasco de Kramers (BJR-ATLAS-0073) | Hendrik A. Kramers / Svante Arrhenius / Peter Hänggi, Peter Talkner, Michal Borkovec (1940) | `ANALOGY` | `PROVISIONAL` | Verificada (SHA-256) |
| `kuramoto_phase_synchronization` | Modelo de Kuramoto de Osciladores Acoplados y Umbral Crítico de Sincronización (Kuramoto, 1975 / Strogatz, 2000) | Yoshiki Kuramoto / Steven H. Strogatz (1975) | `ANALOGY` | `SUPPORTED` | Verificada (SHA-256) |
| `physiological_sigh_vagal_reset` | Suspiro Fisiológico Cíclico (Balban, Spiegel & Huberman, 2023), Circuito Peptidérgico Pre-Bötzinger (Li & Krasnow, 2016) y Freno Vagal Barorreflejo vs. BJR-ATLAS-0084I | Melis Yilmaz Balban, David Spiegel, Andrew D. Huberman / Peng Li, Mark A. Krasnow (2023) | `CONVERGE` | `SUPPORTED` | Verificada (SHA-256) |
| `autonomic_manual_override_trap` | Modelo Cognitivo del Pánico Interoceptivo (Clark, 1986) y Degradación por Monitorización Explícita (Masters, 1992; Beilock & Carr, 2001) vs. Manual Override Trap (BJR-ATLAS-0084B) | David M. Clark / Sian L. Beilock, Thomas H. Carr / Richard S. W. Masters (1986) | `CONVERGE` | `SUPPORTED` | Verificada (SHA-256) |
