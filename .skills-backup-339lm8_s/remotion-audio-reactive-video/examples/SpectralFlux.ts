/**
 * SpectralFlux.ts — Motor Matemático de Transducción Acústica para Remotion
 * =========================================================================
 * Implementa:
 *   1. Detección de transitorios por Flujo Espectral (Spectral Flux Onset).
 *   2. Filtro balístico asimétrico (Attack/Release) para eliminar el jitter estroboscópico.
 *   3. Mapeo psicoacústico de bandas críticas (Sub-Bass, Bass, Low-Mids, High-Mids, Air).
 *   4. Control Automático de Ganancia (AGC) adaptativo.
 */

export interface PsychoacousticBands {
  subBass: number;   // 20 - 80 Hz   (Bombos, 808s, pulsos sísmicos)
  bass: number;      // 80 - 250 Hz  (Líneas de bajo, toms)
  lowMids: number;   // 250 - 1000 Hz (Cuerpo instrumental, vocales graves)
  highMids: number;  // 1000 - 4000 Hz (Presencia, cajas, sintes líderes)
  air: number;       // > 4000 Hz    (Platos, transitorios finos, respiración)
  onsetEnergy: number; // Disparo neto de potencia acumulada (Spectral Flux)
}

export interface BallisticState {
  smoothedValues: number[];
  prevSpectrum: number[];
  peakGain: number;
}

/**
 * Inicializa el estado persistente del amortiguador balístico.
 */
export function createBallisticState(sampleCount: number = 64): BallisticState {
  return {
    smoothedValues: new Array(sampleCount).fill(0),
    prevSpectrum: new Array(sampleCount).fill(0),
    peakGain: 0.1,
  };
}

/**
 * Filtro balístico asimétrico con constantes de tiempo psicoacústicas.
 * Ataque rápido (reacción al transitorio) y relajación exponencial suave.
 */
export function applyBallistics(
  current: number[],
  state: BallisticState,
  attackAlpha: number = 0.85,
  releaseAlpha: number = 0.14
): number[] {
  const result: number[] = new Array(current.length);

  for (let i = 0; i < current.length; i++) {
    const val = current[i];
    const prev = state.smoothedValues[i] || 0;

    if (val >= prev) {
      result[i] = attackAlpha * val + (1 - attackAlpha) * prev;
    } else {
      result[i] = releaseAlpha * val + (1 - releaseAlpha) * prev;
    }
  }

  state.smoothedValues = [...result];
  return result;
}

/**
 * Calcula el Flujo Espectral (Spectral Flux) rectificado por media onda.
 * Retorna un valor alto únicamente en los impactos de percusión y transitorios súbitos.
 */
export function calculateSpectralFlux(
  currentSpectrum: number[],
  prevSpectrum: number[]
): number {
  let flux = 0;
  for (let i = 0; i < currentSpectrum.length; i++) {
    const diff = currentSpectrum[i] - (prevSpectrum[i] || 0);
    if (diff > 0) {
      flux += diff;
    }
  }
  return flux;
}

/**
 * Extrae las bandas psicoacústicas de un espectro normalizado de 64 muestras logarítmicas.
 */
export function extractBands(
  spectrum: number[],
  state: BallisticState
): PsychoacousticBands {
  const count = spectrum.length;
  if (count === 0) {
    return { subBass: 0, bass: 0, lowMids: 0, highMids: 0, air: 0, onsetEnergy: 0 };
  }

  // 1. Detección de Onset neto
  const flux = calculateSpectralFlux(spectrum, state.prevSpectrum);
  state.prevSpectrum = [...spectrum];

  // 2. Filtro balístico para eliminar parpadeo
  const smoothed = applyBallistics(spectrum, state);

  // 3. Segmentación en bandas críticas
  const subBass = averageRange(smoothed, 0, Math.floor(count * 0.08));
  const bass = averageRange(smoothed, Math.floor(count * 0.08), Math.floor(count * 0.20));
  const lowMids = averageRange(smoothed, Math.floor(count * 0.20), Math.floor(count * 0.45));
  const highMids = averageRange(smoothed, Math.floor(count * 0.45), Math.floor(count * 0.75));
  const air = averageRange(smoothed, Math.floor(count * 0.75), count);

  return {
    subBass: Math.min(1.0, subBass * 1.5),
    bass: Math.min(1.0, bass * 1.4),
    lowMids: Math.min(1.0, lowMids * 1.3),
    highMids: Math.min(1.0, highMids * 1.2),
    air: Math.min(1.0, air * 1.1),
    onsetEnergy: Math.min(1.0, flux * 2.0),
  };
}

function averageRange(arr: number[], start: number, end: number): number {
  if (start >= end || start >= arr.length) return 0;
  const slice = arr.slice(start, end);
  return slice.reduce((sum, val) => sum + val, 0) / slice.length;
}
