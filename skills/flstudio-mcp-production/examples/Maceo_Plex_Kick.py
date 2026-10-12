# name = Maceo Plex Kick & Sub-Rumble SOTA (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador algorítmico interactivo de bombo Melodic Techno y matriz de sub-rumble en semicorcheas.

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def createDialog():
    """Formulario interactivo nativo de FL Studio 21/2024/2025."""
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Maceo Plex Kick & Rumble", "Generador de bombo Techno analógico y lecho sub-rumble.")
    form.AddInputKnob("Num Bars", 4, 1, 16)
    form.AddInputKnob("Kick Length", 80, 40, 240)
    form.AddInputKnob("Rumble Vel", 0.70, 0.1, 1.0)
    form.AddInputKnob("Swing Ticks", 3, 0, 15)
    form.AddInputCombo("Sub Tuning", "F1 (21.8Hz),E1 (20.6Hz),G1 (24.5Hz)", 0)
    return form

def generate_kick_and_rumble(score_obj, num_bars=4, kick_len=80, rumble_vel_scale=0.70, swing_ticks=3, sub_choice=0):
    score_obj.clear()
    
    # Constantes temporales (480 PPQ)
    BAR = 1920
    BEAT = 480
    SIXTEENTH = 120
    
    # Frecuencia fundamental del bombo y sub
    sub_notes = [29, 28, 31] # F1, E1, G1
    kick_note = 41 # F2 (~43.65 Hz fundamental)
    rumble_note = sub_notes[min(sub_choice, len(sub_notes) - 1)]
    
    for bar in range(int(num_bars)):
        base_time = bar * BAR
        
        for beat in range(4):
            beat_time = base_time + (beat * BEAT)
            
            # 1. Bombo 4-on-the-floor con saturación Tanh
            k = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            k.number = kick_note
            k.time = beat_time
            k.length = int(kick_len)
            k.velocity = 1.0
            
            # Pocket swing en tiempos débiles (2 y 4)
            if (beat == 1 or beat == 3) and swing_ticks > 0:
                k.time += int(swing_ticks)
                
            score_obj.addNote(k)
            
            # 2. Sub-rumble en semicorcheas 2, 3 y 4
            rumble_matrix = [(1, 0.45), (2, 0.70), (3, 0.55)]
            for step, vel in rumble_matrix:
                r = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                r.number = rumble_note
                
                # Offset micro-temporal para evitar colisión de fase con la cola del kick
                step_time = beat_time + (step * SIXTEENTH)
                r.time = step_time + 5
                r.length = SIXTEENTH - 10
                
                # Modulación dinámica
                bar_mod = 0.9 if (bar % 2 != 0) else 1.0
                r.velocity = min(1.0, vel * rumble_vel_scale * bar_mod)
                score_obj.addNote(r)

def apply(form):
    """Callback de ejecución desde el diálogo interactivo."""
    num_bars = form.GetInputValue("Num Bars")
    kick_len = form.GetInputValue("Kick Length")
    rumble_vel = form.GetInputValue("Rumble Vel")
    swing_ticks = form.GetInputValue("Swing Ticks")
    sub_choice = form.GetInputValue("Sub Tuning")
    
    generate_kick_and_rumble(flp.score, num_bars, kick_len, rumble_vel, swing_ticks, sub_choice)

def createScore():
    """Punto de entrada directo de fallback para compatibilidad heredada."""
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_kick_and_rumble(target_score)
