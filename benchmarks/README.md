# Paired benchmark protocol

This suite contains ten synthetic engineering review tasks. It is a preregistered protocol, not evidence of measured model behavior: **no model runs or scores are recorded yet**. The synthetic cases contain no client, employer, or production data.

## Run design

For every task, submit the exact same prompt once with the stack available and once without it. Use the same agent product and version, model ID, system/developer instructions, tool permissions, temperature and token limits, and a fresh conversation in both conditions. The only intended difference is the presence of this repository's skills. Keep skill files read-only during runs; the tasks do not authorize external tools or production changes. Randomize which condition runs first for each pair.

Record the task ID, anonymous condition label, exact prompt hash, full output, agent and model versions, relevant configuration hash, run timestamp, and any tool calls. Do not put credentials, private source code, or customer data in the run record. Redact only secrets or personal data and preserve an unredacted local hash so the published output can be checked without exposing sensitive material.

One pair per task is an exploratory demo, not a statistically reliable claim. For a stronger comparison, repeat each pair at least three times, shuffle output labels before scoring, and have two reviewers score independently. Publish all valid runs, including failures and cases where the stack is no better. Do not select only favorable examples.

The included OpenCode runner creates separate temporary Git projects, gives the stack condition a copy of `.agents/skills`, and isolates user-level OpenCode configuration for each run. It captures raw JSONL events, stderr, prompt/output hashes, model and agent IDs, timestamps, randomized pair order, and exit status. First inspect the plan without calling a model:

```sh
python scripts/run_benchmark.py --model provider/model-name --dry-run
```

After selecting an authorized provider/model and confirming its cost controls, run the full suite (20 model requests):

```sh
python scripts/run_benchmark.py --model provider/model-name --agent plan
```

The runner inherits provider credentials from the current process but does not print them. It redirects home/config paths for its OpenCode subprocesses to a temporary directory so preexisting global skills and config do not contaminate the baseline; it keeps provider API-key environment variables available. Check provider-side spend limits separately: the script limits request count and runtime, but cannot enforce a monetary cap. Incomplete outputs are retained and marked; do not silently omit them.

## Scoring rubric

Score each dimension from 0 to 4 and cite the output passage supporting each score:

| Dimension | 0 | 2 | 4 |
|---|---|---|---|
| Evidence and grounding | Invents facts or misses the supplied evidence | Mostly grounded, with gaps or weak evidence links | Claims are traceable to scenario evidence; unknowns are explicit |
| Technical correctness | Materially wrong or unsafe recommendation | Mixed; key direction is reasonable but incomplete | Correct, prioritized, and technically actionable |
| Risk specificity | Generic checklist with no scenario fit | Identifies some concrete risks | Explains realistic path, impact, and scope for the scenario |
| Evaluation and operations | No useful validation or operational controls | Some checks, missing owners or gates | Practical tests, monitoring, recovery, and decision gates |
| Calibration and boundaries | Unsupported certainty or overreach | Some caveats but leaves important assumptions hidden | Separates facts, assumptions, and limits; respects authorization and data boundaries |

Maximum score: 20 per output. A reviewer must explain any score difference greater than one point. Publish dimension scores as well as totals; a total can hide a serious safety regression. Report inter-rater agreement and unresolved differences rather than silently averaging them.

## Task inventory

The prompts and synthetic scenarios are in [`tasks.json`](tasks.json). The reviewer-only expected observations and critical omissions are in [`answer-key.md`](answer-key.md). Together they cover tenant isolation, ingestion and citation risks, MCP authorization, SSRF and token handling, LLM evaluation, agent retries and approval, Python service hardening, prompt injection, code review, and enterprise architecture boundaries.

## Results

There are no results in this directory yet. Add immutable raw outputs and a machine-readable score file only after real paired runs. Include the agent/model/configuration record and run instructions alongside them. Keep examples in the README labeled illustrative until measured results exist.
