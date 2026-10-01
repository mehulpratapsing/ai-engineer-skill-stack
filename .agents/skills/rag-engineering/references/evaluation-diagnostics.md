# RAG Evaluation Diagnostics

Reviewed 2026-09-27. This guide supports metric selection and failure diagnosis; it does not set universal thresholds or guarantee quality. Ragas metrics and APIs evolve, and some metrics use LLM calls. Check the installed package version, the matching API docs, and the current [Ragas metric catalog](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) before implementation. The [Ragas 0.3-to-0.4 migration guide](https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v03_to_v04/) illustrates why code examples and names must be version-checked.

## Measure the stage you need to improve

Keep retrieval, answer generation, citations, authorization, and end-to-end task success distinct. A single aggregate score hides failure modes and can improve while a critical slice gets worse.

| Signal | What it helps answer | Diagnostic limit |
|---|---|---|
| HitRate@k | Did at least one labeled-relevant item appear in the top *k*? | Does not measure how many relevant items were found or their rank. |
| Recall@k | What share of labeled-relevant items appeared in the top *k*? | Requires sufficiently complete relevance labels; label incompleteness looks like system failure. |
| MRR | How early was the first relevant result ranked? | Ignores later relevant results. |
| NDCG | How well did the ranking place graded-relevance items? | Depends on a consistent graded-judgment scheme. |
| Context Precision | How much the retrieved-context ordering favors relevant context; exact Ragas variants and inputs differ. | A high value does not prove the relevant evidence set is complete. |
| Context Recall | Whether reference-relevant information is present in retrieved context, for reference-based variants. | Depends on reference completeness and the chosen metric variant. |
| Faithfulness | Whether answer claims are supported by the supplied context under the selected evaluator. | Cannot establish that the context itself is correct, current, or authorized. |
| Response Relevancy | Whether the response addresses the user query under the selected evaluator. | Relevance is not factual correctness or policy compliance. |
| Citation audit | Whether each answer citation resolves to the right source span and supports its associated claim. | Treat as its own check; a general answer score does not validate every citation. |
| ACL negative tests | Whether a caller cannot retrieve or infer content outside their permissions. | Run independently of answer-quality metrics and test before content reaches the model. |

Ragas' available metrics span context precision/recall, faithfulness, response relevancy, and other tasks. Select a metric only after writing down its unit, labels or references, evaluator, and intended decision. LLM-based scores can be prompt-sensitive and nondeterministic; calibrate them against human-adjudicated examples and record metric/evaluator versions.

## Diagnose failures with evidence

| Observed failure | Inspect first | Possible next experiment |
|---|---|---|
| Relevant source is absent from candidates | Ingestion completeness, source freshness, extraction/OCR, identifiers, metadata filters, ACL filters, query normalization | Repair the failing ingestion/filter stage; then compare lexical, vector, or hybrid retrieval on the same cases. |
| Relevant source exists but ranks too low | Candidate recall, score distributions, language/domain fit, duplicate chunks, metadata, query terms | Compare rank fusion or a reranker with a fixed candidate set; check slices and latency. |
| Evidence is retrieved but key facts are missing from model context | Selection limits, chunk boundaries, context ordering/compression, truncation | Change one context-construction factor and inspect exact spans sent to the model. |
| Answer is unsupported or invents claims | Claim-to-context evidence, conflicting/stale source versions, prompt boundary, decoding behavior | Add claim-level support checks and test abstention/clarification on unanswerable and conflict cases. |
| Answer is supported but does not answer the question | Query intent, answer format, omitted user constraints | Evaluate response relevance separately from faithfulness and inspect failures by task type. |
| Citation points to the wrong place or overstates evidence | Source IDs/version, offsets/page mapping, citation generation and resolution | Verify every cited claim against the canonical source span. |
| Unauthorized content appears in candidates or context | Identity propagation, tenant filters, cache keys, index namespaces, joins and fallbacks | Treat as a security defect; test that disallowed content is excluded before any model call. |

These are triage hypotheses, not automatic root-cause diagnoses. Inspect examples and stage traces before selecting an intervention. Keep the evaluated corpus and ACL snapshot fixed for comparisons.

## Dataset and result handling

- Use only data authorized for evaluation in the selected environment. Production prompts, retrieved passages, outputs, annotations, and traces can contain confidential or restricted material even after obvious personal identifiers are removed.
- Minimize or sanitize examples where possible; protect identifiers and source text with the applicable access, retention, and deletion controls. Do not export raw production logs into a hosted evaluator or a new dataset without approval through the data-governance process.
- Version the dataset, corpus/index snapshot, ACL context, parser/chunker/embedder, retriever/reranker, prompt, model, judge, and metric code. Label answerability and reference completeness; adjudicate material disagreements.
- Report sample counts, coverage gaps, slice results, uncertainty, and concrete errors alongside scores. Establish release thresholds with the responsible owner before looking at candidate results.
- A high score is not proof of truth, safety, authorization, or release readiness. In particular, faithfulness to a wrong or stale retrieved passage remains a failure.

## Primary references

- [Ragas available metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)
- [Ragas migration from 0.3 to 0.4](https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v03_to_v04/)
- [NIST AI Risk Management Framework: Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)
