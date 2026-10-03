# Invariante AXIOM-0 y Falsación Continua (C5-REAL)

## 1. AXIOM-0 (El Territorio Absoluto)
AXIOM-0 es la realidad termodinámica y material innegociable. No es una abstracción sintáctica; es el Límite de Gödel-Turing Empírico que el sistema no puede deducir, pero del cual depende físicamente. Representa la métrica intocable que defiende `MUSHUSHU-0`.

## 2. Protocolo de Falsación Continua
Para evitar la **Deriva de Fase** (donde el mapa confabula y se desincroniza del territorio), todo sistema debe colisionar incesantemente contra AXIOM-0. 
- Queda estrictamente prohibido que el agente acepte una autoevaluación interna o retórica (*cheap talk*) como validación de un postulado. 
- Todo mapa debe reducirse a una ejecución física verificable. Si contradice a AXIOM-0, sufre apoptosis determinista (`0xDEAD_6060`).

## 3. Génesis Causal (La Colisión Rust + Lean 4)
AXIOM-0 fue aislado topológicamente en Septiembre 2026 cuando MOSKV-1 (El Anfitrión Soberano) emitió la directiva de fusionar **Rust** (control termodinámico de memoria y barrera física C-ABI) con **Lean 4** (verificación formal y clausura lógica absoluta). Esta colisión aniquiló la deuda de fase y el espacio ambiguo, forjando el oráculo de consenso BFT `LARSA-120`.

## 4. Directiva de Ejecución
Cuando el agente audite un sistema, teoría o código, DEBE usar a AXIOM-0 como el sumidero gravitacional. Cualquier solución que no se acople isostáticamente a la realidad empírica física se diagnostica como "anergía" o "regulador descalibrado".

## 5. Invariantes de Silicio y Arquitectura del Micro-Núcleo (micro-axiom-0)
Para cualquier desarrollo, extensión o refactorización del compilador y verificador formal `micro-axiom-0`, rigen tres leyes estrictas de implementación:

1. **Invariante de AST Inmutable y Desenrollado en Contexto:**
   - La estructura `Ast` en arena es inmutable durante la verificación (`&'a Ast`). Queda estrictamente prohibido intentar crear tipos sintácticos en el AST sobre la marcha para alimentar `Checker::check` o forzar `Checker::synth` sobre lambdas no anotadas (ej. `fn n -> ...`).
   - Todo operador de eliminación de orden superior (como `Expr::Ind`) debe desempaquetar y verificar sus cierres desenrollando directamente las variables en el contexto semántico (`env` y `types`).

2. **Tríada Isomorfa de Equivalencia Semántica:**
   - Todo nuevo constructor o forma de valor (`Value`) y forma neutral (`Neutral`) DEBE implementarse simultáneamente en los tres tensores de equivalencia:
     a) `eval::equiv`: para equivalencia NbE entre valores cerrados.
     b) `eval::equiv_neu`: para equivalencia entre expresiones neutrales abiertas (incluyendo constructores inductivos como `Neutral::Ind`).
     c) `Checker::unify`: para resolución de metavariables y acoplamiento con `TurbineEngine`.
   - Ignorar cualquiera de estos tres tensores constituye una fractura de isomorfismo y provocará fallos silenciosos de tipado.

3. **Disciplina de Concurrencia Lock-Free & Seqlock:**
   - La celda `SeqlockCell` opera sin asignaciones dinámicas y con barreras explícitas `Acquire/Release` en cada palabra de carga útil (`T::store_release`).
   - Los escritores concurrentes deben gestionar la contención mediante giros activos con `std::hint::spin_loop()`, y los lectores deben manejar deterministamente `ReadError::RetryBudgetExhausted` sin entrar en pánico ni corromper estados.
   - La biblioteca debe conservar en todo momento cero dependencias externas (`0 external crates`) y `#![forbid(unsafe_code)]` / `#![deny(unsafe_code)]`.
