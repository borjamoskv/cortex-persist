# name = Xenharmonic 24-TET Makam Bayati & Slide Ornamentation (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador microtonal 24-TET en D con afinación Sikah (-50 cents) y notas slide nativas de FL Studio.

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
    form = flp.ScriptDialog("24-TET Makam Bayati Generator", "Generador de melodía microtonal árabe con notas slide nativas.")
    form.AddInputKnob("Ciclos Frase", 2, 1, 4)
    form.AddInputKnob("Tempo Division", 240, 120, 480)
    form.AddInputCheckbox("Slide Glissando", True)
    form.AddInputCombo("Modo Xenarmonico", "Makam Bayati (D),Makam Rast (C),Locrian Neutral 2nd", 0)
    return form

def generate_microtonal_melody(score_obj, cycles=2, ticks_per_note=240, use_slides=True, mode_type=0):
    score_obj.clear()
    
    # Definición de escalas microtonales: pitch MIDI base + offset en cents (-100 a +100)
    if mode_type == 0:
        # Makam Bayati en D: D, E half-flat (-50c), F, G, A, Bb, C, D
        scale = [
            (62, 0),     # D4
            (64, -50),   # E4 half-flat (Sikah)
            (65, 0),     # F4
            (67, 0),     # G4
            (69, 0),     # A4
            (70, 0),     # Bb4
            (69, 0),     # A4
            (67, 0),     # G4
            (65, 0),     # F4
            (64, -50),   # E4 half-flat
            (62, 0),     # D4
            (60, 0),     # C4
            (62, 0),     # D4 (Resolución)
        ]
    elif mode_type == 1:
        # Makam Rast en C: C, D, E half-flat (-50c), F, G, A, B half-flat (-50c), C
        scale = [
            (60, 0),
            (62, 0),
            (64, -50),
            (65, 0),
            (67, 0),
            (69, 0),
            (71, -50),
            (72, 0),
            (69, 0),
            (67, 0),
            (64, -50),
            (60, 0),
        ]
    else:
        # Locrian Neutral 2nd: D, Eb half-flat (-50c), F, G, Ab, Bb, C, D
        scale = [
            (62, 0),
            (63, -50),
            (65, 0),
            (67, 0),
            (68, 0),
            (70, 0),
            (72, 0),
            (68, 0),
            (63, -50),
            (62, 0),
        ]
        
    current_time = 0
    ticks = int(ticks_per_note)
    
    for c in range(int(cycles)):
        for step_idx, (pitch, fine_tune) in enumerate(scale):
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = pitch
            n.time = current_time
            n.length = int(ticks * 0.85)
            n.velocity = 0.85 if step_idx == 0 else 0.75
            
            # Aplicar microtonalidad nativa de FL Studio
            if hasattr(n, 'pitchoffset'):
                n.pitchoffset = int(fine_tune)
                
            score_obj.addNote(n)
            
            # Ornamentación slide: agregar micro-slide hacia notas con fine tuning
            if use_slides and HAS_FLPIANOROLL and fine_tune != 0 and (step_idx % 3 == 0):
                slide_n = flp.Note()
                slide_n.number = pitch + (1 if fine_tune < 0 else -1)
                slide_n.time = current_time + int(ticks * 0.4)
                slide_n.length = int(ticks * 0.4)
                slide_n.velocity = 0.80
                slide_n.slide = True # Nota slide nativa FL Studio
                score_obj.addNote(slide_n)
                
            current_time += ticks

def apply(form):
    cycles = form.GetInputValue("Ciclos Frase")
    ticks = form.GetInputValue("Tempo Division")
    slides = form.GetInputValue("Slide Glissando")
    mtype = form.GetInputValue("Modo Xenarmonico")
    generate_microtonal_melody(flp.score, cycles, ticks, slides, mtype)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_microtonal_melody(target_score)
