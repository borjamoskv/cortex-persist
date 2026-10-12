# name = Trap 808 Multi-Octave Glide Architect (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Arquitectura de sub-graves 808 con glissandos multi-octava nativos (note.slide) y saturación de transitorios.

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Trap 808 Glide Architect", "Generador de patrones 808 con slides multi-octava de alta energía.")
    form.AddInputCombo("Nota Fundamental", "C1 (24),D1 (26),E1 (28),F1 (29),G1 (31)", 0)
    form.AddInputKnob("Compases", 4, 1, 8)
    form.AddInputCombo("Estilo de Glide", "Octava Superior (+12),Quinta Justa (+7),Doble Octava (+24),Glides Variados", 3)
    return form

def generate_808_glides(score_obj, root_choice=0, bars=4, glide_style=3):
    score_obj.clear()
    
    BAR = 1920
    BEAT = 480
    SIXTEENTH = 120
    
    roots = [24, 26, 28, 29, 31] # C1, D1, E1, F1, G1
    root = roots[min(root_choice, len(roots) - 1)]
    
    current_time = 0
    
    for bar in range(int(bars)):
        # Patrón rítmico de 808 clásico: Beat 1, Beat 2.5 (and), Beat 4
        hits = [
            {"offset": 0, "length": BEAT + SIXTEENTH * 2, "has_glide": False},
            {"offset": BEAT * 2 - SIXTEENTH, "length": BEAT, "has_glide": True},
            {"offset": BEAT * 3, "length": BEAT - 40, "has_glide": (bar % 2 == 1)},
        ]
        
        for h in hits:
            hit_start = current_time + h["offset"]
            
            # Nota principal 808 sostenida
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = root
            n.time = hit_start
            n.length = h["length"]
            n.velocity = 0.98
            score_obj.addNote(n)
            
            # Nota Slide nativa de FL Studio
            if h["has_glide"] and HAS_FLPIANOROLL:
                if glide_style == 0:
                    glide_pitch = root + 12
                elif glide_style == 1:
                    glide_pitch = root + 7
                elif glide_style == 2:
                    glide_pitch = root + 24
                else:
                    glide_pitch = root + (12 if bar % 2 == 0 else 7)
                    
                slide = flp.Note()
                slide.number = glide_pitch
                # La nota slide entra al final de la nota sostenida
                slide.time = hit_start + int(h["length"] * 0.55)
                slide.length = int(h["length"] * 0.45)
                slide.velocity = 0.95
                slide.slide = True # Activa portamento sin retrigger
                score_obj.addNote(slide)
                
        current_time += BAR

def apply(form):
    rc = form.GetInputValue("Nota Fundamental")
    b = form.GetInputValue("Compases")
    gs = form.GetInputValue("Estilo de Glide")
    generate_808_glides(flp.score, rc, b, gs)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_808_glides(target_score)
