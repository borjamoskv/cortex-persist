#!/usr/bin/env python3
"""
c5_model_router.py - CLI Universal de Enrutamiento C5-REAL v3.0.
Resuelve en < 100 us (100% offline, stdlib pura) el estrato, esfuerzo y opción óptima
para cualquier superficie (Antigravity, Claude Code, Codex, Gemini CLI, Local Loopback).
Soporta --llm-digest opcional cuando se solicite reescritura semántica explícita en red.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sys

HOME_DIR = Path.home()
PROJECTS_DIR = Path(os.environ.get("CORTEX_PROJECTS_ROOT", str(HOME_DIR / "10_PROJECTS"))).expanduser()
BABYLON_ROOT = Path(
    os.environ.get(
        "BABYLON_ROOT",
        str(PROJECTS_DIR / "BABYLON-60" if (PROJECTS_DIR / "BABYLON-60").is_dir() else HOME_DIR / "BABYLON-60"),
    )
).expanduser()

for candidate in (BABYLON_ROOT, BABYLON_ROOT / "01_KISH_ENGINE"):
    if str(candidate) not in sys.path and candidate.is_dir():
        sys.path.insert(0, str(candidate))

from babylon60.cognitive_pilot.universal_autoroute import (  # noqa: E402
    evaluate_universal_route,
    infer_universal_target,
)


def digest_and_route(
    user_query: str,
    *,
    host: str = "antigravity_ui",
    active_model: str = "Orchestrator (Argon)",
    active_mode: str = "Orchestrator",
    context_tokens: int = 0,
    llm_digest: bool = False,
) -> tuple[str, str, str]:
    """Devuelve (target_option_or_capability, target_effort, clean_prompt) en O(1) sin llamada de red."""
    verdict = evaluate_universal_route(
        active_model,
        active_mode,
        user_query,
        source="c5_model_router CLI",
        host=host,
        context_tokens=context_tokens,
    )
    target = infer_universal_target(user_query, context_tokens=context_tokens)
    chosen_model = verdict.concrete_option or verdict.capability_description
    chosen_level = target.effort

    digested_prompt = user_query.strip()
    if llm_digest:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client()
            res = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=f"Reescribe esta petición como un objetivo técnico directo de 1 línea sin ambigüedad:\n{user_query}",
                config=types.GenerateContentConfig(max_output_tokens=256),
            )
            if res.text:
                digested_prompt = res.text.strip()
        except Exception:
            pass

    return chosen_model, chosen_level, digested_prompt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Petición o tarea a evaluar")
    parser.add_argument(
        "--host",
        default="antigravity_ui",
        choices=["antigravity_ui", "claude_code", "codex_cli", "gemini_cli", "local_loopback", "generic"],
        help="Superficie objetivo (por defecto: antigravity_ui)",
    )
    parser.add_argument("--active-model", default="Orchestrator (Argon)", help="Modelo activo observado")
    parser.add_argument("--active-mode", default="Orchestrator", help="Modo/esfuerzo activo observado")
    parser.add_argument("--context-tokens", type=int, default=0, help="Tokens acumulados en la sesión")
    parser.add_argument("--llm-digest", action="store_true", help="Opcional: sintetizar prompt vía Gemini Flash API")
    parser.add_argument("--json", action="store_true", help="Emitir veredicto completo como JSON puro")
    args = parser.parse_args()

    query = " ".join(args.query).strip() if args.query else "Revisa por qué falla el tipado en auth.py"

    if args.json:
        verdict = evaluate_universal_route(
            args.active_model,
            args.active_mode,
            query,
            source="CLI",
            host=args.host,
            context_tokens=args.context_tokens,
        )
        print(json.dumps(asdict(verdict), ensure_ascii=False, indent=2))
        return 0

    model, level, prompt = digest_and_route(
        query,
        host=args.host,
        active_model=args.active_model,
        active_mode=args.active_mode,
        context_tokens=args.context_tokens,
        llm_digest=args.llm_digest,
    )
    print(f"🔄 [ROTAR A: {model} | NIVEL: {level}]")
    print(f"Pre-Flight Prompt:\n{prompt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
