---
name: cloudflare-mcp-usage
display_name: Automatización & Operaciones Cloudflare MCP
description: Uso y automatización del servidor MCP oficial de Cloudflare API para Workers, DNS, KV/R2, Pages y reglas de red, con degradación automática hacia navegador si falta API Token. Dispara con "cloudflare", "mcp cloudflare", "zonas dns cloudflare", "cloudflare worker", "desplegar cloudflare", "gestión cloudflare", "kv r2 cloudflare", "cloudflare api mcp", "cloudflare mcp usage", "debug cloudflare mcp", "cloudflare graphql mcp", "cloudflare execute", "cloudflare endpoints".
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

# Automatización y Operaciones Cloudflare MCP

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

## Composición Funtorial (MASS Stage 2)
- PRE-REQUISITO: [c5-real-devsecops-scaffold]
- POST-CADENA: [safari-browser-agent]

Utiliza esta habilidad cuando una tarea solicite interactuar con Cloudflare MCP, Cloudflare API MCP o un servidor MCP de Cloudflare para inspeccionar, consultar, configurar, desplegar o depurar recursos en Cloudflare.

El servidor MCP oficial de Cloudflare API opera bajo la modalidad *Code Mode*. Debe ser tratado como una interfaz de descubrimiento y ejecución determinista, nunca como un conjunto de herramientas arbitrarias memorizadas.

## Regla Núcleo

**Prohibido inventar rutas de API, datasets GraphQL, cuerpos de petición o nombres de parámetros de memoria.**

Sigue estrictamente esta secuencia operativa:

1. **Documentación y Búsqueda:** Utiliza las capacidades de documentación y búsqueda del MCP para localizar el endpoint relevante, el esquema, el dataset, los permisos y ejemplos de llamada.
2. **Determinación de Ámbito:** Confirma si la petición está delimitada a nivel de cuenta (`account-scoped`), zona (`zone-scoped`), usuario (`user-scoped`) o token (`token-scoped`).
3. **Ejecución Precisa:** Invoca la capacidad `execute` únicamente tras conocer la estructura exacta de la llamada.
4. **Inspección de Respuesta:** Examina el cuerpo de respuesta devuelto por Cloudflare, no solo el código de estado HTTP (GraphQL puede responder HTTP 200 conteniendo `errors`).

Si el servidor MCP expone `docs`, `search` y `execute`:
- `docs`: Comprender la firma y sintaxis esperada por el servidor MCP.
- `search`: Localizar endpoints de la API, operaciones OpenAPI, datasets GraphQL, nombres de parámetros y requerimientos de permisos.
- `execute`: Despachar la petición final utilizando el endpoint descubierto y parámetros exactos.

## Verificaciones Previas a la Ejecución

Verifica estos campos antes de ejecutar:
- **Identidad del Recurso:** ID de cuenta (`account ID`), ID de zona (`zone ID`), nombre de worker/script, ruta, ID de registro DNS o ID de regla de firewall.
- **Ámbito:** Las APIs de cuenta requieren `account ID`; las APIs de zona requieren `zone ID`.
- **Permisos:** El token debe incluir el permiso específico de lectura/edición y el recurso debe residir dentro del ámbito permitido para ese token.
- **Riesgo Operativo:** Para operaciones de creación, actualización, eliminación (`delete`), purga de caché, despliegues o rotaciones de seguridad, explica el impacto y obtén confirmación previa a menos que el usuario lo haya autorizado explícitamente.
- **Ventana Temporal:** Las consultas de analítica y logs deben iniciar con un rango temporal estrecho.

## Diagnóstico de Errores de Autenticación

Trata estos errores primariamente como problemas de autenticación o sesión:
- `10000: Authentication error`
- `401 Unauthorized`
- `Authentication failed`
- `Invalid token`
- Errores de ausencia de OAuth, sesión o token.

**No intentes resolver estos fallos mutando parámetros de negocio.** Diagnostica:
1. ¿Está el cliente MCP autenticado contra el servidor MCP de Cloudflare?
2. ¿Está presente la variable `CLOUDFLARE_API_TOKEN` en el runtime de ejecución?
3. ¿Utiliza la petición el encabezado `Authorization: Bearer <API_TOKEN>` en lugar de cabeceras API-key legadas?
4. ¿Ha expirado, sido revocado o eliminado el token?
5. ¿Utiliza el token filtrado por IP de cliente (*Client IP Address Filtering*)? El servidor oficial MCP no soporta tokens con restricción de IP estática.

Petición canónica de verificación:
```text
GET /client/v4/user/tokens/verify
```

## Errores de Permisos y Titularidad (Entitlements)

Clasifica estos fallos como problemas de autorización o disponibilidad de producto en el plan de la cuenta:
- `403`
- `not authorized for that account`
- `zones [...] are not authorized`
- `does not have access to the path`
- `requires entitlement: ...`
- `node is not available` / `node is disabled`

Diagnóstico secuencial:
1. Confirmar que el ID de cuenta o zona es exacto.
2. Confirmar que el token tiene alcance sobre esa cuenta o zona específica.
3. Confirmar que el token posee los permisos requeridos de lectura o edición.
4. Ante `requires entitlement: ...`, explica con claridad que la cuenta carece de la suscripción o plan requerido. Detén reintentos en bucle con parámetros aleatorios.
5. Propón un dataset o endpoint alternativo únicamente tras buscarlo formalmente.

## GraphQL y Analítica

Para métricas de Workers, eventos de seguridad, analítica DNS, WAF o reportes globales:
- Buscar primero el dataset GraphQL correcto.
- Confirmar si pertenece a `viewer.accounts(...)` o `viewer.zones(...)`.
- Comprobar disponibilidad del dataset mediante introspección previa.
- Especificar siempre `limit` donde el esquema lo exija.
- Comenzar con un rango temporal estrecho y expandir bajo demanda.
- Solicitar únicamente campos y dimensiones estrictamente necesarios.
- Verificar el campo `errors` en la respuesta incluso con HTTP 200.

## Formato Temporal Obligatorio

Los filtros de tiempo en Cloudflare GraphQL (`datetime_gt`, `datetime_geq`, `datetime_lt`, `datetime_leq`) deben utilizar UTC ISO 8601 en segundos:
```text
2026-06-16T00:00:00Z
```

Prohibido utilizar:
- `2026-06-16` (formato solo fecha en campos `Time`)
- `2026-06-16 00:00:00`
- `2026-06-16T08:00:00+08:00` (zonas horarias locales no UTC)
- Lenguaje natural (`ayer`, `yesterday`)

Si el usuario provee fechas locales o tiempos relativos, conviértelos a UTC antes de la llamada. Si la API rechaza milisegundos, truncalos conservando solo segundos.

Para campos cuyo tipo en el esquema sea explícitamente `Date`, utiliza formato de fecha pura:
```text
2026-06-16
```

## Control de Límites de Tasa (Rate Limits - HTTP 429)

Cuando se agote el presupuesto REST, IP o GraphQL:
- Leer el encabezado `Retry-After` si está presente.
- Prohibido lanzar bucles de reintento inmediato.
- Reducir la ventana temporal, el número de cuentas/zonas consultadas y los campos solicitados.
- Cachear resultados de descubrimiento repetidos durante la tarea activa.

## Estilo de Respuesta Epistémica

Al reportar un fallo de MCP/API al usuario:
- Categorizar nítidamente: autenticación, permiso, titularidad, formato de fecha, esquema, retención o rate limit.
- Indicar la verificación mínima útil siguiente.
- Jamás exponer tokens completos ni cabeceras de autorización en el chat.
- Si el fallo responde a una limitación de plan de cuenta, decláralo y detén los reintentos.

---

## Integración de Automatización y Cadena de Degradación (Zero-Friction SOP)

1. **Gestión de Dominios, DNS y Workers**:
   - Preferir siempre el servidor MCP oficial `cloudflare` mediante llamadas declarativas (`docs` $\to$ `search` $\to$ `execute`).
   - Si no existe `CLOUDFLARE_API_TOKEN` en el entorno o Keychain, degradar de forma fluida hacia el subagente `/browser` para operar directamente sobre `dash.cloudflare.com` utilizando la sesión activa en Safari/Chrome.
2. **Cadena de Fallback**:
   `MCP Server -> Browser Subagent -> REST API (curl)`.
