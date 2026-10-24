---
name: c5_rust_fail_fast_invariant
description: Invariante de solidez bare-metal, fail-fast estricto y veto a .unwrap() en producción en repositorios Rust C5-REAL (INV_C5_RUST_FAIL_FAST).
trigger: "model_decision"
---

# Invariante de Solidez Bare-Metal y Fail-Fast en Rust (INV_C5_RUST_FAIL_FAST)

## 1. Veto a .unwrap() en Código de Producción
- Queda terminantemente prohibido el uso de `.unwrap()` fuera de módulos de test (`#[cfg(test)]` o `tests/`).
- En parsing de gramáticas (Pest/Nom/logos) y extracción de iteradores, es obligatorio usar `.ok_or_else(|| ...)?` propagando tipos de error de dominio (`Result<T, E>`).
- En condiciones donde una invariante formal del compilador o solucionador garantiza la existencia (ej. `SatResult::Sat` previo a `solver.get_model()`, o binding de sockets del sistema), se DEBE emplear `.expect("Mensaje explícito de la invariante formal violada")`.

## 2. Veto a Generic Catch (Crash over Catch)
- Prohibidos `except Exception:`, `except: pass` y `catch (error) {}` que enmascaren fallos de runtime. Toda excepción debe tiparse de forma exhaustiva o propagarse de forma no interceptada para preservar el principio *fail-fast: crash over catch*.
