#!/usr/bin/env python3
"""
CoreMIDI & MPE Virtual Daemon Bridge for FL Studio 2025
C5-REAL High-Exergy Audio Engineering Engine

Opens a low-latency virtual MIDI output port ('Antigravity MCP Out')
and provides sub-cent microtonal pitch-bend (14-bit MPE) and CC automation.
"""

import sys
import time
import argparse

def get_mido_backend():
    try:
        import mido
        return mido
    except ImportError:
        print("[!] 'mido' or 'python-rtmidi' not installed. Install via: pip install mido python-rtmidi", file=sys.stderr)
        return None

def run_daemon(port_name: str = "Antigravity MCP Out"):
    mido = get_mido_backend()
    if not mido:
        sys.exit(1)
        
    print(f"[*] Opening virtual CoreMIDI output port: '{port_name}'...")
    try:
        with mido.open_output(port_name, virtual=True) as outport:
            print(f"[✓] Virtual MIDI port active and listening.")
            print(f"[*] In FL Studio: Open Options > MIDI settings (F10), find '{port_name}' and enable on Port 15.")
            print(f"[*] Press Ctrl+C to stop daemon.")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[✓] CoreMIDI daemon stopped.")

def send_test_note(note: int = 60, velocity: int = 100, duration: float = 0.5, port_name: str = "Antigravity MCP Out"):
    mido = get_mido_backend()
    if not mido:
        sys.exit(1)
        
    try:
        with mido.open_output(port_name, virtual=True) as outport:
            print(f"[*] Sending Note On: note={note}, vel={velocity} on '{port_name}'")
            outport.send(mido.Message('note_on', note=note, velocity=velocity))
            time.sleep(duration)
            outport.send(mido.Message('note_off', note=note, velocity=0))
            print("[✓] Note Off sent.")
    except Exception as e:
        print(f"[!] Error sending test note: {e}")

def send_microtonal_pitch_bend(cents_offset: float, semitone_range: int = 2, channel: int = 0, port_name: str = "Antigravity MCP Out"):
    """
    Calculates 14-bit pitch bend for sub-cent microtonal deviation.
    Pitch bend range: -8192 to +8191 representing +/- semitone_range * 100 cents.
    """
    mido = get_mido_backend()
    if not mido:
        sys.exit(1)

    total_cents = semitone_range * 100.0
    normalized = max(-1.0, min(1.0, cents_offset / total_cents))
    bend_val = int(normalized * 8191)

    try:
        with mido.open_output(port_name, virtual=True) as outport:
            print(f"[*] Sending Microtonal Pitch Bend: {cents_offset:+.2f} cents -> Bend value {bend_val} on ch {channel}")
            outport.send(mido.Message('pitchwheel', pitch=bend_val, channel=channel))
            print("[✓] Pitchwheel message sent.")
    except Exception as e:
        print(f"[!] Error sending pitch bend: {e}")

def main():
    parser = argparse.ArgumentParser(description="Antigravity CoreMIDI / MPE Virtual Bridge for FL Studio")
    parser.add_argument("--daemon", action="store_true", help="Keep virtual port open indefinitely")
    parser.add_argument("--test-note", type=int, metavar="NOTE", help="Send test MIDI note (0-127)")
    parser.add_argument("--cents", type=float, default=0.0, help="Microtonal fine detune in cents (-100 to +100)")
    parser.add_argument("--port", type=str, default="Antigravity MCP Out", help="Virtual port name")

    args = parser.parse_args()

    if args.daemon:
        run_daemon(args.port)
        return

    if args.test_note is not None:
        if args.cents != 0.0:
            send_microtonal_pitch_bend(args.cents, port_name=args.port)
        send_test_note(note=args.test_note, port_name=args.port)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
