# name = Markov Chain Stochastic Melody Engine (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador estocástico de melodías mediante matrices de transición de Markov de primer orden.

import random

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Markov Chain Melody Engine", "Generador melódico estocástico con sesgo a grados tonales.")
    form.AddInputKnob("Notas Totales", 32, 8, 64)
    form.AddInputKnob("Ticks por Nota", 240, 60, 480)
    form.AddInputKnob("Probabilidad de Salto", 0.25, 0.05, 0.70)
    form.AddInputCombo("Modo Tonal", "Eolico (Menor Natural),Dórico,Lidio,Kurd Arabe", 0)
    return form

def generate_markov_melody(score_obj, num_notes=32, ticks_per_note=240, leap_prob=0.25, mode_idx=0):
    score_obj.clear()
    
    # Grados de escala sobre C4 (60)
    modes = [
        [60, 62, 63, 65, 67, 68, 70, 72, 74, 75], # Aeolian
        [60, 62, 63, 65, 67, 69, 70, 72, 74, 75], # Dorian
        [60, 62, 64, 66, 67, 69, 71, 72, 74, 76], # Lydian
        [60, 61, 63, 65, 67, 68, 70, 72, 73, 75], # Kurd
    ]
    scale = modes[min(mode_idx, len(modes) - 1)]
    
    current_idx = 0 # Inicia en tónica
    current_time = 0
    ticks = int(ticks_per_note)
    
    for i in range(int(num_notes)):
        pitch = scale[current_idx]
        
        n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
        n.number = pitch
        n.time = current_time
        n.length = int(ticks * random.uniform(0.7, 0.95))
        # Dinámica con acento en tiempos fuertes
        is_downbeat = (current_time % 960 == 0)
        n.velocity = 0.88 if is_downbeat else random.uniform(0.68, 0.78)
        score_obj.addNote(n)
        
        # Transición de Markov:
        # Mayor probabilidad de movimiento por grados conjuntos (+/- 1)
        # Menor probabilidad de salto armónico (+/- 2 o +/- 4) con resolución en contrasentido
        if random.random() < leap_prob:
            leap_dir = 1 if current_idx < len(scale) // 2 else -1
            current_idx = max(0, min(len(scale) - 1, current_idx + (leap_dir * random.choice([2, 3, 4]))))
        else:
            step = random.choice([-1, 1, 1, -1, 0]) # Sesgo dinámico
            current_idx = max(0, min(len(scale) - 1, current_idx + step))
            
        current_time += ticks

def apply(form):
    notes = form.GetInputValue("Notas Totales")
    ticks = form.GetInputValue("Ticks por Nota")
    leap = form.GetInputValue("Probabilidad de Salto")
    m = form.GetInputValue("Modo Tonal")
    generate_markov_melody(flp.score, notes, ticks, leap, m)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_markov_melody(target_score)
