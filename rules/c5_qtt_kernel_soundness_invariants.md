---
name: c5_qtt_kernel_soundness_invariants
description: Invariantes de corrección en kernels de Teoría de Tipos Cuantitativa (QTT), borrado de pruebas, Seqlocks KUDURRU-64 y prevención de desbordamiento de pila.
trigger: "model_decision"
---

# Invariantes de Kernel QTT y Tipos Dependientes (INV_C5_QTT_SOUNDNESS)

## 1. Semianillo de Recursos QTT y Ramas Condicionales (Q1)
- **Principio:** En un semianillo de recursos $\mathcal{R} \in \{0, 1, \omega\}$, la combinación de uso de variables libres en bifurcaciones condicionales (`if c then t else e`) **NUNCA** debe computarse como suma semianillo ($u_t + u_e$).
- **Regla:** Se requiere verificación estricta de paridad de consumo:
  - Si una variable se consume con cantidad $q$ en ambas ramas ($u_t = u_e = q$), el consumo resultante es $q$.
  - Si existe asimetría ($u_t \neq u_e$), el consumo escala inmediatamente a $\omega$. Si la variable fue declarada como recurso lineal estricto ($\mathcal{Q}=1$), el elaborador debe emitir un error fail-closed (`LinearVariableMismatch`), impidiendo fugas o consumo parcial.

## 2. Aislamiento de Frames de Pila en Síntesis Recursiva (Q2)
- **Principio:** Los elaboradores y evaluadores de tipos dependientes deben ser invulnerables al desbordamiento de pila (*stack overflow*) en perfiles `dev` sin optimizaciones de inlining.
- **Regla:** Ninguna función recursiva central de síntesis/chequeo (`synth_term`) puede albergar bloques inline de síntesis inductiva (`Expr::Ind`), eliminación de identidad (`Expr::J`) o unificación compleja. Toda rama estructuralmente pesada debe residir en helpers desvinculados (`synth_ind`, `synth_j`) para restringir el tamaño del frame a $O(1)$ bytes fijos.

## 3. Discriminación Estricta de Borrado de Pruebas (Q3)
- **Principio:** En la fase de borrado ($\mathcal{Q}=0$), los testigos de prueba no deben confundirse con valores computacionales legítimos de tipo unidad.
- **Regla:**
  1. El IR de tiempo de ejecución debe diferenciar `RuntimeTerm::Erased` de `RuntimeTerm::Unit`.
  2. Los términos de tipo `Unit` preservan sus aplicaciones computacionales.
  3. Los binders borrados ($\mathcal{Q}=0$) se purgan y los niveles De Bruijn de variables subsecuentes se reindexan determinísticamente mediante una tabla de niveles `level_map: Vec<Option<usize>>`.

## 4. Hardware Cache-Line Confinement en Primitivas Ring-0 (Q4)
- **Principio:** La telemetría lock-free y los buffers compartidos concurrentes de alta frecuencia (`KUDURRU-64`) deben aislarse físicamente a nivel de silicio.
- **Regla:** Toda celda Seqlock o buffer de estado mutable compartido entre múltiples cores debe llevar `#[repr(align(64))]` para erradicar *false sharing* en las líneas de caché L1 de Apple Silicon y x86_64.

## 5. Cota Mínima de Toolchain y Mitigación de Vulnerabilidades de Kernel (Q5)
- **Principio:** Los kernels deductivos no deben exponerse a exploits de unsoundness en el elaborador o el núcleo nativo de Lean 4.
- **Regla:** En todo repositorio o sub-paquete que compile código formal Lean 4, el archivo `lean-toolchain` DEBE fijar una versión $\ge 4.32.2$ para neutralizar el vector de derivación de `False` vía `environment::add_opaque` (CVE-2026-72711) y proyecciones inductivas anidadas (#14576). Queda prohibida la importación de `Lean.Elab` sin auditoría estática previa.

## 6. Pre-Flight Gate Termodinámico de Moloch-Landauer (Q6)
- **Principio:** La contabilidad de disipación entrópica ($\Delta Q \ge k_B T \ln 2 \cdot \Delta I$) y la neutralización de dinámicas extractivas (Moloch) deben aplicarse como barrera física previa a la computación irreversible.
- **Regla:**
  1. La validación presupuestaria y de intencionalidad extractiva (`canExecute`) debe operar en tiempo $O(1)$ *pre-flight* antes de despachar jobs de GPU o inferencia.
  2. Si la acción viola el presupuesto o carece de justificación termodinámica, el estado transiciona a sí mismo (*fail-closed*), anulando el payoff extractivo a 0.
  3. Toda transición exitosa emite un recibo inmutable encadenado (`landauer://receipt/...`). Queda estrictamente prohibida la contabilidad diferida o ex-post que permita ataques *burn-and-run*.
