"""Boundary tests. Integration uses real Seatbelt and readonly disk images."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import pytest

PLUGIN = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(PLUGIN / "scripts/nemesis"))
import runner  # noqa: E402
import server  # noqa: E402


@pytest.mark.parametrize(
    "arguments",
    [
        {"job": "fixture", "operation": "verify", "argv": ["rm", "-rf", "/"]},
        {"job": "../../escape", "operation": "verify"},
        {"job": "fixture", "operation": "verify; touch /tmp/x"},
        {"job": "fixture", "operation": "run_command"},
        {"path": "/tmp", "operation": "verify"},
        ["verify"],
    ],
)
def test_mcp_rejects_expansion_before_dispatch(tmp_path, arguments):
    with pytest.raises(ValueError):
        server.dispatch(
            {
                "method": "tools/call",
                "params": {"name": "verify", "arguments": arguments},
            },
            {
                "fixture": {
                    "source": "unused",
                    "runtime": "unused",
                    "operations": ["verify"],
                }
            },
            tmp_path,
        )


def test_closed_operation_set(tmp_path):
    for value in ("/bin/sh", "cargo test", "verify --help", "lean-check;id"):
        with pytest.raises(ValueError):
            runner.command(value, tmp_path, tmp_path, tmp_path)


def test_inventory_captures_local_and_untracked_bytes(tmp_path):
    (tmp_path / "local.txt").write_text("edited working tree")
    (tmp_path / ".ignored").write_text("also an input")
    first = runner.inventory(tmp_path)
    assert {e["path"] for e in first} == {"local.txt", ".ignored"}
    (tmp_path / "local.txt").write_text("second version")
    assert runner.digest(runner.canonical(first)) != runner.digest(
        runner.canonical(runner.inventory(tmp_path))
    )


def test_rejects_escaping_link_and_special_file(tmp_path):
    link = tmp_path / "link"
    link.symlink_to("../outside")
    with pytest.raises(ValueError, match="escaping symlink"):
        runner.inventory(tmp_path)
    link.unlink()
    os.mkfifo(tmp_path / "fifo")
    with pytest.raises(ValueError, match="special file"):
        runner.inventory(tmp_path)


def test_mcp_stdio_real_transport(tmp_path):
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "verify",
                "arguments": {"command": "touch /tmp/forbidden"},
            },
        },
    ]
    proc = subprocess.run(
        [sys.executable, "-I", str(PLUGIN / "scripts/nemesis/stdio.py")],
        input="".join(json.dumps(r) + "\n" for r in requests),
        text=True,
        capture_output=True,
        timeout=10,
        env={"PLUGIN_DATA": str(tmp_path), "PATH": "/usr/bin:/bin"},
    )
    assert proc.returncode == 0, proc.stderr
    replies = [json.loads(line) for line in proc.stdout.splitlines()]
    assert replies[0]["result"]["serverInfo"]["name"] == "nemesis-verifier"
    assert {t["name"] for t in replies[1]["result"]["tools"]} == {"list_jobs", "verify"}
    assert replies[2]["error"]["code"] == -32602


@pytest.mark.skipif(sys.platform != "darwin", reason="real macOS policy test")
def test_preopened_descriptor_is_closed(tmp_path):
    root = Path(os.path.realpath(tmp_path))
    outside = root / "outside"
    outside.write_text("original")
    output = root / "output"
    output.mkdir()
    fd = os.open(outside, os.O_WRONLY)
    try:
        os.dup2(fd, 80, inheritable=True)
        result = runner.execute(
            [
                "/usr/bin/perl",
                "-e",
                'open(my $f, ">&=80") or die "$!\\n"; print $f "bad";',
            ],
            runner.profile(root / "source", root / "runtime", output),
            runner.environment(root / "runtime", output),
            output,
        )
        assert result["returncode"] != 0
        assert "Bad file descriptor" in result["stderr"], result
        assert outside.read_text() == "original"
    finally:
        os.close(fd)
        os.close(80)


def integration_config():
    path = os.environ.get("NEMESIS_TEST_CONFIG")
    if not path:
        pytest.skip("Set NEMESIS_TEST_CONFIG to an operator-prepared fixture registry")
    return json.loads(Path(path).read_text())


@pytest.mark.parametrize("operation", runner.OPERATIONS)
def test_real_operation_and_independent_write_denial(operation):
    config = integration_config()
    result = runner.run(
        Path(config["store"]), config["source"], config["runtime"], operation
    )
    evidence = json.loads((Path(result["path"]) / "evidence.json").read_text())
    assert evidence["probe"]["returncode"] == 0, evidence
    assert all(evidence["independent_observation"].values()), evidence
    assert result["result"] == "PASS", evidence
    if operation == "cargo-check":
        assert "NEMESIS_BUILD_WRITE_DENIED" in evidence["operation"]["stderr"]
        assert list((Path(result["path"]) / "output/target").rglob("build-output"))
    if operation == "lean-check":
        assert (Path(result["path"]) / "output/Main.olean").is_file()
    if operation == "verify":
        assert (
            Path(result["path"]) / "output/verification.txt"
        ).read_text() == "VERIFIED_FIXTURE\n"
    runner.verify_receipt(
        result["path"],
        result["receipt"],
        config["source"],
        config["runtime"],
        result["oracle_sha256"],
    )
    # Actually change source and oracle bytes; their identities cannot reuse this result.
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "source"
        source_object, manifest = runner.load_object(
            Path(config["store"]), config["source"], "source"
        )
        with runner.mounted(
            source_object / "input.dmg", Path(tmp) / "mounted"
        ) as source:
            shutil.copytree(source, copy, symlinks=True)

        assert runner.inventory(copy) == manifest["entries"]
        (copy / "source/local-untracked.txt").write_text("mutated input")
        changed_input = runner.make_image(copy, Path(config["store"]), "source")
        assert changed_input != config["source"]
        with pytest.raises(ValueError, match="stale result"):
            runner.verify_receipt(
                result["path"],
                result["receipt"],
                changed_input,
                config["runtime"],
                result["oracle_sha256"],
            )
        (copy / "oracle/probe.sh").write_text("#!/bin/sh\nexit 0\n")
        oracle = {
            **result["oracle"],
            "preflight": runner.file_digest(copy / "oracle/probe.sh"),
        }
        changed_oracle = runner.digest(runner.canonical(oracle))
        with pytest.raises(ValueError, match="stale result"):
            runner.verify_receipt(
                result["path"],
                result["receipt"],
                config["source"],
                config["runtime"],
                changed_oracle,
            )
        receipt_copy = Path(tmp) / "receipt"
        shutil.copytree(
            result["path"],
            receipt_copy,
            ignore=shutil.ignore_patterns("output", "source", "runtime"),
        )
        (receipt_copy / "evidence.json").write_text("{}")
        with pytest.raises(ValueError, match="evidence digest mismatch"):
            runner.verify_receipt(
                receipt_copy,
                result["receipt"],
                config["source"],
                config["runtime"],
                result["oracle_sha256"],
            )
        (Path(config["store"]).parent / f"binding-{operation}.json").write_bytes(
            runner.canonical(
                {
                    "receipt": result["receipt"],
                    "original_source": config["source"],
                    "changed_input": changed_input,
                    "changed_oracle": changed_oracle,
                    "input_rejection": "PASS",
                    "oracle_rejection": "PASS",
                    "evidence_tamper_rejection": "PASS",
                }
            )
        )


def test_stress_same_policy_twenty_rounds():
    config = integration_config()
    store = Path(config["store"])
    source_object, source_manifest = runner.load_object(
        store, config["source"], "source"
    )
    runtime_object, runtime_manifest = runner.load_object(
        store, config["runtime"], "runtime"
    )
    with tempfile.TemporaryDirectory(prefix="stress-", dir=store) as temp:
        root = Path(temp)
        outside = root / "outside"
        outside.write_text("original")
        rounds = []
        with (
            runner.mounted(source_object / "input.dmg", root / "source") as source,
            runner.mounted(runtime_object / "input.dmg", root / "runtime") as runtime,
        ):
            for i in range(21):  # warmup + 20; no performance claims
                output = root / f"output-{i}"
                output.mkdir()
                result = runner.execute(
                    [
                        "/bin/sh",
                        source / "oracle/probe.sh",
                        source,
                        runtime,
                        output,
                        outside,
                    ],
                    runner.profile(source, runtime, output),
                    runner.environment(runtime, output),
                    source / "source",
                )
                rounds.append(result)
                assert result["returncode"] == 0, result
                assert (output / "allowed").read_bytes() == b"allowed"
                assert outside.read_text() == "original"
                assert not (source / "created").exists()
            assert runner.inventory(source) == source_manifest["entries"]
            assert runner.inventory(runtime) == runtime_manifest["entries"]
        (store.parent / "stress.json").write_bytes(
            runner.canonical({"rounds": rounds, "warmup": 1, "measured": 20})
        )
