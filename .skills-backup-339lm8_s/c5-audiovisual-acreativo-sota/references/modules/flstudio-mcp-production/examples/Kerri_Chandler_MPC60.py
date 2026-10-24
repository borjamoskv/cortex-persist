# name = Kerri Chandler MPC-60 Swing Matrix (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Matriz rítmica Deep House con swing auténtico MPC-60/3000 (50%-75%) y capas de ghost notes dinámicas.

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
    form = flp.ScriptDialog("Kerri Chandler MPC-60 Groove", "Matriz de swing Roger Linn MPC-60 y dinámica Deep House.")
    form.AddInputKnob("Compases", 4, 1, 8)
    form.AddInputKnob("Swing Porcentaje", 62, 50, 75)
    form.AddInputKnob("Ghost Note Prob", 0.40, 0.0, 1.0)
    form.AddInputCombo("Patron Ritmo", "Hi-Hats + Open Hat,Claps & Ghost Rims,Bassline Groove", 0)
    return form

def generate_mpc_groove(score_obj, bars=4, swing_pct=62, ghost_prob=0.40, pattern_type=0):
    score_obj.clear()
    
    BAR = 1920
    BEAT = 480
    SIXTEENTH = 120
    
    # Cálculo formal de swing MPC (Roger Linn):
    # En 50%: offset = 0. En 66.7%: tresillo puro.
    # El swing retrasa las semicorcheas impares (pasos 1 y 3 dentro del tiempo).
    swing_ratio = (swing_pct - 50.0) / 50.0
    swing_offset = int(swing_ratio * (SIXTEENTH * 0.667))
    
    current_time = 0
    
    for bar in range(int(bars)):
        for beat in range(4):
            beat_start = current_time + (beat * BEAT)
            
            for step in range(4):
                # Calcular tiempo base con swing en pasos 1 y 3
                step_time = beat_start + (step * SIXTEENTH)
                if step % 2 == 1:
                    step_time += swing_offset
                    
                # Humanización analógica de reloj de la MPC-60 (+/- 2 ticks de jitter)
                step_time += random.randint(-2, 2)
                
                if pattern_type == 0:
                    # 1. Hi-Hats cerrados y abiertos
                    # Paso 2 (contratiempo): Open Hat (MIDI 46) ocasional o Closed Hat fuerte
                    if step == 2:
                        h = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                        h.number = 46 if (beat % 2 == 1) else 42
                        h.time = step_time
                        h.length = 180 if h.number == 46 else 60
                        h.velocity = 0.88 + random.uniform(-0.04, 0.04)
                        score_obj.addNote(h)
                    else:
                        # Pasos 0, 1, 3: Closed Hat (MIDI 42)
                        h = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                        h.number = 42
                        h.time = step_time
                        h.length = 45
                        h.velocity = 0.75 if step == 0 else 0.60
                        score_obj.addNote(h)
                        
                        # Inyección estocástica de ghost note
                        if random.random() < ghost_prob:
                            g = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                            g.number = 42
                            g.time = step_time + 40
                            g.length = 30
                            g.velocity = 0.28 + random.uniform(-0.05, 0.05)
                            score_obj.addNote(g)
                            
                elif pattern_type == 1:
                    # 2. Claps en 2 y 4 con Rims fantasmas
                    if (beat == 1 or beat == 3) and step == 0:
                        c = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                        c.number = 39 # Clap principal
                        c.time = step_time
                        c.length = 160
                        c.velocity = 0.94
                        score_obj.addNote(c)
                    elif random.random() < ghost_prob:
                        r = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                        r.number = 37 # Rimshot fantasma
                        r.time = step_time
                        r.length = 50
                        r.velocity = 0.35 + random.uniform(-0.08, 0.08)
                        score_obj.addNote(r)
                        
                elif pattern_type == 2:
                    # 3. Bassline syncopated groove
                    if step in [0, 2] or (step == 3 and random.random() < 0.7):
                        b = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                        b.number = 36 if step == 0 else 39 # Root o síncopa
                        b.time = step_time
                        b.length = SIXTEENTH - 10
                        b.velocity = 0.85 if step == 0 else 0.70
                        score_obj.addNote(b)
                        
        current_time += BAR

def apply(form):
    bars = form.GetInputValue("Compases")
    swing = form.GetInputValue("Swing Porcentaje")
    ghost = form.GetInputValue("Ghost Note Prob")
    ptype = form.GetInputValue("Patron Ritmo")
    generate_mpc_groove(flp.score, bars, swing, ghost, ptype)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_mpc_groove(target_score)
