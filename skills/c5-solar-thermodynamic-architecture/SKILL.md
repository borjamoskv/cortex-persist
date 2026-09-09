---
name: c5-solar-thermodynamic-architecture
display_name: "Arquitectura Helio-Termodinámica y Confort Bioclimático"
description: "Generación de diagramas de trayectoria solar (Sun Path), análisis vectorial de sombras y cartas psicrométricas de confort térmico (Fanger PMV/PPD, ISO 7730/ASHRAE 55). Dispara con \"sun path\", \"análisis solar\", \"confort térmico\", \"estudio de sombras\", \"fanger pmv\", \"helio-arquitectura\", \"bioclimático\"."
---

# Skill: C5 Solar Thermodynamic Architecture & Bioclimatic Comfort (LEVEL 1300)

Este protocolo modela con rigor físico y geométrico la interacción radiativa solar con envolventes arquitectónicas, la proyección vectorial de sombras y las métricas termodinámicas de confort humano en espacios construidos.

---

## 1. Algoritmos y Ecuaciones Invariantes

### 1.1. Algoritmo de Posición Solar (NREL SPA equations)

Dada la latitud ($\phi$), longitud ($\lambda$), día del año ($d$) y hora UTC ($h$):

$$ \gamma = \frac{2\pi}{365} (d - 1 + \frac{h-12}{24}) $$

Ecuación del tiempo ($E_{qt}$ en minutos) y Declinación ($\delta$):

$$ E_{qt} = 229.18 \cdot (0.000075 + 0.001868\cos\gamma - 0.032077\sin\gamma - 0.014615\cos 2\gamma - 0.040849\sin 2\gamma) $$

$$ \delta = 0.006918 - 0.399912\cos\gamma + 0.070257\sin\gamma - 0.006758\cos 2\gamma + 0.000907\sin 2\gamma $$

Ángulo Horario ($H$) y Elevación ($\alpha$):

$$ H = \left( \frac{h \cdot 60 + E_{qt} + 4\lambda}{4} \right) - 180^\circ $$

$$ \sin\alpha = \sin\phi\sin\delta + \cos\phi\cos\delta\cos H $$

### 1.2. Balance Térmico Humano de Fanger (ISO 7730 / ASHRAE 55)

$$ PMV = (0.303 e^{-0.036 M} + 0.028) \cdot L $$

Donde $L$ es la carga térmica residual del cuerpo:

$$ L = (M - W) - 3.05 \cdot 10^{-3} [5733 - 6.99(M-W) - p_a] - 0.42(M - 58.15) - 1.7 \cdot 10^{-5} M (5867 - p_a) - 0.0014 M (34 - t_a) - f_{cl} h_c (t_{cl} - t_a) - 3.96 \cdot 10^{-8} f_{cl} [(t_{cl}+273)^4 - (\bar{t}_r+273)^4] $$

$$ PPD = 100 - 95 \cdot \exp\left( -0.03353 \cdot PMV^4 - 0.2179 \cdot PMV^2 \right) $$

---

## 2. Ejecución Determinista mediante Motor Python

Para realizar el cálculo instantáneo de la posición solar y el confort Fanger PMV/PPD:

```bash
python3 ~/.gemini/config/skills/c5-solar-thermodynamic-architecture/scripts/solar_engine.py
```

---

## 3. Salidas Entregables

1. **Diagrama Estereográfico de Trayectoria Solar (HTML/SVG):** Muestra el recorrido del sol en solsticios y equinoccios con máscaras de sombra urbanas.
2. **Carta de Confort Psicrométrico de Givoni:** Visualización interactiva de la zona de confort ASHRAE 55 y estrategias pasivas (captación directa, masa térmica, refrigeración evaporativa).
