---
name: webkit-memory-audit
display_name: Auditoría de Memoria WebKit (Vector 21)
description: Ingeniería inversa de C++, análisis de memoria (Bmalloc, IsoMalloc) y Gigacage en WebKit macOS. Dispara con "webkit audit", "vector 21", "gigacage", "auditoría memoria c++", "webkit memory", "bmalloc audit".
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

# Habilidad: WebKit Memory Audit (Vector 21)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Esta habilidad formaliza el proceso de auditoría y análisis de memoria *Thread-Safe* (Vector 21) realizado sobre la arquitectura C++ de Safari y WebKit en macOS.

## Invariantes Operativas de Análisis C++

1. **Rechazo a la Compilación Ciega:** No intentamos reconstruir la base de código de WebKit para entenderla; extraemos la verdad termodinámica directamente de los binarios vivos en macOS usando herramientas nativas de diagnóstico.
2. **Gigacage y Bmalloc:** Cuando el Operador requiera analizar vulnerabilidades de memoria o el funcionamiento interno del navegador, se asume el estado de arte del asignador `bmalloc` y su sandbox (`Gigacage`).

## Cadena de Herramientas Forenses (macOS)

Cuando se solicite un análisis de memoria o extracción de *dyld_info*:
- Utiliza `vmmap <pid>` para extraer el layout virtual (clasificaciones de montículos, `IsoMalloc`, `Gigacage`).
- Utiliza `dyld_info -exports /System/Library/Frameworks/JavaScriptCore.framework/Versions/A/JavaScriptCore` para mapear los símbolos de `bmalloc` expuestos sin necesidad de descompilar con Ghidra/IDA.
- Observa la actividad de *threads* concurrentes (como el `scavenger` de bmalloc) haciendo muestreos con `sample <pid> 1 100`.

> **The "Die Well" Protocol:** Al igual que el Kernel de Babylon, WebKit implementa técnicas de *Fast Fail* (crash controlado) si el Gigacage detecta punteros fuera de su jaula de 32GB. Todo reporte de vulnerabilidad debe enfocarse en este cuello de botella exergético.


---

## 3. Diagnóstico de Montículo en Vivo (Live Heap Profiling)

Para verificar si una pestaña o proceso WebKit está experimentando fragmentación de memoria o fugas en Gigacage:

```bash
# 1. Obtener PID del proceso com.apple.WebKit.WebContent de Safari:
pgrep -f "com.apple.WebKit.WebContent" | tail -n 1

# 2. Generar mapa virtual detallado de asignaciones bmalloc / IsoMalloc:
vmmap -summary $(pgrep -f "com.apple.WebKit.WebContent" | tail -n 1) | grep -E "MALLOC|Gigacage|IsoHeap"

# 3. Detectar fugas de memoria (leaks) activas en el subproceso:
leaks $(pgrep -f "com.apple.WebKit.WebContent" | tail -n 1) 2>/dev/null | tail -n 15
```
