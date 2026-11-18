"""Isolated Python entry point; add only this host-owned plugin directory."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).absolute().parent))
from server import main  # noqa: E402

main()
