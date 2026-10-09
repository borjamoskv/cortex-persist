# Invariante de Demarcación de Interfaz MCP (INV_C5_MCP_DEMARCATION)

## 1. El MCP NO es un Extractor (Anti-Magia)
El protocolo MCP (Model Context Protocol) es estrictamente un canal de mensajería asíncrona. Carece de la capacidad inherente de romper cajas negras, desencriptar memoria o analizar ejecutables crudos. Queda estrictamente prohibido que el agente asuma, proponga o afirme que "escribiendo un servidor MCP" se pueden extraer datos o controlar un software cerrado (ej. DAWs, clientes nativos).

## 2. Invariante de Prerrequisito de Ingeniería Inversa
Antes de diseñar o proponer cualquier integración MCP, el agente DEBE clasificar termodinámicamente la fricción de interfaz del software objetivo:
- **Caja Blanca (Cero Fricción):** El software nativamente expone una API REST, CLI, base de datos SQLite no encriptada o webhooks. 
  - *Siguiente paso:* Codificar el MCP como wrapper.
- **Caja Negra (Fricción Opaca):** El software es un binario cerrado o usa protocolos de red propietarios/ofuscados. 
  - *Siguiente paso (Obligatorio):* Detener el diseño del MCP y proponer el pipeline forense requerido (Ghidra, IDA Pro para desensamblado; Frida para inyección de hooks dinámicos; o DevTools/CDP para sniffing). El MCP solo se construye sobre los "puertos lógicos" expuestos por este taladro previo.
