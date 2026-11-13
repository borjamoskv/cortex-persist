#!/usr/bin/env python3
# Copyright 2026 Borja Moskv (borjamoskv)
"""Protocol example with synthetic times/costs. Never calls a model or network."""

import json
import sys


def main():
    request = json.load(sys.stdin)
    candidate = request["candidate"]
    concurrency = candidate["concurrency"]
    task_count = candidate["task_count"]
    # Saturates at N=2 and regresses beyond it, purely as a fixture.
    duration = task_count / min(concurrency, 2) * (1 + max(0, concurrency - 2) * 0.15)
    tasks = [
        {
            "task_id": f"task-{i}",
            "status": "success",
            "latency_ms": 1000,
            "critical_failure": False,
        }
        for i in range(task_count)
    ]
    for task in tasks:
        print(json.dumps({"type": "task", "task": task}), flush=True)
    run = {
        key: candidate[key]
        for key in (
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
        duration_seconds=duration,
        cost_total=candidate["expected_cost"],
        tasks=tasks,
    )
    print(json.dumps({"type": "result", "run": run}), flush=True)


if __name__ == "__main__":
    main()
