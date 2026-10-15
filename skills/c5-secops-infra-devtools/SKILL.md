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

1. Identifica la petición y busca el alias en la tabla o en `references/aliases.json`.
2. Lee solo el módulo pertinente antes de seguir su procedimiento.
3. Conserva sus roles, restricciones y referencias a recursos.
4. Los nombres originales siguen disponibles mediante aliases y comandos independientes.
5. La carga del hub no inicia auditorías, scripts, servicios externos ni cambios de infraestructura.
6. Cada procedimiento se ejecuta únicamente cuando lo requiere la petición del usuario.

## Resolver aliases

Ejecuta `python3 scripts/route.py --query "frase o nombre original"` desde esta carpeta.
El resolver devuelve candidatos y rutas; no ejecuta los módulos.
Normaliza mayúsculas y acentos, prioriza coincidencias exactas y respeta límites de palabra.
Si devuelve varios módulos, lee solo los pertinentes sin sustituir sus contratos por similitud temática.
Los recursos de cada módulo se resuelven desde su carpeta preservada.

## Módulos de ámbito global

| Módulo completo | Nombres y triggers conservados |
| --- | --- |
| [existence-gap-audit](references/modules/existence-gap-audit/MODULE.md) | `existence-gap-audit`, `/existence-gap-audit`, `auditoría`, `audit`, `revisa este repo`, `código alucinado`, `dependencias fantasma`, `slopsquatting`, `vibe coding`, `supply chain`, `¿esto se ejecuta?`, `imports rotos`, `auditar workflows` |
| [c5-html-report-injection-audit](references/modules/c5-html-report-injection-audit/MODULE.md) | `c5-html-report-injection-audit`, `/c5-html-report-injection-audit`, `inyección html`, `xss reporte`, `autoescape jinja`, `auditar exportador`, `escape de ledger` |
| [c5-browser-forensics-and-extension-triage](references/modules/c5-browser-forensics-and-extension-triage/MODULE.md) | `c5-browser-forensics-and-extension-triage`, `/c5-browser-forensics-and-extension-triage`, `auditar navegador`, `virus en chrome`, `extensiones sospechosas`, `growbot`, `purgar extension chrome`, `triage navegador` |
| [electron-asar-forensic-audit](references/modules/electron-asar-forensic-audit/MODULE.md) | `electron-asar-forensic-audit`, `/electron-asar-forensic-audit`, `auditar app electron`, `extraer asar`, `asar python`, `descompilar electron`, `forense electron app`, `ingeniería inversa electron` |
| [electron-mac-bundle-collision-diagnostics](references/modules/electron-mac-bundle-collision-diagnostics/MODULE.md) | `electron-mac-bundle-collision-diagnostics`, `/electron-mac-bundle-collision-diagnostics`, `electron crash mac`, `crash ips macos`, `bundle collision electron`, `diagnóstico electron mac`, `leveldb lock purge`, `cierre inesperado electron` |
| [ghidra-ida-binary-audit](references/modules/ghidra-ida-binary-audit/MODULE.md) | `ghidra-ida-binary-audit`, `/ghidra-ida-binary-audit`, `auditar binario`, `ghidra`, `ida pro`, `descompilar binario`, `buffer overflow audit`, `ingeniería inversa` |
| [webkit-memory-audit](references/modules/webkit-memory-audit/MODULE.md) | `webkit-memory-audit`, `/webkit-memory-audit`, `webkit audit`, `vector 21`, `gigacage`, `auditoría memoria c++`, `webkit memory`, `bmalloc audit` |
| [macos-lulu-firewall-diagnostics](references/modules/macos-lulu-firewall-diagnostics/MODULE.md) | `macos-lulu-firewall-diagnostics`, `/macos-lulu-firewall-diagnostics`, `lulu firewall`, `little snitch`, `redes macos`, `diagnóstico firewall`, `reglas de red macos`, `bloqueo sockets mac` |
| [c5-sovereign-identity-hardening](references/modules/c5-sovereign-identity-hardening/MODULE.md) | `c5-sovereign-identity-hardening`, `/c5-sovereign-identity-hardening`, `identidad soberana`, `data breach`, `filtración de correo`, `have i been pwned`, `k-anonimato`, `hardened identity`, `alias email` |
| [github-architect](references/modules/github-architect/MODULE.md) | `github-architect`, `/github-architect`, `audita mi github`, `qué repos archivar`, `itera /github-architect`, `generar ci workflow`, `github architect`, `auditoría repositorios github` |
| [github-api-rate-limit-optimization](references/modules/github-api-rate-limit-optimization/MODULE.md) | `github-api-rate-limit-optimization`, `/github-api-rate-limit-optimization`, `github rate limit`, `error 429 github`, `optimizar github api`, `secondary rate limit`, `evitar 429 github`, `resiliencia api github` |
| [jujutsu-vcs-management](references/modules/jujutsu-vcs-management/MODULE.md) | `jujutsu-vcs-management`, `/jujutsu-vcs-management`, `jujutsu vcs`, `jj repo`, `jujutsu git`, `control de versiones jj`, `jj vcs`, `jujutsu management` |
| [vscode-git-packed-refs-diagnostics](references/modules/vscode-git-packed-refs-diagnostics/MODULE.md) | `vscode-git-packed-refs-diagnostics`, `/vscode-git-packed-refs-diagnostics`, `vscode git enoent`, `packed-refs`, `corrupción git`, `reparar git vscode` |
| [homebrew-ecosystem-management](references/modules/homebrew-ecosystem-management/MODULE.md) | `homebrew-ecosystem-management`, `/homebrew-ecosystem-management`, `homebrew`, `brew audit`, `dependencias macos`, `paquetes homebrew`, `gestión homebrew`, `entorno brew` |
| [cloudflare-mcp-usage](references/modules/cloudflare-mcp-usage/MODULE.md) | `cloudflare-mcp-usage`, `/cloudflare-mcp-usage`, `cloudflare`, `mcp cloudflare`, `zonas dns cloudflare`, `cloudflare worker`, `desplegar cloudflare`, `kv r2 cloudflare`, `cloudflare api mcp` |
| [safari-browser-agent](references/modules/safari-browser-agent/MODULE.md) | `safari-browser-agent`, `/safari-browser-agent`, `safari agent`, `navegar safari`, `mcp safari`, `controlar safari`, `safari browser agent`, `safari automation`, `inspeccionar safari`, `mac maestro`, `automatizar safari jxa`, `bypass webdriver`, `mac maestro bridge`, `control jxa macos`, `windowserver automation` |
| [whatsapp-nexus-protocol](references/modules/whatsapp-nexus-protocol/MODULE.md) | `whatsapp-nexus-protocol`, `/whatsapp-nexus-protocol`, `whatsapp nexus`, `bot whatsapp`, `baileys rust`, `pasarela whatsapp`, `whatsapp gateway`, `enviar whatsapp`, `mensajes whatsapp`, `wa-nexus` |
| [c5-socint-extraction-suite](references/modules/c5-socint-extraction-suite/MODULE.md) | `c5-socint-extraction-suite`, `/c5-socint-extraction-suite`, `socint suite`, `inteligencia social`, `scraping redes`, `reddit socint`, `substack socint`, `auditar tweet`, `analizar hilo x` |
| [youtube-analysis-pipeline](references/modules/youtube-analysis-pipeline/MODULE.md) | `youtube-analysis-pipeline`, `/youtube-analysis-pipeline`, `youtube analysis`, `youtube transcript`, `auditoría youtube`, `analizar video youtube`, `falsabilizar video youtube`, `falsabilizar video` |
| [c5-sre-postmortem-architect](references/modules/c5-sre-postmortem-architect/MODULE.md) | `c5-sre-postmortem-architect`, `/c5-sre-postmortem-architect`, `incident review`, `postmortem sre`, `análisis de incidentes`, `5 whys`, `postmortem report`, `análisis 5 whys`, `blameless postmortem` |
