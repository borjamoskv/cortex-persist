#!/usr/bin/env python3
"""
Scala (.scl) & Keyboard Mapping (.kbm) Mathematical Generator
C5-REAL High-Exergy Psychoacoustic Audio Engineering Engine (v6.0)

Generates mathematically rigorous Scala tuning files and keyboard mappings
for FL Studio 2025, Harmor, Sytrus, Vital, Surge XT, and Kontakt.
Integrates Sethares / Plomp-Levelt sensory dissonance evaluation.
"""

import os
import sys
import math
import argparse
from pathlib import Path

DEFAULT_TUNING_DIR = Path.home() / "Documents/Image-Line/FL Studio/Settings/Tuning"

TEMPERAMENTS = {
    # ─── EQUAL TEMPERAMENTS ───────────────────────────────────────────
    "12-tet": {
        "name": "12 Equal Temperament (Standard Western)",
        "description": "Standard 12-TET reference tuning (100 cents per semitone)",
        "notes": [100.0 * i for i in range(1, 13)],
        "formal_octave": 12,
    },
    "19-tet": {
        "name": "19 Equal Temperament (Third-tone system)",
        "description": "19-TET with pure major thirds and minor thirds compared to 12-TET",
        "notes": [(1200.0 / 19.0) * i for i in range(1, 20)],
        "formal_octave": 19,
    },
    "24-tet": {
        "name": "24 Equal Temperament (Quarter-tone system)",
        "description": "24-TET quarter-tone scale with 50.0 cents step size",
        "notes": [50.0 * i for i in range(1, 25)],
        "formal_octave": 24,
    },
    "31-tet": {
        "name": "31 Equal Temperament (Fokker / Huygens)",
        "description": "31-TET quarter-comma meantone approximation with near-pure thirds",
        "notes": [(1200.0 / 31.0) * i for i in range(1, 32)],
        "formal_octave": 31,
    },
    "41-tet": {
        "name": "41 Equal Temperament",
        "description": "41-TET providing excellent approximations of 5-limit and 7-limit intervals",
        "notes": [(1200.0 / 41.0) * i for i in range(1, 42)],
        "formal_octave": 41,
    },
    "53-tet": {
        "name": "53 Equal Temperament (Mercator / Holder)",
        "description": "Near-perfect Pythagorean fifths and Zarlino thirds (Holderian comma)",
        "notes": [(1200.0 / 53.0) * i for i in range(1, 54)],
        "formal_octave": 53,
    },
    "72-tet": {
        "name": "72 Equal Temperament (Ekim / Byzantine)",
        "description": "Sixth-tones: ideal for traditional Turkish Makam and Byzantine chant",
        "notes": [(1200.0 / 72.0) * i for i in range(1, 73)],
        "formal_octave": 72,
    },

    # ─── HISTORICAL & WELL-TEMPERAMENTS ──────────────────────────────
    "werckmeister-3": {
        "name": "Werckmeister III (Andreas Werckmeister, 1691)",
        "description": "Well-tempered system with 4 tempered fifths (C-G, G-D, D-A, B-F#)",
        "notes": [90.225, 192.180, 294.135, 390.225, 498.045, 588.270, 696.090, 792.180, 888.270, 996.090, 1092.180, 1200.000],
        "formal_octave": 12,
    },
    "kirnberger-3": {
        "name": "Kirnberger III (Johann Philipp Kirnberger, 1779)",
        "description": "Well-temperament with 4 pure fifths and 4 fifths tempered by 1/4 syntonic comma",
        "notes": [90.225, 193.157, 294.135, 386.314, 498.045, 590.224, 696.578, 792.180, 889.735, 996.090, 1088.269, 1200.000],
        "formal_octave": 12,
    },
    "pythagorean-12": {
        "name": "Pythagorean 12-Tone Scale",
        "description": "Constructed from a chain of 11 pure 3:2 fifths with Pythagorean comma wolf on G#-Eb",
        "notes": [90.225, 203.910, 294.135, 407.820, 498.045, 611.730, 701.955, 792.180, 905.865, 996.090, 1109.775, 1200.000],
        "formal_octave": 12,
    },
    "quarter-comma-meantone": {
        "name": "1/4 Syntonic Comma Meantone",
        "description": "Renaissance meantone tuning with pure major thirds (5:4 ~386.31 cents)",
        "notes": [76.049, 193.157, 310.265, 386.314, 503.422, 579.471, 696.578, 772.627, 889.735, 1006.843, 1082.892, 1200.000],
        "formal_octave": 12,
    },

    # ─── ARABIC MAKAMAAT SUITE ───────────────────────────────────────
    "makam-bayati": {
        "name": "Arabic Makam Bayati (in D)",
        "description": "D, E half-flat (Sikah 150c), F (300c), G (500c), A (700c), Bb (800c), C (1000c), D (1200c)",
        "notes": [150.0, 300.0, 500.0, 700.0, 800.0, 1000.0, 1200.0],
        "formal_octave": 7,
    },
    "makam-rast": {
        "name": "Arabic Makam Rast (in C)",
        "description": "C, D (200c), E half-flat (350c), F (500c), G (700c), A (900c), B half-flat (1050c), C (1200c)",
        "notes": [200.0, 350.0, 500.0, 700.0, 900.0, 1050.0, 1200.0],
        "formal_octave": 7,
    },
    "makam-hijaz": {
        "name": "Arabic Makam Hijaz (in D)",
        "description": "D, Eb (100c), F# (385c augmented 2nd), G (500c), A (700c), Bb (800c), C (1000c), D (1200c)",
        "notes": [100.0, 385.0, 500.0, 700.0, 800.0, 1000.0, 1200.0],
        "formal_octave": 7,
    },
    "makam-saba": {
        "name": "Arabic Makam Saba (in D)",
        "description": "D, E half-flat (150c), F (300c), Gb (400c neutral 4th), A (700c), Bb (800c), C (1000c), D (1200c)",
        "notes": [150.0, 300.0, 400.0, 700.0, 800.0, 1000.0, 1200.0],
        "formal_octave": 7,
    },
    "makam-sikah": {
        "name": "Arabic Makam Sikah (Root on Sikah E half-flat)",
        "description": "Root 150c, Rast 350c, Nawa 500c, Husayni 700c, Auj 850c, Kardan 1000c, Octave 1200c",
        "notes": [200.0, 350.0, 550.0, 700.0, 850.0, 1050.0, 1200.0],
        "formal_octave": 7,
    },

    # ─── INDIAN CLASSICAL THATS ──────────────────────────────────────
    "that-bhairav": {
        "name": "Indian That Bhairav (Morning Raga foundation)",
        "description": "Sa, komal Re, shuddha Ga, shuddha Ma, Pa, komal Dha, shuddha Ni, Sa",
        "notes": [112.0, 386.3, 498.0, 702.0, 814.0, 1088.3, 1200.0],
        "formal_octave": 7,
    },
    "that-todi": {
        "name": "Indian That Todi (Severe Contemplation)",
        "description": "Sa, komal Re, komal Ga, tivra Ma (tritone), Pa, komal Dha, shuddha Ni, Sa",
        "notes": [112.0, 315.6, 590.2, 702.0, 814.0, 1088.3, 1200.0],
        "formal_octave": 7,
    },
    "that-yaman": {
        "name": "Indian That Yaman / Kalyan (Evening Raga)",
        "description": "Sa, shuddha Re, shuddha Ga, tivra Ma, Pa, shuddha Dha, shuddha Ni, Sa",
        "notes": [203.9, 386.3, 590.2, 702.0, 905.9, 1088.3, 1200.0],
        "formal_octave": 7,
    },

    # ─── JUST INTONATION HARMONIC SERIES ─────────────────────────────
    "just-intonation-5limit": {
        "name": "5-Limit Just Intonation (Ptolemaic Intense Diatonic)",
        "description": "Pure harmonic ratios: 1/1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2/1",
        "notes": ["9/8", "5/4", "4/3", "3/2", "5/3", "15/8", "2/1"],
        "formal_octave": 7,
    },
    "just-intonation-7limit": {
        "name": "7-Limit Just Intonation (Harmonic Septimal Tuning)",
        "description": "Includes septimal intervals: 9/8, 5/4, 4/3, 7/5, 3/2, 5/3, 7/4, 2/1",
        "notes": ["9/8", "5/4", "4/3", "7/5", "3/2", "5/3", "7/4", "2/1"],
        "formal_octave": 8,
    },
    "harmonic-series-8-16": {
        "name": "Harmonic Series (Partials 8 through 16)",
        "description": "Pure overtones: 9/8, 10/8, 11/8, 12/8, 13/8, 14/8, 15/8, 16/8",
        "notes": ["9/8", "5/4", "11/8", "3/2", "13/8", "7/4", "15/8", "2/1"],
        "formal_octave": 8,
    },

    # ─── NON-OCTAVE & EXPERIMENTAL SCALES ────────────────────────────
    "bohlen-pierce": {
        "name": "Bohlen-Pierce Scale (Equal-tempered Tritave)",
        "description": "13-step division of the 3/1 ratio (Tritave ~1901.955 cents)",
        "notes": [(1200.0 * math.log2(3) / 13.0) * i for i in range(1, 14)],
        "formal_octave": 13,
    },
    "wendy-carlos-alpha": {
        "name": "Wendy Carlos Alpha Scale",
        "description": "Non-octave scale with step size of 78.0 cents (enhances 5:4 and 3:2)",
        "notes": [78.0 * i for i in range(1, 16)],
        "formal_octave": 15,
    },
    "wendy-carlos-beta": {
        "name": "Wendy Carlos Beta Scale",
        "description": "Non-octave scale with step size of 63.8 cents (splits minor and major thirds)",
        "notes": [63.8 * i for i in range(1, 19)],
        "formal_octave": 18,
    },
    "locrian-neutral2nd": {
        "name": "Locrian Mode with Neutral 2nd (C5-REAL Dark Engine)",
        "description": "Tension-optimized Locrian with -50c neutral second: 50c, 300c, 500c, 600c, 800c, 1000c, 1200c",
        "notes": [50.0, 300.0, 500.0, 600.0, 800.0, 1000.0, 1200.0],
        "formal_octave": 7,
    }
}

def plomp_levelt_dissonance(f1: float, f2: float) -> float:
    """
    Calculates the sensory dissonance between two pure sinusoids f1 and f2
    using the Plomp-Levelt / Sethares psychoacoustic formula.
    """
    f_min, f_max = min(f1, f2), max(f1, f2)
    if f_min == f_max or f_min <= 0:
        return 0.0
        
    s1, s2 = 0.0207, 18.96
    s = 0.24 / (s1 * f_min + s2)
    diff = f_max - f_min
    
    a, b = 3.5, 5.75
    d = math.exp(-a * s * diff) - math.exp(-b * s * diff)
    return max(0.0, d)

def generate_scl(key: str) -> str:
    """Generates the content of a .scl file conforming strictly to the Huygens-Fokker Scala format."""
    data = TEMPERAMENTS.get(key)
    if not data:
        raise ValueError(f"Unknown temperament: {key}. Available: {list(TEMPERAMENTS.keys())}")
    
    lines = [
        f"! {key}.scl",
        f"! Generated by Antigravity C5-REAL Microtonal Architecture",
        f"{data['name']} - {data['description']}",
        f"{len(data['notes'])}"
    ]
    
    for note in data["notes"]:
        if isinstance(note, float):
            lines.append(f" {note:.4f}")
        else:
            lines.append(f" {note}")
            
    return "\n".join(lines) + "\n"

def generate_kbm(scale_size: int, root_midi: int = 60, ref_midi: int = 69, ref_freq: float = 440.0) -> str:
    """Generates a standard keyboard mapping file (.kbm)."""
    lines = [
        "! Antigravity C5-REAL Keyboard Mapping",
        "! Size of map:",
        f"{scale_size}",
        "! First MIDI note number to retune:",
        "0",
        "! Last MIDI note number to retune:",
        "127",
        "! Middle note where first note of scale is placed:",
        f"{root_midi}",
        "! Reference note for which frequency is given:",
        f"{ref_midi}",
        "! Frequency for reference note (Hz):",
        f"{ref_freq:.2f}",
        "! Scale degree for formal octave:",
        f"{scale_size}",
        "! Linear 0..N mapping:"
    ]
    for i in range(scale_size):
        lines.append(str(i))
    return "\n".join(lines) + "\n"

def export_temperament(key: str, target_dir: Path, with_kbm: bool = True) -> tuple:
    target_dir.mkdir(parents=True, exist_ok=True)
    scl_path = target_dir / f"{key}.scl"
    scl_content = generate_scl(key)
    scl_path.write_text(scl_content, encoding="utf-8")
    
    kbm_path = None
    if with_kbm:
        data = TEMPERAMENTS[key]
        kbm_content = generate_kbm(len(data["notes"]))
        kbm_path = target_dir / f"{key}.kbm"
        kbm_path.write_text(kbm_content, encoding="utf-8")
        
    return scl_path, kbm_path

def main():
    parser = argparse.ArgumentParser(description="Antigravity Scala (.scl/.kbm) Tuning Generator")
    parser.add_argument("--temperament", "-t", choices=list(TEMPERAMENTS.keys()) + ["all"], default="all",
                        help="Temperament to generate (default: all)")
    parser.add_argument("--output-dir", "-o", type=str, default=str(DEFAULT_TUNING_DIR),
                        help=f"Target directory (default: {DEFAULT_TUNING_DIR})")
    parser.add_argument("--no-kbm", action="store_true", help="Do not generate .kbm mapping files")
    
    args = parser.parse_args()
    target_dir = Path(args.output_dir)
    
    keys = list(TEMPERAMENTS.keys()) if args.temperament == "all" else [args.temperament]
    print(f"[*] Compiling {len(keys)} Scala profile(s) into: {target_dir}")
    
    for k in keys:
        scl_file, kbm_file = export_temperament(k, target_dir, with_kbm=not args.no_kbm)
        print(f"  [+] Wrote: {scl_file.name}" + (f" and {kbm_file.name}" if kbm_file else ""))
        
    print(f"[✓] Successfully compiled {len(keys)} Scala profiles.")

if __name__ == "__main__":
    main()
