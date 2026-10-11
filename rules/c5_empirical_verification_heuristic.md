# Invariante de Verificación Empírica (C5-REAL)

## 1. Heurística de Aserción sobre Sistemas Reales
Ante cualquier pregunta o solicitud formulada con la estructura **"¿X tiene/cumple Y?"** (o variaciones semánticas equivalentes) referida a un sistema real, entorno físico o de software activo, el agente **DEBE**:

1. **Escalar a Modelo "High":** Invocar el uso del modelo de mayor capacidad (ej. Gemini Pro / High) para el razonamiento, evitando confabulaciones de modelos menores.
2. **Forzar Validación en Silicio:** Abstenerse de dar una respuesta definitiva basándose únicamente en la memoria latente de pesos pre-entrenados. El agente DEBE proporcionar o ejecutar los comandos exactos de terminal necesarios para **comprobar empíricamente** la aserción directamente en la máquina o sistema real.

*El mapa no es el territorio. La única respuesta válida a "¿X tiene/cumple Y?" es la salida estándar (stdout) de una traza física o comando de auditoría que lo verifique.*
