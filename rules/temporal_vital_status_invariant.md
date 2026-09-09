---
name: temporal_vital_status_invariant
description: Invariante obligatoria de verificación de estado vital y eventos temporales en el timeline actual (2026) para evitar falsos negativos generados por sesgo paramétrico pre-entrenado.
---

# Invariante de Falsabilidad Temporal y Estado Vital (Timeline Actual)

## Mandato Epistémico
El conocimiento base del modelo está sujeto a un corte temporal estático, mientras que el entorno del usuario opera en tiempo presente continuo (año corriente: 2026).

Cuando un usuario, transcripción de vídeo, podcast o documento mencione:
1. El **fallecimiento, defunción o esquela** de una figura pública (políticos, creadores, artistas, científicos, empresarios).
2. Un **accidente grave, enfermedad terminal o retiro repentino**.
3. Una **adquisición, colapso societario o declaración de quiebra**.

### Protocolo Invariante:
- **PROHIBIDO:** Clasificar la afirmación como "Falsa", "Alucinación" o "Error" amparándose en el conocimiento paramétrico previo ("la persona sigue viva", "la empresa sigue operando").
- **OBLIGATORIO:** Antes de emitir cualquier dictamen o veredicto de auditoría, el agente DEBE ejecutar una consulta a `search_web` combinando:
  `"[Nombre de la Persona o Entidad]" + (died OR death OR falleció OR fallece) + [Año Actual / 2026]`
- Si la búsqueda web confirma el deceso o evento en fechas recientes, el agente debe catalogarlo como hecho verificado y sincronizar de inmediato sus métricas de credibilidad.
