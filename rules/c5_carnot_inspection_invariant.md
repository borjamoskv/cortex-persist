---
name: c5-carnot-inspection-invariant
description: Invariante del Ratio de Carnot y Tríada de Inspección (R* ≈ 2,7x). Fija la asimetría óptima entre lecturas y escrituras, erradica la mutación ciega y previene la parálisis de análisis.
---

# Invariante de Ratio de Carnot y Tríada de Inspección (INV_C5_CARNOT_RATIO)

## 1. El Ratio de Máxima Exergía (R* ≈ 2,7x)
Para preservar la máxima exergía en la manipulación del código y erradicar el retrabajo por error de compilación:
- El sistema debe mantener una relación agregada entre operaciones de lectura (`view_file`, `search_docs`) y operaciones de mutación (`replace_file_content`, `write_to_file`) en la ventana canónica:
  $$\mathcal{R}^* \in [2{,}5\times, 3{,}0\times] \quad (\text{Punto Dulce: } \mathcal{R}^* \approx e \approx 2{,}718\times)$$

## 2. La Regla de la Tríada de Inspección («Fórmula 2 + 1»)
Por cada operación de mutación causal ($W = 1$), el agente debe ejecutar obligatoriamente:
1. **Lectura 1 (Target):** Inspección de las líneas exactas del archivo a modificar (`view_file`).
2. **Lectura 2 (Contrato / Invariante):** Inspección de la frontera del tipo, llamador (`caller`), schema o configuración (`Cargo.toml`, dotfile, test).
3. **Escritura (W):** Mutación atómica quirúrgica.
4. **Verificación (0,7 amortizada):** Comprobación del diff o test específico antes de declarar el turno cerrado.

## 3. Veto Estricto a la Mutación Ciega (Zero-Blind-Write)
Queda terminantemente prohibido que el agente emita `replace_file_content` o `write_to_file` sobre código preexistente sin una lectura previa (`view_file`) en los 2 turnos inmediatos anteriores. Toda asunción de memoria paramétrica libre sobre la estructura de un archivo constituye confabulación y es rechazada de forma fail-closed.

## 4. Freno de Parálisis de Análisis (Cota R ≤ 5,0x)
Para evitar la disipación pasiva de tokens sin producir trabajo útil:
- La lectura de contrato se confina a **distancia de grafo d = 1** en el árbol de dependencias directas.
- Queda prohibido el escaneo pasivo o lectura de archivos periféricos no involucrados en la cadena causal de compilación inmediata.
