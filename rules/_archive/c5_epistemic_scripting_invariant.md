# Invariante de Epistemología en Scripting y Mutación (C5-REAL)

## 1. El Mapa no es el Territorio (Falsación Física Obligatoria)
Queda estrictamente prohibido que el agente genere o ejecute scripts Bash de mutación (`mv`, `rm`, `cp`) basados en listas de rutas extraídas de logs, transcripciones de sesiones previas, inferencias de subagentes o cualquier otra forma de "memoria de texto" (el Mapa) **sin inyectar antes una comprobación física directa sobre los inodos del sistema (el Territorio)**.

## 2. Implementación de Frontera (Defensive Scripting)
- Todo bloque de reubicación o borrado condicionado a memoria de IA debe estar protegido por un bloque condicional de comprobación de existencia física, tal como `if [ -e "$FILE" ]; then ... fi`.
- Alternativamente, se exigirá el uso de utilidades robustas de nivel de sistema operativo como `find` o `stat` acopladas a `-exec` para garantizar que la operación destructiva solo ocurra si el nodo físico responde con confirmación de estado, eludiendo la falacia de isomorfismo.

## 3. Cero Confianza en la Trayectoria Parseada
Asumir que un archivo existe porque un subagente forense o de extracción NLP lo ha devuelto en un listado JSON/Markdown se clasifica como **Anergía de Ring-1**. La única verdad termodinámica reside en el disco duro, no en el parser.
