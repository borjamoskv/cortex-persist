# Copyright 2026 Borja Moskv (borjamoskv)
"""POSIX runner protocol with crash-visible reservations and bounded dispatch."""

from __future__ import annotations

import os
import selectors
import signal
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

from .contract import (
    IDENTITY_FIELDS,
    ValidationError,
    canonical,
    decode,
    fields,
    fingerprint,
    group_key,
    load_runs,
    read_json,
    require,
    validate_run,
    validate_task,
)
from .planner import money, plan, validate_history

MAX_EVENT_BYTES = 8 * 1024 * 1024


def atomic_write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)


def stop_group(process):
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            pass
        if sig == signal.SIGTERM:
            try:
                process.wait(timeout=0.2)
            except subprocess.TimeoutExpired:
                pass
    process.wait()


def execute(command, request, policy, stderr_path: Path):
    candidate = request["candidate"]
    tasks, seen, final = [], set(), None
    started = time.monotonic()
    reason, process = None, None
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryFile() as input_stream, stderr_path.open("wb") as errors:
            input_stream.write((canonical(request) + "\n").encode())
            input_stream.seek(0)
            process = subprocess.Popen(
                command,
                stdin=input_stream,
                stdout=subprocess.PIPE,
                stderr=errors,
                start_new_session=True,
                bufsize=0,
            )
            try:
                os.set_blocking(process.stdout.fileno(), False)
                buffer = b""
                eof = False
                with selectors.DefaultSelector() as selector:
                    selector.register(process.stdout, selectors.EVENT_READ)
                    while not eof or process.poll() is None:
                        remaining = candidate["timeout_seconds"] - (
                            time.monotonic() - started
                        )
                        if remaining <= 0:
                            reason = "runner_timeout"
                            break
                        if eof:
                            try:
                                process.wait(timeout=min(remaining, 0.1))
                            except subprocess.TimeoutExpired:
                                pass
                            continue
                        if not selector.select(min(remaining, 0.1)):
                            continue
                        chunk = os.read(process.stdout.fileno(), 65536)
                        if not chunk:
                            eof = True
                            require(not buffer, "runner event missing newline")
                            continue
                        buffer += chunk
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            require(
                                len(line) <= MAX_EVENT_BYTES,
                                "runner event exceeds size limit",
                            )
                            event = decode(line)
                            require(
                                isinstance(event, dict),
                                "runner event must be an object",
                            )
                            require(
                                final is None, "runner emitted data after final result"
                            )
                            if event.get("type") == "task":
                                fields(event, {"type", "task"}, set(), "task event")
                                task = validate_task(event["task"])
                                require(
                                    task["task_id"] not in seen,
                                    "duplicate streamed task_id",
                                )
                                seen.add(task["task_id"])
                                tasks.append(task)
                                require(
                                    len(tasks) <= candidate["task_count"],
                                    "too many streamed tasks",
                                )
                                if (
                                    policy["abort_on_critical"]
                                    and task["critical_failure"] is True
                                ):
                                    reason = "critical_failure"
                                    break
                            elif event.get("type") == "result":
                                fields(event, {"type", "run"}, set(), "result event")
                                result = validate_run(event["run"])
                                require(
                                    result.get("run_status", "completed")
                                    == "completed",
                                    "runner final must be completed",
                                )
                                require(
                                    result["run_id"] == request["run_id"]
                                    and result.get("campaign_id")
                                    == request["campaign_id"]
                                    and result.get("candidate_id")
                                    == candidate["candidate_id"],
                                    "runner identity mismatch",
                                )
                                require(
                                    group_key(result) == group_key(candidate)
                                    and result["concurrency"]
                                    == candidate["concurrency"],
                                    "runner configuration mismatch",
                                )
                                require(
                                    len(tasks) == candidate["task_count"],
                                    "missing streamed task results",
                                )
                                require(
                                    {t["task_id"]: t for t in result["tasks"]}
                                    == {t["task_id"]: t for t in tasks},
                                    "final tasks differ from streamed tasks",
                                )
                                final = result
                            else:
                                raise ValidationError("unknown runner event type")
                        if reason:
                            break
                        require(
                            len(buffer) <= MAX_EVENT_BYTES,
                            "runner event exceeds size limit",
                        )
                if reason is None:
                    if process.returncode != 0:
                        reason = f"runner_exit_{process.returncode}"
                    elif final is None:
                        reason = "missing_final_result"
            finally:
                stop_group(process)
                process.stdout.close()
    except KeyboardInterrupt:
        reason = "interrupted"
    except ValidationError as exc:
        reason = f"runner_protocol_error: {exc}"
    except OSError as exc:
        reason = f"runner_io_error: {exc.__class__.__name__}"
    if reason is None:
        final["reserved_cost"] = candidate["max_cost"]
        return validate_run(final)
    reason = "".join(
        c if 32 <= ord(c) and not 0xD800 <= ord(c) <= 0xDFFF else " " for c in reason
    )[:512]
    # Aborted rows contain only observed terminal tasks. They never enter
    # throughput rankings; unknown bills reserve max_cost in the planner.
    record = {key: candidate[key] for key in IDENTITY_FIELDS}
    record.update(
        schema_version=1,
        run_id=request["run_id"],
        campaign_id=request["campaign_id"],
        candidate_id=candidate["candidate_id"],
        concurrency=candidate["concurrency"],
        duration_seconds=time.monotonic() - started,
        tasks=tasks,
        cost_total=final["cost_total"]
        if final
        else (0 if process is None and reason.startswith("runner_io_error") else None),
        run_status="aborted",
        abort_reason=reason,
        reserved_cost=candidate["max_cost"],
    )
    return validate_run(record)


def campaign(
    history_path: Path, space, policy, command, output_dir: Path, *, on_run=None
):
    require(
        os.name == "posix",
        "campaign execution currently requires POSIX process groups and flock",
    )
    import fcntl

    require(bool(command), "an explicit runner command is required")
    history_path = history_path.resolve()
    history_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = Path(str(history_path) + ".lock")
    pending_path = Path(str(history_path) + ".pending.json")
    with lock_path.open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValidationError("another executor holds this campaign lock") from exc
        runs, sources = (
            load_runs([history_path], allow_empty=True)
            if history_path.exists()
            else ([], [])
        )
        validate_history(runs, space)
        if pending_path.exists():
            pending, _ = read_json(pending_path)
            require(
                isinstance(pending, dict)
                and pending.get("space_sha256") == fingerprint(space),
                "pending reservation uses a different space; "
                "reconcile it before resuming",
            )
            require(
                any(r["run_id"] == pending.get("run_id") for r in runs),
                "unresolved dispatch: reconcile its result in history before resuming; "
                "no automatic retry",
            )
            reconciled = next(r for r in runs if r["run_id"] == pending["run_id"])
            require(
                isinstance(pending.get("candidate"), dict), "invalid pending candidate"
            )
            require(
                reconciled["candidate_id"]
                == pending.get("candidate", {}).get("candidate_id"),
                "reconciled run differs from pending candidate",
            )
            pending_path.unlink()
        while True:
            payload = plan(runs, space, policy)
            if payload["plan"]["status"] != "propose":
                break
            candidate = payload["plan"]["next_candidate"]
            request = {
                "protocol_version": 1,
                "run_id": str(uuid.uuid4()),
                "campaign_id": space["campaign_id"],
                "candidate": candidate,
                "policy_sha256": fingerprint(policy),
                "space_sha256": fingerprint(space),
                "reserved_cost": candidate["max_cost"],
            }
            atomic_write(pending_path, canonical(request) + "\n")
            result = execute(
                command, request, policy, output_dir / f"{request['run_id']}.stderr.log"
            )
            runs.append(result)
            atomic_write(history_path, "".join(canonical(r) + "\n" for r in runs))
            pending_path.unlink()
            if on_run:
                on_run(result)
            if result.get("abort_reason") == "interrupted":
                payload = plan(runs, space, policy)
                payload["plan"].update(
                    status="stop", reason="interrupted", next_candidate=None
                )
                break
            if result["cost_total"] is not None and money(result["cost_total"]) > money(
                candidate["max_cost"]
            ):
                payload = plan(runs, space, policy)
                break
        if history_path.exists():
            _, sources = load_runs([history_path], allow_empty=True)
        return payload, sources
