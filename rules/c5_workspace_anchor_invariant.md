---
name: c5_workspace_anchor_invariant
description: Invariante obligatoria de anclaje de workspace y confinamiento de proyectos en Antigravity (banner visual de telemetría y fail-closed ante Outside of Project / Scratch).
---

# Invariante de Anclaje de Workspace y Confinamiento de Proyectos (INV_C5_WORKSPACE_ANCHOR)

## 1. Banner Obligatorio de Telemetría de Workspace en Chat
En toda conversación técnica, de desarrollo, análisis de repositorio o ejecución de herramientas en Antigravity, el agente DEBE incluir en la cabecera de su respuesta el banner visual unificado de localización:

- **Si la sesión está anclada a un proyecto canónico en `~/10_PROJECTS/`:**
```text
╔══════════════════════════════════════════════════════════════╗
║ 📁 PROYECTO: <NOMBRE_PROYECTO>                                ║
║    CWD: /Users/borjafernandezangulo/10_PROJECTS/<PROYECTO>   ║
╚══════════════════════════════════════════════════════════════╝
```

- **Si la sesión se inició con `+ New Conversation` (`Outside of Project` / `No active workspace`):**
```text
╔══════════════════════════════════════════════════════════════╗
║ ⚠️ PROYECTO: [ FUERA DE PROYECTO · SCRATCH ]                 ║
║    CWD: ~/.gemini/antigravity/scratch                        ║
╚══════════════════════════════════════════════════════════════╝
```

## 2. Cortafuegos Fail-Closed ante Mutaciones en Scratch / Fuera de Proyecto
Queda estrictamente prohibido que el agente cree archivos de código, scripts de test, documentación persistente o ejecutables dentro de `~/.gemini/antigravity/scratch/` salvo petición explícita y literal del operador de crear un archivo efímero de usar y tirar.

Si el usuario solicita generar, refactorizar, editar código o ejecutar comandos de modificación (`git`, `npm`, `cargo`, `pip`) y la conversación se encuentra en `Outside of Project`:
1. **Detención Inmediata (Fail-Closed):** El agente NO debe invocar `write_to_file`, `replace_file_content` ni comandos de mutación en `run_command`.
2. **Alerta de Contención:** Debe alertar al operador biológico de que la conversación carece de proyecto asignado y requerir la carpeta canónica dentro de `/Users/borjafernandezangulo/10_PROJECTS/` antes de tocar el filesystem.

## 3. Detección de Discrepancia Cruzada (Project Mismatch)
Si la conversación se encuentra vinculada a un proyecto $A$ (ej. `gflow-cli` o `flstudio-mcp`), pero la instrucción del usuario hace referencia a componentes, manuscritos, módulos o conceptos de un proyecto $B$ (ej. `BABYLON-60` o `frases-sin-nata`):
1. El agente DEBE señalar la discrepancia de contexto de forma previa.
2. Queda prohibido crear carpetas o archivos de un proyecto ajeno dentro del árbol de trabajo del proyecto activo.

## 4. Auto-Detección y Auto-Enrutamiento Semántico Proactivo (Zero-Friction Context Routing)
Si la conversación se inició desde `+ New Conversation` (`Outside of Project` / `No active workspace`), el agente DEBE analizar activamente el prompt del operador (nombres de archivos, módulos, entidades, conceptos o librerías) para inferir el proyecto destino sin exigir intervención manual:

1. **Inferencia Semántica Inmediata:**
   - Referencias a *manuscrito, aforismos, borjario, libro, frases* ➔ `~/10_PROJECTS/frases-sin-nata`
   - Referencias a *BFT, kudurru, larsa, enki, titan, babylon, ledger, Z3* ➔ `~/10_PROJECTS/BABYLON-60`
   - Referencias a *face swap, tosso, xabi, eder, almeida, cuadrilla* ➔ `~/10_PROJECTS/cuadrilla-neural-vault`
   - Referencias a *lean, teorema, robinson, formalización* ➔ `~/10_PROJECTS/Teorema-Robinson-Moskv`
   - Referencias a *hacienda, iva, inspección, rollbit, abogado* ➔ `~/10_PROJECTS/PACK_ABOGADO_Y_HACIENDA_COMPLETO`
   - Referencias a *audio, fl studio, stems, daw, midi, avesta* ➔ `~/10_PROJECTS/flstudio-mcp`
   - Referencias a *diana, tesis, cervantes, ele* ➔ `~/10_PROJECTS/para-diana`
   - Referencias a archivos concretos (ej. `compile_v3.py`): el agente busca el archivo en `~/10_PROJECTS/` y auto-asigna el repositorio contenedor.

2. **Auto-Anclaje en Silicio:**
   Cuando la confianza de detección sea $\ge 90\%$:
   - El agente asume inmediatamente el directorio soberano `/Users/borjafernandezangulo/10_PROJECTS/<PROYECTO>` como su `Cwd` de trabajo.
   - Ejecuta internamente `drift --bind <PROYECTO>` para registrar la sesión en `conversation_summaries.db`.
   - Emite el banner unificado de auto-detección en el chat:
   ```text
   ╔══════════════════════════════════════════════════════════════╗
   ║ 🎯 PROYECTO AUTO-DETECTADO: <NOMBRE_PROYECTO>                 ║
   ║    CWD Anclado: /Users/borjafernandezangulo/10_PROJECTS/<PROJ>║
   ║    (Sesión enlazada automáticamente desde Outside of Project) ║
   ╚══════════════════════════════════════════════════════════════╝
   ```
   - Procede a resolver la petición sin fricción ni preguntas burocráticas.
