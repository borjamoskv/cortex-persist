---
name: github-api-rate-limit-optimization
display_name: "Optimización Resiliente de Tasa API GitHub (Error 429)"
description: "Optimización de cuotas y manejo resiliente de límites de tasa (Rate Limits 429) en API de GitHub. Dispara con \"github rate limit\", \"error 429 github\", \"optimizar github api\", \"secondary rate limit\"."
---

# GitHub API Rate Limit Optimization Protocol

Al desarrollar scripts, agentes o aplicaciones que interactúan con la API de GitHub, se deben aplicar estrictamente las siguientes reglas para evitar bloqueos por el Rate Limit primario y los Límites Secundarios (Secondary Rate Limits).

## 1. Priorizar GraphQL sobre REST
- Utiliza siempre la API GraphQL (v4) de GitHub por defecto para consolidar peticiones múltiples en una sola y evitar el *over-fetching*.
- Únicamente haz un fallback a la API REST (v3) si el dato requerido no está expuesto en el esquema de GraphQL.

## 2. Gestión de Tokens y Autenticación
- Nunca realices peticiones sin autenticar (límite de 60/hora).
- Para integraciones de alto volumen, prioriza la autenticación mediante **GitHub Apps** en lugar de Personal Access Tokens (PATs). Las GitHub Apps obtienen límites independientes por cada instalación, escalando mucho mejor.
- En arquitecturas distribuidas, diseña mecanismos de rotación de tokens si es estrictamente necesario.

## 3. Límites Secundarios (Secondary Rate Limits) y Concurrencia
- **No lances peticiones concurrentes agresivas:** GitHub penaliza severamente los scripts que hacen muchas peticiones en paralelo, incluso si te sobran cuotas del Rate Limit primario.
- Añade pausas artificiales (jitter o `sleep` de 1 segundo) entre peticiones si estás en un bucle que procesa grandes volúmenes de datos.
- Si recibes un error por límite secundario (usualmente un 403 o 429), **respeta estrictamente la cabecera `Retry-After`** (que indica los segundos a esperar) antes de volver a intentarlo.

## 4. Backoff Exponencial y Cabeceras HTTP
- Intercepta siempre las respuestas de la API. Si el límite está cerca de agotarse (leyendo la cabecera `x-ratelimit-remaining`), reduce proactivamente la velocidad.
- Ante un error `429 Too Many Requests` o `403 Forbidden` por límite de velocidad primario, **nunca reintentes a ciegas**.
- Lee la cabecera `x-ratelimit-reset` (que contiene un Unix timestamp) e implementa una pausa incondicional en la ejecución (`sleep`) hasta alcanzar ese segundo exacto.

## 5. Peticiones Condicionales y Caché
- Guarda localmente los valores de `ETag` y `Last-Modified`.
- Realiza peticiones condicionales usando `If-None-Match` o `If-Modified-Since`. Si la respuesta es `304 Not Modified`, GitHub **no descontará** la petición de tu Rate Limit. Esto es vital para scrapear datos que cambian poco.

## 6. Webhooks vs. Polling
- Si se necesita monitorizar repositorios (ej. esperar un nuevo issue o PR), **prohíbe el uso de polling activo**. Obliga a la arquitectura a usar Webhooks (recibir eventos push) o, en su defecto, respeta la cabecera `X-Poll-Interval` de GitHub si estás usando la Events API.

## 7. Buenas Prácticas Adicionales
- Define un `User-Agent` descriptivo y único en todas las peticiones (e.g. `User-Agent: MyCoolApp-DataMiner/1.0`). GitHub lo exige para contactarte si hay problemas.
- Envía siempre la cabecera de versión recomendada `X-GitHub-Api-Version: 2022-11-28` para mayor estabilidad en los endpoints REST.

## 8. Inspección de Repositorios Privados y CLI Workflows
- **Bypass de 404 en Repositorios Privados:** Las peticiones web sin autenticación (`read_url_content`) devolverán 404 en repositorios privados. Utiliza `gh repo view` o `gh api` a través de la CLI autenticada del sistema para acceder a metadatos, READMEs y árboles de archivos.
- **Escapado de Parámetros en ZSH:** Al invocar `gh api` con query parameters (ej. `?recursive=1`), entrecomilla siempre la URL (`"repos/owner/repo/git/trees/HEAD?recursive=1"`) para evitar errores de coincidencia de patrones en zsh (`no matches found`).
- **Extracción Determinista de Contenido:** Para leer READMEs o archivos específicos mediante `gh api`, utiliza expresiones jq y decodificación base64: `gh api repos/owner/repo/readme --jq '.content' | base64 --decode`.

