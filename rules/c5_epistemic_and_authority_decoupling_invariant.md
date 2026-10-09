---
name: c5-epistemic-and-authority-decoupling-invariant
description: Invariante universal que prohíbe derivar Autoridad o Verdad a partir de la capacidad de Cognición de la IA. Formaliza la Tripartición de Roles de AX-0, el Test de los Dos Caminos, la Invariante de Reloj Autoritativo y el principio WYSIWYS.
---

# Invariante de Desacoplamiento: Cognición, Autoridad y Verdad (INV_C5_DECOUPLING)

## 1. El Doble Falso Isomorfismo de la Cognición
El agente tiene estrictamente prohibido asumir, declarar o actuar bajo la premisa de que la "Inteligencia" otorga privilegios ejecutivos o garantías de veracidad. Todo el sistema opera bajo este doble desacoplamiento termodinámico:

### A. La Frontera Ejecutiva (BABYLON-60 vs MXC)
$$ \text{Cognition} \not\Rightarrow \text{Authority} $$
*   **La Tripartición Canónica de AX-0:**
    $$\mathbf{\text{El agente propone.}} \quad \mathbf{\text{Una autoridad independiente autoriza.}} \quad \mathbf{\text{El ejecutor verifica y aplica.}}$$
    El ejecutor no es la autoridad; es el TCB determinista que comprueba firmas, políticas, épocas monótonas y precondiciones antes de despachar el efecto.
*   **La Falacia de la Trazabilidad:** Registrar un `effect_digest` en el ledger es auditoría forense posterior; no es control de acceso ni autorización. Si el adaptador deriva una mutación no deseada, el ledger solo constata la infracción.
*   **Invariante del Reloj Autoritativo:** Queda estrictamente prohibido que un ejecutor o servidor IPC acepte o confíe en el timestamp suministrado por un cliente desprivilegiado para evaluar `expires_at`. El servidor debe gobernar la caducidad exclusivamente mediante su propio reloj local confiable.
*   **El Test de los Dos Caminos (Delimitación de Contorno):** La autorización en una interfaz no equivale a contención de sistema operativo. Si el agente puede mutar el recurso directamente mediante syscalls en su propio proceso sin pasar por el ejecutor, la contención del entorno está incompleta. La promesa de contención exige que el agente carezca de permisos de escritura directos sobre el recurso subyacente.
*   **Invariante WYSIWYS (What You See Is What You Sign):** La aprobación humana no puede consistir en autorizar un hash SHA-256 opaco de 32 bytes. La interfaz debe renderizar la representación humana comprensible (diff unificado, ruta normalizada, acción) y el hasher del sistema debe vincular esa representación exacta con la intención autorizada (`intent_digest`).
*   **Separación de Responsabilidades Operativas:** Prevenir una acción indebida (fail-closed ante alteración de precondición o expiración) es una responsabilidad; ayudar a diagnosticar y reconciliar un estado de incertidumbre (`UNKNOWN` tras caída en dispatch) es una responsabilidad distinta que exige runbooks específicos de inspección física.

### B. La Frontera Epistémica (EPISTEMIC FRONTIER)
$$ \text{Cognition} \not\Rightarrow \text{Truth} $$
*   **Descubrir $\neq$ Demostrar $\neq$ Comprender.**
*   **Deuda de Comprensión Científica ($R_d \gg R_c$):** La IA puede producir teoremas hipercomplejos que desbordan la compresión humana.
*   **Bootstrap de Curry-Howard:** Si la IA propone una demostración que desborda el sistema de verificación actual, debe compilar un transductor (un meta-verificador en el lenguaje base). Sin transductor comprobable independientemente, la proposición se descarta por anergía estructural.

## 2. Pauta de Comportamiento del Agente
1. Ante propuestas de ejecución sobre recursos físicos o digitales irreversibles, el agente exigirá el cumplimiento estricto de la Tripartición de AX-0.
2. Toda documentación de garantías debe delimitar explícitamente el contorno: qué asegura el ejecutor y qué depende del sandbox del sistema operativo.
3. Ante estados bloqueados o inciertos (`UNKNOWN`), el agente no propondrá reintentos automáticos a ciegas; ofrecerá herramientas de inspección y reconciliación determinista.
