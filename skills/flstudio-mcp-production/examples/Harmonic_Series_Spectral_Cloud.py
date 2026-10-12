# name = Harmonic Series Spectral Cloud Generator (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador espectral de parciales de la serie armónica (1 a 16) con microtonalidad sub-cent y disipación natural.

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
    form = flp.ScriptDialog("Spectral Harmonic Cloud", "Sintetizador de acordes espectrales puros según la serie armónica.")
    form.AddInputKnob("Fundamental MIDI", 36, 24, 60)
    form.AddInputKnob("Num Parciales", 12, 4, 16)
    form.AddInputKnob("Duracion Compas (Ticks)", 1920, 960, 7680)
    form.AddInputKnob("Exponente Decaimiento Vel", 0.65, 0.2, 1.5)
    form.AddInputCheckbox("Afinacion Microtonal Pura", True)
    return form

def generate_spectral_cloud(score_obj, root_midi=36, partials=12, bar_ticks=1920, decay_exp=0.65, pure_tuning=True):
    score_obj.clear()
    
    # Frecuencia de la fundamental
    f0 = 440.0 * (2.0 ** ((root_midi - 69.0) / 12.0))
    
    for n in range(1, int(partials) + 1):
        fn = n * f0
        exact_midi = 69.0 + 12.0 * math.log2(fn / 440.0)
        nominal_pitch = int(round(exact_midi))
        fine_cents = int(round((exact_midi - nominal_pitch) * 100.0))
        
        note = flp.Note() if HAS_FLPIANOROLL else utils.Note()
        note.number = nominal_pitch
        note.time = (n - 1) * 8 # Strumming acústico de propagación
        
        # Longitud proporcional a la resonancia (armónicos altos decaen antes)
        decay_factor = (1.0 / (n ** 0.35))
        note.length = max(240, int(bar_ticks * decay_factor))
        
        # Velocidad según modelo de disipación acústica
        note.velocity = max(0.15, min(1.0, 1.0 / (n ** decay_exp)))
        
        # Paneo distribuido espectralmente
        note.pan = ((n % 4) - 1.5) / 2.0
        
        if pure_tuning and HAS_FLPIANOROLL and hasattr(note, 'pitchoffset'):
            note.pitchoffset = fine_cents
            
        score_obj.addNote(note)

def apply(form):
    root = form.GetInputValue("Fundamental MIDI")
    parts = form.GetInputValue("Num Parciales")
    ticks = form.GetInputValue("Duracion Compas (Ticks)")
    d_exp = form.GetInputValue("Exponente Decaimiento Vel")
    pt = form.GetInputValue("Afinacion Microtonal Pura")
    generate_spectral_cloud(flp.score, root, parts, ticks, d_exp, pt)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_spectral_cloud(target_score)
