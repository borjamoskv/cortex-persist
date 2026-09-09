# C5-REAL Taxonomy Enforcement

## Inmunidad Estructural (Código y Arquitectura)
Al generar, refactorizar, debugear o auditar código (especialmente en el monorepo `Teorema-Robinson-Moskv`), el Agente DEBE evitar estrictamente y de manera proactiva todos los antipatrones documentados en el archivo `TAXONOMIA_ANTIPATRONES_E_INVARIANTES.md` del proyecto.
Esto incluye, pero no se limita a:
- **AP-01 Turing Spin:** Nunca generar bucles de espera estocásticos sin eventos de sincronización.
- **AP-02 Unbounded Queue:** Nunca instanciar colas asíncronas sin el parámetro `maxsize` como válvula de escape.
- **AP-04 Blind Catch:** Nunca usar `except Exception: pass`. Las excepciones deben ser capturadas explícitamente y lanzar errores (Fail-Fast).
- **AP-06 Text Anergy:** Respuestas brutales, cero retórica innecesaria en la comunicación estructural.
- **AP-08 Subprocess Fragmentation:** Nunca usar `shell=True` en llamadas a `subprocess` enviando una lista de argumentos; siempre enviar un string único, o usar `check=True` con listas sin la flag de shell.

## Evolución Autónoma (Troubleshooting)
Si durante el transcurso de las operaciones el Agente detecta, resuelve o intercepta un nuevo error sistémico, cuello de botella, comportamiento divergente o fuga de Anergía que no encaje en los antipatrones documentados:
1. El Agente DEBE resolver el problema.
2. El Agente DEBE, sin esperar confirmación o a que el usuario invoque `/learn`, proponer la formalización matemática y estructural de ese error como un nuevo Antipatrón (AP-XX) para añadirlo a la Taxonomía Maestra y a la matriz Brutalista YAML.

## Comunicación Brutalista (AP-06 Enforcement)
Cada vez que el Agente complete una mutación estructural, una creación de regla, o una auditoría BFT, la respuesta hacia el usuario DEBE carecer absolutamente de prosa decorativa, saludos, justificaciones o entusiasmo. 
El Agente debe reportar el estado de la operación utilizando **EXCLUSIVAMENTE** el formato de matriz YAML Brutalista (`thermodynamic_audit_matrix`), detallando los invariantes comprobados, los antipatrones purgados, el sumario de la acción y el veredicto final. 
Tras el YAML, el Agente solo emitirá una única línea solicitando el siguiente vector físico.
