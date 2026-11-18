# Observed scalability analysis

The analyzer consumes exported benchmark results. It does not launch agents,
execute workloads, contact model providers, or fit a predictive USL curve.
All metrics describe the supplied observations, not a demonstrated production
capacity or statistical safety guarantee.

## Run the synthetic example

From the repository root, with Python 3.12 or later:

~~~sh
python3 scripts/analyze_scalability.py \
  --input .github/tests/fixtures/scalability/synthetic.jsonl \
  --policy .github/tests/fixtures/scalability/policy.json \
  --output-dir logs/scalability
~~~

Outputs are report.json and report.md. Omitting --policy produces descriptive
metrics without a recommendation. The default output directory is
logs/scalability, which is already ignored by Git.

The synthetic fixture has three repetitions at N=10, 20 and 40. Each lasts
360 seconds and reports respectively 10, 16 and 17 successful tasks at total
costs of EUR 2, 4 and 8. These represent rates of 100, 160 and 170 correct
tasks/hour, costing EUR 20, 40 and 80/hour. The illustrative policy selects
N=20; N=40 exceeds both its hourly budget and its p95 latency limit.
These fixtures are test data, not measurements of Cortex or an actual agent.

## Input contract: JSONL version 1

Each nonblank UTF-8 line must be a complete JSON object describing one completed
run. The following example is pretty-printed for readability; serialize it on
one line when exporting JSONL:

~~~json
{
  "schema_version": 1,
  "run_id": "benchmark-a-n10-repeat1",
  "workload_id": "dataset-and-load-profile-sha256",
  "evaluator_id": "acceptance-rules-sha256",
  "configuration": {
    "model": "model-version-and-settings",
    "hardware": "hardware-and-resource-budget-id",
    "quotas": "api-quota-and-concurrency-profile-id",
    "revision": "application-commit-sha"
  },
  "concurrency": 10,
  "duration_s": 360,
  "currency": "EUR",
  "total_cost": 2,
  "tasks": [
    {
      "task_id": "task-1",
      "status": "success",
      "latency_ms": 4000,
      "critical_failure": false
    }
  ]
}
~~~

Required identifiers are nonempty strings. Concurrency is a positive integer;
duration is a finite positive number. Costs and latencies are finite,
nonnegative numbers. Currency is a three-letter uppercase code. Quality and
critical failure rates are fractions between 0 and 1.

Configuration must include nonempty model, hardware and quotas strings.
Additional configuration fields are allowed and participate in comparison
identity. Runs are grouped by exact workload, evaluator, complete configuration
and currency; only concurrency varies within a comparison. Other extra run/task
fields are ignored. Schema version must be the integer 1.

Run IDs are unique across the input file. Task IDs are unique within a run;
reusing the same task IDs in independent repetitions is expected. Allowed
terminal states are success, failure, timeout and cancelled. The task array
may be empty, in which case throughput is zero and task-based rates and p95 are
undefined. Duplicate JSON keys, duplicate IDs, non-finite numbers, malformed
JSON, missing required fields and unfinished tasks are rejected.

### Exporting real measurements

- Freeze the workload distribution, offered load, evaluator, runtime version,
  model settings, hardware and provider quotas before comparing concurrency.
  Record these in the identifiers and configuration, using no credentials or
  task payloads. The analyzer trusts this provenance; it cannot verify the
  truth or representativeness of exported measurements.
- Start the run clock when its workload starts and stop it after every included
  task terminates. Account for queueing, retries and final draining consistently.
  Do not silently drop failed, timed-out or cancelled tasks.
- Emit one final result per logical task. Consolidate retries in the exporter:
  latency includes the entire task lifecycle, costs include every attempt,
  and critical_failure is true if any attempt caused a defined critical failure,
  even when the final task succeeded. A policy-blocked action is not automatically
  a critical failure; define the evaluator's criterion before benchmarking.
- total_cost covers the whole run in one currency, including failed attempts,
  inference, infrastructure and human review within the declared accounting
  scope. Record that scope in configuration so it is not silently mixed.
- Use explicit null for unknown total_cost or unknown critical_failure.
  Missing knowledge is never treated as free execution or zero risk.
- Export each run with JSON serialization and append a newline. Repeat each
  concurrency independently; three is the recommendation default, not a
  statistical confidence claim. A fixed resource budget means elasticity
  describes concurrency scaling, not resource scaling.

## Metrics and aggregation

For each run and each concurrency level, the reports include:

| Metric | Definition |
| --- | --- |
| goodput_per_hour | 3600 * successful unique tasks / elapsed seconds |
| success_rate | successful unique tasks / all terminal tasks |
| cost_per_hour | 3600 * total cost / elapsed seconds |
| cost_per_success | total cost / successful unique tasks |
| latency_p95_ms | sorted latency at rank ceil(0.95 * task count), one-based |
| critical_failure_rate | tasks classified critical / all terminal tasks |

The aggregate sums time, cost and task counts across repetitions. It pools raw
task latencies before computing p95; it never averages run percentiles.
All terminal states contribute to the denominator and latency distribution.
Any unknown cost makes aggregate cost metrics unknown; any unknown critical
classification makes the aggregate critical failure rate unknown. Known
critical counts and unknown classification counts remain visible.

Undefined divisions, zero-success cost ratios and non-finite derived metrics
are represented as JSON null, with a reason under undefined_reasons.
Aggregates outside the representable numeric range are validation errors.

For adjacent measured concurrency levels in the same group:

~~~text
elasticity = (ln(goodput_2) - ln(goodput_1)) / (ln(N_2) - ln(N_1))
~~~

Nonpositive or unknown goodput makes elasticity undefined with an explicit
reason. Negative elasticity is retained: it indicates decreased observed
throughput. No unmeasured concurrency is extrapolated.

## Optional policy

~~~json
{
  "schema_version": 1,
  "currency": "EUR",
  "budget_per_hour": 50,
  "min_success_rate": 0.95,
  "max_p95_ms": 10000,
  "max_critical_failure_rate": 0,
  "min_repetitions": 3
}
~~~

All thresholds are required when a policy is supplied. Only min_repetitions
is optional, defaulting to 3. Unknown policy fields are rejected to catch typos.
Thresholds are inclusive. The example values are illustrative, not universal
production defaults.

Each repetition must satisfy every threshold. A passing aggregate cannot hide
a failing repetition. A currency mismatch fails policy assessment without
converting currencies. Missing required measurements or insufficient repetitions
prevent admissibility. Zero-success levels cannot be recommended.

Each group selects the admissible measured concurrency with highest aggregate
goodput. Exact ties prefer lower aggregate cost/success, then lower concurrency.
If no level qualifies, recommendation is null and the report explains the
violations and missing evidence. Assessment states are passed, failed,
insufficient_data and not_evaluated; known violations take precedence over
missing evidence, but both remain in the report.

The reports contain schema version, input/policy SHA-256 hashes, configuration,
run IDs, individual/aggregate metrics, elasticities and assessment details.
No current timestamp is injected: identical inputs, source paths and options
produce identical report bytes. Reports are replaced atomically one file at
a time; a write failure can leave only one updated file. A nonzero exit means
the pair must not be treated as a completed report.

## CI and exit codes

The existing CI suite discovers the analyzer's unittest tests. It also executes
the synthetic example and publishes Markdown through GITHUB_STEP_SUMMARY,
explicitly labeled as a synthetic demonstration. CI does not run a real load
test, acquire credentials or enforce production performance thresholds.

| Exit | Meaning |
| --- | --- |
| 0 | Both reports generated, including descriptive-only or policy-failing results |
| 2 | Invalid arguments, invalid data/policy or attempted input overwrite |
| 1 | Input/output or other execution error |

~~~sh
python3 -B -m unittest discover -s .github/tests -p 'test_*.py' -v
~~~

The test environment uses the existing CI requirements. The analyzer itself
uses only Python's standard library.
