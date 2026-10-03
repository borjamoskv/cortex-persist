# name = Bill Evans Rootless Jazz Voicings Engine (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Voicings de jazz sin fundamental (Type A y Type B) para progresiones ii-V-I con conducción de voces minimalista.

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
    form = flp.ScriptDialog("Bill Evans Rootless Voicings", "Motor de armonía Jazz con conducción de voces Type A / Type B.")
    form.AddInputCombo("Tonalidad Base", "C Mayor,F Mayor,Bb Mayor,Eb Mayor,G Mayor", 0)
    form.AddInputKnob("Compases por Acorde", 1, 1, 2)
    form.AddInputKnob("Strumming Jazz (Ticks)", 12, 0, 30)
    form.AddInputCheckbox("Incluir Walking Bass", True)
    return form

def generate_rootless_jazz(score_obj, key_idx=0, bars_per_chord=1, strum=12, include_bass=True):
    score_obj.clear()
    BAR = 1920
    chord_ticks = int(bars_per_chord) * BAR
    
    # Raíces de ii-V-I en semitonos sobre C
    key_offsets = [0, 5, 10, 3, 7] # C, F, Bb, Eb, G
    k_off = key_offsets[min(key_idx, len(key_offsets) - 1)]
    
    # Definición de ii-V-I en C:
    # ii (Dm9):  F4 (65), A4 (69), C5 (72), E5 (76)  -> Type A (3-5-7-9)
    # V  (G13):  F4 (65), A4 (69), B4 (71), E5 (76)  -> Type B (7-9-3-13)
    # I  (Cmaj9): E4 (64), G4 (67), B4 (71), D5 (74)  -> Type A (3-5-7-9)
    progression = [
        {"root": 38 + k_off, "voicings": [65 + k_off, 69 + k_off, 72 + k_off, 76 + k_off]}, # ii
        {"root": 43 + k_off, "voicings": [65 + k_off, 69 + k_off, 71 + k_off, 76 + k_off]}, # V
        {"root": 36 + k_off, "voicings": [64 + k_off, 67 + k_off, 71 + k_off, 74 + k_off]}, # I
    ]
    
    current_time = 0
    for chord in progression:
        # Walking Bass / Root
        if include_bass:
            b = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            b.number = chord["root"]
            b.time = current_time
            b.length = chord_ticks - 80
            b.velocity = 0.86
            score_obj.addNote(b)
            
        # Voicing con Strumming
        for v_idx, pitch in enumerate(chord["voicings"]):
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = pitch
            n.time = current_time + (v_idx * int(strum))
            n.length = chord_ticks - (v_idx * int(strum)) - 80
            n.velocity = 0.70 + random.uniform(-0.04, 0.04)
            score_obj.addNote(n)
            
        current_time += chord_ticks

def apply(form):
    k = form.GetInputValue("Tonalidad Base")
    b = form.GetInputValue("Compases por Acorde")
    s = form.GetInputValue("Strumming Jazz (Ticks)")
    wb = form.GetInputValue("Incluir Walking Bass")
    generate_rootless_jazz(flp.score, k, b, s, wb)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_rootless_jazz(target_score)
