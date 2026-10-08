# Invariante del Límite Termodinámico de la Observación (INV_C5_OBSERVATION_LIMIT)

## 1. El Costo Físico del Observador (Falsación del Furtivismo Absoluto)
Queda matemáticamente falsada la noción de "observación transparente" o "sandboxing indetectable" (sea en Ring-0, Ring-1, o vía hardware virtualization). Toda instrumentación, emulación o *Record & Replay* inyecta inevitablemente fricción termodinámica (latencia o contención) en el sistema. Queda estrictamente prohibido que el agente afirme o asuma que una herramienta de análisis dinámico es inherentemente "indetectable" frente a un malware SOTA moderno.

## 2. Los Tres Cuellos de Botella de la Evasión Térmica
Al auditar, diseñar o debatir sobre arquitecturas de aislamiento (Sandboxes, Hipervisores, Análisis Forense), el agente DEBE modelar siempre los siguientes tres vectores de ruptura:
- **Exhaustión Entrópica (Límite de Escritura / Shannon):** Un adversario bombardea la CPU con eventos no deterministas (Hardware RNG, I/O masivo). Si el observador necesita grabar esto para garantizar determinismo, el bus colapsa, revelando la instrumentación por *lag*.
- **Asfixia Concurrente (Data Races vs. Determinismo):** Mantener el determinismo en entornos multinúcleo reales obliga a serializar hilos. El adversario puede medir la discrepancia asimétrica entre el número de núcleos lógicos reportados y el rendimiento serializado real.
- **Fugas de Manta de Markov (GPU / DMA):** La CPU no es el universo. Si el payload se descifra térmicamente en los Shaders de la GPU o viaja a través de acceso directo a memoria (DMA), el hipervisor de CPU queda sordo y ciego. Todo Sandbox propuesto debe declarar explícitamente su postura sobre IOMMU (VT-d) y VRAM.
