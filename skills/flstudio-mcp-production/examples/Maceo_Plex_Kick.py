# name = Maceo Plex Kick & Sub-Rumble
# author = Moskv-1 (C5-REAL)
# description = Generador algoritmico de bombo Techno y disparadores de sub-rumble en semicorcheas.

import utils
import math

def createScore():
    score.clear()
    
    # Resolución termodinámica
    BAR = 1920
    BEAT = 480
    SIXTEENTH = 120
    
    # Topología Frecuencial
    # F2 (41) = ~43.65 Hz (Fundamental del bombo)
    # F1 (29) = ~21.83 Hz (Lecho del Sub-Rumble)
    kick_note = 41 
    rumble_note = 29 
    
    # Generaremos un bloque de 4 compases (macro-bucle)
    num_bars = 4
    
    for bar in range(num_bars):
        base_time = bar * BAR
        
        for beat in range(4):
            beat_time = base_time + (beat * BEAT)
            
            # 1. EL BOMBO (4-on-the-floor)
            # Alta exergía, transitorio puro. Longitud quirúrgica para evitar solapamiento de graves (anergía de fase).
            k = utils.Note()
            k.number = kick_note
            k.time = beat_time
            k.length = 80 # Decay rápido
            k.velocity = 1.0 # Señal de control máxima para saturación Tanh
            
            # Ligero swing en los tiempos débiles (2 y 4) para el pocket
            if beat == 1 or beat == 3:
                k.time += 3
            
            score.addNote(k)
            
            # 2. EL SUB-RUMBLE (Semicorcheas intermitentes)
            # Pasos de semicorchea 2, 3 y 4 (skip el primer paso donde golpea el kick)
            # Matriz de velocity para crear el 'bombeo' (sidechain) sin usar compresor
            rumble_matrix = [(1, 0.45), (2, 0.70), (3, 0.55)]
            
            for step, vel in rumble_matrix:
                r = utils.Note()
                r.number = rumble_note
                
                # Offset base
                step_time = beat_time + (step * SIXTEENTH)
                
                # Retardo micro-temporal C5-REAL (Invariante de respiración)
                # Empujamos el rumble 5 ticks atrás para asegurar que nunca colisione con la fase de la cola del kick
                r.time = step_time + 5 
                r.length = SIXTEENTH - 10
                
                # Desgaste de velocidad en compases pares para inducir movimiento
                if bar % 2 != 0:
                    r.velocity = vel * 0.9
                else:
                    r.velocity = vel
                    
                score.addNote(r)
