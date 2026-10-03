---
name: c5-rubin-acoustic-linter
display_name: Linter Acústico de Exergía y Purga de Nata (Protocolo Rubin)
description: Auditoría determinista de exergía acústica y purga de nata sónica (Protocolo Rubin). Computa Factor Cresta (WCF), Planitud Espectral de Wiener (SFM), Emborronamiento Temporal (TSI) y Coherencia de Fase Subgrave (LPC). Dispara con "linter acústico", "auditoría de mezcla", "purga de nata en audio", "rubin audit", "crest factor audio", "medir compresión".
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

## 3. Protocolo de Ejecución en Silicio

Para auditar un archivo de audio en el entorno local:

```bash
python3 ~/.gemini/config/skills/c5-rubin-acoustic-linter/scripts/audit_acoustic_exergy.py <ruta_audio.wav>
```

### Clasificación de Salida:
- Si no hay banderas activas: `EXERGÍA PURA (EL HUESO)` (El sistema preserva la señal sin grasa disipativa).
- Si hay una o más banderas: `NATA ACÚSTICA DETECTADA` (Reporte detallado de anomalías para aplicar sustracción de pistas o descompresión).
