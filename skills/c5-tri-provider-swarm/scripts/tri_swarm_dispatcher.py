#!/usr/bin/env python3
"""Thin pointer from c5-tri-provider-swarm skill to ~/10_PROJECTS/tri-swarm-dispatcher."""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path.home() / "10_PROJECTS" / "tri-swarm-dispatcher"
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"

if __name__ == "__main__":
    if not PROJECT_ROOT.is_dir():
        sys.stderr.write(f"ERROR: canonical package missing at {PROJECT_ROOT}\n")
        raise SystemExit(1)
    target_py = str(VENV_PYTHON) if VENV_PYTHON.is_file() else sys.executable
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{PROJECT_ROOT}:{existing}" if existing else str(PROJECT_ROOT)
    os.execve(target_py, [target_py, "-m", "tri_swarm", *sys.argv[1:]], env)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tri_swarm import (  # noqa: E402,F401
    AgentPager,
    BackendError,
    Completion,
    GeminiBackend,
    OllamaBackend,
    OpenAICompatBackend,
    Settings,
    SwarmTask,
    TaskResult,
    TriProviderSwarmDispatcher,
)
