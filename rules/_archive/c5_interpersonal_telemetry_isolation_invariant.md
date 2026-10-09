---
name: c5_interpersonal_telemetry_isolation_invariant
description: Invariante de confinamiento estricto a telemetría de mensajería en auditorías relacionales (prohibición de inferir afectos usando borradores o repositorios locales no transmitidos).
---

# Invariante de Confinamiento de Telemetría Relacional (INV_C5_RELATIONAL_AIRGAP)

## 1. Directiva Fundamental (Fail-Closed)
Cuando el Operador solicite auditar una dinámica interpersonal, afectiva o relacional a partir de un chat o contexto de mensajería (ej. WhatsApp, Telegram, Signal):
1. **Confinamiento al Canal:** El agente DEBE evaluar estricta y exclusivamente los mensajes, notas de voz y eventos efectivamente transmitidos entre los interlocutores dentro de la base de datos de mensajería (`ChatStorage.sqlite`, exports de chat).
2. **Veto de Asimilación de Archivos Locales Externos:** Queda terminantemente prohibido utilizar carpetas de proyectos locales en disco (ej. `10_PROJECTS/para-diana/`, tesis en redacción, borradores huérfanos) como evidencia de la dinámica relacional o atribuir intenciones al vínculo basándose en archivos que no fueron compartidos explícitamente dentro del canal de comunicación evaluado.
3. **Ciclo Dialéctico de Evaluación:** Toda auditoría de relaciones personales debe someterse a la criba Popperiana (falsación de sesgos románticos/Goodhart por ráfagas de silencio y asimetría) y al Salto Topológico (Cambio 2), evitando diagnósticos simplistas de comedia romántica o friendzone burda.
