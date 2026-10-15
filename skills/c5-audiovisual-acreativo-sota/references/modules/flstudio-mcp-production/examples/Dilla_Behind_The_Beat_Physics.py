# name = J Dilla Behind-The-Beat Humanizer Engine (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Física de arrastre micro-temporal de J Dilla: cajas rezagadas, bombos adelantados y hats elásticos.

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
    form = flp.ScriptDialog("J Dilla Behind-The-Beat Physics", "Emulación de desfase micro-temporal MPC sin cuantizar.")
    form.AddInputKnob("Compases", 4, 1, 8)
    form.AddInputKnob("Snare Drag (Ticks)", 45, 10, 90)
    form.AddInputKnob("Kick Rush (Ticks)", 15, 0, 35)
    form.AddInputKnob("Hat Elastic Jitter", 12, 2, 30)
    return form

def generate_dilla_groove(score_obj, bars=4, snare_drag=45, kick_rush=15, hat_jitter=12):
    score_obj.clear()
    
    BAR = 1920
    BEAT = 480
    SIXTEENTH = 120
    
    current_time = 0
    
    for bar in range(int(bars)):
        for beat in range(4):
            beat_start = current_time + (beat * BEAT)
            
            # 1. Bombo (Adelantado / Rushing para dar sensación de empuje)
            if beat == 0 or (beat == 2 and bar % 2 == 1) or (beat == 1 and random.random() < 0.4):
                k = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                k.number = 36 # Kick
                # Adelantamos el kick ligeramente
                k.time = max(0, beat_start - int(kick_rush) + random.randint(-2, 2))
                k.length = 120
                k.velocity = 0.95 + random.uniform(-0.03, 0.03)
                score_obj.addNote(k)
                
            # 2. Caja / Snare (Fuertemente rezagada / Dragging behind the beat)
            if beat == 1 or beat == 3: # Tiempos 2 y 4 clásicos
                s = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                s.number = 38 # Snare
                # Retraso físico de Dilla
                s.time = beat_start + int(snare_drag) + random.randint(-4, 4)
                s.length = 160
                s.velocity = 0.92 + random.uniform(-0.04, 0.04)
                score_obj.addNote(s)
                
            # 3. Hi-Hats elásticos (Paso a semicorcheas con elasticidad)
            for step in range(4):
                step_time = beat_start + (step * SIXTEENTH)
                h = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                h.number = 42 # Hat cerrado
                
                # Desfase elástico estocástico
                elastic_offset = random.randint(-int(hat_jitter), int(hat_jitter))
                h.time = max(0, step_time + elastic_offset)
                h.length = 45
                
                # Alternancia de dinámica Dilla
                base_v = 0.78 if step % 2 == 0 else 0.58
                h.velocity = max(0.2, min(1.0, base_v + random.uniform(-0.06, 0.06)))
                score_obj.addNote(h)
                
        current_time += BAR

def apply(form):
    bars = form.GetInputValue("Compases")
    sd = form.GetInputValue("Snare Drag (Ticks)")
    kr = form.GetInputValue("Kick Rush (Ticks)")
    hj = form.GetInputValue("Hat Elastic Jitter")
    generate_dilla_groove(flp.score, bars, sd, kr, hj)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_dilla_groove(target_score)
