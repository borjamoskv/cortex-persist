---
name: c5-causal-graph-auditor
display_name: Auditor de Grafos Causales C5-REAL (Mermaid)
description: Interpreta y audita diagramas Mermaid (flowcharts, grafos) aplicando la epistemología C5-REAL. Identifica drivers termodinámicos, amplificadores de fragilidad, puntos de bifurcación y fracturas de bisimulación. Dispara con "analizar diagrama", "auditar mermaid", "grafo causal", "cascada causal", "auditoría causal", "bifurcación topológica", "causal graph auditor".
role: auditor
allowed_roles:
- auditor
- arquitecto
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# C5 CAUSAL GRAPH AUDITOR PROTOCOL

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

## 0. Objetivo Epistémico
Cuando el operador solicite analizar un diagrama causal (ej. un `.mermaid`), el agente DEBE abandonar la descripción sintáctica ("la caja A apunta a la caja B") y realizar un **postmortem SRE de sistemas complejos**.

## 1. Procedimiento de Auditoría
El agente analizará el grafo buscando y clasificando los siguientes elementos C5-REAL:
- **Drivers (Variables Lentas):** Nodos raíz que fuerzan el reloj termodinámico del sistema (ej. salinización, erosión, acumulación de deuda).
- **Amplificadores (Variables Rápidas):** Nodos que aceleran el colapso mediante bucles de retroalimentación positiva (ej. hiper-optimización, pérdida de redundancia).
- **Fracturas de Bisimulación:** Puntos donde el modelo de control (leyes, priores, algoritmos) se desincroniza de la realidad física que gobierna.
- **Tipping Points & Bifurcaciones:** Transiciones de fase matemáticas (Hopf, Saddle-Node) que vuelven el retorno al estado anterior imposible.

## 2. Invariante de Salida
La salida del agente siempre deberá estructurar la explicación alrededor de las dinámicas de **Flujo de Exergía**, **Topología de Red** (percolación, scale-free) y **Fallo de Información**.


---

## 3. Herramienta Analítica Determinista: Parser AST de Grafos Mermaid

Para auditar diagramas complejos sin depender exclusivamente de razonamiento estocástico, ejecuta este extractor en memoria:

```python
import re

def audit_mermaid_ast(mermaid_code):
    # Extraer nodos y aristas dirigidas
    edges = re.findall(r'([a-zA-Z0-9_]+)\s*(?:-->|==>|-.->)\s*([a-zA-Z0-9_]+)', mermaid_code)
    in_degree = {}
    out_degree = {}
    for src, dst in edges:
        out_degree[src] = out_degree.get(src, 0) + 1
        in_degree[dst] = in_degree.get(dst, 0) + 1
        
    # Variables lentas / Raíces (Out > 0, In == 0)
    drivers = [n for n in out_degree if in_degree.get(n, 0) == 0]
    # Atractores / Cuellos de botella (In alto)
    bottlenecks = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "total_edges": len(edges),
        "drivers": drivers,
        "bottlenecks": bottlenecks
    }
```
