# name = AIR Moon Safari Space-Pop Rhodes (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador armónico Space-Pop estilo AIR (Am9 -> D9 -> Fmaj7 -> E7#9) con micro-timing y panorámica estéreo.

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
    form = flp.ScriptDialog("AIR Moon Safari Voicings", "Motor armónico Space-Pop / French Touch con humanización Rhodes.")
    form.AddInputKnob("Compases Repeticion", 2, 1, 4)
    form.AddInputKnob("Rhodes Microtiming", 12, 0, 30)
    form.AddInputKnob("Stereo Tremolo Depth", 0.35, 0.0, 1.0)
    form.AddInputCheckbox("Bajo Minimoog Separado", True)
    return form

def generate_air_chords(score_obj, repetitions=2, microtiming=12, pan_depth=0.35, separate_bass=True):
    score_obj.clear()
    BAR = 1920
    
    # Voicings extendidos estilo AIR (Moon Safari):
    # 1. Am9:    A1 (bajo) + G3, C4, E4, B4
    # 2. D9:     D2 (bajo) + F#3, C4, E4, A4
    # 3. Fmaj7:  F1 (bajo) + A3, C4, E4, G4 (add9)
    # 4. E7(#9): E1 (bajo) + G#3, D4, G4 (Hendrix chord / French Touch)
    progression = [
        {"bass": 33, "keys": [55, 60, 64, 71]},
        {"bass": 38, "keys": [54, 60, 64, 69]},
        {"bass": 29, "keys": [57, 60, 64, 67]},
        {"bass": 28, "keys": [56, 62, 67, 75]},
    ]
    
    current_time = 0
    for rep in range(int(repetitions)):
        for idx, chord in enumerate(progression):
            # Bajo Minimoog (Color 1 para ruteo opcional a otro sintetizador)
            if separate_bass:
                b = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                b.number = chord["bass"]
                b.time = current_time
                b.length = BAR - 30
                b.velocity = 0.88
                b.pan = 0.0 # Bajo en el centro acústico
                if HAS_FLPIANOROLL and hasattr(b, 'color'):
                    b.color = 1 # Canal MIDI 2 / Color verde
                score_obj.addNote(b)
                
            # Teclado Rhodes con micro-timing orgánico y apertura estéreo
            pan_sign = 1 if idx % 2 == 0 else -1
            for k_idx, note_num in enumerate(chord["keys"]):
                k = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                k.number = note_num
                jitter = random.randint(-int(microtiming), int(microtiming))
                k.time = max(0, current_time + (k_idx * 6) + jitter)
                k.length = BAR - 50
                k.velocity = 0.72 + random.uniform(-0.06, 0.06)
                k.pan = max(-1.0, min(1.0, (pan_sign * pan_depth) + (k_idx * 0.05)))
                if HAS_FLPIANOROLL and hasattr(k, 'color'):
                    k.color = 0 # Canal MIDI 1 / Color principal
                score_obj.addNote(k)
                
            current_time += BAR

def apply(form):
    rep = form.GetInputValue("Compases Repeticion")
    mt = form.GetInputValue("Rhodes Microtiming")
    pan = form.GetInputValue("Stereo Tremolo Depth")
    bass = form.GetInputValue("Bajo Minimoog Separado")
    generate_air_chords(flp.score, rep, mt, pan, bass)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_air_chords(target_score)
