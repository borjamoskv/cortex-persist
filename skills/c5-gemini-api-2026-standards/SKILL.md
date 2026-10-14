---
name: c5-gemini-api-2026-standards
display_name: Estándares Gemini API 2026 & Tensor de Transducción
description: 'Estándares Gemini API 2026: cuotas, selección 3.8-flash, renovación JXA, diagnóstico HTTP y salidas Pydantic. Dispara con "gemini api 2026", "renovar gemini", "gemini api key", "tensor de transducción", "structured outputs", "gemini json schema", "cuotas gemini api".'
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

## 6. Gate de Thinking Tokens — Modelos Frontier (Gemini 4 Argon / Familia Reasoning)

> **⚠️ CAUTION:** `gemini-4-argon` y todo modelo de la familia Gemini 4 Reasoning NO están disponibles en Free Tier ni en AI Pro. Operan con una ventana de 1M de tokens y razonamiento dinámico desacoplado de topes fijos (hasta 65.536 tokens/turno en el IDE). Los tokens de pensamiento se **facturan como output tokens** ($5\times$ el coste de entrada; $10/1M intro hasta Nov 2026 → $20/1M desde Dic 2026). **Cualquier tarea mal acotada o llamada sin control de thinking puede drenar el 50% de la cuota diaria en 2 turnos.**

### Invariante Obligatorio: Pre-Flight Context Audit y ThinkingConfig Gate

Queda **estrictamente prohibido** invocar modelos de la familia `gemini-4-*` (Argon u otros modelos con capacidad de thinking) sin:
1. **Auditar el contexto previo:** Si la ventana o el prompt arrastran contexto acumulado extenso, se DEBE podar o compactar antes de invocar Argon para evitar la multiplicación exponencial de tokens.
2. **Declarar explícitamente el `thinking_budget` o `thinking_mode`:** La ausencia de configuración hereda el default `medium` = coste máximo silencioso.
3. **Limitar `max_output_tokens`:** En SDK y llamadas programáticas directas, acotar `max_output_tokens <= 16384` (frente a los 65536 por defecto).
4. **Veto a `background=True` por defecto:** No activar ejecución desacoplada salvo para migraciones batch masivas explícitas.
5. **Preservar el Prefijo de Implicit Caching (95% Descuento):** Mantener instrucciones y anclajes inmutables durante la tarea; no reordenar ni editar prefijos a mitad de ejecución.

```python
from google.genai.types import GenerateContentConfig, ThinkingConfig

# CASO 1: Desactivar thinking completamente (máximo ahorro de cuota)
config = GenerateContentConfig(
    max_output_tokens=8192,
    thinking_config=ThinkingConfig(thinking_budget=0),
)

# CASO 2: Thinking mínimo (bajo coste, precisión de Argon para ejecución de planes)
config = GenerateContentConfig(
    max_output_tokens=16384,
    thinking_config=ThinkingConfig(mode="low"),
)

# CASO 3: Thinking equilibrado (refactorización multifichero y lógica de negocio)
config = GenerateContentConfig(
    max_output_tokens=16384,
    thinking_config=ThinkingConfig(mode="medium"),
)

# CASO 4: Thinking profundo (solo arquitectura crítica / bugs raíz, con log obligatorio)
config = GenerateContentConfig(
    max_output_tokens=32768,
    thinking_config=ThinkingConfig(mode="high"),  # Exige justificación explícita
)
```

### Árbol de Decisión de Selección de Modelo

| Caso de uso | Modelo recomendado | Thinking Config | Max Output Tokens |
|---|---|---|---|
| Boilerplate, tests unitarios, UI, backend | `gemini-3.8-flash` | N/A (tope estricto 1K/4K/10K) | Default |
| Ejecución de planes ya aprobados | `gemini-4-argon` | `budget=0` o `mode="low"` | $\le 16384$ |
| Refactorización multifichero / lógica cruzada | `gemini-4-argon` | `mode="medium"` | $\le 16384$ |
| Arquitectura raíz / verificación formal | `gemini-4-argon` | `mode="high"` (con log explícito) | $\le 32768$ |

### Detección de Anergía Silenciosa (Drenaje de Cuota)

Si la cuota cae >10% por consulta en un script o sesión, el agente DEBE:
1. Auditar el modelo usado (`response.model` o header de respuesta).
2. Inspeccionar si `thinking_config` y `max_output_tokens` están declarados en el código.
3. Si no están declarados y el modelo es `gemini-4-*` → clasificar como **Anergía Silenciosa**, abortar y aplicar el cerrojo de `max_output_tokens <= 16384` y `mode="low"` / `thinking_budget=0`.
