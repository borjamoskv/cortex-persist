#!/usr/bin/env python3
"""
Unit Test Suite for FL Studio 2025 MCP & Audio Engineering Protocol
C5-REAL High-Exergy Verification Harness
"""

import os
import sys
import ast
import math
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
EXAMPLES_DIR = BASE_DIR / "examples"
HARDWARE_DIR = BASE_DIR / "hardware"
TUNING_DIR = Path.home() / "Documents/Image-Line/FL Studio/Settings/Tuning"
MUSIC_DIR = Path.home() / "Music"

class TestFLStudioProductionSuite(unittest.TestCase):

    def test_01_all_scripts_ast_validity(self):
        """Verifies that every single script compiles without syntax errors."""
        all_py = list(BASE_DIR.glob("**/*.py"))
        self.assertGreater(len(all_py), 15, "Expected at least 15 Python scripts in suite")
        for p in all_py:
            with self.subTest(script=p.name):
                content = p.read_text(encoding="utf-8")
                try:
                    tree = ast.parse(content, filename=str(p))
                    self.assertIsNotNone(tree)
                except SyntaxError as se:
                    self.fail(f"SyntaxError in {p.name} at line {se.lineno}: {se.msg}")

    def test_02_pianoroll_entrypoints(self):
        """Verifies that all Piano Roll scripts in examples/ have valid FL Studio entrypoints."""
        for ex in EXAMPLES_DIR.glob("*.py"):
            with self.subTest(example=ex.name):
                tree = ast.parse(ex.read_text(encoding="utf-8"))
                func_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
                has_create_score = "createScore" in func_names
                has_dialog_apply = ("createDialog" in func_names and "apply" in func_names)
                self.assertTrue(has_create_score or has_dialog_apply,
                                f"{ex.name} missing createScore or createDialog+apply")

    def test_03_hardware_controller_integrity(self):
        """Verifies the Hardware Controller script structure."""
        hw_script = HARDWARE_DIR / "device_Antigravity_MCP.py"
        self.assertTrue(hw_script.exists(), "device_Antigravity_MCP.py must exist")
        content = hw_script.read_text(encoding="utf-8")
        self.assertIn("# name=Antigravity MCP Controller", content)
        self.assertIn("def OnInit():", content)
        self.assertIn("def OnMidiMsg(event):", content)

    def test_04_scala_tunings_octave_closure(self):
        """Verifies that Scala .scl files have formal octave closure (end in 1200 or 2/1)."""
        sys.path.insert(0, str(SCRIPTS_DIR))
        import scala_generator
        for name, data in scala_generator.TEMPERAMENTS.items():
            with self.subTest(temperament=name):
                scl_str = scala_generator.generate_scl(name)
                lines = [l.strip() for l in scl_str.strip().split("\n") if not l.startswith("!")]
                note_count = int(lines[1])
                notes = lines[2:]
                self.assertEqual(len(notes), note_count, f"Declared note count mismatch in {name}")
                last_note = notes[-1]
                # Last note should be an octave (1200.0000 or 2/1) or tritave (for Bohlen-Pierce) or specific formal octave
                self.assertTrue(
                    "1200" in last_note or "2/1" in last_note or "1901" in last_note or name.startswith("wendy"),
                    f"Formal octave period missing in {name}: last note is {last_note}"
                )

    def test_05_plomp_levelt_psychoacoustics(self):
        """Verifies the Plomp-Levelt sensory dissonance function."""
        sys.path.insert(0, str(SCRIPTS_DIR))
        import scala_generator
        # Unison dissonance should be 0
        d_unison = scala_generator.plomp_levelt_dissonance(440.0, 440.0)
        self.assertEqual(d_unison, 0.0)
        # Semitone dissonance (440 vs 466.16) should be higher than a pure fifth (440 vs 660)
        d_semitone = scala_generator.plomp_levelt_dissonance(440.0, 466.16)
        d_fifth = scala_generator.plomp_levelt_dissonance(440.0, 660.0)
        self.assertGreater(d_semitone, d_fifth, "Sensory dissonance of semitone must exceed pure fifth")

    def test_06_music_assets_directory(self):
        """Verifies that ~/Music exists for the Centralization Invariant."""
        self.assertTrue(MUSIC_DIR.exists(), f"Centralized directory {MUSIC_DIR} must exist")

if __name__ == "__main__":
    unittest.main()
