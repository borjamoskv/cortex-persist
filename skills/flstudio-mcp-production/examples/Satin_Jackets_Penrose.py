# name = Satin Jackets Penrose Stair
# author = Moskv-1 (C5-REAL)
# description = Generador algoritmico de acordes no resolutivos con swing MPC (Abmaj7 -> Bb9 -> Cm9 -> Fm9)

import utils
import random

def createScore():
    score.clear()
    
    # Ticks por compás (4 tiempos asumiendo PPQ estándar)
    BAR = 1920
    
    # Progresión de acordes (MIDI note numbers)
    # 1. Abmaj7 (G#3, C4, Eb4, G4)
    ab_maj7 = [56, 60, 63, 67]
    # 2. Bb9 (Bb3, D4, F4, Ab4, C5)
    bb_9 = [58, 62, 65, 68, 72]
    # 3. Cm9 (C3, Eb3, G3, Bb3, D4)
    cm_9 = [48, 51, 55, 58, 62]
    # 4. Fm9 (F3, Ab3, C4, Eb4, G4)
    fm_9 = [53, 56, 60, 63, 67]
    
    progression = [ab_maj7, bb_9, cm_9, fm_9]
    
    for i, chord in enumerate(progression):
        base_time = i * BAR
        
        for note_idx, note_num in enumerate(chord):
            note = utils.Note()
            note.number = note_num
            
            # Humanización C5-REAL (Baja Entropía de Máquina):
            # 1. Strumming algorítmico (micro-retraso progresivo) emulando peso físico
            strum_delay = note_idx * random.randint(5, 15) 
            
            note.time = base_time + strum_delay
            
            # 2. Sustained length con desgaste termodinámico al final del compás
            note.length = BAR - strum_delay - random.randint(15, 60)
            
            # 3. Velocidad: Fundamental fuerte, tensiones más débiles y aleatoriedad
            base_vel = 0.85 if note_idx == 0 else 0.68
            note.velocity = base_vel + random.uniform(-0.07, 0.07)
            
            score.addNote(note)
