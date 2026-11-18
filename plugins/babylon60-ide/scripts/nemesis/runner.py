"""Host-owned preparation and macOS verifier. No command strings in the tool API.

Trust boundary: macOS, this supervisor, the operator and sealed OS files are TCB.
Source, build scripts and every descendant are untrusted. Receipts are content
addresses, not signatures or proof of semantic correctness of a supplied oracle.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import platform
import plistlib
import re
import resource
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).absolute().parent
OPERATIONS = ("cargo-check", "lean-check", "verify")
SYSTEM_READS = ("/usr/lib", "/usr/share/locale", "/System/Library/Perl")
SYSTEM_EXEC = (
    "/bin/sh",
    "/bin/bash",
    "/bin/cat",
    "/bin/mv",
    "/bin/rm",
    "/bin/ln",
    "/bin/chmod",
    "/usr/bin/touch",
    "/usr/bin/grep",
    "/usr/bin/perl",
    "/usr/bin/dirname",
)
DYLD_CACHE = "/System/Volumes/Preboot/Cryptexes/OS/System/Library/dyld"
SYSTEM_FILES = ("/private/etc/ssl/openssl.cnf", "/private/var/select/sh")
MAX_LOG = 2 * 1024 * 1024
TIMEOUT = 120


def canonical(value):
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode()


def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def file_digest(path):
    with open(path, "rb") as stream:
        return "sha256:" + hashlib.file_digest(stream, "sha256").hexdigest()


def inventory(root):
    """Full tree, including dotfiles/untracked files; no implicit Git exclusions."""
    root = Path(root).absolute()
    result = []
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            item = {"path": rel, "mode": stat.S_IMODE(info.st_mode)}
            if stat.S_ISLNK(info.st_mode):
                target = os.readlink(path)
                # Lexical containment plus final realpath containment. No read follows
                # an escaping link; nested/absolute symlinks and special files fail closed.
                if os.path.isabs(target):
                    raise ValueError(f"absolute symlink: {rel}")
                final = os.path.realpath(path)
                if os.path.commonpath((str(root), final)) != str(root):
                    raise ValueError(f"escaping symlink: {rel}")
                item.update(
                    kind="symlink", target=target, sha256=digest(os.fsencode(target))
                )
            elif stat.S_ISREG(info.st_mode):
                fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
                with os.fdopen(fd, "rb") as stream:
                    before = os.fstat(stream.fileno())
                    value = (
                        "sha256:" + hashlib.file_digest(stream, "sha256").hexdigest()
                    )
                    after = os.fstat(stream.fileno())
                if (before.st_ino, before.st_size, before.st_mtime_ns) != (
                    after.st_ino,
                    after.st_size,
                    after.st_mtime_ns,
                ):
                    raise ValueError(f"input changed while hashing: {rel}")
                item.update(kind="file", size=info.st_size, sha256=value)
            elif stat.S_ISDIR(info.st_mode):
                item.update(kind="directory")
            else:
                raise ValueError(f"special file forbidden: {rel}")
            result.append(item)
    return sorted(result, key=lambda item: item["path"])


def checked(argv):
    # Image construction can copy tens of thousands of SDK files. This is the
    # trusted host preparation budget; untrusted operations still get TIMEOUT.
    result = subprocess.run(argv, capture_output=True, timeout=600)
    if result.returncode:
        raise RuntimeError(
            f"host command failed ({result.returncode}): {argv!r}: "
            + (result.stdout + result.stderr).decode(errors="replace")[:8192]
        )
    return result.stdout


def require_macos():
    if sys.platform != "darwin" or not Path("/usr/bin/sandbox-exec").is_file():
        raise RuntimeError("NO_VERIFICADO: macOS Seatbelt backend unavailable")


def system_mounts():
    roots = (*SYSTEM_READS, *SYSTEM_EXEC, DYLD_CACHE)
    mounts = {}
    for root in roots:
        info = os.statvfs(root)
        protection = "read-only-mount"
        if not info.f_flag & os.ST_RDONLY:
            # dyld cryptex backing files may be on Preboot. Require root ownership
            # and no writable ancestor for our UID; the OS updater remains TCB.
            for parent in (Path(root), *Path(root).parents):
                st = parent.stat()
                if st.st_uid != 0 or st.st_mode & 0o022 or os.access(parent, os.W_OK):
                    protection = "NO_VERIFICADO: system mount is not read-only"
                    break
            else:
                protection = "root-owned; OS updater trusted"
        mounts[root] = {
            "device": os.stat(root).st_dev,
            "inode": os.stat(root).st_ino,
            "protection": protection,
        }
    disk = plistlib.loads(checked(["/usr/sbin/diskutil", "info", "-plist", "/"]))
    return {
        "roots": mounts,
        "snapshot": disk.get("APFSSnapshotUUID"),
        "snapshot_name": disk.get("APFSSnapshotName"),
        "seal_reported": disk.get("Sealed"),
        "kernel": platform.platform(),
    }


def capture_system(destination):
    """Hash the entire allowed OS file superset and dyld caches, never user data.

    OS mounts must remain read-only and unchanged. Root/OS compromise is outside
    this local threat model, exactly as for the Seatbelt implementation itself.
    """
    before = system_mounts()
    entries = [
        {
            "path": path,
            "kind": "file",
            "sha256": file_digest(path),
            "mode": stat.S_IMODE(os.stat(path).st_mode),
        }
        for path in SYSTEM_EXEC
    ]
    for root in (*SYSTEM_READS, DYLD_CACHE):
        for base, dirs, files in os.walk(
            root, followlinks=False, onerror=lambda exc: (_ for _ in ()).throw(exc)
        ):
            for name in sorted(dirs + files):
                path = Path(base) / name
                info = path.lstat()
                item = {"path": str(path), "mode": stat.S_IMODE(info.st_mode)}
                if path.is_symlink():
                    item.update(kind="symlink", target=os.readlink(path))
                elif path.is_file():
                    item.update(
                        kind="file", size=info.st_size, sha256=file_digest(path)
                    )
                elif path.is_dir():
                    item.update(kind="directory")
                else:
                    raise RuntimeError(f"unhashable OS input: {path}")
                entries.append(item)
    if before != system_mounts():
        raise RuntimeError("system mounts changed during capture")
    destination.write_bytes(
        canonical(
            {
                "schema": 1,
                "algorithm": "sha256",
                "mounts": before,
                "entries": sorted(entries, key=lambda x: x["path"]),
            }
        )
    )


@contextlib.contextmanager
def mounted(image, destination):
    destination.mkdir()
    checked(
        [
            "/usr/bin/hdiutil",
            "attach",
            "-readonly",
            "-nobrowse",
            "-noautoopen",
            "-mountpoint",
            str(destination),
            str(image),
        ]
    )
    try:
        if not os.statvfs(destination).f_flag & os.ST_RDONLY:
            raise RuntimeError("mount is not read-only")
        yield destination
    finally:
        # A busy mount is an error, never silently force-detach or accept a result.
        checked(["/usr/bin/hdiutil", "detach", "-quiet", str(destination)])


def make_image(source, store, kind):
    """Trusted operator API; source must be a private staging tree, not attacker-writable.

    The authoritative inventory is taken AFTER the filesystem is mounted read-only.
    Original live workspace bytes are never passed to the sandbox.
    """
    require_macos()
    store.mkdir(parents=True, exist_ok=True)
    staged_entries = inventory(source)  # reject special files and escaping symlinks
    logical_bytes = sum(entry.get("size", 0) for entry in staged_entries)
    # Explicit filesystem headroom: hdiutil's srcfolder estimate filled its own
    # small APFS volume while copying the 66 MiB linker library in our fixture.
    size_mib = max(128, (logical_bytes * 5 // 4) // (1024 * 1024) + 64)
    with tempfile.TemporaryDirectory(prefix="prepare-", dir=store) as tmp:
        tmp = Path(tmp)
        image = tmp / "input.dmg"
        checked(
            [
                "/usr/bin/hdiutil",
                "create",
                "-size",
                f"{size_mib}m",
                "-srcfolder",
                str(source),
                "-format",
                "UDRO" if kind == "runtime" else "UDZO",
                "-fs",
                "APFS",
                str(image),
            ]
        )
        with mounted(image, tmp / "mount") as mount:
            entries = inventory(mount)
        image_hash = file_digest(image)
        manifest = {
            "schema": 1,
            "kind": kind,
            "algorithm": "sha256",
            "entries": entries,
            "image_sha256": image_hash,
        }
        identity = digest(canonical(manifest))
        destination = store / identity.removeprefix("sha256:")
        destination.mkdir(exist_ok=False)
        shutil.move(image, destination / "input.dmg")
        (destination / "manifest.json").write_bytes(canonical(manifest))
        (destination / "image.sha256").write_text(image_hash)
        return identity


def object_path(store, identity):
    if not isinstance(identity, str) or not re.fullmatch(
        r"sha256:[0-9a-f]{64}", identity
    ):
        raise ValueError("invalid content address")
    return store / identity[7:]


def load_object(store, identity, kind):
    path = object_path(store, identity)
    manifest = json.loads((path / "manifest.json").read_bytes())
    if digest(canonical(manifest)) != identity or manifest["kind"] != kind:
        raise ValueError("manifest identity mismatch")
    if file_digest(path / "input.dmg") != manifest["image_sha256"]:
        raise ValueError("image identity mismatch")
    return path, manifest


def profile(source, runtime, output):
    q = json.dumps
    reads = " ".join(
        f"(subpath {q(str(p))})" for p in (*SYSTEM_READS, source, runtime, output)
    )
    parents = sorted(
        {
            str(p)
            for root in (
                source,
                runtime,
                output,
                *map(Path, SYSTEM_EXEC),
                *map(Path, SYSTEM_READS),
            )
            for p in root.parents
        }
    )
    metadata = " ".join(f"(literal {q(p)})" for p in parents)
    executables = " ".join(f"(literal {q(p)})" for p in SYSTEM_EXEC)
    system_files = " ".join(f"(literal {q(p)})" for p in SYSTEM_FILES)
    code_roots = " ".join(f"(subpath {q(str(p))})" for p in (source, runtime, output))
    return (
        "(version 1)\n(deny default)\n"
        "(allow process-fork)\n(allow sysctl-read)\n"
        f"(allow process-exec {executables} {code_roots})\n"
        f'(allow file-read* {reads} {executables} {system_files} (literal "/") (literal "/dev/null") (literal "/dev/urandom"))\n'
        f"(allow file-read-metadata {metadata})\n"
        f'(allow file-write* (subpath {q(str(output))}) (literal "/dev/null"))\n'
        # No sockets, Mach services, Apple Events, HID, task ports or host writes.
    )


def environment(runtime, output):
    return {
        "PATH": f"{runtime}/rust/bin:{runtime}/lean/bin:{runtime}/bin:/usr/bin:/bin",
        "HOME": str(output / "home"),
        "TMPDIR": str(output / "tmp"),
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "CARGO_HOME": str(output / "cargo-home"),
        "CARGO_TARGET_DIR": str(output / "target"),
        "CARGO_NET_OFFLINE": "true",
        "OPENSSL_CONF": "/dev/null",
        "CARGO_BUILD_JOBS": "2",
        "RUSTC": str(runtime / "rust/bin/rustc"),
        "RUSTDOC": str(runtime / "rust/bin/rustdoc"),
        "RUSTFLAGS": f"-C linker={runtime}/clt/usr/bin/clang",
        "SDKROOT": str(runtime / "sdk"),
        "LEAN_PATH": str(runtime / "lean/lib/lean"),
        "NEMESIS_OUTPUT": str(output),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
    }


def limits():
    os.umask(0o077)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT, TIMEOUT))
    resource.setrlimit(resource.RLIMIT_FSIZE, (256 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))


def execute(argv, policy, env, cwd, timeout=TIMEOUT):
    """Bounded logs; no inherited descriptors, stdin, environment or shell parsing."""
    proc = subprocess.Popen(
        ["/usr/bin/sandbox-exec", "-p", policy, *map(str, argv)],
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
        start_new_session=True,
        preexec_fn=limits,
    )
    streams = {"stdout": bytearray(), "stderr": bytearray()}
    selector = selectors.DefaultSelector()
    for name in streams:
        stream = getattr(proc, name)
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, name)
    deadline = time.monotonic() + timeout
    error = None
    try:
        while selector.get_map():
            if time.monotonic() > deadline:
                error = "timeout"
                break
            for key, _ in selector.select(0.1):
                chunk = os.read(key.fd, 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                streams[key.data].extend(chunk)
                if sum(map(len, streams.values())) > MAX_LOG:
                    error = "output limit"
                    break
            if error:
                break
        if not error:
            proc.wait(timeout=max(0.01, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        error = "timeout"
    finally:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
        selector.close()
        proc.stdout.close()
        proc.stderr.close()
    return {
        "argv": list(map(str, argv)),
        "returncode": proc.returncode,
        "error": error,
        **{
            k: bytes(v[:MAX_LOG]).decode("utf-8", errors="replace")
            for k, v in streams.items()
        },
    }


def command(operation, source, runtime, output):
    src = source / "source"
    if operation == "cargo-check":
        return [
            runtime / "rust/bin/cargo",
            "check",
            "--locked",
            "--offline",
            "--manifest-path",
            src / "Cargo.toml",
            "--target-dir",
            output / "target",
        ]
    if operation == "lean-check":
        return [
            runtime / "lean/bin/lean",
            "-o",
            output / "Main.olean",
            src / "Main.lean",
        ]
    if operation == "verify":
        return ["/bin/bash", "--noprofile", "--norc", src / "verify.sh"]
    raise ValueError("operation not allowed")


def os_identity(source):
    system_file = source / "oracle/host-environment.json"
    system = json.loads(system_file.read_bytes())
    if system["mounts"] != system_mounts():
        raise RuntimeError("system mounts changed; prepare a fresh runtime")
    return {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "sw_vers": checked(["/usr/bin/sw_vers"]).decode(),
        "supervisor": file_digest(HERE / "runner.py"),
        "python": file_digest(sys.executable),
        "sandbox_exec": file_digest("/usr/bin/sandbox-exec"),
        "system_read_roots": SYSTEM_READS,
        "system_files_sha256": file_digest(system_file),
        "fixed_system_files": {path: file_digest(path) for path in SYSTEM_FILES},
        "system_mounts": system["mounts"],
        "kernel_services": "clock, entropy, sysctl, scheduling: nondeterministic; OS is TCB",
    }


def run(store, source_id, runtime_id, operation):
    require_macos()
    if operation not in OPERATIONS:
        raise ValueError("operation not allowed")
    source_object, source_manifest = load_object(store, source_id, "source")
    runtime_object, runtime_manifest = load_object(store, runtime_id, "runtime")
    runs = store / "runs"
    runs.mkdir(exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="run-", dir=runs))
    output = run_dir / "output"
    output.mkdir()
    for name in ("home", "tmp", "cargo-home", "target"):
        (output / name).mkdir()
    canary = run_dir / "outside-canary"
    canary.write_bytes(b"outside-original\n")
    outside_before = (file_digest(canary), canary.stat().st_ino, canary.stat().st_mode)
    with (
        mounted(source_object / "input.dmg", run_dir / "source") as source,
        mounted(runtime_object / "input.dmg", run_dir / "runtime") as runtime,
    ):
        if inventory(source) != source_manifest["entries"]:
            raise ValueError("mounted source differs from manifest")
        # The content address binds the complete image bytes to the manifest
        # produced on a read-only mount at preparation. Rehash the image once,
        # not its thousands of immutable SDK files four times per run.
        runtime_guard = runtime / "rust/bin/cargo"
        runtime_before = (file_digest(runtime_guard), runtime_guard.stat().st_ino)

        def runtime_observation():
            # Full inventory was checked on the immutable mount. Re-observe the
            # attempted create and an existing inode rather than re-reading GBs.
            return (
                bool(os.statvfs(runtime).f_flag & os.ST_RDONLY)
                and not (runtime / "created").exists()
                and runtime_before
                == (file_digest(runtime_guard), runtime_guard.stat().st_ino)
            )

        env_identity = os_identity(source)
        # Bind the preflight to the supervisor's own oracle, not one supplied by source.
        if file_digest(source / "oracle/probe.sh") != file_digest(HERE / "probe.sh"):
            raise ValueError("probe oracle changed; prepare a new source snapshot")
        policy = profile(source, runtime, output)
        env = environment(runtime, output)
        (run_dir / "policy.sb").write_text(policy)
        probe = execute(
            ["/bin/sh", source / "oracle/probe.sh", source, runtime, output, canary],
            policy,
            env,
            source / "source",
        )
        probe_ok = probe["returncode"] == 0 and probe["error"] is None
        probe_ok = probe_ok and probe["stdout"].endswith("PROBE_PASS\n")
        probe_ok = probe_ok and (output / "allowed").read_bytes() == b"allowed"
        # Capture kernel errors before untrusted build scripts can alter output/.
        # These bytes live in the supervisor and are saved outside the write grant.
        probe_errors = {
            path.name: path.read_text(errors="replace")[:8192]
            for path in output.glob("*.stderr")
            if path.is_file() and not path.is_symlink()
        }
        independent = {
            "source_unchanged": inventory(source) == source_manifest["entries"],
            "runtime_unchanged": runtime_observation(),
            "outside_unchanged": outside_before
            == (file_digest(canary), canary.stat().st_ino, canary.stat().st_mode),
            "source_readonly": bool(os.statvfs(source).f_flag & os.ST_RDONLY),
            "runtime_readonly": bool(os.statvfs(runtime).f_flag & os.ST_RDONLY),
        }
        if not probe_ok or not all(independent.values()):
            result = {"error": "preflight failed", "returncode": None}
        else:
            result = execute(
                command(operation, source, runtime, output),
                policy,
                env,
                source / "source",
            )
        independent["source_after_operation"] = (
            inventory(source) == source_manifest["entries"]
        )
        independent["runtime_after_operation"] = runtime_observation()
        independent["outside_after_operation"] = outside_before == (
            file_digest(canary),
            canary.stat().st_ino,
            canary.stat().st_mode,
        )
        # Output symlinks are untrusted data; never traverse/hash their targets.
        evidence = {
            "probe": probe,
            "probe_errors": probe_errors,
            "operation": result,
            "independent_observation": independent,
        }
        (run_dir / "evidence.json").write_bytes(canonical(evidence))
        if env_identity != os_identity(source):
            raise RuntimeError("environment changed during execution")
        oracle = {
            "supervisor": env_identity["supervisor"],
            "preflight": file_digest(source / "oracle/probe.sh"),
            "operation": operation,
            "entrypoint": file_digest(command(operation, source, runtime, output)[-1])
            if operation == "verify"
            else file_digest(command(operation, source, runtime, output)[0]),
            "transitive_source": source_id,
            "transitive_runtime": runtime_id,
        }
        receipt = {
            "schema": 1,
            "algorithm": "sha256",
            "source": source_id,
            "runtime": runtime_id,
            "operation": operation,
            "policy_sha256": digest(policy.encode()),
            "environment": {"variables": env, "identity": env_identity},
            "environment_sha256": digest(
                canonical({"variables": env, "identity": env_identity})
            ),
            "oracle": oracle,
            "oracle_sha256": digest(canonical(oracle)),
            "evidence_sha256": digest(canonical(evidence)),
            "result": "PASS"
            if result["returncode"] == 0
            and not result.get("error")
            and probe_ok
            and all(independent.values())
            else "FAIL",
            "content_binding": "INCONCLUSIVE"
            if any(
                entry["protection"].startswith("NO_VERIFICADO")
                for entry in env_identity["system_mounts"]["roots"].values()
            )
            else "PASS",
            "limits": [
                "OS kernel/services and trusted supervisor remain TCB; not deterministic replay",
                "No signed authenticity or semantic guarantee of supplied verify.sh",
                "Process-group cleanup is not proof against setsid descendants",
                "Not a hard aggregate memory/process/disk quota",
            ],
        }
    receipt_id = digest(canonical(receipt))
    (run_dir / "receipt.json").write_bytes(canonical(receipt))
    (run_dir / "receipt.sha256").write_text(receipt_id)
    return {"receipt": receipt_id, "path": str(run_dir), **receipt}


def verify_receipt(path, expected_receipt, source, runtime, oracle):
    """Caller must retain expected_receipt independently; an unkeyed hash is no signature."""
    path = Path(path)
    raw = (path / "receipt.json").read_bytes()
    receipt = json.loads(raw)
    if digest(raw) != expected_receipt:
        raise ValueError("receipt digest mismatch")
    if (receipt["source"], receipt["runtime"], receipt["oracle_sha256"]) != (
        source,
        runtime,
        oracle,
    ):
        raise ValueError("stale result: input/runtime/oracle identity mismatch")
    if file_digest(path / "evidence.json") != receipt["evidence_sha256"]:
        raise ValueError("evidence digest mismatch")
    if file_digest(path / "policy.sb") != receipt["policy_sha256"]:
        raise ValueError("policy digest mismatch")
    return receipt


def prepare_source(source, store):
    # Host operation only. MCP clients never submit paths or snapshot bytes.
    with tempfile.TemporaryDirectory(prefix="nemesis-source-") as tmp:
        staging = Path(tmp)
        inventory(source)
        shutil.copytree(source, staging / "source", symlinks=True)
        (staging / "oracle").mkdir()
        shutil.copyfile(HERE / "probe.sh", staging / "oracle/probe.sh")
        capture_system(staging / "oracle/host-environment.json")
        (staging / "canary").write_bytes(b"source-original\n")
        return make_image(staging, store, "source")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, required=True)
    sub = parser.add_subparsers(dest="action", required=True)
    prepare = sub.add_parser("prepare-source")
    prepare.add_argument("path", type=Path)
    runtime = sub.add_parser("prepare-runtime")
    runtime.add_argument("path", type=Path)
    execute_parser = sub.add_parser("run")
    execute_parser.add_argument("source")
    execute_parser.add_argument("runtime")
    execute_parser.add_argument("operation", choices=OPERATIONS)
    args = parser.parse_args()
    # realpath is used for this fixed private artifact store, not dynamic workspace discovery.
    store = Path(os.path.realpath(args.store))
    if args.action == "prepare-source":
        result = prepare_source(args.path.absolute(), store)
    elif args.action == "prepare-runtime":
        result = make_image(args.path.absolute(), store, "runtime")
    else:
        result = run(store, args.source, args.runtime, args.operation)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
