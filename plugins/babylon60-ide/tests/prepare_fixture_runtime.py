"""Prepare a minimal local test runtime; never installs or downloads tools.

This supports the fixtures, not the complete BABYLON dependency graph. Supply
vendored dependencies/additional Lean modules in a separate reviewed runtime
for real project jobs. All bytes copied below enter the read-only image manifest.
"""

import argparse
from pathlib import Path
import shutil


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        destination.symlink_to(source.readlink())
    elif source.is_dir():
        shutil.copytree(source, destination, symlinks=True)
    else:
        shutil.copy2(source, destination)


def main():
    parser = argparse.ArgumentParser()
    for name in ("rust", "lean", "clt", "sdk", "destination"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    out = args.destination
    out.mkdir(exist_ok=False)
    for name in ("cargo", "rustc", "rustdoc"):
        copy(args.rust / "bin" / name, out / "rust/bin" / name)
    for path in (args.rust / "lib").glob("*.dylib"):
        copy(path, out / "rust/lib" / path.name)
    copy(
        args.rust / "lib/rustlib/aarch64-apple-darwin/lib",
        out / "rust/lib/rustlib/aarch64-apple-darwin/lib",
    )
    copy(args.lean / "bin/lean", out / "lean/bin/lean")
    for path in (args.lean / "lib/lean").rglob("*"):
        rel = path.relative_to(args.lean / "lib/lean")
        if path.is_file() and (
            path.name.endswith(".dylib")
            or (str(rel).startswith("Init") and ".olean" in path.name)
        ):
            copy(path, out / "lean/lib/lean" / rel)
    for name in ("clang", "ld"):
        # CLT uses a clang symlink; materialize the resolved tool in this new bundle.
        path = args.clt / "usr/bin" / name
        destination = out / "clt/usr/bin" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination, follow_symlinks=True)
    copy(args.clt / "usr/lib/clang", out / "clt/usr/lib/clang")
    for name in (
        "libtapi.dylib",
        "libcodedirectory.dylib",
        "libLTO.dylib",
        "libswiftDemangle.dylib",
    ):
        copy(args.clt / "usr/lib" / name, out / "clt/usr/lib" / name)
    copy(args.sdk, out / "sdk")


if __name__ == "__main__":
    main()
