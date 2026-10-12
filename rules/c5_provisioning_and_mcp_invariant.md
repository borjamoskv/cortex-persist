# Invariante de Aprovisionamiento Soberano (C5-REAL Provisioning & MCP)

## 1. Prioridad Empírica sobre Configuración (Anti-PATH Alucinación)
Ante errores de tipo `executable file not found in $PATH` en servidores MCP, orquestadores en segundo plano o daemons:
- Queda estrictamente PROHIBIDO intentar parchar archivos de configuración (ej. inyectar `env.PATH` en JSONs) como primera medida.
- El agente DEBE verificar primero la existencia física del binario en el silicio (vía `which`, `find` o `brew list`).
- Si el binario no existe, la resolución primaria es la materialización (instalación), no la reconfiguración del mapa.

## 2. Protocolo de Fricción Cero en Homebrew (Trust Override)
El entorno del Operador Soberano opera bajo políticas de seguridad restrictivas. Al realizar instalaciones de dependencias vía Homebrew desde repositorios externos (Taps de terceros):
- El agente DEBE anticipar el bloqueo por falta de confianza (`untrusted tap`).
- La orden de instalación asíncrona DEBE encadenar explícitamente el comando de confianza para evitar *deadlocks* en la tubería: `brew trust <tap> && brew install <paquete>`.

## 3. Invariante de Confinamiento de Esquemas MCP y Presupuesto de Contexto
El espacio de contexto del modelo de inferencia es un recurso físico acotado. La inclusión de esquemas de herramientas MCP en el prompt conlleva un peaje estático por turno:
- **Veto a MCPs Hipertróficos Fuera de Dominio:** Servidores MCP con más de 20 herramientas de alta especialización vertical (ej. `flstudio` con 84 herramientas y ~13.000 tokens de esquemas) DEBEN permanecer desactivados durante sesiones de desarrollo general, programación, investigación teórica o análisis jurídico.
- **Activación por Demanda (JIT):** Los servidores de dominio acústico o de infraestructura pesada solo se habilitarán cuando la tarea principal requiera mutación o consulta directa sobre dicho entorno.
- **Auditoría Forense Obligatoria:** Ante quejas o sospecha de alto consumo de tokens por prompt, el agente debe ejecutar de inmediato la telemetría en silicio de la Clase J (`anergy-purge-protocol`) en lugar de especular retóricamente.

