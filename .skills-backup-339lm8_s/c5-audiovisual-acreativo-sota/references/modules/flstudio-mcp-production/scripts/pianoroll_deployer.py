#!/usr/bin/env python3
"""
Piano Roll Script Validator & Deployer for FL Studio 2025
C5-REAL High-Exergy Audio Engineering Engine

Validates Python AST, verifies flpianoroll / utils entrypoints,
and hot-deploys scripts to the native Image-Line Piano roll scripts directory.
"""

import os
import sys
import ast
import shutil
import argparse
from pathlib import Path

DEFAULT_PIANOROLL_DIR = Path.home() / "Documents/Image-Line/FL Studio/Settings/Piano roll scripts"
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

def validate_script(file_path: Path) -> tuple[bool, str]:
    """Validates Python syntax and checks for FL Studio Piano Roll entrypoints."""
    if not file_path.exists():
        return False, f"File not found: {file_path}"
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read file: {e}"
        
    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as se:
        return False, f"SyntaxError at line {se.lineno}: {se.msg}"
        
    # Check for functions
    func_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    
    has_create_score = "createScore" in func_names
    has_dialog_apply = ("createDialog" in func_names and "apply" in func_names)
    
    if not (has_create_score or has_dialog_apply):
        return False, f"Missing entrypoints: requires 'createScore()' or 'createDialog()' + 'apply(form)'. Found: {func_names}"
        
    mode = "Interactive Dialog (apply)" if has_dialog_apply else "Direct Batch (createScore)"
    return True, f"Valid FL Studio Piano Roll script [{mode}]"

def list_installed_scripts(target_dir: Path):
    """Lists all installed scripts in the user's FL Studio Piano Roll directory."""
    if not target_dir.exists():
        print(f"[!] Directory does not exist: {target_dir}")
        return
        
    scripts = sorted(list(target_dir.glob("*.py")) + list(target_dir.glob("*.pyscript")))
    print(f"\n[*] Installed Piano Roll Scripts in {target_dir} ({len(scripts)} total):")
    for s in scripts:
        ok, msg = validate_script(s)
        status = "✓" if ok else "✗"
        print(f"  [{status}] {s.name:<45} ({msg})")

def deploy_script(src: Path, target_dir: Path, force: bool = False) -> bool:
    """Validates and copies a script into the FL Studio directory."""
    ok, msg = validate_script(src)
    if not ok and not force:
        print(f"[!] Validation failed for {src.name}: {msg}")
        return False
        
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / src.name
    shutil.copy2(src, dest)
    print(f"[✓] Deployed: {src.name} -> {dest} ({msg})")
    return True

def main():
    parser = argparse.ArgumentParser(description="FL Studio 2025 Piano Roll Script Deployer & Linter")
    parser.add_argument("--list", "-l", action="store_true", help="List all installed piano roll scripts")
    parser.add_argument("--validate", "-v", type=str, help="Validate a specific script file")
    parser.add_argument("--validate-all", action="store_true", help="Validate all scripts in examples/ and installed directory")
    parser.add_argument("--deploy", "-d", type=str, help="Deploy a specific script to FL Studio")
    parser.add_argument("--deploy-examples", action="store_true", help="Deploy all curated examples to FL Studio")
    parser.add_argument("--target-dir", "-t", type=str, default=str(DEFAULT_PIANOROLL_DIR),
                        help=f"Target directory (default: {DEFAULT_PIANOROLL_DIR})")
    parser.add_argument("--force", "-f", action="store_true", help="Force deployment even if validation warns")

    args = parser.parse_args()
    target_dir = Path(args.target_dir)

    if args.list:
        list_installed_scripts(target_dir)
        return

    if args.validate:
        p = Path(args.validate)
        ok, msg = validate_script(p)
        print(f"[{'✓' if ok else '✗'}] {p.name}: {msg}")
        sys.exit(0 if ok else 1)

    if args.validate_all:
        print("[*] Validating curated examples:")
        for ex in sorted(list(EXAMPLES_DIR.glob("*.py")) + list(EXAMPLES_DIR.glob("*.pyscript"))):
            ok, msg = validate_script(ex)
            print(f"  [{'✓' if ok else '✗'}] {ex.name}: {msg}")
        return

    if args.deploy:
        p = Path(args.deploy)
        success = deploy_script(p, target_dir, force=args.force)
        sys.exit(0 if success else 1)

    if args.deploy_examples:
        print(f"[*] Deploying curated examples to {target_dir}:")
        count = 0
        for ex in sorted(list(EXAMPLES_DIR.glob("*.py")) + list(EXAMPLES_DIR.glob("*.pyscript"))):
            if deploy_script(ex, target_dir, force=args.force):
                count += 1
        print(f"[✓] Successfully deployed {count} example script(s).")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
