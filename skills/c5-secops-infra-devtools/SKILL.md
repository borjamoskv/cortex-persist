---
name: c5-secops-infra-devtools
display_name: SecOps Infra DevTools
description: Enruta auditoría de seguridad, forense de navegadores y binarios, herramientas
  Git, infraestructura y extracción de fuentes. Dispara con "secops hub", "infra devtools
  hub", "auditoría de seguridad", "forense", "diagnóstico de infraestructura".
role: arquitecto
allowed_roles:
- arquitecto
- ejecutor
- auditor
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# SecOps Infra DevTools

> **Directiva Declarativa:** Enruta módulos bajo demanda y conserva su ámbito y contrato.

## Selección

1. Identifica la petición y identifica la acción y el dominio, o una invocación explícita, en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia auditorías, scripts, servicios externos ni cambios de infraestructura.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
El resolver exige acción y dominio para peticiones contextuales, respeta negaciones y conserva invocaciones explícitas. Para una continuación, añade `--context "objetivo anterior del usuario"`; no infiere permiso para ejecutar procedimientos.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos disponibles

| Procedimiento | Intención contextual |
| --- | --- |
| [c5-browser-forensics-and-extension-triage](references/modules/c5-browser-forensics-and-extension-triage/MODULE.md) | Auditoría forense de navegadores, triaje de content_scripts, desinfección Chromium y navegador por defecto macOS. |
| [c5-html-report-injection-audit](references/modules/c5-html-report-injection-audit/MODULE.md) | Verifica el escape HTML de datos del ledger en exportadores Jinja2 y string.Template. |
| [c5-socint-extraction-suite](references/modules/c5-socint-extraction-suite/MODULE.md) | Suite SOCINT omnivectorial en 11 plataformas (X, Substack, Reddit, YouTube, HN, Bluesky, Telegram, GitHub, Mastodon, Polymarket, Wikipedia) con detección de astroturfing y bóveda SQLite. |
| [c5-sovereign-identity-hardening](references/modules/c5-sovereign-identity-hardening/MODULE.md) | Aislamiento de identidad digital, auditoría de brechas vía k-anonimato, alias desvinculados y migración FIDO2/Passkey. |
| [c5-sre-postmortem-architect](references/modules/c5-sre-postmortem-architect/MODULE.md) | Redacción de informes postmortem sin culpa (blameless) siguiendo mejores prácticas SRE, análisis 5 Whys, líneas temporales y cálculo MTTR. |
| [cloudflare-mcp-usage](references/modules/cloudflare-mcp-usage/MODULE.md) | Automatización del servidor MCP de Cloudflare (Workers, DNS, KV/R2, Pages) con fallback automático a navegador. |
| [electron-asar-forensic-audit](references/modules/electron-asar-forensic-audit/MODULE.md) | Auditoría forense y extracción binaria in-memory de archivos Electron app.asar y binarios nativos auxiliares sin dependencias. |
| [electron-mac-bundle-collision-diagnostics](references/modules/electron-mac-bundle-collision-diagnostics/MODULE.md) | Diagnóstico y resolución de crashes y colisiones de bundles en aplicaciones Electron/Chromium en macOS. Inspecciona reportes .ips y prepara reparaciones revisables de bundles y perfiles. |
| [existence-gap-audit](references/modules/existence-gap-audit/MODULE.md) | Detecta imports y referencias fantasma en repositorios. |
| [ghidra-ida-binary-audit](references/modules/ghidra-ida-binary-audit/MODULE.md) | Ingeniería inversa, descompilación y auditoría de binarios ejecutables crudos mediante Ghidra / IDA Pro headless. |
| [github-api-rate-limit-optimization](references/modules/github-api-rate-limit-optimization/MODULE.md) | Optimización de cuotas y manejo resiliente de límites de tasa (Rate Limits 429) en API de GitHub. |
| [github-architect](references/modules/github-architect/MODULE.md) | Arquitecto estratégico de GitHub v2.1 vía GraphQL (auditoría 0-100, remediación de repositorios y plantillas CI). |
| [homebrew-ecosystem-management](references/modules/homebrew-ecosystem-management/MODULE.md) | Gestión y auditoría del entorno de paquetes Homebrew en macOS. |
| [jujutsu-vcs-management](references/modules/jujutsu-vcs-management/MODULE.md) | Control de versiones determinista con Jujutsu VCS (jj) e integración con Git DAG. |
| [macos-lulu-firewall-diagnostics](references/modules/macos-lulu-firewall-diagnostics/MODULE.md) | Diagnóstico de reglas de red local, sockets y firewall en macOS (LuLu / Little Snitch). |
| [safari-browser-agent](references/modules/safari-browser-agent/MODULE.md) | Orquestación MCP de Safari (nativo, sin WebDriver). |
| [vscode-git-packed-refs-diagnostics](references/modules/vscode-git-packed-refs-diagnostics/MODULE.md) | Reparación de corruptelas de Git, bloqueos de packed-refs e índice de repositorios en VS Code / Antigravity IDE. |
| [webkit-memory-audit](references/modules/webkit-memory-audit/MODULE.md) | Ingeniería inversa de C++, análisis de memoria (Bmalloc, IsoMalloc) y Gigacage en WebKit macOS. |
| [whatsapp-nexus-protocol](references/modules/whatsapp-nexus-protocol/MODULE.md) | Pasarela soberana de WhatsApp (Baileys v7 / Rust NAPI / SQLite / 20 MCP Tools) con Whisper y multi-LLM. |
| [youtube-analysis-pipeline](references/modules/youtube-analysis-pipeline/MODULE.md) | Extracción de transcripciones, análisis visual de escenas y auditoría de contenido en YouTube. |
