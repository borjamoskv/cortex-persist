# name = Euclidean Polyrhythm & Polymeter Generator (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Algoritmo de Bjorklund para generación de polirritmias euclidianas (E(k, n)) con capas independientes.

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def bjorklund(pulses, steps):
    """Generates Euclidean rhythm pattern E(pulses, steps) using Bjorklund's algorithm."""
    if pulses <= 0:
        return [0] * steps
    if pulses >= steps:
        return [1] * steps
    
    pattern = []
    counts = []
    remainders = []
    divisor = steps - pulses
    remainders.append(pulses)
    level = 0
    
    while True:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level += 1
        if remainders[level] <= 1:
            break
            
    counts.append(divisor)
    
    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)
        else:
            for _ in range(counts[level]):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)
                
    build(level)
    i = pattern.index(1)
    return pattern[i:] + pattern[:i]

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Euclidean Polyrhythm Generator", "Generador de patrones euclidianos E(k, n) con micro-timing.")
    form.AddInputKnob("Steps Layer 1 (N1)", 16, 4, 32)
    form.AddInputKnob("Pulses Layer 1 (K1)", 5, 1, 32)
    form.AddInputKnob("Steps Layer 2 (N2)", 12, 4, 32)
    form.AddInputKnob("Pulses Layer 2 (K2)", 7, 1, 32)
    form.AddInputKnob("Ciclos Compases", 4, 1, 16)
    form.AddInputCombo("Modo Polirritmia", "Poliritmo 4/4 (Compas fijo),Polimetro Continuo", 0)
    return form

def generate_euclidean(score_obj, n1=16, k1=5, n2=12, k2=7, bars=4, mode=0):
    score_obj.clear()
    BAR = 1920
    total_ticks = int(bars) * BAR
    
    pat1 = bjorklund(int(k1), int(n1))
    pat2 = bjorklund(int(k2), int(n2))
    
    # Layer 1: Kick / Low Perc (MIDI 36)
    step_ticks_1 = BAR // int(n1)
    cur_t = 0
    while cur_t < total_ticks:
        step_idx = (cur_t // step_ticks_1) % len(pat1)
        if pat1[step_idx]:
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = 36 # C2
            n.time = cur_t
            n.length = int(step_ticks_1 * 0.8)
            n.velocity = 0.92
            score_obj.addNote(n)
        cur_t += step_ticks_1
        
    # Layer 2: Perc / Rim / High Synth (MIDI 42)
    step_ticks_2 = BAR // int(n2)
    cur_t = 0
    while cur_t < total_ticks:
        step_idx = (cur_t // step_ticks_2) % len(pat2)
        if pat2[step_idx]:
            n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
            n.number = 42 # F#2
            n.time = cur_t
            n.length = int(step_ticks_2 * 0.7)
            n.velocity = 0.78
            if HAS_FLPIANOROLL and hasattr(n, 'color'):
                n.color = 1 # Canal verde
            score_obj.addNote(n)
        cur_t += step_ticks_2

def apply(form):
    n1 = form.GetInputValue("Steps Layer 1 (N1)")
    k1 = form.GetInputValue("Pulses Layer 1 (K1)")
    n2 = form.GetInputValue("Steps Layer 2 (N2)")
    k2 = form.GetInputValue("Pulses Layer 2 (K2)")
    bars = form.GetInputValue("Ciclos Compases")
    mode = form.GetInputValue("Modo Polirritmia")
    generate_euclidean(flp.score, n1, k1, n2, k2, bars, mode)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_euclidean(target_score)
