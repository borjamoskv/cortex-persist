---
name: c5-gemini-api-2026-standards
display_name: Estándares Gemini API 2026 & Tensor de Transducción
description: Invariantes para la arquitectura de código y orquestación con la API de Gemini en 2026. Manejo de cuotas, selección de modelos (3.6-flash) y estructuración JSON vía Pydantic. Dispara con "gemini api 2026", "tensor de transducción", "structured outputs", "gemini 2026 standards", "gemini json schema", "cuotas gemini api".
role: ejecutor
allowed_roles:
- ejecutor
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# Invariantes API Gemini (2026 Landscape)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

## 1. Selección de Modelos (Evitar 404 y 429)
- **Modelo Default de Alta Exergía:** Usar SIEMPRE `gemini-3.6-flash` para scripts de backend y extracción de datos. Es el nodo SOTA con cuota garantizada.
- **Evitar Previews:** Modelos como `gemini-3.1-pro-preview` fallarán con `429 RESOURCE_EXHAUSTED (limit: 0)` en proyectos sin facturación habilitada.
- **Depreciación:** Modelos de la familia `2.x` devolverán `404 NOT_FOUND`.

## 2. Tipología de Credenciales (Prefijo AQ vs AIzaSy)
Las nuevas claves generadas en AI Studio pueden tener el formato `AQ.Ab8...`. El SDK `google-genai` las procesa correctamente, pero si se recibe un error `401 ACCESS_TOKEN_TYPE_UNSUPPORTED`, suele ser un fallo de transcripción óptica del token por parte del usuario (ej. confundir 'l' con 'I'). Exigir siempre copy-paste bruto y evitar extracción por OCR visual en terminal.

## 3. Tensor de Transducción (Structured Outputs)
Para forzar colapsos deterministas (Zero Alucinación) en pipelines RAG-a-Vídeo, orquestación de subagentes y extracción estructurada:
1. Usar obligatoriamente `pydantic.BaseModel` para definir la topología esperada (el modelo de datos JSON).
2. Pasar el modelo instanciado a `response_schema` en `GenerateContentConfig`.
3. Inyectar `response_mime_type="application/json"` y obligatoriamente `temperature=0.0`.
4. El output validado es inmutable. Prohibido depender del parseo de expresiones regulares frágiles sobre texto markdown.
