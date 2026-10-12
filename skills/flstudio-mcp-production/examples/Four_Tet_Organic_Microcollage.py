# name = Four Tet Organic Microcollage Engine (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador de micro-rítmica acústica orgánica estilo Four Tet: kalimbas, arpas desfasadas y panorámica dinámica.

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
    form = flp.ScriptDialog("Four Tet Organic Microcollage", "Puntillismo rítmico acústico y desfasaje estéreo.")
    form.AddInputKnob("Compases", 4, 1, 8)
    form.AddInputKnob("Micro-Timing Jitter (Ticks)", 18, 0, 40)
    form.AddInputKnob("Apertura Estéreo Pan", 0.75, 0.2, 1.0)
    form.AddInputCombo("Modo Pentatónico", "Akebono Japonés,Pentatónica Mayor,Hirajoshi Místico", 0)
    return form

def generate_fourtet_microcollage(score_obj, bars=4, jitter=18, pan_width=0.75, scale_idx=0):
    score_obj.clear()
    
    BAR = 1920
    SIXTEENTH = 120
    
    # Escalas pentatónicas orgánicas y exóticas
    scales = [
        [60, 62, 63, 67, 68, 72, 74, 75, 79, 80], # Akebono (C, D, Eb, G, Ab)
        [60, 62, 64, 67, 69, 72, 74, 76, 79, 81], # Major Pentatonic
        [60, 62, 63, 67, 68, 72, 74, 75, 79, 80], # Hirajoshi
    ]
    scale = scales[min(scale_idx, len(scales) - 1)]
    
    current_time = 0
    
    for bar in range(int(bars)):
        for step in range(16):
            step_time = current_time + (step * SIXTEENTH)
            
            # Probabilidad de nota con micropatrones irregulares
            if random.random() < 0.65:
                n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                n.number = random.choice(scale)
                
                # Desfase humano orgánico
                time_offset = random.randint(-int(jitter), int(jitter))
                n.time = max(0, step_time + time_offset)
                n.length = random.randint(50, 140)
                
                # Dinámica suave con toques acústicos
                n.velocity = 0.65 + random.uniform(-0.15, 0.15)
                
                # Panorámica oscilante y amplia
                n.pan = random.uniform(-pan_width, pan_width)
                score_obj.addNote(n)
                
                # Ocasional eco fantasma microtonal / octava superior
                if random.random() < 0.25:
                    echo = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                    echo.number = n.number + 12
                    echo.time = n.time + 60 + random.randint(-5, 5)
                    echo.length = 40
                    echo.velocity = n.velocity * 0.45
                    echo.pan = -n.pan # Inversión estéreo del eco
                    score_obj.addNote(echo)
                    
        current_time += BAR

def apply(form):
    b = form.GetInputValue("Compases")
    jt = form.GetInputValue("Micro-Timing Jitter (Ticks)")
    pw = form.GetInputValue("Apertura Estéreo Pan")
    sc = form.GetInputValue("Modo Pentatónico")
    generate_fourtet_microcollage(flp.score, b, jt, pw, sc)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_fourtet_microcollage(target_score)
