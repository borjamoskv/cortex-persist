---
name: c5_acoustic_pre_human_audit_invariant
description: Invariante C5-REAL de test acústico obligatorio en silicio antes de trasladar cualquier activo de audio al operador biológico y veto a la simulación matemática de alma sonora (Gate Acústico Anti-Nata).
trigger: "model_decision"
---

# Invariante de Test Acústico Obligatorio Previo a Traslado Humano (INV_C5_ACOUSTIC_GATE)

## 1. Directiva Fundamental (Fail-Closed Acoustic Gate)
Queda **terminantemente prohibido** que cualquier agente, subagente o enjambre declare como «finalizado», «masterizado» o «listo para escucha» cualquier activo de audio (WAV, MP3, FLAC, stem o banda sonora de vídeo) y lo traslade al Operador Biológico (Borja) **sin haber ejecutado previamente un test acústico determinista en silicio y validado sus métricas físicas reales**.

El agente debe asumir por defecto que **la síntesis matemática o algorítmica no equivale a fidelidad acústica** (Aforismo 2: Confundir mapa con territorio). Todo activo no auditado se clasifica como `ESTADO_ACÚSTICO_NO_VERIFICADO`.

---

## 2. Protocolo de Ejecución del Test Acústico en Silicio
Antes de emitir cualquier enlace de reproducción o reporte de finalización en el chat, el agente DEBE ejecutar de forma obligatoria y automatizada la batería de pruebas:

### Paso 1: Linter Acústico de Exergía (Protocolo Rubin)
Ejecutar el script nativo sobre el archivo de audio:
```bash
python3 ~/.gemini/config/skills/c5-rubin-acoustic-linter/scripts/audit_acoustic_exergy.py <ruta_audio.wav>
```
Se auditan de forma no negociable las 4 invariantes físicas:
1. **Weighted Crest Factor (WCF):** Verificar rango dinámico y transitorios ($CF \ge 8.5\text{ dB}$, ideal $\ge 12.0\text{ dB}$). Detección de aplastamiento por limitación brickwall o fatiga.
2. **Spectral Flatness Measure (SFM / Entropía de Wiener):** $SFM < 0.15$ en la banda media (500 Hz – 5.000 Hz). Si $SFM > 0.35$, se declara presencia de ruido blanco artificial, sibilancia o frote de lija.
3. **Low-End Phase Coherence (LPC):** Correlación estéreo en la banda $< 120\text{ Hz}$ ($LPC \ge 0.95$). Veto absoluto a cancelaciones destructivas en el subgrave.
4. **Detección de Aliasing y Clipping:** Inspección de armónicos reflectivos por saturación no lineal ($\tanh$, distorsión analítica) ejecutada sin sobremuestreo (*oversampling* $\ge 4\times$).

### Paso 2: Auditoría Tímbrica y Falsación de Suplantación (Anti-Politono)
- **Veto a la Síntesis Aditiva Ingenua como Sustituto Orgánico:** Queda prohibido trasladar sumas de ondas sinusoidales elementales (`np.sin`) o ráfagas de ruido aleatorio uniforme como si fueran instrumentos acústicos o electromecánicos reales (Rhodes, baterías analógicas, vientos, cuerdas). Si se empleó síntesis elemental, DEBE etiquetarse explícitamente como *«boceto algorítmico de laboratorio / maqueta de frecuencias»*, nunca como *«tema masterizado»*.
- **Veto a Voces de Accesibilidad como Voces Humanas:** Queda prohibido emplear voces sintéticas de texto a voz obsoletas (ej. macOS `say`) pretending que representen cantantes, artistas o *spoken word* profesional.

---

## 3. La Invariante del «Alma» Sonora y el Coste No Falsificable (Aforismo 5)
Superar el Linter Acústico es **condición necesaria, pero NO suficiente** para la entrega musical.
- **Definición Ontológica del Alma:** El «alma» en la música es la presencia de **coste biológico e histórico no falsificable** (Aforismo 5: *Lo voluntario vale menos que lo involuntario*). Un algoritmo de bucle `for` ejecutando notas a tempo tiene coste termodinámico cero: es un autómata voluntario y estéril.
- **Veto a la Pretensión de Alma Algorítmica:** Queda estrictamente prohibido afirmar que una pista ensamblada mediante código determinista posee «calidez», «groove humano» o «alma». Si la pista carece de transducción biológica involuntaria, DEBE clasificarse honestamente como `AUTÓMATA_SINTÉTICO_ESTRUCTURAL`.
- **Las Tres Vías Exclusivas del Alma Sonora:**
  1. *Sampling Histórico Irreemplazable:* Cortes de grabaciones analógicas reales con coste humano real (vinilo, grabaciones de campo, voces vivas desgarradas).
  2. *Inferencia Neuronal con Latente Masivo:* Modelos de difusión (Suno v4 / Udio) cuyos pesos capturan la huella holográfica de la interpretación humana real.
  3. *Transducción Directa del Operador Biológico:* Grabación directa de la interpretación del usuario (Ring-0) sobre el hardware o teclado MIDI en el DAW, actuando el silicio como mero canal esclavo.

---

## 4. Matriz de Decisión y Salida Fail-Closed
1. **Si el Test Acústico y la Auditoría Tímbrica se superan:** Se certifica la entrega adjuntando las métricas cuantitativas del linter.
2. **Si el Test Acústico FALLA:** Prohibición absoluta de *cheap talk*. Declarar el fallo forense inmediato y derivar el trabajo a FL Studio o a modelos neuronales.
