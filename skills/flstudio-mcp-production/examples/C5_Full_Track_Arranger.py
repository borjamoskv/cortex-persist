# name = C5-REAL Full Track Structural Arranger (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador estructural de pista completa con marcadores de sección nativos (Intro, Build, Drop, Breakdown, Climax, Outro).

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("C5 Full Track Arranger", "Genera una estructura de pista completa de 56 compases con marcadores.")
    form.AddInputCombo("Tonalidad General", "Do Menor (Cm),Re Dórico (Dm),La Menor (Am)", 0)
    form.AddInputCheckbox("Generar Marcadores de Seccion", True)
    form.AddInputCheckbox("Climax Tercera de Picardia", True)
    return form

def generate_track_arrangement(score_obj, key_idx=0, add_markers=True, picardy_climax=True):
    score_obj.clear()
    
    BAR = 1920
    
    # Raíz según tonalidad
    roots = [36, 38, 33] # C, D, A
    root = roots[min(key_idx, len(roots) - 1)]
    
    # Secciones formales (Compases, Nombre, Densidad)
    sections = [
        {"name": "1. Intro (Atmosphere)", "bars": 8, "type": "intro"},
        {"name": "2. Build-Up (Rising Tension)", "bars": 8, "type": "build"},
        {"name": "3. Drop 1 (Exergy Main Groove)", "bars": 16, "type": "drop1"},
        {"name": "4. Breakdown (Dub Silence)", "bars": 8, "type": "breakdown"},
        {"name": "5. Climax (Picardy Modulation)", "bars": 8, "type": "climax"},
        {"name": "6. Outro (Dissipation)", "bars": 8, "type": "outro"},
    ]
    
    current_time = 0
    
    for sec in sections:
        sec_start = current_time
        sec_ticks = sec["bars"] * BAR
        
        # Añadir marcador de sección si el host lo soporta
        if add_markers and HAS_FLPIANOROLL and hasattr(flp, 'Marker'):
            try:
                m = flp.Marker()
                m.name = sec["name"]
                m.time = sec_start
                flp.score.addMarker(m)
            except Exception:
                pass
                
        # Generar contenido musical según sección
        sec_type = sec["type"]
        
        for bar in range(sec["bars"]):
            bar_start = sec_start + (bar * BAR)
            
            if sec_type in ["intro", "outro"]:
                # Pad etéreo simple
                for n_offset in [0, 7, 12]:
                    n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                    n.number = root + 24 + n_offset
                    n.time = bar_start
                    n.length = BAR - 80
                    n.velocity = 0.60
                    score_obj.addNote(n)
                    
            elif sec_type == "build":
                # Redoble acelerado / arpegio ascendente
                step_div = 4 if bar < 4 else (8 if bar < 6 else 16)
                step_len = BAR // step_div
                for s in range(step_div):
                    n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                    n.number = root + 12 + ((s % 4) * 3)
                    n.time = bar_start + (s * step_len)
                    n.length = int(step_len * 0.7)
                    # Crescendo
                    n.velocity = min(1.0, 0.65 + ((bar * step_div + s) / float(sec["bars"] * 16)) * 0.35)
                    score_obj.addNote(n)
                    
            elif sec_type in ["drop1", "climax"]:
                # Bombo 4-on-the-floor en graves
                is_picardy = (sec_type == "climax" and picardy_climax)
                chord_3rd = 4 if is_picardy else 3 # Tercera Mayor si es Picardía, Menor si no
                
                for beat in range(4):
                    k = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                    k.number = root # Bombo / Sub fundamental
                    k.time = bar_start + (beat * 480)
                    k.length = 80
                    k.velocity = 1.0
                    score_obj.addNote(k)
                    
                # Acorde rítmico en contratiempos (offbeat stabs)
                for beat in [1, 3]:
                    for p_off in [12, 12 + chord_3rd, 19]:
                        st = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                        st.number = root + 24 + p_off
                        st.time = bar_start + (beat * 480) + 240
                        st.length = 180
                        st.velocity = 0.88 if not is_picardy else 0.98
                        score_obj.addNote(st)
                        
            elif sec_type == "breakdown":
                # Tensión y silencio (solo una nota suspendida con colas de delay)
                if bar == 0 or bar == 4:
                    n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                    n.number = root + 24 + 10 # 7ma menor de suspensión
                    n.time = bar_start
                    n.length = BAR * 2
                    n.velocity = 0.75
                    score_obj.addNote(n)
                    
        current_time += sec_ticks

def apply(form):
    k = form.GetInputValue("Tonalidad General")
    m = form.GetInputValue("Generar Marcadores de Seccion")
    p = form.GetInputValue("Climax Tercera de Picardia")
    generate_track_arrangement(flp.score, k, m, p)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_track_arrangement(target_score)
