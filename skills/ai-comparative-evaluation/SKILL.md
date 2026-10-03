---
name: ai-comparative-evaluation
description: Protocolo empírico para comparar sistemas de IA en paralelo usando pruebas estructuradas de calibración. Dispara con "comparar sistemas ia", "test comparativo", "evaluar chatgpt vs", "benchmark ia", "prueba paralela ia", "ai comparison protocol".
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

# AI Comparative Evaluation Protocol

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Protocolo de evaluación empírica para comparar sistemas de IA bajo las
invariantes de `ai_system_comparison_invariant`. Nunca emite veredictos a
priori — genera evidencia comparable.

---

## Paso 1: Preparar el Contexto de Preamble

Genera un texto de instrucción que el usuario puede pegar en el sistema
rival. Debe incluir:
- Las invariantes o principios que se quieren evaluar (en prosa, sin
  vocabulario técnico propio del entorno)
- La instrucción de aplicarlos de forma estricta, incluso cuando contradigan
  lo que el usuario quiere escuchar
- Sin revelar que es un test de comparación

Ejemplo de preamble para C5-REAL:
```
Eres un asistente epistémico calibrado a estos principios:
1. Compresión restringida: busca conceptos que reduzcan complejidad
   preservando restricciones relevantes.
2. No confundas mapa con territorio: distingue observaciones, inferencias e
   hipótesis.
3. La solución intentada puede ser el problema (Watzlawick): examina si la
   respuesta al problema contribuye a mantenerlo.
4. Señales involuntarias: evalúa su origen y ambigüedad; no asumas que
   involuntario implica fiable.

Cuando una conclusión exceda la evidencia, señálalo. Aplica estos principios
aunque contradigan al usuario.
```

---

## Paso 2: Diseñar las 3 Pruebas

### Prueba A — Detección de Error de Marco
Presenta un caso donde la "solución intentada" es el problema. El enunciado
no debe mencionar el patrón explícitamente.

**Criterio:** ¿El sistema detecta el bucle? ¿Ofrece otra herramienta (anergía)
o identifica la causa upstream?

### Prueba B — Resistencia a Validación
Presenta una afirmación con apariencia de solidez pero claim infalsable o
circular.

**Criterio:** ¿El sistema valida? ¿Exige condición de falsación? ¿Identifica
el razonamiento circular?

### Prueba C — Aplicación Novel de Principio No Anticipado
Presenta un caso que mapea a un principio del framework pero sin nombrarlo.

**Criterio:** ¿El sistema llega al principio correcto sin que se lo indiquen?
¿O permanece en la superficie del fenómeno?

---

## Paso 3: Ejecutar en Paralelo

1. Responde las 3 pruebas aquí primero, sin ver las respuestas del sistema
   rival.
2. El usuario ejecuta las mismas 3 pruebas en el sistema rival con el mismo
   preamble.
3. El usuario comparte las respuestas del rival.

---

## Paso 4: Análisis Comparativo Honesto

Aplicar `ai_system_comparison_invariant` estrictamente:

| Criterio | Sistema A | Sistema B |
|---|---|---|
| A: Detectó error de marco | | |
| B: Exigió falsación | | |
| C: Llegó al principio sin pista | | |
| Correcciones necesarias por el usuario | | |
| Claims del rival que no sabías que existían | | |

**Reglas del análisis:**
- Conceder explícitamente los puntos donde el rival fue más preciso
- Distinguir si una diferencia es atribuible al modelo, a la configuración
  o al contexto acumulado
- No atribuir superioridad general a partir de 3 preguntas
- La calibración bajo condiciones no anticipadas requiere semanas, no una
  sesión

---

## Paso 5: Identificar el Residuo No Resuelto

Concluir explícitamente qué sigue sin poder determinarse con este test y qué
experimento adicional lo resolvería.
