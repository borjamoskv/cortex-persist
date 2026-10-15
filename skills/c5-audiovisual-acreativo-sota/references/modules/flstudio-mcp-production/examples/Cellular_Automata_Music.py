# name = Wolfram Cellular Automata Melodic Engine (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Generador algorítmico basado en autómatas celulares 1D de Stephen Wolfram (Reglas 30, 90, 110, 150).

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def wolfram_step(cells, rule):
    """Computes next generation of 1D elementary cellular automaton with periodic boundary."""
    n = len(cells)
    next_gen = [0] * n
    for i in range(n):
        left = cells[(i - 1) % n]
        center = cells[i]
        right = cells[(i + 1) % n]
        neighborhood = (left << 2) | (center << 1) | right
        next_gen[i] = (rule >> neighborhood) & 1
    return next_gen

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Cellular Automata Engine", "Generador de secuencias complejas mediante autómatas celulares 1D.")
    form.AddInputCombo("Regla Wolfram", "Regla 30 (Caos determinista),Regla 90 (Fractal Sierpinski),Regla 110 (Turing-completo),Regla 150 (Auto-similar)", 0)
    form.AddInputKnob("Num Generaciones", 16, 8, 64)
    form.AddInputKnob("Tamano Vector (Celdas)", 12, 6, 24)
    form.AddInputKnob("Paso Temporal (Ticks)", 120, 60, 480)
    form.AddInputCombo("Escala de Cuantizacion", "Menor Dorica (C),Mayor Pentatonica,Phrygian Dominant", 0)
    return form

def generate_ca_score(score_obj, rule_idx=0, generations=16, cell_count=12, step_ticks=120, scale_idx=0):
    score_obj.clear()
    
    rules = [30, 90, 110, 150]
    rule = rules[min(rule_idx, len(rules) - 1)]
    
    # Escalas de cuantización (offsets semitonales sobre C3 = 48)
    scales = [
        [48, 50, 51, 53, 55, 57, 58, 60, 62, 63, 65, 67], # C Dorian
        [48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72, 74], # C Major Pentatonic
        [48, 49, 52, 53, 55, 56, 58, 60, 61, 64, 65, 67], # C Phrygian Dominant
    ]
    scale = scales[min(scale_idx, len(scales) - 1)]
    
    # Inicializar estado con una sola celda central activa
    cells = [0] * int(cell_count)
    cells[len(cells) // 2] = 1
    
    current_time = 0
    ticks = int(step_ticks)
    
    for gen in range(int(generations)):
        for cell_idx, state in enumerate(cells):
            if state == 1:
                n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
                pitch_idx = cell_idx % len(scale)
                n.number = scale[pitch_idx]
                n.time = current_time
                n.length = int(ticks * 0.85)
                n.velocity = 0.82
                n.pan = ((cell_idx / float(len(cells))) - 0.5) * 1.5 # Apertura espacial
                score_obj.addNote(n)
                
        cells = wolfram_step(cells, rule)
        current_time += ticks

def apply(form):
    ridx = form.GetInputValue("Regla Wolfram")
    gens = form.GetInputValue("Num Generaciones")
    cells = form.GetInputValue("Tamano Vector (Celdas)")
    step = form.GetInputValue("Paso Temporal (Ticks)")
    sc = form.GetInputValue("Escala de Cuantizacion")
    generate_ca_score(flp.score, ridx, gens, cells, step, sc)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_ca_score(target_score)
