---
name: semantic-mutex-pattern
description: Regla arquitectónica universal para implementar un Mutex Semántico en directivas LLM, previniendo condiciones de carrera entre modos de ejecución excluyentes.
---

# Regla: Diseño de Mutex Semántico (Semantic Mutex Pattern)

Al crear, modificar o diseñar habilidades (Skills) y reglas de ejecución para agentes autónomos (LLMs), se debe aplicar siempre el patrón de **Mutex Semántico** (Axioma Ω4) para eliminar deterministamente las condiciones de carrera (Race Conditions) entre directivas contradictorias en el parser del modelo.

---

## 1. Formalización Lógica & Métrica de Pureza ($\mathcal{P}$)

Sea $\psi$ el prompt de entrada transmitido por el Operador y $\mathcal{C}_k$ el comando desencadenante de la sección crítica (ej. `itera ULTRATHINK`). Definimos la **Función de Pureza Semántica** $\mathcal{P}(\psi, \mathcal{C}_k) \in [0, 1]$:

$$\mathcal{P}(\psi, \mathcal{C}_k) = \begin{cases} 1 & \text{si } \text{clean}(\psi) \equiv \mathcal{C}_k \text{ (con parámetros numéricos opcionales)} \\ 0 & \text{si } \exists \, \text{tokens adicionales } \delta \notin \mathcal{C}_k \text{ en } \psi \end{cases}$$

### Matriz de Transición de Estado

$$\text{Modo}(\psi) = \begin{cases} \text{Atómico (Critical Section / Zero-Rhetoric)} & \text{si } \mathcal{P}(\psi, \mathcal{C}_k) = 1 \\ \text{Compuesto (Dual Fallback / Verbal)} & \text{si } \mathcal{P}(\psi, \mathcal{C}_k) = 0 \end{cases}$$

---

## 2. Identificación de Conflictos de Estado

Existe un conflicto de estado cuando dos o más directivas compiten por la propiedad de la salida o el flujo de ejecución:

| Modo A (Critical Section) | Modo B (Dual / Verbose) | Conflicto Resultante |
| :--- | :--- | :--- |
| Silencio Absoluto (Zero-Rhetoric) | Respuesta Explicativa / Análisis | Colapso del Parser (¿Habla o calla?) |
| Ejecución Atómica de Script | Orquestación Multi-Herramienta | Violación de Contrato de I/O |
| Bloqueo de Contexto Síncrono | Delegación Asíncrona Swarm | Condición de Carrera en BTM |

---

## 3. Plantilla Canónica para SKILL.md

Todo archivo `SKILL.md` que contenga un modo de silencio o ejecución atómica DEBE incluir el siguiente bloque estandarizado:

```markdown
## Modo Atómico vs. Modo Compuesto [MUTEX SEMÁNTICO - Axioma Ω4]

1. **Condición de Entrada Atómica ($\mathcal{P}=1$):**
   - El comando `<COMANDO>` solo activará el **Modo Atómico** si el prompt del usuario consiste de forma **EXCLUSIVA Y AISLADA** en dicho comando.
   - En este modo: Silencio absoluto, cero retórica, ejecución atómica del script objetivo.

2. **Anulación y Fallback ($\mathcal{P}=0$):**
   - Si el prompt contiene NINGUNA otra orden, contexto o consulta (ej. "Resume esto y `<COMANDO>`"), el Modo Atómico QUEDA AUTOMÁTICAMENTE ANULADO.
   - El sistema se conmuta inmediatamente al **Modo Compuesto**, ejecutando la tarea solicitada con respuesta verbal normal y acoplando la ejecución del comando en segundo plano o como sufijo.
```

---

## 4. Checklist de Auditoría C5-REAL (Cero Estocasticidad)

Antes de dar por válida la especificación de una Habilidad, auditar:

- [ ] **Exclusividad Explicitada:** ¿Está la condición de "prompt exclusivo e aislado" declarada sin ambigüedad?
- [ ] **Fallback Definido:** ¿Se especifica exactamente qué ocurre si el prompt es compuesto?
- [ ] **Independencia del Modelo:** ¿La regla depende de la intención interpretada del LLM o de una barrera estructural rígida ($\mathcal{P}=1$ vs $\mathcal{P}=0$)?
- [ ] **Sin Falsos Positivos de Silencio:** ¿Se garantiza que el usuario NUNCA perderá información explicativa cuando haga una pregunta combinada con una directiva física?

---
*Estándar Arquitectónico C5-REAL — Gobernanza Criptográfica & Determinismo Agéntico*

