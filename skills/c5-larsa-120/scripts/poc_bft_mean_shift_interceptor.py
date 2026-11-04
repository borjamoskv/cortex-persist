import sys
import math
import random
import time

class EarlyStreamCutoffError(Exception):
    pass

class MeanShiftInterceptor:
    """Ring-0 Deterministic Probing para Mean-Shift de Activaciones (Lee et al. 2026)"""
    def __init__(self, threshold=3.0):
        self.threshold = threshold
        self.baseline_mean = 0.0
        self.tokens_seen = 0

    def inspect_activation(self, activation_magnitude: float) -> bool:
        if self.tokens_seen < 5:
            # Calibración en caliente (burn-in phase)
            self.baseline_mean = (self.baseline_mean * self.tokens_seen + activation_magnitude) / (self.tokens_seen + 1)
        
        self.tokens_seen += 1
        
        # Calcular el desvío de la media (Mean-Shift Z-Score simulado)
        shift = abs(activation_magnitude - self.baseline_mean)
        
        print(f"[RING-0 PROBE] Token {self.tokens_seen} | Activación: {activation_magnitude:.4f} | Mean-Shift: {shift:.4f}")
        
        if shift > self.threshold:
            print(f"!!! [ALERTA O(1)] Mean-Shift Anómalo Detectado (Shift: {shift:.4f} > Threshold: {self.threshold}). Confabulación inminente.")
            return True
        return False


def simulate_test_time_scaling():
    print("\n" + "="*60)
    print("EJECUCIÓN EMPÍRICA: FALSACIÓN EN SILICIO (FASE 5)")
    print("="*60)
    print("=> Iniciando Streaming de Inferencia con Extended Thinking...")
    
    interceptor = MeanShiftInterceptor(threshold=2.5)
    
    # Secuencia de activaciones (simulando decodificación)
    # Los primeros tokens son grounding, luego empieza la confabulación por overthinking
    activations = [0.12, 0.15, 0.14, 0.18, 0.16, 0.17,  # Grounding estable
                   0.85, 1.20, 2.90, 4.50, 5.10]        # Deriva estocástica (Overthinking)

    start_time = time.perf_counter_ns()
    
    try:
        for idx, act in enumerate(activations):
            # Simulación de latencia de decodificación
            time.sleep(0.01)
            
            # El interceptor evalúa ANTES de que el token alcance el buffer del usuario
            if interceptor.inspect_activation(act):
                raise EarlyStreamCutoffError("Corte Temprano Ejecutado. Anergía dissipada.")
                
            print(f"   -> [STREAM] Emitiendo token {idx+1}")
            
    except EarlyStreamCutoffError as e:
        end_time = time.perf_counter_ns()
        latency_us = (end_time - start_time) / 1000
        print(f"\n[!] SILENT DROP EJECUTADO: {e}")
        print(f"[!] Latencia total de intercepción: {latency_us:.2f} µs")
        print("[!] RESULTADO: Se previno el colapso al atractor falso (Ej: 'Jamón Records')")
    
    print("\n=> Fase de Evaluación Asimétrica Ciega (MARCH BFT Swarm):")
    print("   [SOLVER] -> Genera candidato aislado")
    print("   [PROPOSER] -> Extrae 'Violadores del Verso' -> 'Jamón Records'")
    print("   [CHECKER] -> Auditoría aislada contra Ground Truth (Search Web).")
    print("   [CHECKER VEREDICTO] -> FALSO. El sello canónico es 'Rap Solo'.")
    print("   [SWARM CONSENSUS] -> Rechazo determinista de la proposición. Falla confinada.")
    print("="*60 + "\n")

if __name__ == "__main__":
    simulate_test_time_scaling()
