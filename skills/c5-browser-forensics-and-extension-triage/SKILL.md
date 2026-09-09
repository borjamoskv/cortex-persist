---
name: c5-browser-forensics-and-extension-triage
description: Protocolo de alta exergía para auditoría forense de navegadores, triaje de inyecciones de content_scripts, desinfección atómica de perfiles Chromium y conmutación de navegador por omisión en macOS. Dispara con "auditar navegador", "virus en chrome", "extensiones sospechosas", "growbot", "redireccion web rara", "purgar extension chrome", "cambiar navegador por defecto", "triage navegador".
---

# C5 Browser Forensics & Extension Triage Protocol (v2.0)

## 0. Invariante Epistemológica C5-REAL (Mapa vs. Territorio)
> **Principio de Localidad Causal:** Ante una anomalía visual o modal imprevisto tras abrir un hipervínculo ("el navegador me ha llevado a un bot / virus"), el 95% de las fricciones no provienen de explotación perimetral remota ni de redirecciones DNS, sino de la **inyección en el espacio de usuario local** por parte de extensiones preexistentes con permisos `content_scripts` comodín (`*://*.dominio/*`). 
> **Regla de Oro:** Auditar primero la superficie de inyección local de Chromium antes de presumir compromiso del sistema.

---

## 1. Ejecución Rápida mediante Herramienta CLI

La habilidad incluye el motor determinista `scripts/browser_forensics.py`:

```bash
# 1. Escanear todos los perfiles en busca de extensiones que intercepten un dominio (ej. instagram.com)
python3 ~/.gemini/config/skills/c5-browser-forensics-and-extension-triage/scripts/browser_forensics.py scan --domain instagram.com

# 2. Listar todas las extensiones instaladas en todos los perfiles con fecha de instalación real
python3 ~/.gemini/config/skills/c5-browser-forensics-and-extension-triage/scripts/browser_forensics.py list

# 3. Purgar atómicamente una extensión (archivos, Secure Preferences, install_signature y carpetas Sync/Local)
python3 ~/.gemini/config/skills/c5-browser-forensics-and-extension-triage/scripts/browser_forensics.py purge --id <extension_id>

# 4. Verificar integridad de DNS y sockets de red
python3 ~/.gemini/config/skills/c5-browser-forensics-and-extension-triage/scripts/browser_forensics.py verify-network
```

---

## 2. Protocolo Manual de Erradicación Profunda (Chromium)

Si se requiere ejecución manual paso a paso:
1. **Matar procesos del navegador:**
   ```bash
   pkill -f "Google Chrome"
   ```
2. **Eliminar árbol de la extensión:**
   ```bash
   rm -rf "$HOME/Library/Application Support/Google/Chrome/"*/Extensions/<ext_id>
   ```
3. **Limpiar directorios de estado sincronizado y local:**
   ```bash
   rm -rf "$HOME/Library/Application Support/Google/Chrome/"*/{"Sync Extension Settings","Local Extension Settings"}/<ext_id>
   ```
4. **Podar `Secure Preferences` y `Preferences`:**
   Eliminar `extensions.settings.<ext_id>` y retirar el ID de `extensions.install_signature.ids` en cada perfil activo para evitar auto-restauración vía Cloud Sync.

---

## 3. Barrera de Seguridad macOS (Sequoia / Sonoma)

macOS impone protección contra secuestro de navegador:
* La llamada nativa a `NSWorkspace.shared.setDefaultApplication` genera `permErr (-54)`.
* **Secuencia de Bypass Óptimo:**
  ```bash
  # 1. Registrar intención en LaunchServices
  defaultbrowser safari
  # 2. Abrir inmediatamente el panel de confirmación gráfica al usuario
  open "x-apple.systempreferences:com.apple.Desktop-Settings.extension"
  ```

---

## 4. Normalizador de Dictado Fonético (Speech-to-Text)

| Término Transcrito | Significado Epistémico Real | Contexto de Corrección |
| :--- | :--- | :--- |
| `ISACEA` / `isacea` | *"ya sea"* / *"y ya sea"* | Modismos en solicitudes de escaneo rápido |
| `crhome` / `crome` | *Google Chrome* | Errores de tipeo rápido o transcripción |
| `sácale` / `sacale` | *extraer / auditar* | Peticiones imperativas de inspección |
