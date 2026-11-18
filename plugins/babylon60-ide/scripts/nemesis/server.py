"""Minimal MCP stdio adapter: immutable startup registry, no arbitrary paths/argv."""

import json
import os
from pathlib import Path
import sys

from runner import OPERATIONS, run

MAX_REQUEST = 65536


def dispatch(request, jobs, store):
    method = request.get("method")
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "nemesis-verifier", "version": "0.1.0"},
        }
    if method == "ping":
        return {}
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "list_jobs",
                    "description": "List operator-prepared immutable verification jobs.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                    },
                },
                {
                    "name": "verify",
                    "description": "Run a fixed operation on an operator-prepared snapshot.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "job": {"type": "string", "enum": sorted(jobs)},
                            "operation": {"type": "string", "enum": list(OPERATIONS)},
                        },
                        "required": ["job", "operation"],
                        "additionalProperties": False,
                    },
                },
            ]
        }
    if method == "tools/call":
        params = request.get("params", {})
        args = params.get("arguments", {})
        if not isinstance(args, dict):
            raise ValueError("arguments must be an object")
        if params.get("name") == "list_jobs" and not args:
            value = jobs
        elif params.get("name") == "verify" and set(args) == {"job", "operation"}:
            if not isinstance(args["job"], str) or args["job"] not in jobs:
                raise ValueError("unknown job")
            job = jobs[args["job"]]
            if args["operation"] not in job["operations"]:
                raise ValueError("operation not allowed for this job")
            value = run(store, job["source"], job["runtime"], args["operation"])
        else:
            raise ValueError("unknown tool or unsupported arguments")
        return {"content": [{"type": "text", "text": json.dumps(value)}]}
    raise ValueError("unsupported method")


def main():
    data = os.environ.get("PLUGIN_DATA")
    if not data:
        raise RuntimeError("PLUGIN_DATA must be set by the trusted host")
    store = Path(os.path.realpath(data))
    registry = store / "jobs.json"
    jobs = json.loads(registry.read_bytes()) if registry.is_file() else {}
    if not isinstance(jobs, dict):
        raise ValueError("invalid host registry")
    while True:
        line = sys.stdin.buffer.readline(MAX_REQUEST + 1)
        if not line:
            break
        if len(line) > MAX_REQUEST:
            raise ValueError("request too large")
        request = json.loads(line)
        if "id" not in request:
            continue
        response = {"jsonrpc": "2.0", "id": request["id"]}
        try:
            response["result"] = dispatch(request, jobs, store)
        except (ValueError, OSError, RuntimeError) as exc:
            response["error"] = {"code": -32602, "message": str(exc)}
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
