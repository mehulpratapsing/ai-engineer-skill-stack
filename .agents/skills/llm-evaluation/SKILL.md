---
name: llm-evaluation
license: Apache-2.0
description: Create and run reproducible evaluations for LLM, RAG, prompt, model, and agent changes using golden data, calibrated judges, regression gates, and risk-based analysis.
---

# LLM Evaluation

Use this skill to replace subjective spot checks with a repeatable decision about system quality. Begin with the intended user outcome and cost of failure; select metrics and release gates that measure those outcomes.

## Workflow

1. **Define the decision and failure taxonomy.** Specify the evaluated system boundary, user task, baseline, intended population, high-impact error classes, and whether this is exploration, a release gate, or production monitoring. Define acceptance thresholds with the owning team; never invent a universal threshold or infer safety from an average score.
2. **Build a governed golden dataset.** Use authorized, representative examples with stable IDs, expected answers or claims, relevant evidence, and labels for answerability, risk, and important slices. Include normal, rare, ambiguous, adversarial, multilingual, stale/conflicting, and permission-boundary cases where they apply. Record source, annotation instructions, adjudication, version, and known coverage gaps. Prevent train/evaluation leakage. Minimize and protect confidential, proprietary, personal, and otherwise restricted data; do not copy production conversations into datasets or evaluation tools unless the approved data process permits it. Use synthetic or sanitized cases where authorization is absent.
3. **Choose complementary measurements.** Separate retrieval quality, answer correctness/relevance, faithfulness to evidence, citation support, refusal/abstention, safety, tool selection/execution, and user/task outcomes. Use deterministic checks for exact constraints where possible. Use Ragas or other metric suites as one component, not as a universal score. Measure latency, availability, tokens, and cost alongside quality.
4. **Calibrate LLM-as-judge.** Write a task-specific rubric with clear pass/fail anchors and evidence requirements. Ask for a verdict and concise rubric-linked evidence, such as cited answer spans; do not ask for or expose hidden chain-of-thought. Blind the judge to model identity when practical. Compare judge results against independently labeled human examples; inspect disagreement by slice, test judge sensitivity to phrasing/position, and record judge model, prompt, and version. Keep human adjudication in the loop for ambiguous or consequential decisions. A judge score alone cannot establish correctness or release safety.
5. **Run reproducible comparisons.** Freeze dataset, prompts, model/provider/version, retrieval/index versions, decoding settings, tools, and judge configuration. Use paired comparisons on the same cases. Report per-slice results and confidence intervals or other appropriate uncertainty, sample counts, missingness, and failed cases; avoid relying on a mean that hides severe regressions.
6. **Set release and monitoring gates.** Define critical-slice floors, allowed regression, uncertainty handling, cost/latency budgets, and rollback conditions before viewing candidate results. Preserve a baseline. Add regression coverage for every confirmed defect. Where online experiments are appropriate, use approved exposure, privacy, and stop controls.
7. **Make results actionable.** Link failures to stage and category; distinguish measurement limitations from product defects. Recommend the next experiment and identify when evidence is insufficient to decide.

## Evaluation report

Include objective and decision; system/data/config versions; dataset coverage and governance; metric definitions and judge calibration; baseline comparison with per-slice uncertainty; representative failures; release decision against pre-set thresholds; residual risks; and next actions. Retain only evaluation inputs, outputs, and traces permitted by the applicable data policy, with minimization, access controls, and retention limits. A reproducible report does not require broadly accessible raw production text.

Read [Ragas' current metric catalog](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) and confirm APIs against the installed version. Pair with `rag-engineering` for retrieval diagnostics, `agent-engineering` for trajectory and tool-use evaluation, and `security-review` for adversarial security testing.
