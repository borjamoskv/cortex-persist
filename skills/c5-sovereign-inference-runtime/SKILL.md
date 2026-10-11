---
name: c5-sovereign-inference-runtime
display_name: Motor Soberano de Inferencia y Adaptador LM Studio C5-REAL
description: 'Despliegue y auditoría de motores de inferencia local bare-metal. Dispara con "eridu-infer", "inferencia soberana", "appliance ia", "lm studio protocolo", "motor inferencia local", "air-gapped infer", "servidor openai local rust", "sovereign inference runtime", "desplegar eridu-infer", "tríada jurídica".'

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

# C5-REAL Sovereign Inference Runtime Protocol (Nivel Omega)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Implementación & Despliegue Bare-Metal)
> - **Modo de Acceso a Worktree:** `read-write` (Mutación atómica de código, binarios y configuraciones)
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este protocolo rige la arquitectura, compilación y despliegue de **appliances de inferencia soberana local (air-gapped)** sobre Apple Silicon, erradicando el bloat de Electron/Python mediante kernels compactos en Rust (`eridu-infer`) y blindando la privacidad bajo el marco del EU AI Act.

---

## 1. Protocolo de Ingeniería Inversa y Compatibilidad LM Studio
Al interactuar o emular la pila de LM Studio:
- **Descubrimiento de Socket:** El CLI `lms` sondea los puertos candidatos `[41343, 52993, 16141, 39414, 22931]` enviando `GET /lms-status` esperando `{"package": string, "version": string}`.
- **Payload Bun Mach-O:** El ejecutable `~/.lmstudio/bin/lms` contiene el código en la sección `__bun` del segmento `__BUN`. Se inspecciona con `otool -l` y `dd`.
- **Canales WebSocket (`lms_communication`):** Mensajes tipados (`channelCreate`, `channelSend`, `rpcCall`, `rpcResult`).
- **Autenticación Dual:** Sal estática `"Var6lhhZGAUOowV+6cOrFc1H"` concatenada con token dinámico en `~/.lmstudio/.internal/lms-key-2`.

---

## 2. Arquitectura de Silicio de `eridu-infer`
Todo motor soberano de inferencia en BABYLON-60 debe cumplir:
1. **Binario Único Bare-Metal:** Compilado en Rust con Tokio y Axum, con tamaño $< 2\text{ MB}$ y consumo en reposo $< 10\text{ MB}$ de RAM.
2. **Enlace Dual de Puertos:**
   - Puerto `41343`: Compatible con handshake y sondeo del CLI de LM Studio.
   - Puerto `1234`: Compatible con la API estándar de OpenAI (`/v1/chat/completions`, `/v1/models`).
3. **Consola Web HUD Autónoma:** Servida en `/` y `/hud` desde una constante HTML embebida (`HUD_HTML`). Cero dependencias de Node, CDN o internet exterior.
4. **Daemon Launchd en macOS:**
   - Plist en `~/Library/LaunchAgents/com.babylon60.eridu-infer.plist`.
   - Modos CLI: `--install-daemon`, `--uninstall-daemon`, `--status`.
   - Logs en `~/.babylon60/logs/`.

---

## 3. Topología de Memoria Unificada (UMA) sin Swap
Para garantizar latencias sub-segundo sin desbordamiento a disco SSD:
- **Regla del 50% de UMA:** La suma de los pesos de los modelos cuantizados no debe exceder el 50-60% de la memoria física disponible para reservar el resto a KV-Cache de contexto largo:
  - Sistema 1 (LAYA / ModernBERT): $\approx 0.3\text{ GB}$ (FP16).
  - Embeddings (BGE-M3): $\approx 2.1\text{ GB}$ (FP16).
  - Reranker (BGE-Reranker-v2): $\approx 1.2\text{ GB}$ (Q8_0).
  - Razonador (DeepSeek-R1 Distill 32B): $\approx 19.4\text{ GB}$ (Q4_K_M).
  - Redactor (Llama 3.3 70B Instruct): $\approx 38.2\text{ GB}$ (Q4_K_M).
  - **Total Confinado:** $61.2\text{ GB}$ en hardware Mac Studio de 128 GB.

---

## 4. Gobernanza Causal y Cumplimiento EU AI Act (Arts. 9-15)
- **Causal Gate Ring-0:** Intercepta la petición antes de que toque la GPU.
- **Hash WORM:** Deriva SHA-256 del contenido del prompt, modelo y timestamp.
- **Recibo SCITT:** Emite un identificador de atestación determinista (`B60-...`) grabado en SQLite WAL local.
- **Certificación Legal:** Demuestra formalmente ante AEPD/AESIA la ausencia de transmisión externa y la inmutabilidad del procesamiento local.
