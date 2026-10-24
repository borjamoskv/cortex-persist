#!/usr/bin/env python3
"""
README Linter & Cognitive Ingress Auditor v1.0
Author: Borja Fernández Angulo (Investigador en Sistemas Complejos)

Evaluates a README.md file against C5-REAL standards:
- The 15-Second Cognitive Ingress Rule
- Elevator Pitch & Kolmogorov Compression
- Badge Authenticity vs Vanity
- Architecture & Visual Proof Presence (SVG, Mermaid, VHS, Asciinema)
- Zero-Friction O(1) Quickstart Command
- Document Hierarchy & Links Integrity
"""

import sys
import os
import re
from typing import Dict, List, Any

class ReadmeLinter:
    def __init__(self, content: str):
        self.content = content
        self.lines = content.splitlines()
        self.score = 100
        self.deductions: List[Dict[str, Any]] = []
        self.passes: List[str] = []

    def deduct(self, points: int, reason: str, category: str):
        self.score = max(0, self.score - points)
        self.deductions.append({
            "points": points,
            "category": category,
            "reason": reason
        })

    def record_pass(self, check: str):
        self.passes.append(check)

    def audit(self) -> Dict[str, Any]:
        self._audit_hero_and_title()
        self._audit_elevator_pitch()
        self._audit_badges()
        self._audit_visual_demonstration()
        self._audit_quickstart()
        self._audit_architecture_and_invariants()
        self._audit_navigation_and_links()

        grade = "A" if self.score >= 90 else ("B" if self.score >= 80 else ("C" if self.score >= 70 else ("D" if self.score >= 60 else "F")))

        return {
            "score": self.score,
            "grade": grade,
            "passes": self.passes,
            "deductions": self.deductions
        }

    def _audit_hero_and_title(self):
        # Must have an H1 in the first 5 lines
        has_h1 = any(line.strip().startswith("# ") for line in self.lines[:5])
        if has_h1:
            self.record_pass("H1 Project Title present in hero zone (first 5 lines)")
        else:
            self.deduct(15, "Missing H1 project title in the top 5 lines", "Hero Section")

    def _audit_elevator_pitch(self):
        # Must have a blockquote or crisp description right under the title
        has_pitch = False
        for line in self.lines[:12]:
            clean = line.strip()
            if clean.startswith("> ") or (len(clean) > 20 and not clean.startswith("#") and not clean.startswith("[!")):
                has_pitch = True
                break
        if has_pitch:
            self.record_pass("Crisp elevator pitch found in the top 12 lines")
        else:
            self.deduct(15, "Missing clear one-sentence elevator pitch in hero section", "Cognitive Ingress")

    def _audit_badges(self):
        # Check badges for presence of CI or License
        ci_badge = any("workflow" in line.lower() or "actions" in line.lower() or "ci" in line.lower() for line in self.lines[:20])
        license_badge = any("license" in line.lower() for line in self.lines[:20])

        if ci_badge and license_badge:
            self.record_pass("High-exergy CI and License badges present")
        elif ci_badge or license_badge:
            self.record_pass("Partial badge coverage (CI or License present)")
            self.deduct(5, "Missing either CI status or License badge", "Badges")
        else:
            self.deduct(10, "No CI build status or License badges found in header", "Badges")

    def _audit_visual_demonstration(self):
        # Look for images, SVG diagrams, VHS demos, or Mermaid diagrams
        has_diagram = "```mermaid" in self.content or ".svg" in self.content or ".gif" in self.content or "![demo" in self.content.lower() or "![hero" in self.content.lower() or "asciinema" in self.content.lower()
        if has_diagram:
            self.record_pass("Visual proof / architecture diagram / demo present")
        else:
            self.deduct(20, "Missing visual proof, architecture diagram, or terminal demo", "Visual Ingress")

    def _audit_quickstart(self):
        # Look for quickstart / installation code block
        has_quickstart = False
        quickstart_headers = ["quickstart", "inicio rápido", "installation", "instalación", "getting started", "usage", "uso"]
        for i, line in enumerate(self.lines):
            clean = line.strip().lower()
            if any(qh in clean for qh in quickstart_headers):
                # Verify that a code block follows within the next 10 lines
                subsequent = "\n".join(self.lines[i:i+15])
                if "```" in subsequent:
                    has_quickstart = True
                    break
        if has_quickstart:
            self.record_pass("Zero-friction Quickstart code block present")
        else:
            self.deduct(15, "Missing clear Quickstart or Installation code section", "DevEx")

    def _audit_architecture_and_invariants(self):
        # Check if architecture, design invariants, or features are documented
        content_lower = self.content.lower()
        has_arch = "architecture" in content_lower or "arquitectura" in content_lower or "invariants" in content_lower or "invariantes" in content_lower or "features" in content_lower or "características" in content_lower
        if has_arch:
            self.record_pass("Architecture / Invariants section present")
        else:
            self.deduct(10, "Missing formal Architecture or Invariants section", "Ontology")

    def _audit_navigation_and_links(self):
        # Check for license or security links
        content_lower = self.content.lower()
        has_license_ref = "license" in content_lower or "licencia" in content_lower
        has_contrib_or_security = "contributing" in content_lower or "security" in content_lower or "seguridad" in content_lower
        if has_license_ref and has_contrib_or_security:
            self.record_pass("Governance links (License + Contributing/Security) present")
        elif has_license_ref:
            self.record_pass("License referenced")
            self.deduct(5, "Missing CONTRIBUTING.md or SECURITY.md reference", "Governance")
        else:
            self.deduct(10, "Missing License and Governance references", "Governance")


def main():
    if len(sys.argv) < 2:
        print("Usage: readme_linter.py <path_to_README.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    linter = ReadmeLinter(content)
    result = linter.audit()

    print("=" * 60)
    print(f"README AUDIT REPORT: {os.path.basename(filepath)}")
    print(f"Score: {result['score']}/100 | Grade: {result['grade']}")
    print("=" * 60)

    print("\n[PASSED CHECKS]:")
    for p in result["passes"]:
        print(f"  ✓ {p}")

    if result["deductions"]:
        print("\n[DEDUCTIONS & ACTIONABLE FIXES]:")
        for d in result["deductions"]:
            print(f"  ✗ [-{d['points']} pts] [{d['category']}] {d['reason']}")
    else:
        print("\n[PERFECT SCORE]: Exceeds C5-REAL standards for cognitive ingress!")
    print("=" * 60)

    # Return exit code 0 if score >= 80, 1 otherwise
    sys.exit(0 if result["score"] >= 80 else 1)


if __name__ == "__main__":
    main()
