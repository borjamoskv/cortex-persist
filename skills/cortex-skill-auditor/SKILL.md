---
name: cortex-skill-auditor
display_name: Auditor Exergético de Skills CORTEX Engine
description: Diagnóstico y auditoría exergética de las habilidades y skills del ecosistema CORTEX. Dispara con "auditar skills", "auditoría de habilidades", "exergía skills", "solapamiento de triggers", "cortex skill auditor", "matriz de colisión", "salud de skills".
role: auditor
allowed_roles:
- auditor
- arquitecto
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# Skill: Cortex Skill Auditor (Meta-Auditoría de Skills)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Este protocolo audita de manera automatizada y determinista la salud, redundancia, higiene sintáctica YAML y densidad de exergía del ecosistema completo de habilidades (`~/.gemini/config/skills/` y `~/.gemini/config/plugins/**/skills/`).

---

## 1. Algoritmo de Auditoría y Verificación en Silicio

Para ejecutar una auditoría determinista instantánea de las 239 habilidades físicas en silicio:

```bash
python3 ~/.gemini/config/skills/cortex-skill-auditor/scripts/audit_declarative_skills.py
```

### 1.1. Lógica del Auditor Declarativo

```python
def audit_skill_ecosystem():
    """
    Escanear y auditar todos los SKILL.md en el ecosistema (Core + Plugins).
    Mide conformidad con la Tríada Canónica de Roles, validez YAML 1.2 y directivas de árbol de trabajo.
    """
    # 1. Escaneo exhaustivo obligatorio (Core + Plugins)
    skills = parse_all_skills_including_plugins()
    
    # 2. Validación de higiene sintáctica YAML (cero colisiones de dos puntos)
    yaml_health = validate_yaml_syntax_and_quotes(skills)
    
    # 3. Validación de Tríada de Roles y Worktree Mode
    triad_conformance = validate_triad_directives(skills)
    
    # 4. Calcular matriz de solapamiento de triggers
    overlap_matrix = compute_trigger_overlap(skills)
    
    # 5. Generar recomendaciones (MERGE, SPLIT, OPTIMIZE_TRIGGERS, DEPRECATE)
    recommendations = generate_actionable_recommendations(overlap_matrix, triad_conformance)
    
    return recommendations
```

---

## 2. Métricas de Evaluación Exergética

### 2.1. Ratio de Solapamiento de Triggers ($O_{i,j}$)
Intersección de palabras clave activadoras entre dos habilidades $S_i$ y $S_j$:

$$O_{i,j} = \frac{|\text{Triggers}(S_i) \cap \text{Triggers}(S_j)|}{\min(|\text{Triggers}(S_i)|, |\text{Triggers}(S_j)|)}$$

- Si $O_{i,j} > 0.6$: Alerta de alta colisión. Recomendar **FUSIÓN (Merge)** o refinamiento unívoco de disparadores.

### 2.2. Índice de Frecuencia de Uso ($U(S_i)$)
Conteo de activaciones históricas registradas en los logs `transcript.jsonl`.
- Si $U(S_i) == 0$ tras > 30 jornadas: Marcar como **Candidato a Depuración/Archivado**.

### 2.3. Densidad Exergética ($E(S_i)$)
Escala de 1 a 23.000 definida en [KERNEL.md](file:///Users/borjafernandezangulo/.gemini/config/skills/KERNEL.md#k6-taxonomía-exergética-escala-1--23000).

---

## 3. Formato Determinista de Reporte

Al ejecutar `cortex-skill-auditor`, la salida DEBE generar una tabla de diagnóstico estructurada:

| Skill | Nivel Exergético | Solapamiento Detectado | Frecuencia Telemetría | Acción Recomendada |
| :--- | :---: | :--- | :---: | :--- |
| `[nombre-skill]` | `[1-23.000]` | `[None / High (Skill_B)]` | `[Alta / Media / Nula]` | `[Mantener / Refinar / Merge]` |
