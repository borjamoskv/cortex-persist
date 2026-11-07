# Copyright 2026 Borja Moskv (borjamoskv)

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn, cast

WRITE_TOOLS = frozenset({"write_to_file", "replace_file_content"})


def json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON keys are not allowed.")
        result[key] = value
    return result


def reject_constant(_value: str) -> NoReturn:
    raise ValueError("Non-finite JSON numbers are not allowed.")


def target_from_payload(raw: bytes) -> Path:
    payload: object = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=json_object,
        parse_constant=reject_constant,
    )
    if not isinstance(payload, dict):
        raise ValueError("Expected a JSON object.")
    tool_call = cast(dict[str, object], payload).get("toolCall")
    if not isinstance(tool_call, dict):
        raise ValueError("Missing or invalid toolCall.")
    call = cast(dict[str, object], tool_call)
    name = call.get("name")
    if not isinstance(name, str) or name not in WRITE_TOOLS:
        raise ValueError("Unsupported write tool.")
    args = call.get("args")
    if not isinstance(args, dict):
        raise ValueError("Missing or invalid tool arguments.")
    target = cast(dict[str, object], args).get("TargetFile")
    if not isinstance(target, str) or not target.strip() or "\x00" in target:
        raise ValueError("TargetFile must be a non-empty absolute path.")
    path = Path(target).expanduser()
    if not path.is_absolute():
        raise ValueError("Relative TargetFile paths are not allowed.")
    return path


def resolve_destination(target: Path) -> Path:
    resolved = target.resolve(strict=False)
    ancestor = resolved
    # Python 3.13+ suppresses symlink loops in non-strict resolution.
    while True:
        try:
            ancestor.resolve(strict=True)
        except FileNotFoundError:
            ancestor = ancestor.parent
        else:
            return resolved


def authorize_target(target: Path, roots: Sequence[Path]) -> None:
    if not roots:
        raise ValueError("At least one authorized root is required.")
    authorized: list[Path] = []
    missing_roots: list[Path] = []
    for root in roots:
        root = root.expanduser()
        if not root.is_absolute():
            raise ValueError(f"Authorized root '{root}' must be an absolute path.")
        try:
            canonical = root.resolve(strict=True)
        except FileNotFoundError:
            # Tolerantly allow non-existent root directory if its non-strict resolution is valid
            canonical = root.resolve(strict=False)
            missing_roots.append(canonical)
            continue
        except OSError as error:
            raise ValueError(f"Authorized root '{root}' cannot be resolved: {error}.") from None
        if not canonical.is_dir():
            raise ValueError(f"Authorized root '{root}' must be an existing directory.")
        authorized.append(canonical)

    resolved = resolve_destination(target)
    # Check against active existing roots first
    if any(resolved.is_relative_to(root) for root in authorized):
        if resolved.is_dir():
            raise ValueError("TargetFile must not be a directory.")
        return

    # Check against tolerated non-existent roots
    if any(resolved.is_relative_to(root) for root in missing_roots):
        if resolved.is_dir():
            raise ValueError("TargetFile must not be a directory.")
        return

    # Target is outside all authorized roots
    if missing_roots and not authorized:
        missing_str = ", ".join(f"'{r}'" for r in missing_roots)
        raise ValueError(
            f"TargetFile '{target}' is outside authorized roots; configured roots do not exist: {missing_str}."
        )
    if missing_roots:
        missing_str = ", ".join(f"'{r}'" for r in missing_roots)
        raise ValueError(
            f"TargetFile '{target}' is outside authorized roots (inactive missing roots: {missing_str})."
        )
    raise ValueError(f"TargetFile '{target}' is outside the authorized roots.")


def evaluate_request(raw: bytes, roots: Sequence[Path]) -> dict[str, str]:
    try:
        target = target_from_payload(raw)
        authorize_target(target, roots)
    except ValueError as error:
        return {"decision": "deny", "reason": str(error)}
    except (OSError, RuntimeError) as error:
        return {
            "decision": "deny",
            "reason": f"Cannot validate filesystem paths: {type(error).__name__}.",
        }
    return {"decision": "allow"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-root", action="append", type=Path, default=[])
    args = parser.parse_args()
    roots = cast(list[Path], args.allow_root)
    result = evaluate_request(sys.stdin.buffer.read(), roots)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
