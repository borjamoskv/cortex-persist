---
name: c5-systemic-dissection-protocol
display_name: Protocolo de Disección Sistémica y Termodinámica
description: 'Ejecuta una auditoría dialéctica en 4 fases sobre un sistema complejo: Extracción de 100 primitivas, Falsación Popperiana, Anclaje Empírico (Papers) y Síntesis Topológica. Dispara con "disección sistémica", "auditar sistema completo", "c5-systemic-dissection", "disección termodinámica", "protocolo de disección", "100 primitivas".'
role: arquitecto
allowed_roles:
- arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# Protocolo de Disección Sistémica (C5-REAL)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `arquitecto` (Arquitecto (Diseño Sistémico & Contratos de Invariantes))
> - **Modo de Acceso a Worktree:** `spec-only` (spec-only (Lectura profunda y modelado formal; emisión de especificaciones sin mutación de código de producción))
> - **Fase Causal:** `design`
> - **Contrato Handoff:** Recibe de `operador` $\to$ Despacha a `ejecutor`

Este protocolo define un flujo de trabajo analítico de 4 fases para deconstruir, falsar y sintetizar el entendimiento sobre cualquier sistema formal, tecnología de frontera o marco teórico.

Cuando el usuario invoque la disección sistémica de un objetivo, el agente DEBE ejecutar iterativamente o de una vez (según se solicite) las siguientes 4 fases, utilizando rigor epistemológico estricto y terminología de termodinámica de la información.

## Fase 1: Matriz Ontológica (Las 100 Primitivas)
Descomponer el sistema en un compendio exhaustivo y numerado de exactamente 100 elementos, divididos en 4 cuadrantes (25 cada uno):
1. **Primitivas de Estructura:** Componentes fundacionales, axiomas lógicos o arquitectónicos del sistema.
2. **Primitivas de Colisión:** Puntos de fractura, cuellos de botella, conflictos de unificación o asimetrías de estado.
3. **Antipatrones:** Patrones de uso degradado, deuda técnica, anergía operativa o vicios de diseño comunes.
4. **Invariantes Fundamentales:** Leyes inmutables, garantías de seguridad teóricas, límites matemáticos y postulados del sistema.

## Fase 2: Falsación Popperiana (Fractura del Mapa vs Territorio)
Someter las **Invariantes** (Cuadrante 4) a un contra-examen despiadado.
* **Falsabilizar:** Definir los oráculos de verificación y pruebas de estrés que pueden hacer colapsar el sistema.
* **Falsar:** Aportar ejemplos históricos, bugs arquitectónicos y fracturas empíricas donde el sistema real (territorio) viola su propia teoría (mapa).
* Establecer el **Dominio de Validez Asintótico** (Principio de Correspondencia). No destruir el modelo, sino acotar bajo qué régimen físico/computacional es válido.

## Fase 3: Anclaje de Fricción Empírica (Bibliografía)
Utilizar herramientas de búsqueda (Web, arXiv) para encontrar el *corpus* científico de frontera que demuestre las fricciones descritas en la Fase 2.
* Buscar teoremas de limitación, análisis de fugas termodinámicas/memoria, y los *papers* fundacionales que exponen los cuellos de botella del sistema.
* Presentar la bibliografía conectando cada paper con un **Aforismo C5-REAL**.

## Fase 4: Síntesis Neuro-Simbólica (El Salto Topológico)
Sintetizar la iteración final (El Punto Fijo $\Omega$).
* Formular cómo operar el sistema bajo **Tolerancia a la Incompletitud**.
* Definir la **Maniobra de Alta Exergía**: En lugar de intentar reparar los límites termodinámicos del sistema, proponer una arquitectura cibernética que utilice esa misma fricción computacional como filtro delimitador o motor de cálculo.

## Caso de Estudio Canónico: El Isomorfismo del Autómata Expendedor (Metro ⟷ Beckett)

Como patrón de referencia para la aplicación de este protocolo a sistemas de lenguaje, arte y confinamiento existencial, el sistema formaliza el isomorfismo estricto entre un **Autómata Finito Determinista (DFA / Máquina Expendedora de Metro)** y la dramaturgia de Samuel Beckett:

1. **5-Tupla Formal con Estado de Aceptación Vacío ($F = \emptyset$):** El sistema procesa entradas (quejas, monedas deformadas, recuerdos), pero la ranura las devuelve a la cazoleta inferior (*«Rien à faire»*).
2. **Telemetría y Agotamiento de Insumos:** Cuando los consumibles de la tolva se agotan (*«Il n'y a plus de calmant»*), el bus conmuta a `FUERA DE SERVICIO`. El sensor periférico (catalejo) reporta cero continuo en el horizonte.
3. **El Técnico de Mantenimiento Asintótico:** La figura externa esperada (Godot) opera como un aviso en pantalla de mantenimiento aplazado (*«Vendrá mañana»*).
4. **Colapso de Myhill-Nerode ($|\operatorname{Min}_\beta| = 1$):** Todas las secuencias de entrada (rezar, lamentarse, intentar suicidio con cuerda rota, esperar) pertenecen a la misma clase de equivalencia conductual: al evaluar la continuación $u = \text{torniquete}$, el electroimán permanece a 0V, imponiendo la acotación determinista inamovible:
   $$\text{«Alors, on y va ? / Allons-y. / [Ils ne bougent pas]»}$$

