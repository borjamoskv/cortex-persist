---
name: c5-spaced-repetition-architect
display_name: Arquitecto de Repetición Espaciada, Anki & Control Entrópico Cognitivo C5
description: Generación de tarjetas Anki (CSV/TSV), Cloze Deletion, descomposición de micro-tareas bajo baja fricción termodinámica y gestión de carga cognitiva/ADHD. Dispara con "anki maker", "tarjetas anki", "anki flashcards", "repetición espaciada", "adhd assistant", "descomposición de tareas", "micro-tasking", "spaced repetition".
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

# Skill: C5 Spaced Repetition & Cognitive Friction Management

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Este protocolo automatiza la extracción de conocimientos atómicos desde documentos y notas de estudio para generar mazos de repetición espaciada (Anki / SM-2) y estructura planes de acción con descompresión de fricción cognitiva (ADHD-friendly task decomposition).

---

## 1. Módulo Anki Flashcard Generator (Compresión Diamantina)

1. **Extracción Atómica de Conceptos:**
   - Aislar proposición primaria $\mathcal{T}$.
   - Prohibido acumular múltiples hechos en una sola tarjeta (Principio de Minimalidad Atómica).
2. **Formato Cloze Deletion & Q/A:**
   - Cloze Syntax: `{{c1::respuesta_clave}}` para anclaje de recuerdos.
   - Front/Back Q/A con etiquetado contextual (`#domain::subdomain`).
3. **Exportación Determinista:**
   - Salida en formato TSV / CSV separado por tabulaciones, listo para importar en Anki con preservación de campos HTML/Markdown.

---

## 2. Módulo de Descomposición de Micro-Tareas (Fricción Cero / ADHD-Friendly)

1. **Partición de Masa Crítica:**
   - Desglosar proyectos complejos en bloques de ejecución $< 15$ minutos.
   - Reducir el Límite de Gödel-Turing eliminando la parálisis por análisis.
2. **First Action Trigger:**
   - Definir la primera acción física imperativa (ej. *"Abrir archivo X en línea 42"* en lugar de *"Refactorizar módulo Y"*).
3. **Dopamine Micro-Checkpoints:**
   - Secuenciación determinista de retroalimentación inmediata para prevenir el agotamiento disipativo (Thermal Throttling).
