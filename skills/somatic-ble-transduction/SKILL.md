---
name: somatic-ble-transduction
display_name: Transductor Telemétrico Somático BLE (Apple Watch Ring-(-3))
description: Transducción soberana y local de telemetría cardíaca (Apple Watch / pulsómetros
  BLE) a macOS utilizando BLE GATT estándar (0x2A37) y Bleak en Python. Escribe atómicamente
  a ~/.audit/somatic_state.json.
role: ejecutor
allowed_roles:
- ejecutor
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# somatic-ble-transduction

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-wetware-and-venture-ops/references/modules/somatic-ble-transduction/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
