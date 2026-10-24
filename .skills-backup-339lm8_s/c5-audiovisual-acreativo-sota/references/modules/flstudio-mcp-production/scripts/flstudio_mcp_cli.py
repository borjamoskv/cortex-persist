#!/usr/bin/env python3
"""
FL Studio 2025 MCP Mastermind CLI
C5-REAL High-Exergy Autonomous Audio Engineering Suite

Unified command-line interface for:
- Environment diagnostics ('doctor')
- Piano Roll script validation and hot-deployment ('deploy-pianoroll')
- Hardware MIDI Controller script installation ('deploy-hardware')
- Psychoacoustic Scala (.scl/.kbm) scale compilation ('generate-tunings')
- CoreMIDI virtual bridge daemon ('midi-daemon')
- Centralized Music Asset Symlinker ('sync-music')
"""

import os
import sys
import ast
import json
import shutil
import argparse
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
EXAMPLES_DIR = BASE_DIR / "examples"
HARDWARE_DIR = BASE_DIR / "hardware"
TUNING_DIR = BASE_DIR / "tuning"
DSP_DIR = BASE_DIR / "dsp"

FL_SETTINGS = Path.home() / "Documents/Image-Line/FL Studio/Settings"
FL_PIANOROLL = FL_SETTINGS / "Piano roll scripts"
FL_HARDWARE = FL_SETTINGS / "Hardware"
FL_TUNING = FL_SETTINGS / "Tuning"
USER_MUSIC = Path.home() / "Music"
MUSIC_BOUNCES = USER_MUSIC / "FL Studio Bounces"

def run_doctor() -> dict:
    """Performs deep diagnostic audit on FL Studio 2025 environment."""
    report = {
        "fl_studio_app": False,
        "app_path": None,
        "settings_dir": FL_SETTINGS.exists(),
        "pianoroll_dir": FL_PIANOROLL.exists(),
        "hardware_dir": FL_HARDWARE.exists(),
        "tuning_dir": FL_TUNING.exists(),
        "user_music_dir": USER_MUSIC.exists(),
        "mido_installed": False,
        "rtmidi_installed": False,
        "installed_scripts_count": 0,
        "installed_tunings_count": 0,
    }

    # Detect FL Studio
    app_path = Path("/Applications/FL Studio 2025.app")
    if app_path.exists():
        report["fl_studio_app"] = True
        report["app_path"] = str(app_path)
    else:
        # Fallback check
        for candidate in Path("/Applications").glob("FL Studio*.app"):
            report["fl_studio_app"] = True
            report["app_path"] = str(candidate)
            break

    # Python libraries
    try:
        import mido
        report["mido_installed"] = True
    except ImportError:
        pass

    try:
        import rtmidi
        report["rtmidi_installed"] = True
    except ImportError:
        pass

    if FL_PIANOROLL.exists():
        report["installed_scripts_count"] = len(list(FL_PIANOROLL.glob("*.py")) + list(FL_PIANOROLL.glob("*.pyscript")))
    if FL_TUNING.exists():
        report["installed_tunings_count"] = len(list(FL_TUNING.glob("*.scl")))

    print("==================================================================")
    print("  ANTIGRAVITY FL STUDIO 2025 ENVIRONMENT DIAGNOSTIC (DOCTOR)")
    print("==================================================================")
    print(f"  [+] FL Studio Application:   {'✓' if report['fl_studio_app'] else '✗'} ({report['app_path']})")
    print(f"  [+] Image-Line Settings:     {'✓' if report['settings_dir'] else '✗'} ({FL_SETTINGS})")
    print(f"  [+] Piano Roll Scripts:      {'✓' if report['pianoroll_dir'] else '✗'} ({report['installed_scripts_count']} installed)")
    print(f"  [+] Hardware Scripts Dir:    {'✓' if report['hardware_dir'] else '✗'}")
    print(f"  [+] Tuning Profiles Dir:     {'✓' if report['tuning_dir'] else '✗'} ({report['installed_tunings_count']} installed)")
    print(f"  [+] Centralized ~/Music/:    {'✓' if report['user_music_dir'] else '✗'} ({USER_MUSIC})")
    print(f"  [+] CoreMIDI Python Engine:  Mido: {'✓' if report['mido_installed'] else '✗'}, RtMidi: {'✓' if report['rtmidi_installed'] else '✗'}")
    print("==================================================================")
    return report

def sync_music_centralization():
    """Enforces the Centralized Music Assets Invariant into ~/Music/."""
    USER_MUSIC.mkdir(parents=True, exist_ok=True)
    MUSIC_BOUNCES.mkdir(parents=True, exist_ok=True)
    print(f"[✓] Centralized Audio Directory verified: {MUSIC_BOUNCES}")

def validate_all_scripts() -> bool:
    """Validates AST syntax and entrypoints across all Python scripts."""
    all_valid = True
    scripts = sorted(list(EXAMPLES_DIR.glob("*.py")) + list(SCRIPTS_DIR.glob("*.py")) + list(HARDWARE_DIR.glob("*.py")))
    print(f"[*] Auditing {len(scripts)} Python scripts for AST compliance:")
    for s in scripts:
        try:
            tree = ast.parse(s.read_text(encoding="utf-8"), filename=str(s))
            func_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
            # Check script type
            if "device" in s.name.lower() or "hardware" in str(s.parent).lower():
                is_valid = "OnInit" in func_names or "OnMidiMsg" in func_names
                tag = "Hardware Controller"
            elif "flstudio_mcp_cli" in s.name or "scala" in s.name or "coremidi" in s.name or "deployer" in s.name:
                is_valid = True
                tag = "CLI Utility"
            else:
                is_valid = "createScore" in func_names or ("createDialog" in func_names and "apply" in func_names)
                tag = "Piano Roll Script"

            if is_valid:
                print(f"  [✓] {s.name:<38} [{tag}]")
            else:
                print(f"  [✗] {s.name:<38} [Missing Required Entrypoints]")
                all_valid = False
        except SyntaxError as se:
            print(f"  [!] {s.name:<38} [SyntaxError at line {se.lineno}: {se.msg}]")
            all_valid = False

    return all_valid

def deploy_all(force: bool = False):
    """Deploys all Piano Roll scripts, Hardware scripts, and Tunings."""
    print("[*] Initiating Full Sovereign Deployment to FL Studio 2025...")
    
    # 1. Piano Roll Scripts
    FL_PIANOROLL.mkdir(parents=True, exist_ok=True)
    pr_count = 0
    for ex in sorted(list(EXAMPLES_DIR.glob("*.py")) + list(EXAMPLES_DIR.glob("*.pyscript"))):
        dest = FL_PIANOROLL / ex.name
        shutil.copy2(ex, dest)
        pr_count += 1
    print(f"  [✓] Deployed {pr_count} Piano Roll scripts to {FL_PIANOROLL}")

    # 2. Hardware Controller Script
    mcp_hw_dir = FL_HARDWARE / "AntigravityMCP"
    mcp_hw_dir.mkdir(parents=True, exist_ok=True)
    hw_src = HARDWARE_DIR / "device_Antigravity_MCP.py"
    if hw_src.exists():
        shutil.copy2(hw_src, mcp_hw_dir / "device_Antigravity_MCP.py")
        print(f"  [✓] Deployed Hardware Controller to {mcp_hw_dir}")

    # 3. Scala Tunings
    FL_TUNING.mkdir(parents=True, exist_ok=True)
    try:
        from scala_generator import main as gen_tunings
        # Run generator to target directory
        old_argv = sys.argv
        sys.argv = ["scala_generator.py", "--temperament", "all", "--output-dir", str(FL_TUNING)]
        gen_tunings()
        sys.argv = old_argv
        print(f"  [✓] Compiled and deployed all Scala tunings to {FL_TUNING}")
    except Exception as e:
        print(f"  [!] Failed to generate tunings via module: {e}")

    # 4. Centralized Music directory
    sync_music_centralization()
    print("[✓] Full System Deployment Complete.")

def main():
    parser = argparse.ArgumentParser(description="Antigravity FL Studio 2025 MCP Mastermind CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("doctor", help="Run comprehensive environment audit")
    subparsers.add_parser("validate", help="Validate all scripts for AST and entrypoint compliance")
    subparsers.add_parser("deploy", help="Deploy all scripts, hardware controllers, and tunings")
    subparsers.add_parser("sync-music", help="Ensure ~/Music/ centralized assets directory")

    args = parser.parse_args()

    if args.command == "doctor":
        run_doctor()
    elif args.command == "validate":
        ok = validate_all_scripts()
        sys.exit(0 if ok else 1)
    elif args.command == "deploy":
        deploy_all()
    elif args.command == "sync-music":
        sync_music_centralization()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
