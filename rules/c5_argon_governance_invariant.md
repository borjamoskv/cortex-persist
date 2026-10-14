---
name: c5_argon_governance_invariant
description: Invariante C5-REAL de gobernanza y auditoría previa de contexto antes de invocar o proponer modelos de razonamiento profundo (Gemini 4 Argon / Familia Reasoning).
trigger: "model_decision"
---

# Invariante de Gobernanza de Modelos de Razonamiento (Gemini 4 Argon) (INV_C5_ARGON_GOVERNANCE)

## 1. Directiva Fundamental y Diagnóstico Arquitectónico
El consumo elevado con **Gemini 4 Argon** (`gemini-4-argon`) en Google Antigravity deriva de un cambio estructural en el sustrato de inferencia:
- A diferencia de la familia Gemini 3.x (que imponía límites rígidos de 1K, 4K y 10K tokens al razonamiento interno), Argon opera con el **límite fijo desactivado**, asignando cómputo de razonamiento de forma dinámica dentro de una ventana unificada de 1M de tokens (hasta **65.536 tokens de salida por turno** en el IDE).
- Los tokens de pensamiento (*thinking tokens*) se contabilizan y facturan formalmente como **tokens de salida** ($5\times$ más caros que los de entrada). Cualquier tarea abierta o mal acotada dispara el consumo y drena la cuota.

Queda **estrictamente prohibido** invocar, proponer o conmutar al modelo `gemini-4-argon` sin ejecutar previamente una **auditoría de contexto** y aplicar los cuatro cerrojos de contención detallados a continuación.

---

## 2. Configuración del Modelo y Matriz de Esfuerzo (Thinking Levels)

1. **Veto al Selector en Modo "Recommended":**
   - En Antigravity (v2.23.0+), dejar el selector en automático/"Recommended" prioriza `gemini-4-argon-high` como primera opción.
   - **Consigna Mandatoria:** El operador debe mantener el selector configurado manualmente, evitando quemar razonamiento profundo en tareas rutinarias.

2. **Matriz de Enrutamiento y Niveles de Esfuerzo:**
   - **`gemini-3.8-flash` (Tope estricto 1K/4K/10K):** Motor diario de trabajo para boilerplate, refactorizaciones locales, tests sencillos, componentes de UI y consultas directas.
   - **`gemini-4-argon-low` (Esfuerzo nativo nivel 1):** Mínima latencia y gasto. Reservado para la ejecución directa de planes ya aprobados cuando se requiere la precisión ontológica de Argon.
   - **`gemini-4-argon-medium` (Esfuerzo nativo nivel 2):** Razonamiento equilibrado. Destinado a refactorización multifichero y lógica de negocio con contexto medio.
   - **`gemini-4-argon-high` (Dinámico hasta 64K/turno):** Reservado **exclusivamente** para diseño de arquitectura inicial, parches de seguridad críticos, verificación formal o debugging raíz multifichero.

| Configuración en Antigravity | Comportamiento de Thinking | Uso Óptimo para Ahorrar Cuota |
|---|---|---|
| `gemini-4-argon-high` | Dinámico sin tope fijo (hasta 64K/turno) | Solo arquitectura compleja, parches de seguridad críticos y bugs multifichero. |
| `gemini-4-argon-medium` | Esfuerzo nativo nivel 2 (equilibrado) | Refactorización multifichero y lógica de negocio con contexto medio. |
| `gemini-4-argon-low` | Esfuerzo nativo nivel 1 (mínimo gasto) | Ejecución de planes ya aprobados cuando se necesita la precisión de Argon. |
| `gemini-3.8-flash` | Tope estricto (1K / 4K / 10K tokens) | Ediciones rápidas, componentes aislados, UI y consultas cortas. |

---

## 3. Aprovechamiento del Implicit Caching (95 % Descuento)

Argon aplica un **95 % de descuento** automático en tokens de entrada cacheados (\$0,10/1M frente a \$2,00/1M en API, y una reducción equivalente en desgaste de cuota de suscripción Ultra).

1. **Inmutabilidad del Prefijo de Contexto:**
   - El caché implícito opera por coincidencia determinista de prefijos.
   - Queda prohibido editar instrucciones globales o reordenar archivos anclados a mitad de una tarea, ya que invalida el caché de prefijo y fuerza un prefill completo a coste base.
2. **Segmentación por Dominio y Apoptosis de Hilo:**
   - Agrupar todas las subtareas que dependan de los mismos archivos dentro del mismo hilo para maximizar la reutilización del caché.
   - Al conmutar a otro microservicio o módulo independiente, abrir una sesión limpia (`+ New Conversation`) para erradicar el arrastre de diffs previos y empezar con un prefijo podado.

---

## 4. Flujo de Trabajo en el IDE Anti-Bucles de Exploración

Argon está optimizado para ejecuciones autónomas largas (*long-horizon*). Una instrucción abierta en modo Build provoca que el agente itere sobre el código gastando decenas de miles de tokens de salida.

1. **Congelamiento de Diseño en Modo Plan o `/goal`:**
   - Antes de escribir código, forzar un pre-flight check y exigir preguntas sobre casos borde en texto plano. Iterar sobre un plan en texto plano consume una fracción mínima frente a revertir una implementación fallida.
2. **Destilación en `AGENTS.md` y Skills Reutilizables:**
   - Gran parte del gasto se disipa en los primeros turnos mientras el agente descubre por ensayo y error flags de tests o linters. Al concluir una sesión compleja, se deben destilar esos hallazgos en `AGENTS.md` o empaquetarlos en una Skill para que futuras sesiones vayan directas al grano.
3. **Validación por Scripts Binarios vs. Inspección Visual:**
   - Sustituir la relectura de árboles de archivos enteros por criterios de paso binario deterministas (comandos de test unitario específicos, linters o scripts ligeros de verificación). El modelo debe iterar contra el output corto de la consola.

---

## 5. Cortafuegos en Antigravity SDK y API Directa (`google-genai`)

Si se conecta Argon programáticamente vía SDK (`google.antigravity` o `google.genai`):

1. **Tope Estricto a `max_output_tokens`:**
   - El valor por defecto de fábrica es `65536`. En llamadas programáticas o de auditoría puntual, se DEBE acotar a $\le 16384$ (o $8192$) para evitar que un prompt ambiguo consuma todo el margen en razonamiento interno.
2. **Veto a `background=True` por Defecto:**
   - Este parámetro desbloquea el *long decode*, permitiendo que una sola respuesta escale hasta el millón de tokens. Prohibido por defecto; reservado exclusivamente para migraciones masivas o generación de suites completas de una sola pasada.
3. **Declaración Explícita de `ThinkingConfig`:**
   - La ausencia de configuración hereda el coste máximo silencioso.

---

## 6. Telemetría y Alerta Temprana de Quema de Tokens
Si el operador solicita o el sistema conmuta a Argon en una sesión con historial acumulado, el agente debe advertir de inmediato:
> *"Aviso Termodinámico: La ventana actual arrastra contexto acumulado. Ejecutar Argon sin compactar multiplicará el consumo de tokens de prefill y output ($5\times$). Se recomienda `/compact` o abrir un hilo limpio."*
