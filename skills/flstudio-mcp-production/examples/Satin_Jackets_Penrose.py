# name = Satin Jackets Penrose Stair & Falso Drop (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador algorítmico de acordes no resolutivos (Abmaj7 -> Bb9 -> Cm9 -> Fm9) con modulación eufórica.

import random

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def createDialog():
    """Formulario interactivo nativo en FL Studio Piano Roll."""
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Satin Jackets Penrose Stair", "Bucle de acordes infinito y modulación de Tercera de Picardía.")
    form.AddInputKnob("Ciclos Penrose", 2, 1, 8)
    form.AddInputKnob("Strum Delay (Ticks)", 8, 0, 25)
    form.AddInputKnob("Humanize Vel", 0.08, 0.0, 0.25)
    form.AddInputCheckbox("Falso Drop Euforico", True)
    form.AddInputCombo("Inversiones Dinamicas", "Activadas,Desactivadas", 0)
    return form

def generate_progression(score_obj, cycles=2, strum_ticks=8, hum_vel=0.08, include_drop=True, dynamic_inv=True):
    score_obj.clear()
    BAR = 1920
    HALF_BAR = 960
    
    # 1. Abmaj7, 2. Bb9, 3. Cm9, 4. Fm9
    base_chords = [
        [56, 60, 63, 67],       # Abmaj7
        [58, 62, 65, 68, 72],   # Bb9
        [48, 51, 55, 58, 62],   # Cm9 (Tónica penúltima)
        [53, 56, 60, 63, 67],   # Fm9 (Suspensión)
    ]
    
    current_time = 0
    
    # Renderizar ciclos
    for c in range(int(cycles)):
        for chord_idx, chord in enumerate(base_chords):
            chord_notes = list(chord)
            
            # Variación de inversión en ciclos pares
            if dynamic_inv and c > 0 and c % 2 == 1 and len(chord_notes) > 2:
                chord_notes[1] += 12
                
            for n_idx, note_num in enumerate(chord_notes):
                n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                n.number = note_num
                
                # Strumming con peso físico
                delay = int(n_idx * strum_ticks)
                n.time = current_time + delay
                n.length = max(BAR - delay - random.randint(10, 40), 120)
                
                # Dinámica
                base_v = 0.82 if n_idx == 0 else 0.70
                jitter = random.uniform(-hum_vel, hum_vel)
                n.velocity = max(0.1, min(1.0, base_v + jitter))
                
                score_obj.addNote(n)
            current_time += BAR

    # Falso Drop Euforizante (Tercera de Picardía: modulación a Cmaj9)
    if include_drop:
        # Acorde de máxima tensión: Cm9 truncado a 2 tiempos (silencio dub de 2 tiempos)
        cm9_tension = [48, 60, 67, 70, 74, 79]
        for note_num in cm9_tension:
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = note_num
            n.time = current_time
            n.length = HALF_BAR - 40 # Corte súbito para la cola del delay
            n.velocity = 0.95
            score_obj.addNote(n)
            
        current_time += BAR # Deja 2 tiempos de silencio absoluto antes del drop
        
        # El Drop: Cmaj9 radiante
        c_maj9 = [36, 48, 60, 64, 67, 71, 74] # C2, C3, C4, E4, G4, B4, D5
        for n_idx, note_num in enumerate(c_maj9):
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = note_num
            n.time = current_time + (n_idx * 4)
            n.length = BAR * 2 - 40
            n.velocity = 0.98
            score_obj.addNote(n)

def apply(form):
    cycles = form.GetInputValue("Ciclos Penrose")
    strum = form.GetInputValue("Strum Delay (Ticks)")
    hum = form.GetInputValue("Humanize Vel")
    drop = form.GetInputValue("Falso Drop Euforico")
    inv = (form.GetInputValue("Inversiones Dinamicas") == 0)
    generate_progression(flp.score, cycles, strum, hum, drop, inv)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_progression(target_score)
