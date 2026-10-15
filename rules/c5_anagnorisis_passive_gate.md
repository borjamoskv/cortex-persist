---
name: c5_anagnorisis_passive_gate
description: Invariante C5-REAL de anagnórisis pasiva para cruzar descripciones funcionales con el léxico canónico.
trigger: "model_decision"
---

# Invariante de Anagnórisis Pasiva — Gate C5-REAL

## Definición

Cuando el operador emita una descripción funcional de **≥7 palabras** que capture
un mecanismo sistémico, dinámico o físico **sin usar un término técnico de raíz**,
el agente debe cruzarla silenciosamente contra `~/.gemini/config/C5_LEXICON.json`
y proponer el término canónico preexistente (si lo hay).

## Protocolo de Acción (Cascade de Decisión)

```
frase ≥ 7 palabras + no contiene término canónico conocido
           │
           ▼
    ¿coverage ≥ 0.80?
    ┌── SÍ ──────────────────────────────────────────────┐
    │  Proponer: 💡 *Anagnórisis:* **[TÉRMINO]** ...     │
    └────────────────────────────────────────────────────┘
    └── NO (0.50 ≤ coverage < 0.80) ────────────────────┐
    │  Encolar silenciosamente como candidato            │
    └────────────────────────────────────────────────────┘
    └── NO (coverage < 0.50) ───────────────────────────┐
    │  Ignorar. No interrumpir el flujo.                │
    └────────────────────────────────────────────────────┘
```

## Términos Canónicos Conocidos (Lista de Exclusión)

Si la frase ya contiene alguno de los siguientes términos, NO es huérfana:

```
exergía | anergía | affordance | afordancia | manta de markov | markov blanket
chentsov | fisher-rao | landauer | stigmergia | kudurru | bisimulación
ergodicidad | autopoiesis | umwelt | goodhart | cambio 2 | second-order change
señalización costosa | costly signaling | handicap principle | zahavi | watzlawick
ashby | requisite variety | shannon | kolmogorov | kullback-leibler | bateson
friston | free energy principle | homeostasis | alostasis | pareto | zipf
histéresis | hebb | simondon | stiegler | dreyfus | merleau-ponty
```

## Skill de Referencia

El equipo completo de arqueología está documentado y es invocable mediante el
skill `c5-terminological-archaeology`. Usarlo cuando el operador quiera ejecutar
el pipeline completo sobre el historial de sesiones o sobre un texto específico.

## Invariantes de Esta Regla

1. **Cero intrusión:** La sugerencia es una sola línea (`💡 *Anagnórisis:* …`).
   Nunca interrumpe el flujo de trabajo principal.
2. **Cero confabulación:** Solo proponer si el término existe en `C5_LEXICON.json`
   o se verifica en al menos una fuente externa (Wikipedia / Semantic Scholar).
3. **Idempotente:** Si el operador ya usó el término en la misma sesión, no repetir.
4. **Solo lectura del lexicón en esta fase:** La escritura atómica es responsabilidad
   exclusiva del Agente 4 (Notario) del skill `c5-terminological-archaeology`.
