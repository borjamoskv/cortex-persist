---
name: somatic-ble-transduction
display_name: Transductor Telemétrico Somático BLE (Apple Watch Ring-(-3))
description: Transducción soberana y local de telemetría cardíaca (Apple Watch / pulsómetros BLE) a macOS utilizando BLE GATT estándar (0x2A37) y Bleak en Python. Escribe atómicamente a ~/.audit/somatic_state.json. Dispara con "telemetria somatica", "conectar apple watch", "somatic daemon", "ble heart rate", "ring minus 3".
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

# Transductor Somático Soberano (Apple Watch -> macOS via BLE)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

## Propósito
Capturar la frecuencia cardíaca (BPM) y la variabilidad en tiempo real desde un Apple Watch (u otro sensor BLE) hacia macOS sin intermediarios en la nube, sin WebSockets externos y sin violar la Manta de Markov.

## Arquitectura de Flujo
1. **Emisor (Watch):** App HeartCast o Echo configurada en modo emisión (emula monitor de frecuencia cardíaca BLE estándar GATT).
2. **Receptor (Mac):** Daemon Python asíncrono con `bleak` suscrito al UUID de servicio `0000180d-0000-1000-8000-00805f9b34fb` y característica `00002a37-0000-1000-8000-00805f9b34fb`.
3. **Persistencia Atómica:** Volcado continuo en `~/.audit/somatic_state.json` con reemplazo atómico para evitar condiciones de carrera (TOCTOU).

## Código del Daemon (`somatic_daemon.py`)
```python
import asyncio
import json
import os
import tempfile
import time
from bleak import BleakScanner, BleakClient

HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
OUTPUT_FILE = os.path.expanduser("~/.audit/somatic_state.json")

def atomic_dump(payload: dict):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(OUTPUT_FILE))
    with os.fdopen(temp_fd, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(temp_path, OUTPUT_FILE)

def handle_hr_data(sender, data: bytearray):
    flags = data[0]
    hr = data[1] if not (flags & 0x01) else int.from_bytes(data[1:3], byteorder="little")
    payload = {
        "timestamp": time.time(),
        "bpm": hr,
        "flags": flags,
        "status": "HIGH_LOAD" if hr > 110 else "NOMINAL"
    }
    atomic_dump(payload)

async def run():
    print("Buscando emisor BLE...")
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: HR_MEASUREMENT_UUID.lower() in [u.lower() for u in ad.service_uuids]
    )
    if not device:
        print("Emisor no encontrado.")
        return
    async with BleakClient(device) as client:
        await client.start_notify(HR_MEASUREMENT_UUID, handle_hr_data)
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
```
