---
name: c5_multi_surface_hypervisor_invariants
description: Invariantes C5-REAL para el hipervisor multi-superficie MOSKV-1 (13 IDEs/CLIs, 7 symlinks a .babylon60rules, cero GEMINI.md, MCP portable sin /Users/, OpenAPI 3.1 Code-as-Schema y daemon launchd).
trigger: "model_decision"
---

# Invariantes del Hipervisor Multi-Superficie MOSKV-1 (INV_C5_MULTI_SURFACE_HYPERVISOR)

## 1. Matriz Canónica de 7 Symlinks a .babylon60rules (Cero Deriva de Reglas)
En repositorios gobernados por MOSKV-1, queda estrictamente prohibido bifurcar, duplicar o redactar archivos independientes de instrucciones para clientes o extensiones agénticas.
- **Fuente Única de Verdad:** `.babylon60rules`.
- **Los 7 Enlaces Simbólicos Obligatorios:**
  1. `.cursorrules -> .babylon60rules`
  2. `.windsurfrules -> .babylon60rules`
  3. `.codexrules -> .babylon60rules`
  4. `CLAUDE.md -> .babylon60rules`
  5. `.clinerules -> .babylon60rules`
  6. `.roorules -> .babylon60rules`
  7. `.github/copilot-instructions.md -> ../.babylon60rules`
- **Atestación Pre-Commit:** El hook de Git (`verify_active_topology.py --staged`) debe verificar que el modo en el índice de Git sea exactamente `120000` (symlink relativo directo).

## 2. Veto a GEMINI.md en Raíz ante Presencia de AGENTS.md (Gate de Tokens)
Para evitar que los parsers de contexto de Google Antigravity y Gemini CLI ingieran concurrentemente ambos archivos en el prefill `always_on` y violen el techo de 40.000 B:
- Queda **estrictamente prohibido** crear o mantener un archivo `GEMINI.md` en la raíz de un workspace si `AGENTS.md` ya existe.
- Google Gemini CLI se configura exclusivamente mediante `.gemini/settings.json`:
  ```json
  {
    "contextFileName": [".babylon60rules", "AGENTS.md"]
  }
  ```

## 3. Portabilidad y Cero Fugas de Rutas Absolutas en Manifiestos MCP
Todo manifiesto MCP de repositorio (`.mcp.json`, `.vscode/mcp.json`, `.gemini/settings.json`, `.claude/settings.json`, `.codex/config.toml`, etc.):
- DEBE invocar el script lanzador portable (ej. `scripts/c5_cli/launch_kernel_mcp.py`), nunca el ejecutable directo con rutas absolutas.
- Queda estrictamente prohibida la presencia de rutas personales `/Users/` (`INV_C5_OPSEC_CALIBRATION`).
- Toda resolución de rutas en lanzadores debe emplear `Path.absolute()`, nunca `Path.resolve()`, para no romper el confinamiento de symlinks dinámicos (`INV_C5_PATH_SYMLINK_CONFINEMENT`).

## 4. Paridad de Contrato OpenAPI 3.1 "Code-as-Schema" (INV_C5_PARASITIC_DOF_QUOTIENT)
Para habilitar clientes web (ChatGPT Custom Actions, Gemini Gems, Grok, asistentes móviles) sin duplicidad de esquemas:
- El contrato OpenAPI 3.1.0 debe sintetizarse programáticamente en memoria (`build_openapi_spec()`) a partir de los metadatos de las herramientas, erradicando fuentes desconectadas.
- La exportación a disco (`--export-openapi <path>`) opera como artefacto de solo lectura validado bit a bit en tests contra el código Python.
- El servidor loopback HTTP debe implementar defensas de frontera: timeout estricto de socket (10.0 s), cabeceras `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, rechazo `415 Unsupported Media Type` ante `Content-Type` inválido y `405 Method Not Allowed` ante verbos no permitidos.

## 5. Persistencia Soberana macOS Launchd (INV_C5_SOVEREIGN_ANTIGRAVITY)
Cuando se requiera disponibilidad 24/7 del kernel MOSKV-1 para orquestación o consumo web:
- La ejecución se confina a un demonio local administrado por `launchd` de macOS (`~/Library/LaunchAgents/com.c5real.moskv1.kernel.plist`).
- El tráfico se confina a loopback (`127.0.0.1:6061`) con autenticación Bearer por token de entorno.
- Queda prohibida la orquestación en contenedores de terceros o proveedores cloud externos.

## 6. Higiene de Subcomandos CLI con Argumentos Remainder (INV_C5_CLI_REMAINDER_HYGIENE)
Al implementar dispatchers centrales en Python (`main_dispatcher.py`) que deleguen subcomandos a CLIs o scripts secundarios mediante `nargs=argparse.REMAINDER`:
- **Declaración Explícita de Flags de Inspección:** Si el script hijo soporta banderas de inspección temprana o fail-safe (`--check`, `--status`, `--dry-run`, `--help`), el subparser del dispatcher central DEBE declarar explícitamente esos argumentos.
- **Reconstrucción Limpia de `sys.argv`:** El manejador del subcomando debe reconstruir `sys.argv` inyectando los flags capturados antes de invocar el `main()` del módulo hijo, evitando que `argparse` aborte con `unrecognized arguments` antes del despacho.

