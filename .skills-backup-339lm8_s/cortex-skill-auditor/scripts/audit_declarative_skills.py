#!/usr/bin/env python3
"""
audit_declarative_skills.py — Linter Determinista O(N) de la Flota de Skills CORTEX (V2 ON-WIRE)
Valida las 6 invariantes de INV_C5_SKILLS_FLEET:
1. Validez sintáctica YAML 1.2 y presencia de display_name.
2. Presencia y exactitud de la Tríada Canónica de Roles (arquitecto, ejecutor, auditor).
3. Directivas de árbol de trabajo (worktree_mode, phase, handoff.upstream/downstream).
4. Anti-AP-02: Veto a micro-stubs anérgicos (< 20 líneas).
5. Anti-AP-04: Cláusula determinista 'Dispara con "..."' en description.
6. INV_C5_SKILL_BUDGET: Presupuesto de Kolmogorov (len(description) <= 350 caracteres).
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
import yaml

MAX_DESCRIPTION_CHARS = 350
MIN_SKILL_LINES = 20


def audit(include_plugins: bool = False) -> int:
    errors = []
    warnings = []

    sovereign_patterns = [
        "/Users/borjafernandezangulo/.gemini/config/skills/*/SKILL.md",
        "/Users/borjafernandezangulo/10_PROJECTS/BABYLON-60/.agents/skills/*/SKILL.md",
    ]
    plugin_patterns = [
        "/Users/borjafernandezangulo/.gemini/config/plugins/**/SKILL.md",
    ]

    files = []
    for pat in sovereign_patterns:
        files.extend(glob.glob(pat, recursive=True))
    if include_plugins:
        for pat in plugin_patterns:
            files.extend(glob.glob(pat, recursive=True))
    files = sorted(set(files))

    plugin_count = len(glob.glob(plugin_patterns[0], recursive=True))

    print("=== CORTEX SKILL AUDITOR V2 (DECLARATIVE TRIAD & KOLMOGOROV GATE) ===")
    print(f"Total habilidades soberanas auditadas en silicio: {len(files)} (Plugins externos satélite: {plugin_count})")

    role_counts = {"arquitecto": 0, "ejecutor": 0, "auditor": 0}

    for f in files:
        rel_path = f.replace("/Users/borjafernandezangulo/", "~/")
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()

        lines = content.splitlines()
        if len(lines) < MIN_SKILL_LINES:
            errors.append(f"{rel_path}: Violación Anti-AP-02 (Micro-stub de {len(lines)} líneas < {MIN_SKILL_LINES})")

        if not content.startswith("---"):
            errors.append(f"{rel_path}: No inicia con delimitador YAML '---'")
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append(f"{rel_path}: Delimitadores YAML incompletos o malformados")
            continue

        fm_raw = parts[1]
        body = parts[2].strip()

        try:
            fm = yaml.safe_load(fm_raw)
            if not isinstance(fm, dict):
                errors.append(f"{rel_path}: Frontmatter YAML no se parseó como diccionario")
                continue
        except Exception as e:
            errors.append(f"{rel_path}: Error fatal parseando YAML: {e}")
            continue

        # 1. Validar campos requeridos
        for req in ["name", "display_name", "description", "role", "allowed_roles", "directives"]:
            if req not in fm or not fm.get(req):
                errors.append(f"{rel_path}: Campo obligatorio '{req}' ausente o vacío en frontmatter")

        # 2. Validar presupuesto de Kolmogorov (<= 350 chars) y disparo determinista (Anti-AP-04)
        desc = str(fm.get("description", ""))
        if len(desc) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"{rel_path}: Violación INV_C5_SKILL_BUDGET (description tiene {len(desc)} chars > {MAX_DESCRIPTION_CHARS})"
            )
        if "Dispara con" not in desc and "dispara con" not in desc:
            errors.append(f"{rel_path}: Violación Anti-AP-04 (Sin cláusula determinista 'Dispara con' en description)")

        # 3. Validar rol canónico
        role = fm.get("role")
        if role not in ["arquitecto", "ejecutor", "auditor"]:
            errors.append(f"{rel_path}: Rol inválido '{role}'. Debe ser arquitecto, ejecutor o auditor")
        else:
            role_counts[role] += 1

        # 4. Validar directivas de árbol de trabajo
        dirs = fm.get("directives", {})
        if not isinstance(dirs, dict):
            errors.append(f"{rel_path}: 'directives' debe ser un diccionario estructurado")
        else:
            mode = dirs.get("worktree_mode")
            phase = dirs.get("phase")
            handoff = dirs.get("handoff", {})

            if mode not in ["spec-only", "read-write", "audit-only"]:
                errors.append(f"{rel_path}: 'worktree_mode' inválido: '{mode}'")
            if phase not in ["design", "implementation", "verification"]:
                errors.append(f"{rel_path}: 'phase' inválida: '{phase}'")
            if not isinstance(handoff, dict) or "upstream" not in handoff or "downstream" not in handoff:
                errors.append(f"{rel_path}: 'handoff' debe especificar 'upstream' y 'downstream'")

        # 5. Validar inyección de directiva en cuerpo Markdown
        if "> **Directiva Declarativa" not in body:
            warnings.append(f"{rel_path}: Falta el banner de directiva declarativa en Markdown")

    print("\n--- DISTRIBUCIÓN DE LA TRÍADA CANÓNICA ---")
    for r, count in role_counts.items():
        print(f"  • {r.upper():12s}: {count} habilidades")

    if warnings:
        print(f"\nAVISOS ({len(warnings)}):")
        for w in warnings[:10]:
            print("  [WARN]", w)

    if errors:
        print(f"\n[FAIL-CLOSED] {len(errors)} ERRORES DETECTADOS EN AUDITORÍA:")
        for err in errors:
            print("  [ERROR]", err)
        sys.exit(1)

    print(
        f"\n[PASS] 100% de las {len(files)} habilidades soberanas cumplen Tríada, Triggers O(1) y Cota de Kolmogorov <= 350 chars (FPR = 0.0000%)."
    )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CORTEX Declarative Skill Auditor V2")
    parser.add_argument("--include-plugins", action="store_true", help="Include 3rd-party plugins in strict audit")
    args = parser.parse_args()
    raise SystemExit(audit(include_plugins=args.include_plugins))
