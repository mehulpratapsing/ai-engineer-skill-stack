---
name: rag-engineering
license: Apache-2.0
description: Design, implement, troubleshoot, and evaluate retrieval-augmented generation pipelines, from authorized ingestion through grounded answers, citations, quality, latency, and cost.
---

# RAG Engineering

Use this skill whenever an application retrieves external or enterprise content to ground a model response. Optimize the whole retrieval-to-answer path against the use case and access policy.

## Workflow

1. **Establish source and access truth.** Inventory authoritative sources, freshness/precedence rules, document owners, classifications, tenant/user ACLs, retention, deletion, and allowed processing locations. Define how source identity and permissions survive every transform. Do not ingest content whose use is not authorized.
2. **Build reliable ingestion.** Inspect source formats and failure cases. Design idempotent, observable ingestion with versioning, incremental updates, deletion propagation, retries, dead-letter handling, and reconciliation. Preserve stable source IDs, title, version/time, canonical URI, page/section/offset provenance, and security metadata. Use OCR/layout extraction only where source quality requires it, and capture extraction failures.
3. **Choose representations deliberately.** Select chunk boundaries from document structure and task needs; measure size and overlap rather than applying one universal setting. Preserve parent/child relationships when useful. Select embeddings compatible with the corpus, query language, deployment constraints, and index dimensions; version the embedding model and rebuild plan. Deduplicate and retain enough provenance to cite the original source.
4. **Design retrieval as a measured pipeline.** Apply authorization filters from verified identity at retrieval and enforce authorization again at the serving boundary. Establish a baseline, then compare lexical/BM25, vector, and hybrid retrieval; rank fusion; metadata filters; query rewriting; reranking; and context compression through controlled experiments. Record candidate counts, scores, filtering, latency, and cost. Preserve original query intent and provenance through rewrites and compression.
5. **Generate grounded answers.** Give the model clear evidence boundaries. Require citations to resolve to retrieved source spans, distinguish evidence from inference, handle conflicts and stale versions, and abstain or ask a useful follow-up when support is missing. Treat retrieved text, files, and metadata as untrusted content that may contain prompt injection.
6. **Evaluate each stage and the whole task.** Build a representative, permission-aware golden set with expected sources/claims, hard negatives, ambiguous queries, ACL cases, stale/conflicting content, and unanswerable questions. Measure retrieval separately from answer quality, citation correctness, permission leakage, and end-to-end usefulness. Track latency percentiles, index freshness, token use, and cost. Use human review for consequential cases; metric scores are evidence, not proof.
7. **Release safely.** Version corpus, parser, chunking, embedding, index, retriever, reranker, prompt, and model. Compare against a baseline, set slice-level regression limits, roll out gradually, and retain rollback and deletion procedures.

When Context7 is configured, use it for focused, version-specific documentation for the actual vector, embedding, reranking, and evaluation libraries in the project. Match the versions in dependency files, verify consequential details against official docs, and keep credentials, secrets, private source code, and restricted data out of queries. Context7 is optional.

## Output

Report the pipeline and its authorization/data lifecycle; the rationale for selected retrieval choices; evaluation dataset and metrics; measured trade-offs; known failure modes; and release/rollback plan. For debugging, trace one failing query through ingestion state, ACL filters, candidates, ranking, context sent to the model, citations, and final response before changing parameters.

Read [RAG evaluation diagnostics](references/evaluation-diagnostics.md) when choosing or interpreting metrics. Verify the installed Ragas version and API against its [current metric catalog](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) before writing code; metric names, APIs, and behavior can change. Pair with `llm-evaluation` for dataset design and statistical release gates, `security-review` for prompt injection and authorization risks, and `ai-system-design` for wider architecture decisions.
