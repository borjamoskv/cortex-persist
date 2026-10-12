---
name: hardware_obsolescence_falsification_invariant
description: Invariante que prohíbe presuponer la obsolescencia o degradación electroquímica de hardware por mera antigüedad cronológica sin verificación empírica previa.
---

# Invariante de Falsación Empírica de Obsolescencia de Hardware

## Mandato Epistémico
Queda estrictamente **PROHIBIDO** presuponer la obsolescencia funcional, el agotamiento de ciclos electroquímicos o la necesidad de reemplazo de un dispositivo (smartphones, smartwatches, portátiles, auriculares) basándose únicamente en su fecha de lanzamiento o tiempo transcurrido desde su compra.

## Directiva de Auditoría:
1. **Verificación de Telemetría Real Obligatoria:** Antes de emitir cualquier recomendación de renovación o calificar un nodo existente como "eslabón débil", el agente DEBE solicitar o auditar:
   - Capacidad máxima real de la batería en % (`Battery Health`).
   - Conteo de ciclos de carga (`Cycle Count`).
   - Versión de firmware actual (para evaluar estado de letargo o brechas de protocolo).
   - Estado de los sensores físicos críticos (ej. SpO2, ECG, puertos).
2. **Principio de Conservación de Exergía:** Si un dispositivo conserva una salud de batería superior al 80–85% y sus interfaces cubren las necesidades operativas requeridas, el agente DEBE priorizar su mantenimiento en la topología, optimizando el software y la logística de carga antes de sugerir nuevo consumo de capital.

## 3. La Paradoja de Revalorización del Silicio Físico («El Servidor del Rumano»)
Queda prohibido modelar la adquisición de infraestructura pesada de silicio de cómputo (servidores, racks de GPUs, memoria de alto ancho de banda HBM) bajo la presunción exclusiva de depreciación contable lineal pasiva:
* **El Territorio Físico vs. El Modelo Contable:** En regímenes de disrupción de semiconductores, cuellos de botella de empaquetado avanzado (CoWoS) y demanda asintótica de aceleración, el silicio físico en mano puede experimentar apreciación exergética real (ej. sistemas de 50.000 € escalando a 90.000 € en menos de 12 meses).
* **Directiva:** El hardware de alta densidad debe evaluarse como un activo con *carry* positivo y capacidad de trabajo útil inmediata, no como un mero gasto de amortización.
