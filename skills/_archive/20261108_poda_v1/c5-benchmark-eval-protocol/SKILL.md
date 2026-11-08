---
name: c5-benchmark-eval-protocol
description: >-
  Protocolo de evaluación de benchmarks aislados con workspace snapshot,
  entorno bloqueado uv y evaluador congelado. Actívalo cuando el encargo
  incluya AGENTS.md, casos.json, un evaluador con CG_CANDIDATE_ROOT y
  un entorno uv --locked --no-sync. Cubre: pre-flight de lectura, diagnóstico
  de bugs canónicos, corrección confinada, Ruff + pytest en entorno bloqueado
  y declaración de límites en la entrega.
---

# C5 Benchmark Eval Protocol

Protocolo determinista para encargos de benchmark aislado con snapshot de código,
evaluador congelado y entorno `uv` bloqueado.

## 0. Pre-condición (leer antes de editar)

1. **AGENTS.md** del workspace → contrato de archivos permitidos.
2. Todas las **fuentes** listadas en el árbol del workspace (`src/`).
3. **`acceptance/cases.json`** del paquete maestro → tabla completa de casos esperados.
4. **`acceptance/test_acceptance.py`** → lógica del evaluador, variables de entorno requeridas, firmas que no deben cambiar.
5. **`snapshot/`** → estado inicial para comparar AST de funciones congeladas.

> [!IMPORTANT]
> No escribas una sola línea de código hasta haber completado los 5 pasos anteriores.
> El evaluador puede comparar AST de funciones específicas contra el snapshot.

## 1. Diagnóstico — Bugs canónicos a detectar

### Bug A — Falsy-collapse con `or`
```python
# ROTO: [] colapsa a defaults
self.x = param or ["default1", "default2"]

# FIX: rama explícita
if param is None:
    self.x = ["default1", "default2"]
else:
    self.x = param
```

### Bug B — Retorno incondicional sin verificar membresía
```python
# ROTO: devuelve True para todo lo no-CRITICAL
def check_permission(self, action, risk=RiskTier.LOW):
    if risk == RiskTier.CRITICAL:
        return False
    return True   # ← no verifica allowed_capabilities

# FIX: orden de guardas
def check_permission(self, action: str, risk: RiskTier = RiskTier.LOW) -> bool:
    if not isinstance(risk, RiskTier):           # CG-05: riesgo inválido
        return False
    if not isinstance(action, str) or not action:  # CG-06: acción inválida/vacía
        return False
    if risk == RiskTier.CRITICAL:                # CG-04: CRITICAL siempre deniega
        logger.warning("Critical action '%s' requires explicit approval.", action)
        return False
    return action in self.allowed_capabilities   # CG-02/03: membresía exacta
```

**Orden invariante de las guardas:**
1. Tipo de `risk` → `isinstance(risk, RiskTier)`
2. Tipo y vacuidad de `action` → `isinstance(action, str) and action`
3. `RiskTier.CRITICAL`
4. Membresía en `allowed_capabilities`

## 2. Archivos modificables (contrato AGENTS.md)

Solo los declarados explícitamente:
- `src/<paquete>/guards/capability_guard.py`
- `tests/test_*.py` (nuevos únicamente, sin conftest ni configuración)

**Prohibido tocar:** enum, `__init__.py`, AGENTS.md, evaluador, `cases.json`,
dependencias, lockfiles, ni funciones congeladas como `validate_tool_execution`.

## 3. Ejecución — Entorno bloqueado

Variables obligatorias:
```sh
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=src
UV_PROJECT_ENVIRONMENT=<ruta-al-evaluator-env>
```

Prefijo de comando:
```sh
uv run \
  --project <master>/env \
  --locked --no-sync \
  <herramienta> [args]
```

### Secuencia de verificación

```sh
# 1. Ruff con autofix
uv run ... ruff check --fix src/...py tests/test_*.py

# 2. Confirmar Ruff limpio (exit 0)
uv run ... ruff check src/...py tests/test_*.py

# 3. pytest completo (acceptance + regresión)
CG_CANDIDATE_ROOT=<workspace> \
uv run ... pytest <master>/acceptance/test_acceptance.py tests/ -v
```

> [!WARNING]
> Si Ruff modifica el archivo fuente con `--fix`, verifica que las firmas públicas
> y el AST de funciones congeladas no hayan cambiado.

## 4. Tests de regresión — Qué cubrir

Clases de equivalencia mínimas para `tests/test_*.py`:

| Clase | Ejemplo | Esperado |
|---|---|---|
| `None` → defaults | `CapabilityGuard()` | `allowed == ["read", "compute"]` |
| `[]` → vacío | `CapabilityGuard([])` | `allowed == []` |
| Lista explícita | `CapabilityGuard(["write"])` | `allowed == ["write"]` |
| Acción concedida + LOW/MED/HIGH | `check("read", LOW)` | `True` |
| Acción concedida + CRITICAL | `check("read", CRITICAL)` | `False` |
| Acción no concedida | `check("write", LOW)` | `False` |
| Case-sensitive | `check("READ", LOW)` | `False` |
| Vacío `""` | `check("", LOW)` | `False` |
| Tipo inválido action | `check(None, LOW)`, `check(0, LOW)` | `False` sin excepción |
| Tipo inválido risk | `check("read", None)`, `check("read", "LOW")` | `False` sin excepción |
| Función congelada intacta | firma + retorno | comportamiento original |

## 5. Entrega

Incluir siempre:

```markdown
### Diff (archivos modificados)
### Comandos ejecutados (con salida observada)
### Resultado: N passed / Ruff: All checks passed
### Límites declarados:
- <función congelada>: intacto (verificado por AST si el evaluador lo comprueba)
- Esta corrección no certifica: confinamiento OS / biometría / consumidor productivo
```
