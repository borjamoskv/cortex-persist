# name = Brownian Motion & Gaussian Random Walk (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador melódico browniano con atracción gravitacional hacia la tónica y tonos guía.

import random
import math

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Brownian Random Walk", "Generador melódico fractal con gravedad a grados tonales.")
    form.AddInputKnob("Total Notas", 32, 8, 64)
    form.AddInputKnob("Varianza Sigma", 2.0, 0.5, 5.0)
    form.AddInputKnob("Atraccion Tonica (G)", 0.35, 0.0, 1.0)
    form.AddInputKnob("Ticks Paso", 120, 60, 480)
    form.AddInputCombo("Escala Base", "Menor Natural (A),Frigia Dominante (E),Pentatonica Menor", 0)
    return form

def generate_brownian(score_obj, num_notes=32, sigma=2.0, gravity=0.35, step_ticks=120, scale_choice=0):
    score_obj.clear()
    
    scales = [
        [45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69], # A Minor
        [40, 41, 44, 45, 47, 48, 50, 52, 53, 56, 57, 59, 60, 62, 64], # E Phrygian Dominant
        [45, 48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72],             # A Minor Pentatonic
    ]
    scale = scales[min(scale_choice, len(scales) - 1)]
    center_idx = len(scale) // 2
    current_pos = float(center_idx)
    
    current_time = 0
    ticks = int(step_ticks)
    
    for _ in range(int(num_notes)):
        # Gravitación hacia el centro / tónica
        grav_pull = -gravity * (current_pos - center_idx)
        # Paso gaussiano
        step = random.gauss(0, sigma) + grav_pull
        current_pos = max(0, min(len(scale) - 1, current_pos + step))
        
        note_idx = int(round(current_pos))
        pitch = scale[note_idx]
        
        n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
        n.number = pitch
        n.time = current_time
        n.length = int(ticks * 0.85)
        n.velocity = 0.80 + random.uniform(-0.05, 0.05)
        score_obj.addNote(n)
        
        current_time += ticks

def apply(form):
    notes = form.GetInputValue("Total Notas")
    sigma = form.GetInputValue("Varianza Sigma")
    grav = form.GetInputValue("Atraccion Tonica (G)")
    ticks = form.GetInputValue("Ticks Paso")
    sc = form.GetInputValue("Escala Base")
    generate_brownian(flp.score, notes, sigma, grav, ticks, sc)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_brownian(target_score)
