---
name: code-review
license: Apache-2.0
description: Review a proposed code change for concrete correctness, security, performance, maintainability, testing, observability, and compatibility defects; report prioritized findings with evidence.
---

# Code Review

Use this skill when reviewing a diff, pull request, patch, or recent implementation. The goal is to find defects the author can act on. Read project conventions and enough surrounding code to understand behavior before judging the change.

## Workflow

1. **Establish review scope.** Identify the base revision and changed files. Read the full diff, relevant callers/callees, schemas/contracts, configuration, and existing tests. Separate pre-existing issues from regressions introduced by the change.
2. **Trace behavior.** Check intended behavior against actual control/data flow, edge cases, error handling, state transitions, retries/idempotency, concurrency, and compatibility. Follow untrusted input to sensitive operations. Review authn/authz at the enforcement point, not only in route declarations or prompts.
3. **Check operational effects.** Look for material performance or cost regressions, unbounded work, missing timeouts/cancellation, unsafe logging, missing metrics/alerts for new failure modes, migration/backward compatibility risks, and tests that fail to cover critical behavior. Consider privacy and data retention for AI inputs, outputs, retrieval, and traces.
4. **Validate only what the scope requires.** Use repository checks or focused tests when requested or required by the workflow. Do not infer correctness from a passing test subset. Report exact checks and outcomes; avoid changing the patch during a review unless asked to implement fixes.
5. **Report actionable findings first.** Use the repository's severity rubric. If it has none, use provisional P0–P3 labels and explain risk rather than pretending the labels are standardized. Each finding must identify a precise file/line, reproducible condition, user/system impact, and practical fix. Include only issues with concrete evidence; label uncertainty as a question or follow-up, not a confirmed bug.

## Output

Start with prioritized findings. For each finding include severity, location, failure scenario, impact, and a concise fix direction. Then give a brief scope/check summary and material residual risks. If there are no findings, say so plainly and name any meaningful unreviewed area or check that was not run. Avoid generic praise, style-only opinions, speculative concerns, and duplicate findings.

Use `security-review` for a dedicated threat-focused assessment; this skill still flags clear security defects visible in the diff. Use `python-production` for implementation guidance and `llm-evaluation` when a change alters model, retrieval, or agent quality behavior.
