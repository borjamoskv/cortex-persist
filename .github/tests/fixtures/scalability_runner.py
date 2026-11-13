"""Local subprocess fault fixture; no external calls."""

import json
import subprocess
import sys
import time

request = json.load(sys.stdin)
c = request["candidate"]
mode = sys.argv[1]
if mode == "timeout":
    time.sleep(60)
if mode == "child":
    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import pathlib,sys,time; time.sleep(0.7); "
            "pathlib.Path(sys.argv[1]).touch()",
            sys.argv[2],
        ]
    )
    print(json.dumps({"type": "unknown", "child_pid": child.pid}), flush=True)
    time.sleep(60)
if mode == "invalid":
    print('{"type":"task","type":"result"}', flush=True)
    sys.exit(0)
if mode == "badkey":
    key = json.dumps("bad\n" + "x" * 1000)
    print("{" + key + ":1," + key + ":2}", flush=True)
    sys.exit(0)
if mode == "oversize":
    print("x" * (9 * 1024 * 1024), flush=True)
    sys.exit(0)
tasks = []
for i in range(c["task_count"]):
    task = {
        "task_id": str(i),
        "status": "failure" if mode == "critical" else "success",
        "latency_ms": 100,
        "critical_failure": mode == "critical",
    }
    tasks.append(task)
    print(json.dumps({"type": "task", "task": task}), flush=True)
    if mode == "critical":
        time.sleep(60)
run = {
    k: c[k]
    for k in (
        "workload_id",
        "evaluator_id",
        "config_id",
        "configuration",
        "currency",
        "concurrency",
        "candidate_id",
    )
}
run.update(
    schema_version=1,
    run_id=request["run_id"],
    campaign_id=request["campaign_id"],
    tasks=tasks,
    cost_total=c["max_cost"] * 2 if mode == "overcharge" else c["expected_cost"],
    duration_seconds=1,
)
if mode == "mismatch":
    run["configuration"] = dict(run["configuration"], model="wrong-model")
if mode == "missing":
    sys.exit(0)
print(json.dumps({"type": "result", "run": run}), flush=True)
if mode == "trailing":
    print("{}", flush=True)
if mode == "nonzero":
    sys.exit(7)
