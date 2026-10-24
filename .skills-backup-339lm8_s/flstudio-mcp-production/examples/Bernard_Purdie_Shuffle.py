# name = Bernard Purdie Half-Time Shuffle Engine (v2.0)
# author = Moskv-1 (C5-REAL)
# description = El legendario medio tiempo shuffle de Bernard Purdie con tresillos de ghost notes y dinámica en el charles.

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
    form = flp.ScriptDialog("Purdie Half-Time Shuffle", "El 'Purdie Shuffle' con tresillos continuos y cajas fantasma dinámicas.")
    form.AddInputKnob("Compases", 4, 1, 8)
    form.AddInputKnob("Velocidad Backbeat", 0.96, 0.8, 1.0)
    form.AddInputKnob("Velocidad Ghost Notes", 0.32, 0.15, 0.50)
    form.AddInputCheckbox("Charles Abierto en Contratiempo", True)
    return form

def generate_purdie_shuffle(score_obj, bars=4, backbeat_vel=0.96, ghost_vel=0.32, open_hats=True):
    score_obj.clear()
    
    BAR = 1920
    BEAT = 480
    TRIPLET = 160 # 480 / 3 = 160 ticks (tresillo de corchea)
    SUB_TRIPLET = 80 # tresillo de semicorchea para las ghost notes
    
    current_time = 0
    
    for bar in range(int(bars)):
        for beat in range(4):
            beat_start = current_time + (beat * BEAT)
            
            # 1. Bombo (Beat 1 y síncopas características)
            if beat == 0 or (beat == 1 and bar % 2 == 1):
                k = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                k.number = 36 # Kick
                k.time = beat_start
                k.length = 140
                k.velocity = 0.94
                score_obj.addNote(k)
            # Bombo en el tercer tresillo del compás
            if beat == 0 or beat == 2:
                k = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                k.number = 36
                k.time = beat_start + (2 * TRIPLET)
                k.length = 120
                k.velocity = 0.86
                score_obj.addNote(k)
                
            # 2. Backbeat Principal en el tiempo 3 (Medio Tiempo / Half-time)
            if beat == 2:
                s = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                s.number = 38 # Snare
                s.time = beat_start
                s.length = 180
                s.velocity = backbeat_vel
                score_obj.addNote(s)
                
            # 3. Ghost Notes en la Caja (Tresillos intermediarios característicos de Purdie)
            ghost_steps = [SUB_TRIPLET, TRIPLET + SUB_TRIPLET, (2 * TRIPLET) + SUB_TRIPLET]
            for g_offset in ghost_steps:
                # No colisionar exactamente con el backbeat fuerte del beat 2
                if beat == 2 and g_offset < SUB_TRIPLET + 20:
                    continue
                if random.random() < 0.85:
                    g = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                    g.number = 38
                    g.time = beat_start + g_offset + random.randint(-3, 3)
                    g.length = 40
                    g.velocity = ghost_vel + random.uniform(-0.05, 0.05)
                    score_obj.addNote(g)
                    
            # 4. Hi-Hats en Tresillos Continuos (1 - & - a)
            for t in range(3):
                h_time = beat_start + (t * TRIPLET)
                is_open = (open_hats and t == 2 and beat % 2 == 1)
                
                h = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                h.number = 46 if is_open else 42
                h.time = h_time
                h.length = 140 if is_open else 60
                h.velocity = 0.88 if is_open else (0.78 if t == 0 else 0.62)
                score_obj.addNote(h)
                
        current_time += BAR

def apply(form):
    bars = form.GetInputValue("Compases")
    bb = form.GetInputValue("Velocidad Backbeat")
    gh = form.GetInputValue("Velocidad Ghost Notes")
    oh = form.GetInputValue("Charles Abierto en Contratiempo")
    generate_purdie_shuffle(flp.score, bars, bb, gh, oh)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_purdie_shuffle(target_score)
