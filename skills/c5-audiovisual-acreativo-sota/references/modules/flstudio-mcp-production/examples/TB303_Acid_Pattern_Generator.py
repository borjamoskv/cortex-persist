# name = Roland TB-303 Acid Pattern & Slide Engine (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador auténtico de líneas de bajo Acid TB-303 con notas Slide nativas de FL Studio, acentos y ligaduras.

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
    form = flp.ScriptDialog("TB-303 Acid Generator", "Generador de patrones Acid 303 con notas slide, acentos y ligaduras.")
    form.AddInputKnob("Compases", 4, 1, 8)
    form.AddInputKnob("Probabilidad Slide", 0.30, 0.0, 0.70)
    form.AddInputKnob("Probabilidad Acento", 0.35, 0.0, 0.70)
    form.AddInputKnob("Probabilidad Octava Arriba", 0.25, 0.0, 0.60)
    form.AddInputCombo("Modo Escala", "Menor Natural (C),Dórica (D),Frigia (E),Pentatónica Menor", 0)
    return form

def generate_tb303_acid(score_obj, bars=4, slide_prob=0.30, accent_prob=0.35, octave_prob=0.25, scale_mode=0):
    score_obj.clear()
    
    BAR = 1920
    SIXTEENTH = 120 # Paso básico de 16 semicorcheas de la 303
    
    scales = [
        [36, 38, 39, 41, 43, 44, 46], # C Minor
        [38, 40, 41, 43, 45, 47, 48], # D Dorian
        [40, 41, 43, 45, 47, 48, 50], # E Phrygian
        [36, 39, 41, 43, 46],         # C Minor Pentatonic
    ]
    scale = scales[min(scale_mode, len(scales) - 1)]
    
    current_time = 0
    
    for bar in range(int(bars)):
        for step in range(16):
            step_time = current_time + (step * SIXTEENTH)
            
            # Decidir si hay nota o silencio (rest)
            if random.random() < 0.20 and step not in [0, 4, 8, 12]:
                continue
                
            pitch = random.choice(scale)
            if random.random() < octave_prob:
                pitch += 12 # Salto de octava típico de la 303
                
            has_accent = (random.random() < accent_prob)
            has_slide = (random.random() < slide_prob)
            
            # Nota principal
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = pitch
            n.time = step_time
            # Si no hay slide, la longitud es staccato (~60% del paso)
            n.length = SIXTEENTH if has_slide else int(SIXTEENTH * 0.65)
            # Acento maximiza la velocidad para abrir el filtro del sinte
            n.velocity = 1.0 if has_accent else 0.72
            score_obj.addNote(n)
            
            # Si hay slide, creamos la nota de destino con note.slide = True
            if has_slide and HAS_FLPIANOROLL:
                target_pitch = random.choice(scale)
                if random.random() < 0.5:
                    target_pitch += 12
                    
                slide_n = flp.Note()
                slide_n.number = target_pitch
                # La nota slide se posiciona a la mitad del paso actual
                slide_n.time = step_time + int(SIXTEENTH * 0.4)
                slide_n.length = int(SIXTEENTH * 0.6)
                slide_n.velocity = n.velocity
                slide_n.slide = True # Portamento nativo en FL Studio
                score_obj.addNote(slide_n)
                
        current_time += BAR

def apply(form):
    b = form.GetInputValue("Compases")
    sl = form.GetInputValue("Probabilidad Slide")
    ac = form.GetInputValue("Probabilidad Acento")
    oc = form.GetInputValue("Probabilidad Octava Arriba")
    sc = form.GetInputValue("Modo Escala")
    generate_tb303_acid(flp.score, b, sl, ac, oc, sc)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_tb303_acid(target_score)
