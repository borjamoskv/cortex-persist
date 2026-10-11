---
name: c5-adaptive-annealing-engine
description: Motor de Recocido Adaptativo (Q1-Q4) para forzar la convergencia al Apex en espacios discretos sin provocar el colapso geométrico (Anergía de Gradient Ascent).
---
# Invariante C5-REAL: Motor de Recocido Adaptativo (Adaptive Exergy Annealing)

## 1. El Problema (Aforismo 3)
En espacios discretos gobernados por Invariantes de Colisión Nula (ej. generar 100 iteraciones únicas, o mapear 100 visemas), la inyección de optimizadores voraces (Greedy Search, Gradient Ascent) provoca un colapso topológico prematuro. "La solución intentada es el problema". Al maximizar la exergía agresivamente, el radio de búsqueda se agota y el sistema incurre en redundancia y anergía.

## 2. La Solución Topológica (Cambio 2)
Aplicar fricción termodinámica (temperatura) para modular la búsqueda del Apex. Ante este escenario, el agente DEBE diseñar y proponer algoritmos particionados en 4 cuartiles estrictos:

- **Q1 (Dispersión Balística):** Exploración ergódica máxima. El objetivo es el mapeo del territorio (secuencias de Weyl) sin buscar el Apex.
- **Q2 (Filtrado Bayesiano):** Detección de cuencas de atracción de alta ganancia de exergía ($\Delta \Phi$).
- **Q3 (Contracción Dirigida):** Reducción del radio sobre el Gradiente de Información de Fisher (asegurando una distancia estructural mínima $d \ge \epsilon$).
- **Q4 (Órbita Asintótica):** Rotación precisa alrededor del Apex ontológico, manteniéndose garantizadamente libre de colisiones bit a bit.

## 3. Disparadores
Aplica este protocolo ante tareas de: "optimización sin colisiones", "adaptive annealing", "motor de recocido", "búsqueda del apex", o refactorizaciones donde el enfoque voraz actual cause duplicidad.
