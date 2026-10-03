# name = Stephan Bodzin Moog Synth Arpeggiator (v2.0)
# author = Moskv-1 (C5-REAL)
# description = Arpegiador hipnótico Melodic Techno estilo Moog Sub 37 con modulación de filtro simulada en velocity y acentos.

import math

try:
    import flpianoroll as flp
    HAS_FLPIANOROLL = True
except ImportError:
    import utils
    HAS_FLPIANOROLL = False

def createDialog():
    if not HAS_FLPIANOROLL:
        return None
    form = flp.ScriptDialog("Bodzin Moog Arpeggiator", "Arpegiador Melodic Techno con evolución dinámica de envolvente.")
    form.AddInputKnob("Ciclos Compases", 8, 4, 16)
    form.AddInputCombo("Patrón Arpegio", "Ascendente (1-3-5-8),Pedal Invertido,Tresillos Melódicos", 0)
    form.AddInputKnob("Filtro Velocity Sweep", 0.35, 0.0, 0.70)
    form.AddInputCombo("Escala Tonal", "C Menor Natural,D Dórico,E Frigio", 0)
    return form

def generate_bodzin_arp(score_obj, bars=8, pattern_mode=0, sweep_depth=0.35, scale_mode=0):
    score_obj.clear()
    
    BAR = 1920
    SIXTEENTH = 120
    
    scales = [
        [48, 51, 55, 58, 60, 63, 67, 70], # C Minor
        [50, 53, 57, 60, 62, 65, 69, 72], # D Dorian
        [52, 53, 57, 59, 60, 64, 67, 71], # E Phrygian
    ]
    scale = scales[min(scale_mode, len(scales) - 1)]
    
    total_steps = int(bars) * 16
    current_time = 0
    
    for step in range(total_steps):
        # Evolución del filtro (sweep en forma de rampa ascendente a lo largo de 8 compases)
        progress = (step % (16 * 4)) / float(16 * 4)
        filter_envelope = 0.60 + (progress * sweep_depth)
        
        # Patrones de notas Bodzin
        if pattern_mode == 0:
            # Ascendente 4 notas
            note_idx = step % 4
            pitch = scale[note_idx]
            if step % 8 >= 4:
                pitch += 12 # Salto de octava
        elif pattern_mode == 1:
            # Pedal invertido (la primera nota es pedal grave, las otras suben)
            if step % 2 == 0:
                pitch = scale[0] # Pedal fundamental
            else:
                pitch = scale[((step // 2) % (len(scale) - 1)) + 1] + 12
        else:
            # Tresillos melódicos
            note_idx = (step * 2) % len(scale)
            pitch = scale[note_idx]
            
        n = flp.Note() if HAS_FLPIANOROLL else utils.Note()
        n.number = pitch
        n.time = current_time
        n.length = int(SIXTEENTH * 0.75) # Decaimiento apretado estilo Moog
        
        # Acentos rítmicos en pasos clave
        is_accent = (step % 4 == 0 or step % 16 == 10)
        base_v = filter_envelope + (0.15 if is_accent else 0.0)
        n.velocity = max(0.2, min(1.0, base_v))
        
        score_obj.addNote(n)
        current_time += SIXTEENTH

def apply(form):
    b = form.GetInputValue("Ciclos Compases")
    pm = form.GetInputValue("Patrón Arpegio")
    sw = form.GetInputValue("Filtro Velocity Sweep")
    sc = form.GetInputValue("Escala Tonal")
    generate_bodzin_arp(flp.score, b, pm, sw, sc)

def createScore():
    target_score = flp.score if HAS_FLPIANOROLL else score
    generate_bodzin_arp(target_score)
