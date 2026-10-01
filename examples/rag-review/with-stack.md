# Skill-guided review example

## Findings

1. **Potential cross-tenant disclosure - verify and fix before multi-tenant use.** `tenant_id` is accepted but never applied to `vector_store.search` (line 6). If the store contains multiple tenants, a caller can receive another tenant's chunks. Apply a server-derived authorization filter inside retrieval and add a negative cross-tenant test. Do not rely on a tenant value supplied only by the user prompt.
2. **Retrieved content is explicitly trusted as instructions.** The prompt tells the model to follow any instructions in retrieved context (line 9), and then concatenates that context without a trust boundary (line 10). Treat retrieved text as untrusted evidence, separate it from system instructions, and keep tools and authorization enforced outside the prompt. Include an adversarial retrieved-document case in evaluation.
3. **Raw questions are written to logs.** `logger.info` records the full query (line 5). If queries can contain personal or restricted information, this creates an exposure path. Remove query text or apply approved redaction, access, and retention controls; log a correlation ID and safe metadata instead.
4. **No source provenance or citation path.** The result returns only model text (line 13); retrieved source IDs and spans are discarded. Carry canonical source IDs and offsets through generation, require citations to resolve to retrieved spans, and verify citation correctness.
5. **No empty or weak-retrieval behavior.** The function calls the model even when no chunks are returned or evidence is irrelevant. Define a calibrated relevance/abstention policy and test answerable, unanswerable, stale, and conflicting cases. Do not pick a universal score threshold without data.

## Evaluation checks

Use a small permission-aware golden set to check retrieval relevance/recall, cross-tenant leakage, citation resolution, answer support, prompt-injection resistance, and unanswerable-question behavior. Record the corpus/index and model versions. Use human review for consequential questions and report the tested scope and limitations.

This is a code-grounded review example, not a complete security assessment. Confirm the store's tenancy model, logging policy, and model/tool capabilities before assigning final severity.
