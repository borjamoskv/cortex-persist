---
name: c5-sre-postmortem-architect
display_name: Arquitecto de Postmortems e Incidentes SRE
description: Redacción de informes postmortem sin culpa (blameless) siguiendo mejores prácticas SRE, análisis 5 Whys, líneas temporales y cálculo MTTR. Dispara con "incident review", "postmortem sre", "análisis de incidentes", "5 whys", "postmortem report", "análisis 5 whys", "blameless postmortem".
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

# Skill: C5 SRE Postmortem Architect

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Este protocolo guía la redacción rigurosa e imparcial de postmortems de incidentes de producción bajo los principios de Site Reliability Engineering (SRE) sin asignación de culpa (blameless).

---

## 1. Pipeline de Análisis de Incidentes

1. **Recopilación y Línea Temporal (Timeline):**
   - Registro cronológico UTC de la detección, alertas, contención y resolución.
   - Cálculo de MTTR (Mean Time to Recovery) y MTTD (Mean Time to Detect).

2. **Análisis de Causa Raíz (5 Whys):**
   - Profundización deductiva en cascada desde el síntoma superficial hasta la falla estructural del sistema o del proceso.

3. **Planes de Acción y Prevención de Reincidencia:**
   - Asignación de tareas preventivas priorizadas (Preventative Action Items) con dueños y SLA de remediación.

---

## 2. Salida Estructurada

Informe técnico en Markdown con resumen ejecutivo de impacto (SLO/SLA afectado), línea temporal y grafo de causas raíz.


---

## 2. Métricas Cuantitativas SRE Obligatorias

Todo reporte de postmortem generado bajo este estándar DEBE incluir el cómputo de:
- **MTTD (Mean Time to Detect):** $\Delta t = T_{	ext{alerta}} - T_{	ext{inicio\_incidente}}$
- **MTTR (Mean Time to Resolve):** $\Delta t = T_{	ext{recuperación}} - T_{	ext{alerta}}$
- **SLO Breach Impact:** Porcentaje del presupuesto de error (*Error Budget*) consumido durante el incidente:
  $$	ext{Burn Rate} = rac{	ext{Tasa de Fallo Real}}{	ext{Tasa de Fallo Permitida por SLO}}$$
