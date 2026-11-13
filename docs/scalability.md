# Scalability analysis and experiment planning

Python 3.12, standard library only. These tools implement ideas 0–2:
observed finite-batch metrics, uncertainty-aware recommendations, and a
cost-aware experiment planner with an explicit local runner protocol.
They do not instrument Cortex agents, fit USL, extrapolate production capacity,
or claim a measured 10x improvement. USL remains a later, separately validated
predictive extension; no custom nonlinear optimizer is shipped in this version.

## Quick start

From the repository root, analyze existing results:

```bash
python3 scripts/analyze_scalability.py \
  --input resultados.jsonl \
  --policy examples/scalability/policy.json \
  --output-dir logs/scalability
```

`--input` is required and repeatable. `--policy` is optional. Outputs default to
the already ignored `logs/scalability/`: `report.json` and `report.md`.
Exit 0 includes abstention and policy violations. Invalid input or an I/O error
exits 2. There is no performance-based CI failure mode.

Propose the first experiment without starting any process:

```bash
python3 scripts/plan_scalability.py \
  --space examples/scalability/space.json \
  --policy examples/scalability/policy.json
```

Exercise the complete protocol with **synthetic times and costs**, no network,
no inference and no provider charges:

```bash
python3 scripts/run_scalability.py \
  --input logs/scalability/runs.jsonl \
  --space examples/scalability/space.json \
  --policy examples/scalability/policy.json \
  --runner python3 examples/scalability/synthetic_runner.py

python3 scripts/analyze_scalability.py \
  --input logs/scalability/runs.jsonl \
  --policy examples/scalability/policy.json

python3 scripts/plan_scalability.py \
  --input logs/scalability/runs.jsonl \
  --space examples/scalability/space.json \
  --policy examples/scalability/policy.json
```

The example chooses N=2 after 15 completed trials. Resuming the same history
does not rerun a resolved campaign. `run_scalability.py` requires POSIX for
process groups and file locking (tested on macOS; CI uses Ubuntu). Its runner
argv follows `--runner` and is executed without a shell. It returns 130 on a
handled keyboard interruption, retaining observations and accounting.

## Run contract, version 1

UTF-8 JSONL, exactly one object per line. This is a single valid record:

```json
{"schema_version":1,"run_id":"r1","workload_id":"load-v1","evaluator_id":"eval-v1","config_id":"config-v1","configuration":{"model":"model-id","hardware":"machine-id","quotas":{"rpm":60}},"currency":"EUR","concurrency":2,"duration_seconds":1,"cost_total":0.02,"tasks":[{"task_id":"t1","status":"success","latency_ms":900,"critical_failure":false}]}
```

| Field | Contract |
| --- | --- |
| `schema_version` | Integer 1, never a boolean. |
| `run_id` | Nonempty identifier, unique across all input files. |
| `workload_id`, `evaluator_id`, `config_id` | Versioned identities chosen by the producer. |
| `configuration` | Object requiring string `model`, string `hardware`, object `quotas`; extra configuration fields are allowed and participate in grouping. Include code revision, dataset hash, retry policy and evaluator settings when relevant. |
| `currency` | Three uppercase letters; currencies are never combined or converted. |
| `concurrency` | Positive integer: nominal admission/worker limit. |
| `duration_seconds` | Finite, positive wall duration of the entire batch, including drain. |
| `cost_total` | Finite nonnegative total, including retries and failures, or `null`. |
| `reserved_cost` | Optional original spending cap for this dispatch; the executor records it on every outcome. It is a reservation, never measured cost. |
| `tasks` | Final logical task outcomes, with retries consolidated. |
| `run_status` | Optional `completed` (default) or `aborted`. |
| `abort_reason` | Required for `aborted`, forbidden for `completed`. |
| `occupancy_intervals` | Optional `[[start_seconds,end_seconds], ...]` relative to batch start, one interval per occupied slot segment. |
| `campaign_id`, `candidate_id` | Optional pair; required by the planner/executor. |

Each task requires `task_id`, terminal `status` (`success`, `failure`, `timeout`,
`cancelled`), finite nonnegative `latency_ms`, and boolean-or-null
`critical_failure`. IDs are unique within a run. Latency includes all attempts
and waits for that logical task. Critical side effects may exist even when a
task eventually succeeds; these two fields are independent observations.

Empty completed batches, duplicate JSON keys, duplicate IDs, non-finite numbers
(including overflow such as `1e999`), unknown top-level/task fields and missing
terminal outcomes are errors. Booleans are not numbers. Blank JSONL lines are
errors. Aborted rows may have no terminal tasks; they retain only observed
outcomes, remain visible individually and never enter performance comparisons.
If an otherwise measured arm also has aborted attempts, its recommendation
remains uncertain (or violated under the critical-abort policy). Excluding
partial timings must not turn surviving trials into a safety endorsement.
Review the abort and use a fresh confirmation campaign to clear that uncertainty.

Grouping uses all identities, the entire canonical configuration and currency.
Changing hardware/model/quota without changing metadata invalidates comparability;
the analyzer cannot detect an unreported configuration change.

## Metrics and uncertainty

- `successes_per_hour = 3600 * total_successes / total_wall_seconds`.
- `success_rate = total_successes / total_tasks`.
- `cost_per_hour = 3600 * total_cost / total_wall_seconds`.
- `cost_per_success = total_cost / total_successes`.
- `p95_terminal_ms`: pooled nearest rank `ceil(0.95 * task_count)`, including
  failures, timeouts and cancellations. Percentiles are never averaged.
- `p95_time_to_success_ms`: the same rank after assigning non-successes infinite
  penalty. A non-finite answer is serialized as `null` with a reason, not Infinity.
  This is an explicit reliability penalty, not a survival estimate of latent
  completion time. Terminal p95 remains a separate, valid observed metric.
- `critical_failure_rate`: fraction with critical failure, available only if
  every task is assessed. `critical_assessed_count` exposes coverage.
- `success_within_deadline_rate`: successes within the inclusive `deadline_ms`,
  divided by all tasks. Null if no deadline is configured.
- `effective_concurrency`: integral of measured occupied slots divided by wall
  time; `occupancy_fraction` divides that integral by nominal slot-time.
  Intervals must remain inside the run and never overlap above nominal N.
  Missing occupancy is unknown, never inferred from total task latencies.
- Elasticity between adjacent nominal concurrencies uses differences of logs.
  Zero throughput and undefined logarithms produce null plus a reason.

Any unknown run cost makes aggregate cost metrics unknown. Zero denominators,
missing assessments and undefined bootstrap draws also retain reasons.
Arithmetic beyond finite aggregate range is an explicit validation error.
Capacity is **observed finite-batch benchmark throughput**, including startup
and drain, not a stationary service-rate estimate.

Bootstrap resamples entire independent run clusters, recomputing ratios and
pooled percentiles. Seeded output is reproducible, including elasticity bands.
Quality fractions use weighted-run Hoeffding bounds, with squared weights
`(tasks_in_run / total_tasks)^2`; zero observed failures therefore never produce
a claim of zero risk. These bounds assume independent runs and fixed planned
task counts. Shared incidents across runs, selection-dependent cluster sizes,
and undocumented drift violate those assumptions.

Intervals are pointwise and exploratory, not simultaneous confidence claims
over all metrics/candidates or valid repeated-significance tests. Adaptive
selection requires fresh fixed-design confirmation runs. Every recommendation
states `confirmation_required: true`; neither throughput optimality nor a
tenfold saving has been statistically certified by these tools.

## Policy

See [example policy](../examples/scalability/policy.json). Defaults are five
repetitions, 20 tasks, 95% confidence, 1000 bootstrap draws (100–10000 allowed),
seed 0, 5% relative tolerance, throughput objective and no quality constraints.
The example's empty constraints demonstrate mechanics, not production readiness.

Objectives: `successes_per_hour` (maximize), `cost_per_success` (minimize).
Monetary objectives/constraints require an explicit policy `currency`.
Supported optional constraints are:

- `min_success_rate`, `min_successes_per_hour`.
- `max_cost_per_hour`, `max_cost_per_success`, `max_p95_terminal_ms`.
- `max_critical_failure_rate`.
- `min_success_within_deadline_rate` (requires `deadline_ms`).

Observed violations exclude a candidate. Unknown inputs, currency mismatch,
insufficient repetitions/tasks or a bound crossing a threshold cause abstention.
Among admissible candidates, the smallest N is selected only if its conservative
objective bound is within tolerance of every non-excluded competitor's optimistic
bound. Otherwise the result is `abstain`; if every candidate violates policy,
it is `no_admissible_configuration`. No recommendation extrapolates to an unseen N.

`abort_on_critical: true` is a deterministic execution rule: one observed critical
task ends the local runner and holds that arm. It is not a statistical SPRT.

## Experiment space and sequential planning

See [example space](../examples/scalability/space.json). Each arm fixes all group
metadata, N and `task_count`, and declares `expected_cost`, `max_cost` and
`timeout_seconds`. A campaign fixes currency, total budget and maximum attempts.
IDs and arms must be unique. History from another campaign or configuration is
rejected. Budgets use decimal arithmetic; unknown bills reserve the run's original
`reserved_cost`, even if a later space changes `max_cost`. Unknown historical
bills without a recorded reservation stop dispatch until reconciled; budget totals
stay null rather than inventing a cap or charging zero.

The planner first covers arms and repetitions, then allocates by relative
uncertainty per expected cost, with periodic lowest-N control probes. This is an
explicit heuristic, not D-optimal Fisher information. Aborted attempts count
toward budget and attempts, but not completed repetitions. Timeouts receive a
cooldown and can be re-probed after other arms. Insufficient funds reserve no
fractional run. A measured bill above `max_cost` halts further dispatch.

An additional critical-rate confidence sequence operates on complete, fixed-size
run means. It spends error probability `alpha / (arms * t * (t+1))` across arms
and looks; it never assumes within-run task independence. Unknown classifications
suspend this inference. A lower bound above the policy threshold temporarily
holds an arm, with later re-probing. The independence/stability assumptions remain
necessary. Bootstrap intervals are used for allocation, not sequential rejection.

After at least four complete control runs, a configured deviation of the latest
control throughput from its prior median halts the campaign as possible drift.
This is a diagnostic heuristic, not a calibrated change-point test. Relabel the
configuration and start a new campaign after investigation; do not pool regimes.

## Runner protocol and recovery

The runner receives one JSON object on stdin: `protocol_version: 1`, assigned
`run_id`, `campaign_id`, full `candidate`, policy/space hashes and `reserved_cost`.
It emits newline-terminated JSON events on stdout, flushing each event:

```json
{"type":"task","task":{"task_id":"t1","status":"success","latency_ms":900,"critical_failure":false}}
```

After every declared task has exactly one terminal event, emit
`{"type":"result","run":{...}}` containing the full run contract, then exit 0.
Final task contents and configuration must exactly match the events/request.
No extra stdout, duplicate events or trailing data are accepted. Events are
limited to 8 MiB each. Stderr is retained in ignored per-run log files.

Before dispatch, the executor durably writes `<history>.pending.json`; it holds
an exclusive `<history>.lock` for the campaign. History is atomically rewritten
and synced after each attempt, then the reservation is removed. A crash with an
unresolved reservation blocks resumption. Recover the actual run record under
its assigned ID and candidate in history, including the original reservation
from the pending file if the bill is unknown; the executor can then reconcile it.
Do not delete pending reservations to retry an execution with unknown billing.

On timeout, critical stop or protocol error, the local process group is terminated.
Only observed terminal tasks are retained in an aborted row. Actual cost is null
unless a validated final bill was received (or launch definitely failed).
The budget reserves the recorded dispatch maximum for null bills; it does not
call them zero or substitute a newly edited maximum.

**The runner must enforce its own provider-side spending cap**, including retries
and in-flight calls. Local termination cannot cancel remote billing. Reservations
are conditional on that declared cap, not a guarantee about third-party charges.
No built-in adapter invokes a provider; any such command must be supplied explicitly.

## Evidence, tests and CI

JSON reports preserve input file SHA-256 hashes, configuration, individual run
IDs/metrics, null reasons, policy/hash, contract/tool/Python versions and a hash
of the analyzer implementation. Markdown escapes input-derived HTML and Markdown.
Reports cannot overwrite their input/configuration files.

New tests run without site packages:

```bash
python3.12 -S -B -m unittest discover -s .github/tests -p 'test_scalability*.py' -v
```

The existing full CI suite still uses its existing pinned PyYAML dependency:

```bash
.venv/bin/python -B -m unittest discover -s .github/tests -p 'test_*.py' -v
```

[CI](../.github/workflows/ci.yml) keeps correctness tests in the existing sanity
job. A separate informational job runs only the synthetic example, writes a job
summary and uploads JSON/JSONL/Markdown evidence. It makes no provider calls and
does not gate merges on measured performance.

Acceptance of a real 10x improvement needs an independent comparison against the
previous version at a fixed workload/evaluator, counting experiment, verification,
failure and retry costs. The synthetic example establishes protocol behavior only.
