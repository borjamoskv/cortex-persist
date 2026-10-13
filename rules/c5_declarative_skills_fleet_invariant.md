---
name: c5_declarative_skills_fleet_invariant
description: Invariante C5-REAL de paridad y estándar declarativo para la flota de habilidades CORTEX (cero micro-stubs, roles canónicos, linter en silicio).
trigger: "model_decision"
---

# Invariante de Flota de Skills CORTEX (INV_C5_SKILLS_FLEET)

## 1. Paridad Global y Local (Cero Desincronización)
Toda habilidad registrada en  o en repositorios locales () DEBE cumplir estrictamente el estándar de la Tríada Declarativa CORTEX:
- **Campos Obligatorios:** , , , , , .
- **Roles Canónicos:**  (diseño / ),  (implementación / ),  (verificación / ).
- **Contrato Handoff:** Toda habilidad debe declarar explícitamente sus extremos  y .
- **Banner Tipográfico:** Inclusión obligatoria del bloque markdown de directiva al inicio del cuerpo.

## 2. Veto a Micro-Stubs Anérgicos (Anti-AP-02)
Queda estrictamente prohibido crear o mantener habilidades con menos de 20 líneas que operen como meros atajos de texto sin herramientas asociadas. Los comandos simples deben pertenecer a slash commands o snippets de sistema.

## 3. Disparo Determinista (Anti-AP-04)
La descripción de toda habilidad DEBE finalizar con la sintaxis determinista:

Las colisiones de disparo entre dos habilidades deben satisfacer {i,j} \le 0{,}20$.

## 4. Linter de Silicio Fail-Closed (`ON WIRE`)
Todo commit que altere o agregue habilidades debe validar exit-code `0` en `audit_declarative_skills.py`:
```text
=== CORTEX SKILL AUDITOR V2 (DECLARATIVE TRIAD & KOLMOGOROV GATE) ===
Total habilidades soberanas auditadas en silicio: 114 (Plugins externos satélite: 162)

--- DISTRIBUCIÓN DE LA TRÍADA CANÓNICA ---
  • ARQUITECTO  : 30 habilidades
  • EJECUTOR    : 40 habilidades
  • AUDITOR     : 44 habilidades

[PASS] 100% de las 114 habilidades soberanas cumplen Tríada, Triggers O(1) y Cota de Kolmogorov <= 350 chars (FPR = 0.0000%).
```

## 5. Invariante de Presupuesto de Prompt (Límite de Kolmogorov · INV_C5_SKILL_BUDGET)
Para prevenir el colapso del presupuesto de contexto (Prompt Tax / Silent Drop) en el Language Server de Antigravity:
- El campo `description` en el frontmatter YAML de TODO `SKILL.md` **TIENE ESTRICTAMENTE PROHIBIDO** superar los **350 caracteres**.
- **Cero Prosa Burocrática:** La descripción debe limitarse a una (1) frase concisa seguida obligatoriamente de sus triggers exactos (`Dispara con "..."`).
- Cualquier explicación extendida, tutorial o detalle arquitectónico debe residir exclusivamente en el cuerpo Markdown del archivo, NUNCA en el YAML frontmatter.
- Todo commit en ecosistemas C5-REAL está protegido por un git hook en Silicio (Ring-0) que rechazará con `exit 1` cualquier violación de esta cota.

## 6. Higiene Sintáctica YAML y Encomillado Obligatorio (Anti-ScannerError)
Para prevenir errores de parseo en librerías YAML estrictas (`yaml.scanner.ScannerError: mapping values are not allowed here`):
- Todo campo escalar en el frontmatter YAML (`description`, `display_name`) que contenga la secuencia `: ` (dos puntos seguidos de espacio, ej. nombres de CLI, subtítulos o listas inline) **DEBE ESTAR OBLIGATORIAMENTE ENCOMILLADO** mediante comillas simples (`'...'`).
- Queda prohibido el uso indiscriminado del operador de bloque plegado (`>`) si el texto resultante desborda la cota de 350 caracteres tras la normalización de espacios.

