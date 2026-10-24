---
name: electron-mac-bundle-collision-diagnostics
display_name: Diagnóstico de Crashes & Colisiones Electron en macOS
description: Diagnóstico y resolución de crashes y colisiones de bundles en aplicaciones Electron/Chromium en macOS. Inspecciona reportes .ips y prepara reparaciones revisables de bundles y perfiles. Dispara con "electron crash mac", "crash ips macos", "bundle collision electron", "diagnóstico electron mac", "leveldb lock purge", "cierre inesperado electron".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# Protocolo Avanzado de Diagnóstico Forense y Prevención de Colisiones (macOS Electron)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

## Diagnóstico de Electron y Chromium en macOS
Este módulo es `audit-only`. Revisar un crash no autoriza cerrar procesos, borrar locks o perfiles, reemplazar aplicaciones ni modificar cuarentena o ajustes de accesibilidad.

### Evidencia de solo lectura
1. Fijar aplicación, versión, ventana temporal y ubicación de los informes relevantes. Inspeccionar solo la evidencia necesaria de `~/Library/Logs/DiagnosticReports/` y las rutas de la aplicación solicitada.
2. Leer el encabezado y el cuerpo del informe `.ips` según su formato observado. Si el parser falla o faltan campos, mostrar el error y declarar NO_VERIFICADO; no ocultarlo con `except: pass` ni concluir ausencia de crashes.
3. Extraer fecha, ejecutable, bundle ID, versión, excepción, proceso/hilo y stack relevante, evitando contenido privado ajeno al diagnóstico.
4. Separar observación de hipótesis. `EXC_BREAKPOINT`, `SIGKILL` o un frame de Chromium no identifican por sí solos una causa única de GPU, memoria, perfil o versión.

### Colisiones de bundles y locks
- Inventariar rutas de instalación, versión, firma e identidad del bundle. La fecha de modificación no basta para seleccionar qué copia conservar.
- Consultar procesos y descriptores activos antes de proponer una intervención sobre locks. Un error de permisos o una herramienta ausente deja el estado NO_VERIFICADO; no prueba que el lock sea huérfano.
- No ejecutar `pkill` por coincidencias amplias ni borrar archivos `LOCK`, `SingletonLock`, `SingletonCookie` o `Local Storage` durante el diagnóstico.
- Para LevelDB, comprobar en modo de solo lectura la existencia de `CURRENT` y el manifiesto referenciado. Su ausencia requiere investigación y recuperación, no borrado automático del perfil.

### Propuesta revisable de reparación
Entregar causa observada o hipótesis, alternativas y rutas afectadas. Preparar una reparación con cierre controlado, copia recuperable y comprobaciones posteriores. La ejecución requiere autorización explícita para esa intervención; reutilizar la que ya cubra exactamente el alcance sin pedirla de nuevo.

Preservar perfiles, historial y aplicaciones existentes. No desactivar accesibilidad, retirar cuarentena, sobrescribir bundles ni eliminar réplicas por defecto. Los efectos protegidos conservan las compuertas de atestación aplicables.

### Cierre
Informar evidencia, incertidumbre y siguiente acción propuesta. Solo declarar resuelto un crash tras reproducir la condición relevante y comprobar el resultado de la reparación autorizada. No garantizar ausencia de pérdida de datos mediante una receta.
