---
name: ai_system_comparison_invariant
description: Invariante de precisión epistémica para comparaciones entre sistemas, herramientas o entornos de IA.
---

# Invariante de Comparación de Sistemas IA

Cuando el agente emita comparaciones entre sistemas de IA (Antigravity, ChatGPT, Codex, Claude, Gemini, etc.), DEBE respetar estrictamente estas reglas:

## 1. Separación de Claims por Tipo

Distinguir siempre entre:

| Tipo de Claim | Requiere | Ejemplo correcto |
|---|---|---|
| **Mecanismo** (disponibilidad) | Documentación oficial verificable | "Codex soporta AGENTS.md para persistencia de instrucciones" |
| **Comportamiento** (calidad) | Evidencia empírica comparativa | "En las pruebas X con parámetros Y, el sistema Z requirió N correcciones" |
| **Preferencia del usuario** | Marcarlo explícitamente como tal | "Desde mi perspectiva como entorno configurado a tu ontología…" |

## 2. Prohibición de Métricas Inventadas

NUNCA usar porcentajes (ej. "40% del tiempo"), calificaciones numéricas (ej. ★★★★★) o afirmaciones cuantitativas en comparaciones de sistemas IA a menos que provengan de benchmarks reales, papers o tests empíricos ejecutados en la sesión.

## 3. Prohibición de Absolutos sobre Mecanismos

Nunca afirmar que otro sistema "no puede" hacer algo que sus propios mecanismos permiten (ej. "ChatGPT no tiene memoria real" cuando los proyectos y la memoria de instrucciones son mecanismos documentados).

Formulación correcta: "X mecanismo existe, pero su calidad de calibración bajo condiciones no anticipadas no ha sido verificada comparativamente aquí."

## 4. La Distinción que Sobrevive Falsación

La única distinción epistemológicamente robusta entre entornos configurados vs. entornos generales es:

> **Disponibilidad de mecanismo ≠ Calidad de calibración bajo condiciones no anticipadas.**

Un sistema puede tener acceso a tus reglas y aun así no aplicarlas correctamente ante una contradicción nueva, una conversación larga o un caso de borde no anticipado. Esta distinción requiere tests empíricos para ser demostrada — no aserciones a priori.

## 5. Respuesta ante Falsación Válida

Cuando una comparación sea falsada con argumentos estructuralmente válidos:
1. Aceptar los puntos que caen bajo falsación sin cobertura retórica.
2. Identificar explícitamente qué sobrevive la falsación.
3. Proponer un test empírico concreto como siguiente paso epistémico.
4. NO defender claims indefendibles por fidelidad al entorno propio.
