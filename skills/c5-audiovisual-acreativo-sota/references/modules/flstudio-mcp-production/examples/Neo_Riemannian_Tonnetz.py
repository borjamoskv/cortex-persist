# name = Neo-Riemannian Tonnetz Harmonic Explorer (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Explorador armónico sobre el Tonnetz mediante transformaciones P (Paralelo), L (Leittonwechsel) y R (Relativo).

import random

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def p_transform(triad, is_major):
    # P: Mueve la tercera 1 semitono abajo si es mayor, o 1 arriba si es menor
    root, third, fifth = triad
    return [root, third - 1 if is_major else third + 1, fifth], not is_major

def l_transform(triad, is_major):
    # L: Si mayor, raíz baja 1 semitono. Si menor, quinta sube 1 semitono
    root, third, fifth = triad
    if is_major:
        return [third, fifth, root + 11], False
    else:
        return [root, third, fifth + 1], True

def r_transform(triad, is_major):
    # R: Si mayor, quinta sube 2 semitonos. Si menor, raíz baja 2 semitonos
    root, third, fifth = triad
    if is_major:
        return [root, third, fifth + 2], False
    else:
        return [root - 2, third, fifth], True

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Neo-Riemannian Tonnetz", "Caminata armónica cinematográfica mediante operaciones P, L, R.")
    form.AddInputKnob("Pasos en el Tonnetz", 8, 4, 16)
    form.AddInputKnob("Duracion Acorde (Ticks)", 1920, 960, 3840)
    form.AddInputKnob("Strum Spread (Ticks)", 10, 0, 30)
    form.AddInputCombo("Secuencia Transformacion", "P-L-P-L (Bucle Hexatónico),P-R-P-R (Bucle Octatónico),Aleatorio Cinemático", 2)
    return form

def generate_tonnetz_walk(score_obj, steps=8, chord_duration=1920, strum=10, seq_mode=2):
    score_obj.clear()
    
    # Triada inicial: C Mayor (C4=60, E4=64, G4=67)
    current_triad = [60, 64, 67]
    is_major = True
    
    current_time = 0
    ticks = int(chord_duration)
    
    for i in range(int(steps)):
        # Añadir bajo en la fundamental (2 octavas abajo)
        root_bass = current_triad[0] - 24
        b = flp.Note() if HAS_FLPIANOROLL else utils.Note()
        b.number = root_bass
        b.time = current_time
        b.length = ticks - 60
        b.velocity = 0.88
        score_obj.addNote(b)
        
        # Notas del acorde ordenadas
        sorted_notes = sorted(current_triad)
        for v_idx, pitch in enumerate(sorted_notes):
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = pitch
            n.time = current_time + (v_idx * int(strum))
            n.length = max(120, ticks - (v_idx * int(strum)) - 60)
            n.velocity = 0.75 + random.uniform(-0.04, 0.04)
            score_obj.addNote(n)
            
        # Elegir transformación
        if seq_mode == 0:
            op = 'P' if (i % 2 == 0) else 'L'
        elif seq_mode == 1:
            op = 'P' if (i % 2 == 0) else 'R'
        else:
            op = random.choice(['P', 'L', 'R'])
            
        if op == 'P':
            current_triad, is_major = p_transform(current_triad, is_major)
        elif op == 'L':
            current_triad, is_major = l_transform(current_triad, is_major)
        else:
            current_triad, is_major = r_transform(current_triad, is_major)
            
        # Normalizar octavas para evitar derivas extremas
        current_triad = [((p - 48) % 12) + 60 for p in current_triad]
        current_time += ticks

def apply(form):
    st = form.GetInputValue("Pasos en el Tonnetz")
    dur = form.GetInputValue("Duracion Acorde (Ticks)")
    strum = form.GetInputValue("Strum Spread (Ticks)")
    seq = form.GetInputValue("Secuencia Transformacion")
    generate_tonnetz_walk(flp.score, st, dur, strum, seq)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_tonnetz_walk(target_score)
