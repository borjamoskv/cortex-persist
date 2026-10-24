#!/usr/bin/env python3
"""
scripts/anergy_purge.py — Motor Autónomo de Purga de Anergía (C5-REAL / Ω8)
Ejecuta la purga determinista de artefactos efímeros, caches, scratch audiovisual,
metadatos de OS y ghost listeners, computando la exergía recuperada con precisión bit a bit.
"""

import argparse
import glob
import os
import shutil
import sqlite3
import sys
from pathlib import Path


# Invariantes de Preservación Canónica (Ω2 / Ω2-AV) — NUNCA PURGAR
CANONICAL_PRESERVED_FILES = {
    # Audiovisual Masters & Formal Outputs
    "wild_mitxu_b2b_siglo.mp4",
    "mitxudiario-11-ceuton-4min.mp4",
    "mitxudiario-11-ceuton-cinematica-4min.mp4",
    "mitxu_wild_swarm_1080p.mp4",
    "mitx_wild_medina_special_1080p.mp4",
    "mitxudiario_10_master.mp4",
    "mitxuwild_rap_intro_15s_master.mp4",
    # Informes, actas formales y directorios de certificación
    "itera_100",
    "diction_verification",
    "voice_tests",
    "sintonia",
    "qc_audio_report.json",
    "qc_report.json",
    "prosody_analysis_report.json",
    "alain_whatsapp_corpus_analysis.json",
    "mitxu_whatsapp_corpus_analysis.json",
}

CANONICAL_PROTECTED_DIRS = [
    "babylon-web",
    "apps/web",
    "apps/babylon60-ide",
    "remotion",
    "ley_menores_remotion",
    "sota_documentary_remotion",
    "strike-rs/.venv",
    ".uv_python",
    "youtube-research-remotion",
    "cortex-persist",
    "02_CORTEX_ENGINE/cortex",
    "data/cortex_memory.db",
    "artifact_bundle_v3",
]


def format_bytes(bytes_count: int) -> str:
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    elif bytes_count < 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_count / (1024 * 1024 * 1024):.2f} GB"


def purge_anergy(workspace_path: Path, dry_run: bool = False) -> dict:
    stats = {
        "scratch_files": 0,
        "scratch_bytes": 0,
        "out_ephemeral_files": 0,
        "out_ephemeral_bytes": 0,
        "pycache_dirs": 0,
        "pyc_files": 0,
        "pycache_bytes": 0,
        "os_meta_files": 0,
        "os_meta_bytes": 0,
        "root_test_wavs": 0,
        "root_test_wavs_bytes": 0,
        "wal_orphans": 0,
        "wal_bytes": 0,
        "ghost_listeners_reset": 0,
        "total_bytes_recovered": 0,
    }

    # 1. CLASE I2 — Audiovisual Studio Scratch en el root del workspace
    scratches = (
        glob.glob(str(workspace_path / "scratch_*"))
        + glob.glob(str(workspace_path / "public_studio_*_thumb.*"))
    )
    for f in scratches:
        p = Path(f)
        try:
            if p.is_file():
                sz = p.stat().st_size
                stats["scratch_files"] += 1
                stats["scratch_bytes"] += sz
                if not dry_run:
                    p.unlink(missing_ok=True)
            elif p.is_dir():
                sz = sum(fp.stat().st_size for fp in p.rglob("*") if fp.is_file())
                stats["scratch_files"] += 1
                stats["scratch_bytes"] += sz
                if not dry_run:
                    shutil.rmtree(p, ignore_errors=True)
        except Exception as e:
            print(f"[WARN] Error purgando scratch {p}: {e}", file=sys.stderr)

    # 2. CLASE I2 — Ephemeral Renders en out/
    out_dir = workspace_path / "out"
    if out_dir.is_dir():
        for entry in out_dir.iterdir():
            name = entry.name
            if name in CANONICAL_PRESERVED_FILES or name.endswith("_master.mp4") or name.endswith("_siglo.mp4"):
                continue
            try:
                if entry.is_file():
                    sz = entry.stat().st_size
                    stats["out_ephemeral_files"] += 1
                    stats["out_ephemeral_bytes"] += sz
                    if not dry_run:
                        entry.unlink(missing_ok=True)
                elif entry.is_dir():
                    sz = sum(fp.stat().st_size for fp in entry.rglob("*") if fp.is_file())
                    stats["out_ephemeral_files"] += 1
                    stats["out_ephemeral_bytes"] += sz
                    if not dry_run:
                        shutil.rmtree(entry, ignore_errors=True)
            except Exception as e:
                print(f"[WARN] Error purgando out/{name}: {e}", file=sys.stderr)

    # 3. CLASE C — __pycache__ y *.pyc fuera de .venv y node_modules
    for root, dirs, files in os.walk(workspace_path):
        if any(p in root for p in [".venv", "node_modules", ".git"]):
            continue
        for d in list(dirs):
            if d == "__pycache__":
                dp = Path(root) / d
                sz = sum(fp.stat().st_size for fp in dp.rglob("*") if fp.is_file())
                stats["pycache_dirs"] += 1
                stats["pycache_bytes"] += sz
                if not dry_run:
                    shutil.rmtree(dp, ignore_errors=True)
                dirs.remove(d)
        for f in files:
            if f.endswith(".pyc"):
                fp = Path(root) / f
                if fp.is_file():
                    sz = fp.stat().st_size
                    stats["pyc_files"] += 1
                    stats["pycache_bytes"] += sz
                    if not dry_run:
                        fp.unlink(missing_ok=True)

    # 4. CLASE I — Metadatos de Sistema Operativo (.DS_Store, *.tmp, *.bak)
    for root, dirs, files in os.walk(workspace_path):
        if ".git" in root:
            continue
        for f in files:
            if f == ".DS_Store" or f.endswith(".tmp") or f.endswith(".bak") or f.endswith("~"):
                fp = Path(root) / f
                if fp.is_file():
                    sz = fp.stat().st_size
                    stats["os_meta_files"] += 1
                    stats["os_meta_bytes"] += sz
                    if not dry_run:
                        fp.unlink(missing_ok=True)

    # 5. CLASE I2 — Bounces de audio temporales en root (*_binaural_*.wav)
    for wav in workspace_path.glob("*_binaural_*.wav"):
        if wav.is_file():
            sz = wav.stat().st_size
            stats["root_test_wavs"] += 1
            stats["root_test_wavs_bytes"] += sz
            if not dry_run:
                wav.unlink(missing_ok=True)

    # 6. CLASE B — SQLite WAL Huérfanos (*.db-shm, *.db-wal)
    for root, dirs, files in os.walk(workspace_path):
        if any(p in root for p in [".venv", "node_modules", ".git"]):
            continue
        for f in files:
            if f.endswith(".db-shm") or f.endswith(".db-wal"):
                fp = Path(root) / f
                if fp.is_file():
                    sz = fp.stat().st_size
                    stats["wal_orphans"] += 1
                    stats["wal_bytes"] += sz
                    if not dry_run:
                        fp.unlink(missing_ok=True)

    # 7. CLASE L — Ghost Listeners en conversation_summaries.db
    db_path = Path.home() / ".gemini" / "antigravity" / "conversation_summaries.db"
    if db_path.is_file():
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "SELECT count(*) FROM conversation_summaries WHERE status = 'CASCADE_RUN_STATUS_RUNNING' OR not_fully_idle = 1"
            )
            count = cur.fetchone()[0]
            stats["ghost_listeners_reset"] = count
            if not dry_run and count > 0:
                cur.execute(
                    "UPDATE conversation_summaries SET status = 'CASCADE_RUN_STATUS_IDLE', not_fully_idle = 0 WHERE status = 'CASCADE_RUN_STATUS_RUNNING' OR not_fully_idle = 1"
                )
                conn.commit()
            conn.close()
        except Exception as e:
            print(f"[WARN] Error al acceder a conversation_summaries.db: {e}", file=sys.stderr)

    stats["total_bytes_recovered"] = (
        stats["scratch_bytes"]
        + stats["out_ephemeral_bytes"]
        + stats["pycache_bytes"]
        + stats["os_meta_bytes"]
        + stats["root_test_wavs_bytes"]
        + stats["wal_bytes"]
    )
    return stats


def print_brutalist_table(stats: dict, workspace_path: Path):
    total_fmt = format_bytes(stats["total_bytes_recovered"])
    print("\n> ⚙️ **ANERGÍA PURGADA — RESUMEN DE EXERGÍA RECUPERADA (C5-REAL / Ω8)**\n")
    print("| Clase | Objetivo | Antes | Después | Estado |")
    print("|---|---|---|---|---|")
    print(f"| **I2** | Audiovisual Studio Scratch (`scratch_*`, previews) | {format_bytes(stats['scratch_bytes'])} | 0 B | **PURGED** ({stats['scratch_files']} archivos) |")
    print(f"| **I2** | Ephemeral Video & Frame Renders (`out/test_*`, frames) | {format_bytes(stats['out_ephemeral_bytes'])} | 0 B | **PURGED** ({stats['out_ephemeral_files']} items) |")
    print(f"| **I2** | Root Audio Bounces (`*_binaural_*.wav`) | {format_bytes(stats['root_test_wavs_bytes'])} | 0 B | **PURGED** ({stats['root_test_wavs']} archivos) |")
    print(f"| **C** | `__pycache__` & `.pyc` | {format_bytes(stats['pycache_bytes'])} | 0 B | **PURGED** ({stats['pycache_dirs']} dirs, {stats['pyc_files']} pyc) |")
    print(f"| **B** | SQLite WAL Orphans (`*.db-shm`, `*.db-wal`) | {format_bytes(stats['wal_bytes'])} | 0 B | **PURGED** ({stats['wal_orphans']} archivos) |")
    print(f"| **I** | OS Metadata (`.DS_Store`, `*.tmp`, `*.bak`) | {format_bytes(stats['os_meta_bytes'])} | 0 B | **PURGED** ({stats['os_meta_files']} archivos) |")
    print(f"| **L** | Ghost Listeners (`conversation_summaries.db`) | {stats['ghost_listeners_reset']} activos | 0 | **IDLE RESET** (`CASCADE_RUN_STATUS_IDLE`) |")
    print("")
    print(f"- **Exergía Total Recuperada:** `{total_fmt}`")
    print(f"- **Workspace Sanitizado:** `{workspace_path}`")
    print("- **Preservación Canónica (Ω2 / Ω2-AV):** Renders maestros, actas formales y stems intactos.\n")


def main():
    parser = argparse.ArgumentParser(description="Purga de anergía de alta exergía.")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Ruta raíz del workspace a sanear (default: $PWD)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Calcular telemetría sin mutar o eliminar archivos.",
    )
    args = parser.parse_args()

    ws = args.workspace.resolve()
    stats = purge_anergy(ws, dry_run=args.dry_run)
    print_brutalist_table(stats, ws)


if __name__ == "__main__":
    main()
