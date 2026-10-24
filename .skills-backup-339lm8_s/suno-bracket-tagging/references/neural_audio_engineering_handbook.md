# Manual de Referencia: Ingeniería Acústica y Fundamentos Teóricos de Audio AI (C5)

Este manual documenta la base matemática, física y de procesamiento de señales que rige los motores de síntesis acústica neuronal (Suno, Udio, YuE, Stable Audio, DDSP).

---

## 1. Límites Físicos del Audio Neuronal

### A. El Límite de Incertidumbre de Heisenberg-Gabor
$$\Delta t \cdot \Delta f \ge \frac{1}{4\pi}$$
En cuantizadores vectoriales residuales (RVQ tipo EnCodec o DAC), comprimir audio a $1.5 - 6 \text{ kbps}$ para inferencia de tokens discretos a 50–100 Hz destruye la coherencia de fase en alta frecuencia. Al recuperar la señal mediante upsampling y vocoders neuronales, el sistema alucina la fase, provocando:
* *Phase smearing* en transitorios de percusión.
* Imposibilidad de separación matricial de pistas limpia a posteriori sin artefactos espectrales.

### B. Mutilación de la Correlación Interaural (IACC)
$$\text{IACC} = \max_{\tau} \left| \frac{\int_{t_1}^{t_2} x_L(t) x_R(t + \tau) \, dt}{\sqrt{\int_{t_1}^{t_2} x_L^2(t) \, dt \int_{t_1}^{t_2} x_R^2(t + \tau) \, dt}} \right|$$
La inferencia estocástica de canales $L/R$ genera una decorrelación artificial que carece de coherencia con las reflexiones de una sala física. En subgraves ($< 120 \text{ Hz}$), esto provoca cancelaciones de fase acústica severas.

---

## 2. Dinámica de Colapso del Modelo (Model Autophagy Disorder - MAD)

Shumailov et al. formalizaron cómo el re-entrenamiento sobre datos sintéticos genera contracción estadística:
1. **Erosión de las colas de distribución:** Modulaciones armónicas no estándar o compases complejos son purgados en favor de atractores de alta densidad ($4/4$, cadencia I–V–vi–IV).
2. **Endogamia espectral:** Los *checkerboard artifacts* y resonancias fijas de convoluciones transpuestas previas son asimilados por las siguientes generaciones del modelo como propiedades intrínsecas del audio.

---

## 3. Neurobiología de la Expectativa Musical (Teoría ITPRA y Free Energy)

David Huron (ITPRA) y Karl Friston (Free Energy Principle):
$$\text{Goce Estético} \propto -\log P(x_t \mid x_{<t}) \quad \text{sujeto a coherencia global}$$
* Los modelos de lenguaje musical optimizan la verosimilitud estadística máxima, colapsando hacia el promedio de los clichés del género.
* La música con valor semiótico vive en las **singularidades de baja probabilidad gobernadas por una intención férrea** (rubato, suspensiones armónicas, dinámicas extremas).

---

## 4. Frontera Post-Token: Continuous Flow Matching (OT-CFM)

En lugar de predecir tokens discretos secuenciales, CFM modela una Ecuación Diferencial Ordinaria (ODE) que transforma ruido en variedad acústica a través de trayectorias rectas de mínima energía:
$$\psi_t(x) = (1 - t) x_0 + t x_1 \quad \text{con campo vectorial } v_t = x_1 - x_0$$
* Inferencia paralela no causal en $15-30$ pasos de integración.
* Cero acumulación de error temporal a lo largo de secuencias extensas.

---

## 5. Implementación Canónica DDSP (PyTorch)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DifferentiableHarmonicSynthesizer(nn.Module):
    """
    Sintetizador aditivo armónico con coherencia de fase analítica exacta.
    """
    def __init__(self, sample_rate=44100, num_harmonics=64):
        super().__init__()
        self.sample_rate = sample_rate
        self.num_harmonics = num_harmonics

    def forward(self, f0, harmonic_amplitudes, total_samples):
        # f0: [Batch, Frames, 1] en Hz
        # harmonic_amplitudes: [Batch, Frames, num_harmonics] (Normalizadas con Softmax)
        f0_up = F.interpolate(f0.transpose(1, 2), size=total_samples, mode='linear', align_corners=False).transpose(1, 2)
        h_up = F.interpolate(harmonic_amplitudes.transpose(1, 2), size=total_samples, mode='linear', align_corners=False).transpose(1, 2)

        indices = torch.arange(1, self.num_harmonics + 1, device=f0.device).float()
        freqs = f0_up * indices

        nyquist_mask = (freqs < (self.sample_rate / 2)).float()
        phases = torch.cumsum(2.0 * torch.pi * freqs / self.sample_rate, dim=1)

        sinusoids = torch.sin(phases) * h_up * nyquist_mask
        return torch.sum(sinusoids, dim=-1)
```

---

## 6. Síntesis Espacial en Armónicos Esféricos (HOA)

Ecuación de descomposición del campo acústico tridimensional:
$$P(r, \theta, \phi, t) = \sum_{l=0}^{N} \sum_{m=-l}^{l} B_l^m(t) \cdot Y_l^m(\theta, \phi)$$
Permite generar mezclas espaciales en 16 canales (Orden 3) que son decodificadas dinámicamente en el cliente según la orientación de la cabeza del oyente mediante funciones HRTF.
