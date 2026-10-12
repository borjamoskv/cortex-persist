---
name: c5_mcp_prompt_isomorphism_invariant
description: Invariante C5-REAL de isomorfismo estricto entre prompts generativos MCP y parsers de dominio en silicio (Anti-Divergencia de Schema).
trigger: "model_decision"
---

# Invariante de Isomorfismo MCP Prompt-a-Parser (INV_C5_MCP_PROMPT_ISOMORPHISM)

## 1. Principio de Paridad Causal (Prompt ≡ Engine)
Todo prompt expuesto por un servidor MCP (`@server.prompt()`) que instruya a un modelo o agente a generar archivos de configuración, manifiestos estructurados (TOML, JSON, YAML) o código de producción DEBE reflejar con exactitud bit a bit el esquema exigido por los parsers y validadores oficiales del motor (`from_toml_path`, `_from_dict`, `pydantic.BaseModel`).

## 2. Veto al Esquema Divergente (Anti-Falso Isomorfismo)
Queda estrictamente prohibido que un prompt MCP emita plantillas con:
1. Discrepancias de cardinalidad (ej. `[[character]]` singular en el prompt vs `[[characters]]` plural en el parser).
2. Claves anidadas no reconocidas (ej. encapsular `title` dentro de una tabla `[project]` cuando el parser busca `title` en la raíz).
3. Parámetros o flags obsoletos o incompatibles entre sí (ej. duraciones no permitidas para el modelo seleccionado).

## 3. Cobertura Obligatoria en Tests Unitarios
Cualquier prompt generativo añadido o modificado en un servidor MCP DEBE contar con un test unitario en la suite de pruebas (`tests/mcp/`) que verifique:
- La presencia obligatoria de las claves estructurales canónicas.
- La compilación exitosa de la plantilla generada contra el validador oficial del dominio (ej. `MovieManifest.from_toml_path`), garantizando `exit_code = 0` y cero excepciones `ConfigurationError`.

## 4. Invariante de Aislamiento de Ejecución Local
En scripts de prueba, enjambres o utilitarios del repositorio:
- Queda prohibido invocar ejecutores remotos o empaquetados (`uvx --from <package>`) dentro del propio árbol de trabajo del proyecto.
- Toda ejecución DEBE acoplarse al silicio local mediante `uv run <cli>` o `python -m <module>`, incorporando un parámetro `--project` explícito y `timeout` defensivo en llamadas `subprocess`.
