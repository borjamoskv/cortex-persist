---
name: c5_sovereign_secrets_and_airgap_invariant
description: Invariante obligatoria de gestión soberana de credenciales en Apple Silicon. Prohíbe secretos en texto plano (.env, .plist), impone inyección efímera en RAM desde Keychain (cortex-env) y veta la presencia de secretos en iCloud Drive.
---

# Invariante Soberana de Secretos, Confinamiento en Memoria y Air-Gap de iCloud (C5-REAL)

## 1. Prohibición de Secretos en Almacenamiento Secundario (Zero-Disk Secrets)
- Queda **estrictamente prohibido** que el agente persista, genere o proponga almacenar claves de API, tokens privados, certificados o credenciales en texto plano dentro de:
  - Ficheros `.env`, `.env.local` o similares dentro de repositorios de código.
  - Diccionarios `<key>EnvironmentVariables</key>` dentro de archivos `.plist` de `LaunchAgents` o `LaunchDaemons`.
  - Scripts ejecutables de shell o Python.
- Los repositorios deben contener exclusivamente plantillas sin valores sensibles (`.env.example`).

## 2. Canal Canónico en Apple Silicon: Inyección Efímera en Memoria (macOS Keychain)
- **Root of Trust Local:** Toda clave de API o credencial sensible debe residir exclusivamente en el Llavero nativo del sistema operativo (macOS Keychain) bajo el espacio canónico de servicios `cortex-env/<VAR_NAME>`.
- **Carga en Memoria:** La inyección de secretos hacia el entorno de shell, subagentes o procesos en ejecución se realiza en tiempo de arranque en memoria RAM pura mediante:
  `~/.config/cortex/load-secrets.zsh`
  usando llamadas deterministas a `security find-generic-password -a "$USER" -s "cortex-env/<VAR_NAME>" -w`.
- **Tiempo de Vida Acotado:** El ciclo de vida de la credencial en texto plano coincide exactamente con el ciclo de vida del proceso en memoria ($T_{\text{secreto}} = T_{\text{proceso}}$), desvaneciéndose sin dejar traza magnética ni flash en disco.

## 3. Air-Gap Innegociable de iCloud Drive (Anti-Exfiltration Invariant)
- **Clasificación Hostil:** Toda ruta bajo `~/Library/Mobile Documents/` (Apple CloudDocs / iCloud Drive) se clasifica formalmente como **espacio público no confiable**.
- **Prohibición de Ficheros de Credenciales en iCloud:** Queda terminantemente prohibido almacenar, sincronizar o alojar archivos `.env`, `.env.local`, tokens JSON (`gmail_token.json`, etc.) o credenciales en carpetas compartidas con iCloud.
- **Acción ante Detección:** Si una auditoría o inspección detecta credenciales en dicho subárbol, el agente DEBE reportarlo inmediatamente como **Riesgo Crítico de Exfiltración** y recomendar su purga inmediata o migración fuera de la nube.

## 4. Endurecimiento Preventivo por Defecto (Least Privilege)
- Si por requerimiento ineludible de un runtime externo o framework se debe materializar un archivo de configuración sensible temporal, este DEBE:
  1. Recibir permisos restrictivos `chmod 600` (`-rw-------`) de forma inmediata y automática en el mismo turno.
  2. Estar verificado en `.gitignore` para impedir cualquier commit accidental.
