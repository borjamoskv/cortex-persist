#!/usr/bin/env python3
"""
Motor de Transducción y Síntesis Vocal AOT (F5-TTS / MPS / Protocolo Rubin)
Sintetiza voz hiperrealista utilizando las referencias catalogadas en voices_manifest.json.
"""

import os
import sys
import json
import argparse
import subprocess
import torch
import soundfile as sf

# 1. Bypass del tokenizador rjieba para español
try:
    import f5_tts.infer.utils_infer as utils_infer
    utils_infer.convert_char_to_pinyin = lambda text_list, **kw: [[c for c in text] for text in text_list]
except ImportError:
    pass

def main():
    parser = argparse.ArgumentParser(description="Síntesis Vocal AOT C5-REAL (F5-TTS)")
    parser.add_argument("--speaker", required=True, help="ID del perfil vocal (ej. borja, luengo, gon, patxi, alain_electro)")
    parser.add_argument("--text", required=True, help="Texto en español a sintetizar")
    parser.add_argument("--output", help="Ruta de salida del audio (.wav u .opus)")
    args = parser.parse_args()

    manifest_path = os.path.expanduser("~/Music/VOICE_CLONES/voices_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"Error: No se encuentra el manifiesto de voces en {manifest_path}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    speaker_key = args.speaker.lower().replace(" ", "_")
    if speaker_key not in manifest:
        print(f"Error: Perfil '{speaker_key}' no encontrado. Disponibles: {list(manifest.keys())}", file=sys.stderr)
        sys.exit(1)

    speaker_data = manifest[speaker_key]
    refs = speaker_data.get("references", [])
    if not refs:
        print(f"Error: No hay audios de referencia para {speaker_key}", file=sys.stderr)
        sys.exit(1)

    ref_item = refs[0]
    ref_audio_path = ref_item["wav_path"]
    ref_transcript = ref_item.get("ref_text", "")

    cadence_info = speaker_data.get("cadence_metrics", {})
    speed = cadence_info.get("rec_speed", 1.12)

    out_path = args.output
    if not out_path:
        out_dir = os.path.expanduser("~/Music/VOICE_SYNTHESIS")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{speaker_key}_synthesis.opus")

    print(f"🎙️ Sintetizando voz para [{speaker_data['display_name']}]...")
    print(f"   ├▸ Referencia: {os.path.basename(ref_audio_path)}")
    print(f"   ├▸ Speed calibrado: {speed:.2f}x")
    print(f"   └▸ Texto: \"{args.text}\"")

    # Inferencia con F5TTS API
    from f5_tts.api import F5TTS
    from f5_tts.infer.utils_infer import infer_batch_process, preprocess_ref_audio_text

    if torch.backends.mps.is_available():
        torch.mps.empty_cache()

    ckpt = os.path.expanduser("~/.cache/f5-tts-es/model_1250000.safetensors")
    vocab = os.path.expanduser("~/.cache/f5-tts-es/vocab.txt")
    kwargs = {
        "model": "F5TTS_Base",
        "device": "mps" if torch.backends.mps.is_available() else "cpu"
    }
    if os.path.exists(ckpt) and os.path.exists(vocab):
        kwargs["ckpt_file"] = ckpt
        kwargs["vocab_file"] = vocab

    f5 = F5TTS(**kwargs)

    prep_file, prep_text = preprocess_ref_audio_text(ref_audio_path, ref_transcript)
    d, sr = sf.read(prep_file)
    audio = torch.from_numpy(d).float().unsqueeze(0) if d.ndim == 1 else torch.from_numpy(d.T).float()

    wav, out_sr, _ = next(
        infer_batch_process(
            (audio, sr),
            prep_text,
            [args.text.lower()],
            f5.ema_model,
            f5.vocoder,
            mel_spec_type=f5.mel_spec_type,
            target_rms=0.1,
            cross_fade_duration=0.15,
            nfe_step=64,
            cfg_strength=1.80,
            sway_sampling_coef=-0.8,
            speed=speed,
            device="mps" if torch.backends.mps.is_available() else "cpu"
        )
    )

    raw_tmp = "/tmp/f5_raw_synthesis.wav"
    sf.write(raw_tmp, wav, out_sr)

    # Masterización broadcast FFmpeg
    filter_chain = (
        "volume=0.88,"
        "highpass=f=55,lowpass=f=7800,"
        "equalizer=f=180:width_type=q:width=1.2:gain=1.5,"
        "equalizer=f=3200:width_type=q:width=1.0:gain=1.8,"
        "asoftclip=type=atan:param=1.2,"
        "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=70:makeup=1.0dB,"
        "loudnorm=I=-16:TP=-1.5:LRA=7"
    )

    cmd_opus = [
        "ffmpeg", "-y", "-i", raw_tmp,
        "-af", filter_chain,
        "-c:a", "libopus", "-b:a", "24k", "-vbr", "on", "-application", "voip",
        out_path
    ]
    subprocess.run(cmd_opus, check=True)

    print(f"✓ Síntesis masterizada guardada en: {out_path}")

    # Copiar a portapapeles de macOS
    try:
        osascript_cmd = f'set the clipboard to POSIX file "{out_path}"'
        subprocess.run(["osascript", "-e", osascript_cmd], check=True)
        print("✓ Audio copiado al portapapeles de macOS (Listo para Cmd+V en WhatsApp)")
    except Exception as e:
        print(f"Aviso portapapeles: {e}")

if __name__ == "__main__":
    main()
