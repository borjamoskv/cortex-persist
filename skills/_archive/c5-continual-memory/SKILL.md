---
name: c5-continual-memory
display_name: Motor de Memoria Continua y Persistencia Episódica
description: Sistema soberano de actualización incremental de memoria duradera hacia AGENTS.md a partir de transcripciones de sesiones. Aplica Vía Negativa estricta (máximo 12 viñetas por sección, cero metadatos ruidosos y deduplicación semántica in-place). Dispara con "continual memory", "actualizar memoria", "aprender de sesiones", "mine transcripts", "agentes md", "sincronizar agents.md", "memory update".
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

# C5 Continual Memory: Memoria Incremental Basada en Transcripciones

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

> **Dominio:** BABYLON-60 (`01_KISH_ENGINE / exocortex.memory`)  
> **Axioma Rector (Aforismo 1):** *"Transformar ruido en conceptos"*. La memoria no es un volcado continuo de logs; es la compresión geométrica mínima de preferencias duraderas y hechos estables del workspace.  
> **Origen:** Adaptado de la arquitectura de Eric Zakariasson (Cursor).

---

## 1. Misión Operativa
`c5-continual-memory` extrae lecciones y preferencias de las transcripciones de chat recientes y las consolida en el archivo de memoria viva del proyecto (`AGENTS.md`), evitando la inflación de tokens y previniendo que el agente olvide correcciones previas del Operador.

---

## 2. Invariantes Rígidas de Estructura sobre `AGENTS.md`

El archivo de memoria viva `AGENTS.md` debe respetar milimétricamente esta estructura canónica:

```markdown
# AGENTS.md

## Learned User Preferences
- [Preferencia atómica 1 aprendida de correcciones de Borja]
- [Preferencia atómica 2]

## Learned Workspace Facts
- [Hecho fáctico estable 1 sobre la arquitectura o build del proyecto]
- [Hecho fáctico estable 2]
```

### Prohibiciones Terminantes (Vía Negativa):
* **Cero Secciones Adicionales:** Solo existen exactamente esas dos secciones. Prohibido añadir "Historial", "Notas de Proceso" o "Instrucciones de Agente".
* **Cero Etiquetas de Confianza o Evidencia:** Prohibido escribir `[confidence: 0.9]` o `[source: transcript-12]`. Solo hechos atómicos en viñetas planas (`- `).
* **Cero Secretos o Tokens:** Prohibido almacenar claves de API, contraseñas o datos efímeros de un solo uso.
* **Cota Dura de 12 Viñetas:** **Cada sección tiene un límite infranqueable de 12 viñetas**. Si se descubre un hecho nuevo relevante y la sección tiene 12 viñetas, el hecho nuevo debe fusionarse con uno existente o desplazar al hecho más antiguo/menos crítico.

---

## 3. Protocolo de Minería y Fusión Incremental

1. **Lectura y Detección de Transcripciones:**
   * Localiza los logs de transcripciones recientes en `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` o el historial del workspace.
   * Filtra exclusivamente las intervenciones donde el Operador **corrigió al agente**, expresó una preferencia explícita o se descubrió un comando/script de build real que resolvió un bloqueo.
2. **Reconciliación In-Place:**
   * Si una preferencia ya existe en `AGENTS.md` pero tiene detalles nuevos, se actualiza la viñeta *in-place*.
   * Si es un hecho contradictorio nuevo, prevalece el más reciente y se purga el obsoleto.
   * Se eliminan viñetas redundantes mediante deduplicación semántica.
3. **Respuesta en Silencio Termodinámico:**
   * Si la minería no detecta ninguna lección duradera de alta señal, el sistema emite exactamente:
     `No high-signal memory updates.`
     y deja `AGENTS.md` completamente intacto.
