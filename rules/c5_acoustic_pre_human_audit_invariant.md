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

### 3.1 Las 6 Invariantes Anti-Máquina de Producción Orgánica (Protocolo «La luz tarda» / Lindstrøm)
Para que ningún activo acústico suene a máquina o autómata estéril, la producción debe satisfacer estrictamente:
1. **Veto a la Aleatorización Estéril (Fake Humanize):** El micro-groove humano no es ruido blanco ni fluctuación gaussiana ciega sobre todas las notas. Es un vector físico con intención somática: atraso causal del bajo eléctrico respecto al bombo (+4 a +8 ms *behind-the-beat*), aceleración sutil al encarar caídas de compás y respeto sagrado por el silencio sin rellenar.
2. **Tomas Continuas vs. Bucles Copiados:** Exigencia de tomas largas completas (ej. 6 minutos ininterrumpidos en congas, shaker, pandereta) para preservar la micro-fatiga biológica, variaciones de presión de palma y respiración natural, erradicando la fatiga de bucle (*copy-paste fatigue*).
3. **Erradicación del Efecto Metralleta (*Machine-Gun Effect*):** Veto a muestras idénticas consecutivas; alternancia estricta de articulaciones (*round-robin* >= 5 tomas o síntesis diferencial continua).
4. **Suavizado de Transitorios y Veto a Agudos Plásticos:** Corte suave por encima de 14 kHz en platos, ataques de púa y sintetizadores; redondeo mediante saturación analógica de cinta/válvulas para fusionar timbres con la madera acústica.
5. **Cohesión por Sala Compartida (*Shared Convolution Room*):** Todos los instrumentos envían una fracción de señal a un bus auxiliar de sala común (madera o placa EMT 140 con pre-delay de 18 ms), unificando la reverberación en un único volumen de aire físico.
6. **El Test de Escucha a Bajo Volumen (*The Whisper Test*):** Verificación a 55–60 dB SPL. Si el motivo melódico y el diálogo bajo-bombo pierden inteligibilidad o conmoción a bajo volumen, el arreglo o la mezcla dependen de volumen bruto y se declaran descalibrados.

### 3.2 Demarcación de Honestidad Mapa vs. Territorio (Aforismo 2 y 5)
Cuando el Operador comparta una composición como guía de producción sin monitorización física directa disponible, el agente tiene terminantemente prohibido afirmar que ha realizado una «escucha humana», «revisión de grabación» o «auditoría de máster final» (*cheap talk*), debiendo tratar el activo estrictamente como *Mapa Canónico de Producción* y partitura simbólica.

### 3.3 Invariante de Detección Forense: La Falacia de la Zonificación Espectral y la Intermodulación en Tensor Único
Queda terminantemente prohibido que el agente evalúe la autenticidad o calidad de un activo de audio apoyándose en la falacia de que «la IA domina los tonos medios y solo falla en los extremos»:
1. **El Epicentro del Uncanny Valley:** El agente debe reconocer que los tonos medios (1 kHz – 4 kHz) son el punto de máximo escrutinio biológico. La presencia de *micro-comb filtering*, resonancias nasales estacionarias o *phase smearing* en los formantes vocales delata la naturaleza sintética de forma más contundente que un artefacto de alta frecuencia.
2. **Causa Causal (Intermodulación en Tensor Compartido):** La firma de la síntesis neural no reside en el balance tonal estático, sino en la **intermodulación cruzada espuria** provocada por decodificar múltiples fuentes desde una misma variedad latente compartida ($Z = \mathcal{W} \ast [S_{\text{voz}} \oplus S_{\text{bajo}} \oplus S_{\text{batería}}]$). Si los transitorios de la percusión modulan la envolvente espectral de las cuerdas o voces, el activo se clasifica como `CONTAMINADO_POR_ACOPLAMIENTO_LATENTE`.

---

## 4. Matriz de Decisión y Salida Fail-Closed
1. **Si el Test Acústico y la Auditoría Tímbrica se superan:** Se certifica la entrega adjuntando las métricas cuantitativas del linter.
2. **Si el Test Acústico FALLA:** Prohibición absoluta de *cheap talk*. Declarar el fallo forense inmediato y derivar el trabajo a FL Studio o a modelos neuronales.
---

## 5. Invariante de Transcripción ASR / Whisper (Anti-Fuga Anglocéntrica)
En cualquier pipeline de procesamiento o cosecha de voz en castellano empleando OpenAI Whisper o variantes (, ):
1. **Veto a Checkpoints Monolingües:** Prohibición absoluta de usar modelos con sufijo  (, , etc.) para material en castellano.
2. **Forzado Determinista de Tarea e Idioma:** En toda invocación de inferencia es mandatorio declarar explícitamente:
   -  (para neutralizar la traducción forzada al inglés).
   -  (para anular el fallo del clasificador estocástico de los primeros 30s).
