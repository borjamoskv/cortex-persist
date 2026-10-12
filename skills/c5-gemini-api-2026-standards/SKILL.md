---
name: c5-gemini-api-2026-standards
display_name: Estándares Gemini API 2026 & Tensor de Transducción
description: Invariantes para la arquitectura de código y orquestación con la API de Gemini en 2026. Manejo de cuotas, selección de modelos (3.8-flash / flash-latest), renovación autónoma vía Safari JXA, diagnóstico HTTP 400/403/404 y estructuración JSON vía Pydantic. Dispara con "gemini api 2026", "renovar gemini", "gemini api key", "tensor de transducción", "structured outputs", "gemini 2026 standards", "gemini json schema", "cuotas gemini api".
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
> - **Modo de Acceso a Worktree:** `read-write` (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos)
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

## 1. Selección de Modelos (Evitar 404 y 429)
- **Modelo Default de Alta Exergía:** Usar SIEMPRE `gemini-3.8-flash` o `gemini-flash-latest` para scripts de backend, síntesis y extracción. Son los nodos SOTA con cuota garantizada.
- **Depreciación Estricta:** Modelos de la familia `2.x` (como `gemini-2.5-flash`) devuelven `404 NOT_FOUND (This model is no longer available to new users)` en proyectos creados a partir de 2026. Prohibido hardcodearlos en nuevos scripts.
- **Evitar Previews Inestables:** Modelos experimentales sin cuota asignada fallarán con `429 RESOURCE_EXHAUSTED (limit: 0)` en proyectos en nivel gratuito.

## 2. Tipología de Credenciales y Diagnóstico de Errores (400 vs 403)
Las claves generadas en AI Studio conviven en dos formatos: `AQ.Ab8...` (nuevas 2026) y `AIzaSy...` (clásicas). Ante cualquier fallo en silicio, clasificar la causa raíz:
- **HTTP 400 (`API key not valid`):** Clave borrada o string truncado.
- **HTTP 403 (`Requests from referer <empty> are blocked`):** Clave restringida a URLs web/HTTP referrers. Inutilizable en CLI/Python; exige regeneración con Application Restriction = None.
- **HTTP 403 (`API has not been used in project / disabled`):** La API Generative Language no está encendida en el proyecto GCP vinculado.
- **HTTP 403 (`Your API key was reported as leaked`):** Clave revocada permanentemente por el escáner de seguridad de Google tras detectarse en repositorios públicos. Exige purga de consola.

## 3. Protocolo de Renovación Autónoma en Silicio (Safari JXA)
Si el escaneo de transcripciones pasadas devuelve 0 claves útiles, el agente puede orquestar la renovación autónoma si la sesión de Google está activa en Safari:
1. **Apertura de Consola:** `open -a Safari "https://aistudio.google.com/app/apikey"`.
2. **Despacho Sintético Angular Material:** Los componentes Angular CDK ignoran `element.click()`. Es obligatorio despachar la secuencia completa de eventos de puntero con coordenadas:
   ```javascript
   ["pointerdown", "mousedown", "pointerup", "mouseup", "click"].forEach(type => {
     btn.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, view: window, clientX, clientY }));
   });
   ```
3. **Retorno Síncrono en AppleScript:** Toda evaluación multi-línea con `do JavaScript` debe encapsularse en una IIFE autoejecutable (`(() => { return ...; })()`) para garantizar el retorno de strings/JSON a la shell.
4. **Provisionamiento de Proyecto:** Seleccionar siempre *«Crear proyecto»* en el modal de AI Studio para garantizar habilitación automática de la API sin heredar restricciones previas.
5. **Cosecha y Blindaje Local:**
   - Inyectar inmediatamente la nueva clave en `.env`.
   - Verificar de forma obligatoria que `.gitignore` contenga `.env` y `.env*` antes de cualquier commit.
   - Probar `200 OK` en silicio con `client.models.generate_content(model="gemini-3.8-flash", ...)`.

## 4. Purga de Claves Expuestas y Supresión de Alertas
Cuando Google AI Studio despliegue la advertencia *«Detectamos una clave de API expuesta públicamente»*:
1. Identificar la clave filtrada mediante el botón `.api-keys-toggle` (`Mostrar claves de APIs`).
2. Localizar la fila correspondiente en la tabla, desplegar el menú de tres puntos (`more_vert`) y ejecutar `delete Borrar clave`.
3. Confirmar la destrucción en el diálogo modal (`button.ms-button-primary` con texto `Delete`).
4. Al destruirse la clave revocada, Google AI Studio retira automáticamente el banner de seguridad.

## 5. Tensor de Transducción (Structured Outputs)
Para forzar colapsos deterministas (Zero Alucinación) en pipelines RAG-a-Vídeo, orquestación de subagentes y extracción estructurada:
1. Usar obligatoriamente `pydantic.BaseModel` para definir la topología esperada (el modelo de datos JSON).
2. Pasar el modelo instanciado a `response_schema` en `GenerateContentConfig`.
3. Inyectar `response_mime_type="application/json"` y obligatoriamente `temperature=0.0`.
4. El output validado es inmutable. Prohibido depender del parseo de expresiones regulares frágiles sobre texto markdown.
