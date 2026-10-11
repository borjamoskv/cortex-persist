---
name: c5-rubin-acoustic-linter
display_name: Linter Acústico de Exergía y Purga de Nata (Protocolo Rubin)
description: Auditoría determinista de exergía acústica, purga de nata sónica (Protocolo Rubin), colapso de duplicados vía APFS clonefile(2) y poda jerárquica de fenotipos (WAV/FLAC/MP3). Computa WCF, SFM, TSI, LPC. Dispara con "linter acústico", "auditoría de mezcla", "purga de nata en audio", "rubin audit", "fenotipos distintos", "dedup apfs audio", "poda de fenotipos", "crest factor audio", "medir compresión".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# C5-REAL Rubin Acoustic Linter (Auditoría de Nata Sonora)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

## 1. Fundamento Operativo (La Ley de Rubin)
Toda señal de audio, mezcla musical o masterización debe someterse a la cota termodinámica de sustracción (*«Subtraction beats Addition»*):
- La acumulación de capas no ortogonales y la compresión agresiva degradan la relación señal/ruido perceptual y saturan el oído humano por fatiga (reflejo estapedial).
- El **Linter Acústico C5** evalúa cuatro invariantes físicas para emitir un diagnóstico binario O(1): `EXERGÍA PURA (EL HUESO)` frente a `NATA ACÚSTICA DETECTADA`.

---

## 2. Las 4 Métricas Físicas Canónicas

1. **Weighted Crest Factor (WCF):**
   - Fórmula: CF = 20 · log_10 ( max |x[n]| / RMS(x) )
   - Umbral de Nata: CF < 8.0 dB (hipercompresión por limitadores *brickwall*).
   - Umbral de Exergía: CF ≥ 12.0 dB (preservación de transitorios dinámicos).

2. **Spectral Flatness Measure (SFM / Entropía de Wiener):**
   - Fórmula: SFM = exp( (1/N) ∑ ln S(f) ) / ( (1/N) ∑ S(f) )
   - Umbral de Nata: SFM > 0.35 en la banda media (500 Hz a 5.000 Hz), denotando ruido blanco, pads continuos y saturación espectral.
   - Umbral de Exergía: SFM < 0.15 (formantes definidos y separación armónica).

3. **Temporal Smearing Index (TSI):**
   - Mide la energía residual en [50 ms, 150 ms] tras un transitorio de ataque (|x[n]| > 3 · RMS).
   - En tempos rápidos (≥ 180 BPM), si TSI > 0.60, se declara violación de la regla de convolución temporal (emborronamiento de transitorios).

4. **Low-End Phase Coherence (LPC):**
   - Correlación estéreo en la banda < 120 Hz: LPC = (L · R) / (||L|| · ||R||).
   - Umbral estricto: LPC ≥ 0.98. Si LPC < 0.85, se diagnostica cancelación destructiva en bajas frecuencias.

---

## 3. Protocolo de Ejecución en Silicio (`rubin_protocol.py` SOTA)

Para auditar un archivo de audio en el entorno local con salida humana o JSON estructurado:

```bash
# Auditoría estándar con informe en terminal y veredicto
python3 scripts/rubin_protocol.py <ruta_audio.mp3|wav|flac>

# Modo JSON estructurado para integración agéntica y CI/CD
python3 scripts/rubin_protocol.py <ruta_audio> --json

# Modo fail-closed estricto (código de salida 1 si se detecta nata)
python3 scripts/rubin_protocol.py <ruta_audio> --fail-closed --territory streaming
```

### Contrato de Salida JSON y Escala de Exergía (21.000):
```json
{
  "verdict": "EXERGÍA PURA (EL HUESO)" | "NATA ACÚSTICA DETECTADA",
  "is_pure_bone": true | false,
  "exergy_score_21k": 20648,
  "metrics": {
    "crest_factor_db": 16.9,
    "spectral_flatness_mid": 0.0451,
    "temporal_smearing_index": 0.644,
    "low_end_phase_coherence": 1.0,
    "true_peak_dbfs": -1.46
  },
  "anomalies": [],
  "subtraction_recommendations": []
}
```

### Integración en Motores de Estudio (`StudioAssetAuditor`):
Los motores de validación de proyectos (como `itera_100.py`) integran el Protocolo Rubin mediante sondeo determinista de subproceso, asignando badges visuales (`[PURISMO ACÚSTICO]` vs. `[NATA LEVE]`) y bloqueando la entrega humana si el score exergético colapsa por debajo de $18.000 / 21.000$.

---

## 4. Geometría de Almacenamiento y Colapso por APFS Clones

Cuando existen archivos idénticos en disco (mismo SHA-256):
- **Prohibición de Hardlinks (`ln`):** Un hardlink acopla mutaciones destructivas entre proyectos DAW (FL Studio).
- **Invariante CoW (`clonefile(2)`):** La deduplicación en macOS debe ejecutarse con `cp -c` (APFS clone). Libera espacio físico manteniendo independencia de mutación y preservando `xattr` de macOS.

---

## 5. Jerarquía Termodinámica de Fenotipos Acústicos

Cuando múltiples formatos del mismo render coexisten en el mismo directorio:
1. **Genotipo Maestro (WAV / AIFF):** Señal PCM pura sin pérdidas. Trabajo en DAW. *Invariante intocable.*
2. **Fenotipo de Distribución (FLAC):** Compresión de Kolmogorov óptima sin pérdida ($K(\sigma) \approx \min$). *Preservar para archivo.*
3. **Fenotipo de Interfaz / Nata Psicoacústica (MP3 / M4A):** Señal degradada por pérdidas irreversibles. Si existe el genotipo maestro (WAV/FLAC) en el mismo árbol, el MP3 es anergía redundante y debe someterse a apoptosis.

