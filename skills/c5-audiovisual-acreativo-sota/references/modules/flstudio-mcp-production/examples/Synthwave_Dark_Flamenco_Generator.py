# name = Synthwave Dark Flamenco Masterpiece (v3.0)
# author = Moskv-1 (C5-REAL)
# description = Generador de la obra completa de 64 compases (o secciones individuales) de Synthwave x Flamenco Oscuro en Re Frigio Dominante.

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
    form = flp.ScriptDialog("Dark Cyber-Flamenco", "Obra completa (64 compases) o secciones individuales de Synthwave x Flamenco.")
    form.AddInputCombo("Sección a Generar", 
                       "Obra Completa (64c con Marcadores)," + 
                       "1. Intro Atmosférica (8c)," + 
                       "2. Desarrollo Bajo Rodante (8c)," + 
                       "3. Tensión & Corte Frigio (8c)," + 
                       "4. Drop 1 Danza Cíborg (16c)," + 
                       "5. Breakdown Falseta Rubato (8c)," + 
                       "6. Build 2 Amalgama Bulerías (8c)," + 
                       "7. Climax Tercera de Picardía (8c)", 0)
    form.AddInputCombo("Canal / Articulación", "Todas las Capas (Multi-Color),Bajo Rodante (Verde),Chords Rasgueados (Naranja),Melodía / Falseta (Rojo),Percusión / Palmas (Amarillo)", 0)
    form.AddInputKnob("Velocidad Rasgueado (Ticks)", 14, 6, 26)
    form.AddInputCheckbox("Slide Glissandos Expresivos", True)
    return form

def add_note_safe(score_obj, pitch, time_t, length_t, vel=0.85, pan=0.0, color_idx=0, is_slide=False):
    n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
    n.number = pitch
    n.time = max(0, int(time_t))
    n.length = max(30, int(length_t))
    n.velocity = max(0.1, min(1.0, vel))
    n.pan = max(-1.0, min(1.0, pan))
    if HAS_FLPIANOROLL:
        if hasattr(n, 'color'):
            n.color = color_idx
        if is_slide and hasattr(n, 'slide'):
            n.slide = True
    score_obj.addNote(n)

def generate_masterpiece(score_obj, section_choice=0, channel_mode=0, strum_ticks=14, use_slides=True):
    score_obj.clear()
    
    BAR = 1920
    PPQ = 480
    SIXTEENTH = 120
    
    # Armonía base Re Frigia Dominante: Gm9, Fmaj7, Ebmaj7(#11), D7(b9)
    cadence = [
        {"root": 31, "chord": [55, 58, 62, 65, 69]}, # Gm9
        {"root": 29, "chord": [53, 57, 60, 64, 67]}, # Fmaj7
        {"root": 27, "chord": [51, 55, 58, 62, 69]}, # Ebmaj7(#11)
        {"root": 26, "chord": [50, 54, 57, 60, 63]}, # D7(b9)
    ]
    picardy_chord = [50, 54, 57, 61, 64] # Dmaj9
    
    # Determinar rango de compases a renderizar
    if section_choice == 0:
        start_bar, end_bar = 0, 64
    elif section_choice == 1:
        start_bar, end_bar = 0, 8
    elif section_choice == 2:
        start_bar, end_bar = 8, 16
    elif section_choice == 3:
        start_bar, end_bar = 16, 24
    elif section_choice == 4:
        start_bar, end_bar = 24, 40
    elif section_choice == 5:
        start_bar, end_bar = 40, 48
    elif section_choice == 6:
        start_bar, end_bar = 48, 56
    elif section_choice == 7:
        start_bar, end_bar = 56, 64
        
    do_all = (channel_mode == 0)
    do_bass = do_all or (channel_mode == 1)
    do_chords = do_all or (channel_mode == 2)
    do_lead = do_all or (channel_mode == 3)
    do_drums = do_all or (channel_mode == 4)
    
    # Inyectar marcadores si se genera la obra completa
    if section_choice == 0 and HAS_FLPIANOROLL and hasattr(flp, 'Marker'):
        markers = [
            (0, "1. Intro Neo-Cádiz"),
            (8 * BAR, "2. Bajo Cyberpunk"),
            (16 * BAR, "3. Tensión & Corte"),
            (24 * BAR, "4. Drop 1 Danza Cíborg"),
            (40 * BAR, "5. Falseta Rubato"),
            (48 * BAR, "6. Amalgama Bulerías"),
            (56 * BAR, "7. Climax Picardía"),
        ]
        for m_t, m_name in markers:
            try:
                m = flp.Marker()
                m.name = m_name
                m.time = m_t
                flp.score.addMarker(m)
            except Exception:
                pass
                
    time_offset = -(start_bar * BAR) if section_choice != 0 else 0
    
    for bar in range(start_bar, end_bar):
        bar_t = (bar * BAR) + time_offset
        
        # Identificar sección actual
        is_intro = (bar < 8)
        is_verse = (8 <= bar < 16)
        is_build1 = (16 <= bar < 24)
        is_drop1 = (24 <= bar < 40)
        is_breakdown = (40 <= bar < 48)
        is_build2 = (48 <= bar < 56)
        is_climax = (56 <= bar < 64)
        
        # Determinar acorde
        if is_climax and (bar < 60):
            chord_notes = picardy_chord
            root = 26
        elif is_build1 or is_build2:
            chord_notes = cadence[3]["chord"] if (bar % 8 >= 4) else cadence[2]["chord"]
            root = cadence[3]["root"] if (bar % 8 >= 4) else cadence[2]["root"]
        else:
            c_idx = ((bar % 8) // 2) % 4
            chord_notes = cadence[c_idx]["chord"]
            root = cadence[c_idx]["root"]
            
        # 1. BAJO RODANTE (Color 1 - Verde)
        if do_bass:
            if is_verse or is_drop1 or (is_climax and bar < 60):
                for step in range(16):
                    s_t = bar_t + (step * SIXTEENTH)
                    is_oct = (step % 2 == 1) or (step % 4 == 3)
                    p = root + (12 if is_oct else 0)
                    v = 0.95 if (step % 4 == 0) else (0.80 if is_oct else 0.70)
                    add_note_safe(score_obj, p, s_t, SIXTEENTH * 0.72, vel=v, color_idx=1)
            elif is_build1:
                # Bajo pulsante en corcheas
                for b_step in range(8):
                    s_t = bar_t + (b_step * (PPQ // 2))
                    add_note_safe(score_obj, root, s_t, PPQ * 0.45, vel=0.88, color_idx=1)
                    
        # 2. CHORDS RASGUEADOS (Color 0 - Naranja)
        if do_chords:
            if is_intro or is_breakdown or (is_climax and bar >= 60):
                # Pads sostenidos etéreos
                for n in chord_notes:
                    add_note_safe(score_obj, n, bar_t, BAR - 40, vel=0.58, color_idx=0)
            elif is_verse or is_drop1 or (is_climax and bar < 60):
                # Ráfagas de rasgueo flamenco
                triggers = [0, 720, 1440] if is_drop1 else [0, 960]
                for tr in triggers:
                    for i, n in enumerate(chord_notes):
                        s_t = bar_t + tr + (i * int(strum_ticks))
                        add_note_safe(score_obj, n, s_t, 640 - (i * int(strum_ticks)), vel=0.88, color_idx=0)
                        
        # 3. LEAD / FALSETA MELISMÁTICA (Color 2 - Rojo)
        if do_lead:
            if is_drop1:
                solo_scale = [62, 63, 66, 67, 69, 70, 74, 75]
                for step in [0, 240, 480, 720, 960, 1200, 1440]:
                    if random.random() < 0.75:
                        s_t = bar_t + step
                        pitch = random.choice(solo_scale)
                        add_note_safe(score_obj, pitch, s_t, 200, vel=0.92, color_idx=2)
                        if use_slides and HAS_FLPIANOROLL and pitch in [63, 75]:
                            # Slide de sensible flamenca a la tónica
                            add_note_safe(score_obj, pitch - 1, s_t + 90, 100, vel=0.85, color_idx=2, is_slide=True)
            elif is_breakdown:
                # Falseta de guitarra flamenca lenta
                if bar % 2 == 0:
                    falseta_notes = [(0, 74), (360, 75), (600, 74), (960, 70), (1440, 69)]
                    for f_t, f_p in falseta_notes:
                        add_note_safe(score_obj, f_p, bar_t + f_t, 280, vel=0.82, color_idx=2)
                        
        # 4. PERCUSIÓN / PALMAS / DRUMS (Color 3 - Amarillo)
        if do_drums:
            if is_drop1 or (is_climax and bar < 60):
                # Kick 1 y 3 (MIDI 36)
                add_note_safe(score_obj, 36, bar_t, 140, vel=1.0, color_idx=3)
                add_note_safe(score_obj, 36, bar_t + (PPQ * 2), 140, vel=0.96, color_idx=3)
                # Snare 2 y 4 (MIDI 38)
                add_note_safe(score_obj, 38, bar_t + PPQ, 240, vel=1.0, color_idx=3)
                add_note_safe(score_obj, 38, bar_t + (PPQ * 3), 240, vel=1.0, color_idx=3)
                # Palmas sincopadas (MIDI 39)
                for ps in [2, 5, 8, 11, 14]:
                    add_note_safe(score_obj, 39, bar_t + (ps * SIXTEENTH) + 10, 80, vel=0.92, color_idx=3)

def apply(form):
    sec = form.GetInputValue("Sección a Generar")
    chan = form.GetInputValue("Canal / Articulación")
    st = form.GetInputValue("Velocidad Rasgueado (Ticks)")
    sl = form.GetInputValue("Slide Glissandos Expresivos")
    generate_masterpiece(flp.score, sec, chan, st, sl)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_masterpiece(target_score)
