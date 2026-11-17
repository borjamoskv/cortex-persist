#!/usr/bin/env python3
"""
scripts/anergy_purge.py — Auditor Forense de Anergía y Entropía APFS (C5-REAL / audit-only)

Opera estrictamente en modo `audit-only` conforme a `MODULE.md`:
- Cero borrados (`unlink` / `rmtree`), cero comodines destructivos y cero mutaciones remotas.
- Prohibida la reescritura de `conversation_summaries.db` y el borrado aislado de `.db-wal`/`.db-shm`.
- Inventario determinista por ruta absoluta exacta, tipo, bytes, `st_dev:st_ino`, estado Git y `lsof`/`kill -0`.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import errno
import json
import os
from pathlib import Path
import shutil
import sqlite3
import stat
import subprocess
import sys

CANONICAL_PRESERVED_FILES: frozenset[str] = frozenset(
    {
        "wild_mitxu_b2b_siglo.mp4",
        "mitxudiario-11-ceuton-4min.mp4",
        "mitxudiario-11-ceuton-cinematica-4min.mp4",
        "mitxu_wild_swarm_1080p.mp4",
        "mitx_wild_medina_special_1080p.mp4",
        "mitxudiario_10_master.mp4",
        "mitxuwild_rap_intro_15s_master.mp4",
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
)

CANONICAL_PROTECTED_DIRS: tuple[str, ...] = (
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
    "tt_metal_audit",
    ".cortex/backups",
)

DEPENDENCY_LOCKFILES: frozenset[str] = frozenset(
    {
        "uv.lock",
        "Cargo.lock",
        "pnpm-lock.yaml",
        "package-lock.json",
        "yarn.lock",
        "poetry.lock",
        "Gemfile.lock",
        "composer.lock",
        "flake.lock",
        "manifest.lock.json",
        "skills-lock.json",
        "skills-lock.global.json",
    }
)

CACHE_DIR_NAMES: frozenset[str] = frozenset(
    {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
)

SKIP_WALK_DIRS: frozenset[str] = frozenset({".git", ".venv", "node_modules"})


@dataclass(frozen=True)
class InventoryItem:
    path: str
    kind: str
    bytes: int
    dev: int
    ino: int
    category: str
    git_status: str
    open_pids: list[int] | str
    eligible: bool
    reason: str


def format_bytes(bytes_count: int) -> str:
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    elif bytes_count < 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024):.2f} MB"
    return f"{bytes_count / (1024 * 1024 * 1024):.2f} GB"


def _entry_kind(mode: int) -> str:
    if stat.S_ISLNK(mode):
        return "symlink"
    elif stat.S_ISDIR(mode):
        return "dir"
    return "file"


def _dir_tree_bytes(root: Path) -> int:
    total = 0
    for cur_root, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(cur_root) / d).is_symlink()]
        for fname in files:
            fpath = Path(cur_root) / fname
            try:
                st = os.lstat(fpath)
                total += st.st_size
            except OSError:
                continue
    return total


def _validate_workspace_scope(workspace_path: Path) -> None:
    home = Path.home().absolute()
    music = (home / "Music").absolute()
    ws = workspace_path.absolute()
    if ws == home:
        raise ValueError(
            f"SCOPE_VIOLATION: Prohibido auditar el directorio raíz personal por defecto ({ws})."
        )
    if ws == music or music in ws.parents:
        raise ValueError(
            f"SCOPE_VIOLATION: ~/Music y ~/Music/LIBRARY están excluidos constitucionalmente ({ws})."
        )
    if not ws.exists() or not ws.is_dir():
        raise FileNotFoundError(f"WORKSPACE_NOT_FOUND: Ruta inexistente o no es directorio ({ws}).")


def _load_git_state(workspace_path: Path) -> tuple[bool, set[str], set[str]]:
    if shutil.which("git") is None:
        return False, set(), set()
    probe = subprocess.run(
        ["git", "-C", str(workspace_path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        return False, set(), set()
    top = Path(probe.stdout.strip()).absolute()
    tracked_proc = subprocess.run(
        ["git", "-C", str(workspace_path), "ls-files", "-z"],
        capture_output=True,
        text=True,
        check=False,
    )
    tracked = {
        str((top / rel).absolute())
        for rel in tracked_proc.stdout.split("\0")
        if rel
    }
    status_proc = subprocess.run(
        ["git", "-C", str(workspace_path), "status", "--porcelain", "--ignored=matching", "-z"],
        capture_output=True,
        text=True,
        check=False,
    )
    ignored: set[str] = set()
    for token in status_proc.stdout.split("\0"):
        if token.startswith("!! "):
            ignored.add(str((top / token[3:]).absolute()))
    return True, tracked, ignored


def _resolve_git_label(abs_path: str, has_git: bool, tracked: set[str], ignored: set[str]) -> str:
    if not has_git:
        return "no_git"
    if abs_path in tracked:
        return "tracked"
    if abs_path in ignored or any(abs_path.startswith(ig.rstrip("/") + "/") for ig in ignored):
        return "ignored"
    return "untracked"


def _pid_is_alive(pid: int) -> bool | None:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError as exc:
        if exc.errno == errno.ESRCH:
            return False
        if exc.errno == errno.EPERM:
            return True
        return None


def probe_open_pids(target: Path, recursive: bool = False) -> list[int] | str:
    lsof_bin = shutil.which("lsof")
    if lsof_bin is None:
        return "NO_VERIFICADO"
    cmd = [lsof_bin, "-t", "+D" if recursive else "--", str(target)]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode not in (0, 1):
        return "NO_VERIFICADO"
    if not proc.stdout.strip() and proc.stderr.strip():
        return "NO_VERIFICADO"
    live_pids: list[int] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.isdigit():
            continue
        pid = int(line)
        alive = _pid_is_alive(pid)
        if alive is None:
            return "NO_VERIFICADO"
        if alive:
            live_pids.append(pid)
    return sorted(set(live_pids))


def _is_protected_relpath(rel_posix: str, name: str) -> bool:
    if name in CANONICAL_PRESERVED_FILES or name.endswith(("_master.mp4", "_siglo.mp4")):
        return True
    for prot in CANONICAL_PROTECTED_DIRS:
        if rel_posix == prot or rel_posix.startswith(prot + "/"):
            return True
    return False


def _build_item(
    path: Path,
    category: str,
    git_status: str,
    eligible_default: bool,
    reason_default: str,
    check_fds: bool = False,
) -> InventoryItem | None:
    try:
        st = os.lstat(path)
    except OSError:
        return None
    kind = _entry_kind(st.st_mode)
    size = _dir_tree_bytes(path) if kind == "dir" else st.st_size
    open_pids: list[int] | str = (
        probe_open_pids(path, recursive=(kind == "dir")) if check_fds else []
    )
    eligible = eligible_default
    reason = reason_default
    if kind == "symlink":
        eligible = False
        reason = "Enlace simbólico preservado (inspección sin desreferencia destructiva)."
    elif open_pids == "NO_VERIFICADO":
        eligible = False
        reason = "Estado de descriptores NO_VERIFICADO en lsof/kill -0 (Fail-Closed)."
    elif isinstance(open_pids, list) and len(open_pids) > 0:
        eligible = False
        reason = f"Descriptores abiertos por procesos vivos: PIDs {open_pids}."
    elif git_status == "tracked" and eligible:
        eligible = False
        reason = "Archivo rastreado en Git; requiere revisión explícita."
    return InventoryItem(
        path=str(path),
        kind=kind,
        bytes=size,
        dev=st.st_dev,
        ino=st.st_ino,
        category=category,
        git_status=git_status,
        open_pids=open_pids,
        eligible=eligible,
        reason=reason,
    )


def _classify_file(fname: str, rel_posix: str) -> tuple[str, bool, str, bool] | None:
    if _is_protected_relpath(rel_posix, fname):
        return ("retained_master", False, "Activo maestro o directorio protegido (Ω2).", False)
    if fname.startswith("evidence_") and fname.endswith(".json"):
        return ("retained_evidence", False, "Recibo primario de evidencia blindado.", False)
    if fname.endswith((".db", ".sqlite", ".sqlite3", ".db-wal", ".db-shm")):
        return (
            "sqlite_protected",
            False,
            "Base SQLite / WAL / SHM blindada (prohibido borrado aislado).",
            True,
        )
    if fname in DEPENDENCY_LOCKFILES:
        return ("retained_lockfile", False, "Lockfile de dependencias o gobernanza.", False)
    if fname.endswith(".lock"):
        return ("lockfile_candidate", True, "Lockfile efímero sin descriptor vivo.", True)
    if fname.endswith(".pyc"):
        return ("reconstructible_cache", True, "Bytecode Python reconstruible.", False)
    if fname == ".DS_Store" or fname.endswith((".tmp", ".bak", "~")):
        return ("ephemeral_artifact", True, "Metadato OS o temporal candidato a revisión.", True)
    if "/" not in rel_posix and (
        fname.startswith(("scratch_", "public_studio_")) or "_binaural_" in fname and fname.endswith(".wav")
    ):
        return ("ephemeral_artifact", True, "Artefacto efímero en raíz sujeto a autorización.", True)
    if rel_posix.startswith("out/"):
        return ("ephemeral_artifact", True, "Render efímero en out/ sujeto a autorización.", True)
    return None


def inspect_conversation_summaries_ro() -> dict[str, object]:
    db_path = Path.home().absolute() / ".gemini" / "antigravity" / "conversation_summaries.db"
    if not db_path.is_file():
        return {"present": False, "status": "NOT_PRESENT", "running_or_not_idle": 0, "open_pids": []}
    open_pids = probe_open_pids(db_path, recursive=False)
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cur = conn.cursor()
        cur.execute(
            "SELECT count(*) FROM conversation_summaries "
            "WHERE status = 'CASCADE_RUN_STATUS_RUNNING' OR not_fully_idle = 1"
        )
        row = cur.fetchone()
        conn.close()
        count = int(row[0]) if row else 0
        return {
            "present": True,
            "status": "READ_ONLY_OBSERVED",
            "running_or_not_idle": count,
            "open_pids": open_pids,
        }
    except sqlite3.Error as exc:
        return {
            "present": True,
            "status": f"NO_VERIFICADO ({exc})",
            "running_or_not_idle": None,
            "open_pids": open_pids,
        }


def audit_anergy(workspace_path: Path) -> dict[str, object]:
    ws = workspace_path.absolute()
    _validate_workspace_scope(ws)
    has_git, tracked, ignored = _load_git_state(ws)

    candidates: list[InventoryItem] = []
    exclusions: list[InventoryItem] = []

    for cur_root, dirs, files in os.walk(ws, followlinks=False):
        root_p = Path(cur_root)
        kept_dirs: list[str] = []
        for dname in dirs:
            if dname in SKIP_WALK_DIRS:
                continue
            dp = root_p / dname
            rel_posix = dp.relative_to(ws).as_posix()
            if _is_protected_relpath(rel_posix, dname):
                git_lbl = _resolve_git_label(str(dp), has_git, tracked, ignored)
                item = _build_item(
                    dp, "retained_master", git_lbl, False, "Directorio canónico blindado (Ω2)."
                )
                if item is not None:
                    exclusions.append(item)
                continue
            if dname in CACHE_DIR_NAMES:
                git_lbl = _resolve_git_label(str(dp), has_git, tracked, ignored)
                item = _build_item(
                    dp,
                    "reconstructible_cache",
                    git_lbl,
                    True,
                    "Caché reconstruible determinísticamente.",
                    check_fds=True,
                )
                if item is not None:
                    (candidates if item.eligible else exclusions).append(item)
                continue
            if not dp.is_symlink():
                kept_dirs.append(dname)
        dirs[:] = kept_dirs

        for fname in files:
            fp = root_p / fname
            rel_posix = fp.relative_to(ws).as_posix()
            spec = _classify_file(fname, rel_posix)
            if spec is None:
                continue
            category, elig_def, reason_def, check_fds = spec
            git_lbl = _resolve_git_label(str(fp), has_git, tracked, ignored)
            item = _build_item(fp, category, git_lbl, elig_def, reason_def, check_fds=check_fds)
            if item is not None:
                (candidates if item.eligible else exclusions).append(item)

    conv_db = inspect_conversation_summaries_ro()
    candidate_bytes = sum(it.bytes for it in candidates)
    excluded_bytes = sum(it.bytes for it in exclusions)

    return {
        "mode": "audit-only",
        "mutations_executed": 0,
        "workspace": str(ws),
        "git_detected": has_git,
        "candidate_count": len(candidates),
        "candidate_observed_bytes": candidate_bytes,
        "exclusion_count": len(exclusions),
        "exclusion_observed_bytes": excluded_bytes,
        "candidates": [asdict(it) for it in candidates],
        "exclusions": [asdict(it) for it in exclusions],
        "conversation_summaries_db": conv_db,
        "uninspected_scopes": "NO_VERIFICADO (confinado estrictamente a --workspace)",
    }


def purge_anergy(workspace_path: Path, dry_run: bool = True) -> dict[str, object]:
    """Alias compatible con llamadas previas; bloquea cualquier intento con dry_run=False."""
    if not dry_run:
        raise PermissionError(
            "FAIL_CLOSED_AUDIT_ONLY: anergy-purge-protocol prohíbe borrados o mutaciones SQLite "
            "desde este módulo. Requiere autorización humana explícita por ruta absoluta e inodo."
        )
    return audit_anergy(workspace_path)


def print_audit_report(report: dict[str, object]) -> None:
    cand_bytes = int(report["candidate_observed_bytes"])
    excl_bytes = int(report["exclusion_observed_bytes"])
    conv = report["conversation_summaries_db"]
    assert isinstance(conv, dict)

    print("\n> 🛡️ **INVENTARIO FORENSE DE ANERGÍA (`audit-only` · 0 MUTACIONES EJECUTADAS)**\n")
    print(f"- **Workspace inspeccionado:** `{report['workspace']}`")
    print(f"- **Candidatos elegibles (sujetos a autorización por inodo):** `{report['candidate_count']}` (`{format_bytes(cand_bytes)}` observados)")
    print(f"- **Rutas blindadas / excluidas (`Fail-Closed`):** `{report['exclusion_count']}` (`{format_bytes(excl_bytes)}` observados)")
    print(
        f"- **`conversation_summaries.db` (solo lectura, prohibido reescribir):** "
        f"`{conv.get('status')}` · `running_or_not_idle={conv.get('running_or_not_idle')}` · `open_pids={conv.get('open_pids')}`"
    )
    print(f"- **Fuera de alcance:** `{report['uninspected_scopes']}`")
    print("- **Nota epistémica:** Los bytes observados miden ocupación en disco, no exergía física.\n")

    candidates = report["candidates"]
    assert isinstance(candidates, list)
    if candidates:
        print("| Ruta Exacta | Tipo | Bytes | `dev:ino` | Git | Categoría |")
        print("|---|---|---:|---|---|---|")
        for item in candidates[:50]:
            print(
                f"| `{item['path']}` | `{item['kind']}` | {format_bytes(int(item['bytes']))} "
                f"| `{item['dev']}:{item['ino']}` | `{item['git_status']}` | `{item['category']}` |"
            )
        if len(candidates) > 50:
            print(f"\n*(+{len(candidates) - 50} candidatos adicionales disponibles con `--json`)*\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventario forense audit-only de anergía por ruta exacta e inodo (C5-REAL)."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Ruta exacta del workspace autorizado para inspección (prohibido $HOME o ~/Music).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Bandera de compatibilidad (este módulo opera siempre en modo audit-only).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ejecuta validación rápida de alcance e inventario en modo audit-only.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Muestra estado resumido del workspace y de conversation_summaries.db en solo lectura.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emite el inventario completo en JSON estructurado por stdout.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = audit_anergy(args.workspace)
    except (ValueError, FileNotFoundError, PermissionError) as exc:
        print(f"[FAIL-CLOSED] {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_audit_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
