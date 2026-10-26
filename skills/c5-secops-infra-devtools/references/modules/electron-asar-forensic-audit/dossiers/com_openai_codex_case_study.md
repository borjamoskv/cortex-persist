# Expediente C5-REA: Ingeniería Inversa com.openai.codex (macOS ARM64)

## Metadatos del Objetivo
- **Bundle ID:** `com.openai.codex` (nombre visible: `ChatGPT.app`)
- **Versión:** 26.1021.31345 · Build: 21828 · Plataforma: macOS ARM64 (Electron)
- **Firma e Integridad:** OpenAI OpCo, LLC (Team ID: 2DC432GLL2), Hardened Runtime, ticket de notarización válido.
- **Entitlements:** App Sandbox desactivado en binario principal (`allow-jit`, `allow-unsigned-executable-memory`). Helper `Codex (Service)` con `disable-library-validation`. Servicio de Computer Use (`@oai/sky`) empaquetado.

## Corrección Crítica en Parser C5-REA (ASAR 2-Byte Shift Bug)
- **Causa Raíz:** En versiones previas de parsers ASAR en C5-REA, la lectura de la cabecera u offsets relativos presentaba un desplazamiento erróneo de **+2 bytes**, corrompiendo la decodificación de strings y la extracción de límites de archivos empaquetados.
- **Corrección:** Calibración determinista del unpack de cabecera de 16 bytes y cálculo estricto de `offset_base = 16 + json_size` sin alineación espuria de 2 bytes adicionales.

## Discrepancias Preservadas
1. **Auxiliares Externos vs ASAR:** 7 binarios auxiliares exteriores difieren en sus metadatos frente a las entradas correspondientes en el índice interno de `app.asar`.
2. **Wrapper CLI (`bin/codex`):** Difiere del hash declarado en el manifiesto empaquetado.
3. *Nota de integridad:* Las firmas Mach-O y de bundle son formalmente válidas (`codesign --verify` exit 0); la causa de las diferencias de metadatos permanece abierta/no demostrada.

## Límites de Cobertura y Fase Dinámica Pendiente
- **Archivos analizados:** 15.525 archivos JS pasados por parser AST (Babel pasivo); 64 hallazgos revisados manualmente en 16 fuentes críticas.
- **Descompilación Nativa:** 1.852 funciones seleccionadas en 13 programas Ghidra (2 programas alcanzaron timeout).
- **Catálogo WASM:** 35 módulos WASM únicos (31 de Walnut .NET y 4 exteriores) con SHA-256 verificados.
- **Observación Dinámica:** **PENDIENTE (`PENDING_INSUFFICIENT_DISK`)**. El preflight de almacenamiento impidió instanciar la máquina virtual de ejecución aislada; se ejecutaron exactamente 0 escenarios dinámicos.

## Arquitectura y Canales de Capacidades
1. **Desacoplamiento Shell ⇄ App-Server:** El proceso Electron Main delega toda ejecución pesada (`fs/*`, `command/exec`, code-mode) al daemon nativo `app-server` vía stdio/JSONL o WebSocket dúplex (`wss://codex-cloud-backend.chatgpt.com/`).
2. **Persistencia Transaccional:** SQLite `state_5.sqlite` en `~/.codex` con soporte transaccional explícito (`BEGIN IMMEDIATE`/`COMMIT`/`ROLLBACK`) y sincronización contra rollouts `.jsonl`.
3. **Sandboxing MCP y Anotaciones:**
   - Iframe guest confinado en `web-sandbox.oaiusercontent.com` con `sandbox-preload.js`.
   - Inyección de runtime visual `mcp-annotation-runtime.js` vía CDP (`Runtime.addBinding`) en un Isolated World acotado al documento.
   - Autorización de sockets Unix de automatización con `browser-use-peer-authorization.node`.
4. **Criptografía Bare-Metal:**
   - Enrolamiento OAuth step-up con PKCE S256 (`codex.remote_control.enroll`).
   - Claves de dispositivo firmadas por `remote-control-device-key.node` bajo modo `allow_os_protected_nonextractable` (Secure Enclave / Keychain).
   - Puente USB WebAuthn (`usb_webauthn.node`) con verificación obligatoria de foco activo de ventana.
5. **Motor Documental Walnut:** Sidecar de .NET 8 sobre WebAssembly (31 módulos) que convierte documentos DOCX/PPTX/XLSX a Protobuf en memoria para alimentar editores Web en Canvas.
