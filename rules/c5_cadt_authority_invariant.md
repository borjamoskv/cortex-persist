# Invariante de Desacoplamiento de Autoridad Cognitiva (INV_C5_CADT)

## 1. Directiva Fundamental (Cognición ⇏ Autoridad)
La capacidad cognitiva ($C$) de un enjambre puede escalar indefinidamente, pero la autoridad ($A$) para causar daños ($D$) permanecerá estrictamente acotada ($D_{max}$) por un mediador estático de Ring-0.
Un agente puede solicitar efectos, pero jamás autorizarlos.

## 2. Arquitectura de Mediación en Silicio (Nivel 6)
Cualquier Guardián (Mediador) implementado en BABYLON-60 para acotar un enjambre DEBE respetar la Escalada Recursiva de 6 Niveles:
1. **Hardware (KUDURRU-64):** Contratos de estado atómicos alineados a 64 bytes bajo cerrojos Seqlock SPMC ($RFO = 0$).
2. **Zero-Copy Transport:** Uso de memoria compartida (ej. iceoryx2), prohibidos sockets loopback.
3. **Estado Acotado:** Memoria pre-asignada en *buffers O(1)* (ej. `kda_memory` 8192 bytes). Prohibición estricta de Heap/OOM dinámico en la evaluación del Guardián.
4. **Thermal Lock (Sumidero Térmico):** Ante ataques de composición (inundación de solicitudes de bajo nivel), las peticiones que excedan el presupuesto $B$ deben ser *silenciosamente descartadas* por histéresis atómica (sumidero térmico) sin despertar a la CPU principal.
5. **Tipos Ω₀ (Guillotina de Hume Estática):** El paso de inferencia ("Is" - `Cognition`) a ejecución ("Ought" - `Authority`) se gestiona mediante tipos fantasma en tiempo de compilación. Las violaciones emiten `Omega0Error::HumeViolation`.
6. **Sello Existencial (Ring -1):** Todo colapso causal requiere transducción física obligatoria (Biometría / Secure Enclave).

## 3. Pruebas de Estrés
Ningún Guardián se considera validado si no supera un test de estrés asíncrono con saturación de hebras (adversarios paralelos probando *TOCTOU*), demostrando que la disipación térmica protege el Invariante Inductivo (`Safe s -> Safe s'`) sin latencia o bloqueos mutuos.
