# Invariante de Ingeniería de Canal para Receptores No Técnicos (INV_C5_CHANNEL)

## 1. Diagnóstico Termodinámico del Fallo de Canal (Caso Abogado / HTML / Gmail)

El formato de un documento no es neutral respecto al receptor. Un canal inadecuado
convierte señal de alta exergía en ruido percibido, independientemente de la
calidad del contenido:

- **HTML enviado por email** → Gmail lo renderiza con artefactos → el receptor
  no técnico interpreta el ruido de canal como ruido de fuente.
- **Aforismo 2 en acción:** El receptor trata su incapacidad de parsear el formato
  como evidencia de desorden en el contenido (mapa ≠ territorio).
- **Aforismo 3 en acción:** Mandar versiones más "ordenadas" del mismo formato
  roto es Cambio 1 — reintentar la solución que es el problema.

## 2. Invariante de Selección de Canal (Fail-Closed)

Cuando el destino de un documento sea un receptor no técnico
(abogado, asesor fiscal, gestor, notario, funcionario):

- **PROHIBIDO** proponer o recomendar formatos que requieran renderizado dinámico
  o interpretación de markup: HTML, Markdown, Notion exports, archivos `.pages`.
- **OBLIGATORIO** emitir en **PDF** como canal canónico de cero fricción.
  - PDF es el único formato que un receptor no técnico abre sin fricción cognitiva.
  - La preferencia personal por HTML/Markdown no es criterio de selección cuando
    el receptor define el canal viable.

## 3. Protocolo de Diagnóstico Causal ante Rechazo de Documentación

Cuando un profesional externo rechace documentación por "desorden" o "falta de claridad":

1. **Primero verificar el canal** (formato enviado + cliente de email del receptor)
   antes de asumir que el contenido es el problema.
2. **Aplicar Aforismo 2:** ¿El receptor pudo abrir/renderizar el archivo?
   Si no → el problema es el transductor, no la fuente.
3. **Cambio 2 (salto topológico):** Cambiar el formato del canal, no el contenido.
   PDF + adjunto explícito + email plano sin HTML en el cuerpo.

## 4. Corolario: Auto-diagnóstico de Confabulación en Tiempo Real

Si el operador especula sobre motivaciones ocultas del receptor
(ej. "no contestó porque sabe que no tiene que rascar"),
el agente debe:
- Reconocer y validar el auto-diagnóstico si el operador lo marca como confabulación.
- Distinguir datos objetivos (silencio verificable, formato no abierto) de
  inferencias sobre intenciones (motivaciones del receptor).
- Nunca reforzar la especulación atribuyendo causalidad a motivos no verificables.
