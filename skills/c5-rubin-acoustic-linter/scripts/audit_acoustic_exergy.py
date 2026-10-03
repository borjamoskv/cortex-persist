#!/usr/bin/env python3
"""
LINTER ACÚSTICO C5 (THE RUBIN ACOUSTIC AUDITOR)
Estándar C5-REAL: Medición determinista de Nata Acústica en señales de audio PCM.
"""

import sys
import numpy as np

def compute_crest_factor(samples: np.ndarray) -> float:
    peak = np.max(np.abs(samples))
    rms = np.sqrt(np.mean(samples**2))
    if rms == 0 or peak == 0:
        return 0.0
    return float(20.0 * np.log10(peak / rms))

def compute_spectral_flatness(samples: np.ndarray) -> float:
    window = np.hanning(len(samples))
    windowed = samples * window
    spectrum = np.abs(np.fft.rfft(windowed))**2
    spectrum = spectrum + 1e-12
    geom_mean = np.exp(np.mean(np.log(spectrum)))
    arith_mean = np.mean(spectrum)
    return float(geom_mean / arith_mean)

def compute_low_end_phase_coherence(left: np.ndarray, right: np.ndarray) -> float:
    num = np.sum(left * right)
    denom = np.sqrt(np.sum(left**2)) * np.sqrt(np.sum(right**2))
    if denom == 0:
        return 1.0
    return float(num / denom)

def audit_acoustic_exergy(left: np.ndarray, right: np.ndarray) -> dict:
    mono = 0.5 * (left + right)
    cf = compute_crest_factor(mono)
    sfm = compute_spectral_flatness(mono)
    lpc = compute_low_end_phase_coherence(left, right)
    
    failures = []
    if cf < 8.0:
        failures.append(f"Anergía por Hipercompresión: Crest Factor {cf:.2f} dB < 8.0 dB")
    if sfm > 0.35:
        failures.append(f"Anergía por Capas Parásitas: Spectral Flatness {sfm:.3f} > 0.35")
    if lpc < 0.85:
        failures.append(f"Anergía por Desfase Estéreo: Coherencia de Fase {lpc:.3f} < 0.85")
        
    is_pure_bone = len(failures) == 0
    return {
        "CrestFactor_dB": round(cf, 2),
        "SpectralFlatness": round(sfm, 3),
        "LowEndPhaseCoherence": round(lpc, 3),
        "Veredicto": "EXERGÍA PURA (EL HUESO)" if is_pure_bone else "NATA ACÚSTICA DETECTADA",
        "Anomalías": failures
    }

def main():
    if len(sys.argv) < 2:
        print("Uso: audit_acoustic_exergy.py <archivo.wav|--test>")
        sys.exit(1)
        
    target = sys.argv[1]
    if target == "--test":
        sr = 44100
        t = np.linspace(0, 1.0, sr, endpoint=False)
        pure = np.sin(2 * np.pi * 100 * t) * np.exp(-t * 15)
        res_pure = audit_acoustic_exergy(pure, pure)
        print("Test 1 (Hueso Seco):", res_pure)
        sludge = np.random.uniform(-0.9, 0.9, sr)
        res_sludge = audit_acoustic_exergy(sludge, sludge)
        print("Test 2 (Nata):", res_sludge)
        sys.exit(0)

    try:
        from scipy.io import wavfile
        sr, data = wavfile.read(target)
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
        elif data.dtype == np.int32:
            data = data.astype(np.float32) / 2147483648.0
            
        if data.ndim == 1:
            left, right = data, data
        else:
            left, right = data[:, 0], data[:, 1]
            
        report = audit_acoustic_exergy(left, right)
        print("\n=== REPORTE DE AUDITORÍA ACÚSTICA C5 (RUBIN LINTER) ===")
        print(f"Archivo: {target}")
        print(f"Veredicto: {report['Veredicto']}")
        print(f"Factor Cresta: {report['CrestFactor_dB']} dB")
        print(f"Planitud Espectral (Wiener): {report['SpectralFlatness']}")
        print(f"Coherencia Estéreo: {report['LowEndPhaseCoherence']}")
        if report['Anomalías']:
            print("Anomalías detectadas:")
            for anom in report['Anomalías']:
                print(f"  [!] {anom}")
        print("========================================================\n")
    except Exception as e:
        print(f"Error procesando audio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
