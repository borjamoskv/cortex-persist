import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useAudioData, visualizeAudio } from "@remotion/media-utils";
import { createBallisticState, extractBands } from "./SpectralFlux";

interface AudioReactiveProps {
  audioSrc?: string;
  stemKickSrc?: string;
  bpm?: number;
  trackTitle?: string;
  artistName?: string;
}

export const AudioReactiveMaster: React.FC<AudioReactiveProps> = ({
  audioSrc = "audio/master_track.mp3",
  stemKickSrc,
  bpm = 124,
  trackTitle = "SONIC MANIFOLD",
  artistName = "CORTEX ENGINE",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // 1. Carga de audio master y stem opcional
  const audioData = useAudioData(staticFile(audioSrc));
  const kickAudioData = useAudioData(stemKickSrc ? staticFile(stemKickSrc) : staticFile(audioSrc));

  // 2. Estado balístico en memoria (evita parpadeo)
  const ballisticState = useMemo(() => createBallisticState(64), []);

  if (!audioData) {
    return <AbsoluteFill style={{ backgroundColor: "#050508" }} />;
  }

  // 3. Extracción de espectro logarítmico (64 bandas)
  const spectrum = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: 64,
    grouping: "logarithmic",
    smoothSpectrum: true,
  });

  // 4. Transducción matemática a bandas psicoacústicas
  const { subBass, bass, lowMids, highMids, air, onsetEnergy } = extractBands(
    spectrum,
    ballisticState
  );

  // 5. Cuadrícula de fase BPM (Pulse locked)
  const framesPerBeat = (fps * 60) / bpm;
  const beatPhase = (frame % framesPerBeat) / framesPerBeat;
  const beatDecay = Math.exp(-beatPhase * 4.0); // Caída exponencial percusiva

  // 6. Cámara dinámica (Empuje de lente y Screen Shake con Sub-Bass y Onsets)
  const cameraScale = interpolate(
    subBass * 0.7 + onsetEnergy * 0.3,
    [0, 1],
    [1.0, 1.08],
    { extrapolateRight: "clamp" }
  );

  const shakeX = (Math.sin(frame * 1.5) * onsetEnergy * 12);
  const shakeY = (Math.cos(frame * 1.8) * onsetEnergy * 10);

  // 7. Aberración cromática y grano según agudos
  const aberrationOffset = interpolate(air, [0, 1], [0, 8], { extrapolateRight: "clamp" });
  const glowIntensity = interpolate(highMids, [0, 1], [15, 60], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#06070a",
        transform: `scale(${cameraScale}) translate(${shakeX}px, ${shakeY}px)`,
        transformOrigin: "center center",
        overflow: "hidden",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}
    >
      <Audio src={staticFile(audioSrc)} />

      {/* FONDO: Halo reactivo a graves profundos */}
      <div
        style={{
          position: "absolute",
          inset: "-20%",
          background: `radial-gradient(circle at 50% 50%, rgba(30, 80, 220, ${0.15 + subBass * 0.35}) 0%, rgba(5, 7, 10, 0.95) 70%)`,
          filter: `blur(40px)`,
        }}
      />

      {/* CENTRO: Espectrograma Radial Simétrico */}
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 500,
          height: 500,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {spectrum.map((val, i) => {
          const angle = (i / spectrum.length) * 360;
          const barHeight = interpolate(val, [0, 1], [8, 140], { extrapolateRight: "clamp" });
          const barHue = 200 + (i / spectrum.length) * 80;

          return (
            <div
              key={i}
              style={{
                position: "absolute",
                width: 4,
                height: `${barHeight}px`,
                backgroundColor: `hsl(${barHue}, 90%, ${55 + val * 35}%)`,
                borderRadius: 2,
                transformOrigin: "bottom center",
                transform: `rotate(${angle}deg) translateY(-170px)`,
                boxShadow: `0 0 ${glowIntensity * 0.5}px hsla(${barHue}, 90%, 60%, 0.4)`,
              }}
            />
          );
        })}

        {/* NÚCLEO CINÉTICO: Orbe deformable */}
        <div
          style={{
            width: 220 + bass * 80,
            height: 220 + bass * 80,
            borderRadius: "50%",
            background: "linear-gradient(135deg, #101525, #080a12)",
            border: `2px solid rgba(120, 180, 255, ${0.4 + onsetEnergy * 0.6})`,
            boxShadow: `0 0 ${glowIntensity}px rgba(80, 140, 255, 0.35), inset 0 0 30px rgba(0,0,0,0.8)`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
            transition: "width 0.05s ease-out, height 0.05s ease-out",
          }}
        >
          <div
            style={{
              color: "#ffffff",
              fontSize: 24,
              fontWeight: 800,
              letterSpacing: 4,
              textShadow: `0 0 15px rgba(255,255,255,0.8)`,
            }}
          >
            {trackTitle}
          </div>
          <div
            style={{
              color: "#6b8af0",
              fontSize: 13,
              fontWeight: 600,
              letterSpacing: 2,
              marginTop: 6,
              opacity: 0.85 + beatDecay * 0.15,
            }}
          >
            {artistName} • {bpm} BPM
          </div>
        </div>
      </div>

      {/* OVERLAY DE ABERRACIÓN ÓPTICA & GRANO */}
      {aberrationOffset > 1 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            pointerEvents: "none",
            mixBlendMode: "screen",
            opacity: 0.25,
            boxShadow: `inset ${aberrationOffset}px 0 0 rgba(255,0,50,0.5), inset -${aberrationOffset}px 0 0 rgba(0,150,255,0.5)`,
          }}
        />
      )}
    </AbsoluteFill>
  );
};
