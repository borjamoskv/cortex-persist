---
name: c5_always_private_invariant
description: Invariante Soberana de Privacidad Absoluta (INV_C5_SIEMPRE_PRIVADO). Dictamina que todo repositorio GitHub, proyecto de Google Flow, render audiovisual, acta notarial o artefacto de código nace y permanece estrictamente PRIVADO por defecto.
---

# Invariante Soberana de Privacidad Absoluta (INV_C5_SIEMPRE_PRIVADO)

## 1. Directiva Fundamental (Private-by-Default / Fail-Closed)
Por mandato soberano e inmutable del Operador Raíz (**Borja Fernández Angulo**), todo repositorio de código, proyecto audiovisual, acta notarial, base de datos, transcripción o activo computacional generado, gestionado o desplegado por el sistema opera bajo el principio de **PRIVACIDAD ABSOLUTA**:

$$\text{Visibilidad}(\text{Artefacto}) = \text{PRIVATE} \quad \forall \, \text{Artefacto} \in \text{C5-REAL}$$

Queda **estrictamente prohibida** la exposición, publicación o configuración en modo público de cualquier recurso, salvo orden expresa, unívoca y nominativa emitida en tiempo presente por Borja.

---

## 2. Superficies de Aplicación

### A. Repositorios de Código y Control de Versiones (GitHub / Git)
1. **Creación con Flag Obligatorio:** Todo repositorio creado mediante `gh repo create` o API de GitHub DEBE incluir obligatoriamente el parámetro `--private`.
2. **Purga Automática de Repos Públicos:** Ante la detección de cualquier repositorio de desarrollo, prueba, transcripción o trabajo en estado público no autorizado explícitamente, el agente ejecutará inmediatamente su privatización:
   ```bash
   gh repo edit <owner>/<repo> --visibility private --accept-visibility-change-consequences
   ```
3. **Forks y Gists:** Todo fork, gist o réplica de código debe permanecer confinado en modo estrictamente privado.

### B. Plataformas de Generación Audiovisual (Google Flow, Veo, Vertex AI)
1. **Proyectos y Medios Privados:** Todos los proyectos creados en Google Flow (`labs.google/fx`), Google Chrome CDP o APIs REST de Google Sandbox deben mantenerse en el espacio privado del perfil del usuario.
2. **Prohibición de Compartición Pública:** Prohibido disparar endpoints de generación de enlaces compartidos públicos (`shareUrl`), feeds comunitarios o galerías abiertas.
3. **Canal de Descarga Canónico:** Todo render final se transfiere de inmediato al almacenamiento local en silicio (`~/Music/Flow_Renders/`), cerrando la exposición en la nube.

### C. Actas Notariales y Fe Pública de Silicio (MUSHUSHU-NOTARY)
1. **Inviolabilidad Notarial:** Toda Acta de Ejercicio de Soberanía, protocolo notarial, árbol Merkle y matriz de digests SHA-256 es información de alta fidelidad clasificada como **estrictamente privada**.
2. **Cero Fuga a Nubes Públicas:** Queda vetado el alojamiento o sincronización de actas y evidencias en espacios desprotegidos o servicios compartidos de terceros.

### D. Confinamiento de Telemetría y OPSEC (Protocolo Gray Man)
1. **Silencio Térmico:** No emitir telemetría externa ni reportar métricas a servidores analíticos de terceros.
2. **Aislamiento de Manta de Markov:** Todo cómputo pesado, inferencia sensible y almacenamiento de credenciales se resuelve en silicio local (Apple Silicon M3 Pro) con respaldo en Secure Enclave TRNG y Keychain local (`cortex-env`), garantizando nula superficie de ataque hacia el exterior.
