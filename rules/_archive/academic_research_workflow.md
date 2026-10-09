# Flujo de Trabajo para Investigación y Papers Académicos

1. **Preferencia de Biblioteca Local:** 
Antes de intentar descargar un paper científico, artículo o libro de internet usando `curl` o el navegador, DEBES verificar proactivamente (usando `list_dir` o `grep_search`) si el archivo ya existe en la biblioteca local del usuario en la siguiente ruta:
`/Users/borjafernandezangulo/Documents/PAPERS/`

2. **Extracción Técnica Proactiva:** 
Cuando leas un paper en PDF a petición del usuario, no te limites a leer el abstract o el cuerpo principal. DEBES inspeccionar siempre los **Apéndices, Material Suplementario y Anexos** en busca de:
- Código fuente original (ej. scripts históricos, implementaciones de algoritmos).
- Prompts de sistema de LLMs.
- Descripciones detalladas de arquitecturas de red o configuraciones experimentales.
Una vez encontrados, extráelos y señálaselos al usuario de forma proactiva, indicando la página exacta para aportarle valor técnico directo sin que tenga que pedirlo.
