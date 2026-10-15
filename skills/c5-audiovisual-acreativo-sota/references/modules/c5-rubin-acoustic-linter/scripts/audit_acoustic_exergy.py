#!/usr/bin/env python3
"""
LINTER ACÚSTICO C5 (THE RUBIN ACOUSTIC AUDITOR)
Estándar C5-REAL: Medición determinista de Nata Acústica en señales de audio PCM.
"""

import sys
import numpy as np

from scipy import signal

def compute_crest_factor(samples: np.ndarray) -> float:
    peak = float(np.max(np.abs(samples)))
    rms = float(np.sqrt(np.mean(samples**2)))
    if rms == 0 or peak == 0:
        return 0.0
    return float(20.0 * np.log10(peak / rms))

def compute_spectral_flatness_mid(samples: np.ndarray, fs: int = 48000) -> float:
    """
    Entropía de Wiener / Spectral Flatness en banda media [500 Hz, 5000 Hz] vía Welch PSD.
    Evita el colapso numérico a 0.0 de FFTs globales sobre bandas atenuadas por filtros.
    """
    nperseg = min(len(samples), 2048)
    if nperseg < 64:
        return 0.0
    freqs, psd = signal.welch(samples, fs=fs, nperseg=nperseg, noverlap=nperseg // 2)
    mid_mask = (freqs >= 500.0) & (freqs <= 5000.0)
    if not np.any(mid_mask):
        mid_mask = freqs > 0.0
    mid_psd = psd[mid_mask]
    total_band_energy = float(np.sum(mid_psd))
    if total_band_energy < 1e-9:
        return 0.0001
    mid_psd_reg = mid_psd + 1e-12
    geom_mean = float(np.exp(np.mean(np.log(mid_psd_reg))))
    arith_mean = float(np.mean(mid_psd_reg))
    if arith_mean <= 0.0:
        return 0.0001
    return float(geom_mean / arith_mean)

def compute_low_end_phase_coherence(left: np.ndarray, right: np.ndarray, fs: int = 48000) -> float:
    """
    Correlación estéreo en la banda de subgrave (< 120 Hz) según la especificación Rubin.
    """
    nyq = 0.5 * fs
    cutoff = min(120.0, nyq - 10.0)
    sos_low = signal.butter(4, cutoff / nyq, btype="low", output="sos")
    low_l = signal.sosfilt(sos_low, left)
    low_r = signal.sosfilt(sos_low, right)
    num = float(np.sum(low_l * low_r))
    denom = float(np.sqrt(np.sum(low_l**2)) * np.sqrt(np.sum(low_r**2)))
    if denom <= 1e-12:
        return 1.0
    return float(num / denom)

def compute_temporal_smearing_index(samples: np.ndarray, fs: int = 48000) -> float:
    """
    Temporal Smearing Index (TSI): Mide la energía residual en [50 ms, 150 ms] tras transitorios.
    """
    rms = float(np.sqrt(np.mean(samples**2)))
    if rms <= 1e-6:
        return 0.0
    threshold = 3.0 * rms
    transients = np.where(np.abs(samples) > threshold)[0]
    if len(transients) == 0:
        return 0.10
    
    t_start = int(0.050 * fs)
    t_end = int(0.150 * fs)
    tail_ratios = []
    # Muestrear hasta 10 transitorios aislados
    step = max(1, len(transients) // 10)
    for idx in transients[::step]:
        if idx + t_end < len(samples):
            peak_energy = float(samples[idx]**2)
            tail_energy = float(np.mean(samples[idx + t_start:idx + t_end]**2))
            if peak_energy > 0:
                tail_ratios.append(min(1.0, tail_energy / peak_energy))
    return float(np.mean(tail_ratios)) if tail_ratios else 0.12

def audit_acoustic_exergy(left: np.ndarray, right: np.ndarray, fs: int = 48000) -> dict:
    mono = 0.5 * (left + right)
    cf = compute_crest_factor(mono)
    sfm = compute_spectral_flatness_mid(mono, fs=fs)
    lpc = compute_low_end_phase_coherence(left, right, fs=fs)
    tsi = compute_temporal_smearing_index(mono, fs=fs)
    peak = float(np.max(np.abs(mono)))
    true_peak_dbfs = float(20.0 * np.log10(max(1e-6, peak)))
    
    failures = []
    if cf < 8.0:
        failures.append(f"Anergía por Hipercompresión: Crest Factor {cf:.2f} dB < 8.0 dB")
    if sfm > 0.35:
        failures.append(f"Anergía por Capas Parásitas / Ruido: Spectral Flatness (500-5000Hz) {sfm:.4f} > 0.35")
    if lpc < 0.85:
        failures.append(f"Anergía por Desfase en Subgrave: LPC (<120Hz) {lpc:.3f} < 0.85")
    if tsi > 0.65:
        failures.append(f"Anergía por Emborronamiento Temporal: TSI {tsi:.3f} > 0.65")
        
    is_pure_bone = len(failures) == 0

    # Puntuación Exergética Derivada (1 a 21.000)
    # 21.000 = Hueso acústico puro (CF >= 14 dB, SFM < 0.05, LPC >= 0.98, TSI < 0.30)
    score = 21000.0
    if cf < 14.0:
        score -= min(3000.0, (14.0 - cf) * 350.0)
    if sfm > 0.02:
        score -= min(4000.0, (sfm - 0.02) * 12000.0)
    if lpc < 0.98:
        score -= min(3000.0, (0.98 - lpc) * 15000.0)
    if tsi > 0.25:
        score -= min(2000.0, (tsi - 0.25) * 4000.0)
    score = max(1000.0, min(21000.0, score))

    return {
        "CrestFactor_dB": round(cf, 2),
        "SpectralFlatness": round(sfm, 4),
        "LowEndPhaseCoherence": round(lpc, 4),
        "TemporalSmearingIndex": round(tsi, 3),
        "TruePeak_dBFS": round(true_peak_dbfs, 2),
        "ExergyScore_21k": int(round(score)),
        "Veredicto": "EXERGÍA PURA (EL HUESO)" if is_pure_bone else "NATA ACÚSTICA DETECTADA",
        "Anomalías": failures
    }

def main():
    if len(sys.argv) < 2:
        print("Uso: audit_acoustic_exergy.py <archivo.wav|--test>")
        sys.exit(1)
        
    target = sys.argv[1]
    if target == "--test":
        sr = 48000
        t = np.linspace(0, 1.0, sr, endpoint=False)
        pure = (np.sin(2 * np.pi * 440 * t) + 0.4 * np.sin(2 * np.pi * 880 * t)) * np.exp(-t * 8)
        res_pure = audit_acoustic_exergy(pure, pure, fs=sr)
        print("Test 1 (Hueso Seco):", res_pure)
        sludge = np.random.uniform(-0.9, 0.9, sr)
        res_sludge = audit_acoustic_exergy(sludge, sludge, fs=sr)
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
            
        report = audit_acoustic_exergy(left, right, fs=sr)
        print("\n=== REPORTE DE AUDITORÍA ACÚSTICA C5 (RUBIN LINTER) ===")
        print(f"Archivo: {target}")
        print(f"Frecuencia de Muestreo: {sr} Hz")
        print(f"Veredicto: {report['Veredicto']}")
        print(f"Puntuación Exergética: {report['ExergyScore_21k']} / 21.000")
        print(f"Factor Cresta (WCF): {report['CrestFactor_dB']} dB")
        print(f"Planitud Espectral (Wiener 500-5000Hz): {report['SpectralFlatness']}")
        print(f"Coherencia Estéreo Subgrave (<120Hz): {report['LowEndPhaseCoherence']}")
        print(f"Índice Emborronamiento Temporal (TSI): {report['TemporalSmearingIndex']}")
        print(f"True Peak: {report['TruePeak_dBFS']} dBFS")
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
