---
name: ai-system-design
license: Apache-2.0
description: Design LLM, RAG, and agent systems from business requirements through architecture, security boundaries, evaluation, operations, and rollout. Use when choosing patterns or reviewing an AI system design.
---

# AI System Design

Use this skill for architecture decisions that affect an AI system's behavior, data access, reliability, cost, or deployment. Produce a design that a delivery team can implement and verify.

## Workflow

1. **Frame the use case.** Identify the user and decision or task, inputs and authoritative sources, expected output, error impact, human role, and system boundary. Inspect the repository, existing architecture, runtime and dependency versions, deployment path, and constraints before proposing a design.
2. **Record constraints.** Capture data classification and residency, identity and tenant boundaries, retention/deletion needs, applicable internal controls, latency/availability targets, throughput, quality thresholds, and spend limits. Ask for a missing fact when it changes authorization, privacy, safety, or a high-impact architecture choice. Otherwise state a bounded assumption and its effect.
3. **Choose the smallest pattern that meets the need.** Compare deterministic code, retrieval, model calls, tools, workflow orchestration, and fine-tuning where relevant. Introduce agents or multiple agents only when their planning or delegated work solves a measured requirement. Explain viable alternatives and why the chosen pattern fits.
4. **Design end-to-end.** Map trust boundaries, identities, data flows, persistence, model/provider calls, retrieval, tool permissions, state, caches, and failure paths. Define contracts and ownership between components. Treat model output and retrieved or tool-provided content as untrusted input.
5. **Make quality and operations measurable.** Set a versioned evaluation plan and release thresholds. Specify tracing, service and quality metrics, audit events, alerts, rate limits, cost/token budgets, timeouts, bounded retries, cancellation, fallbacks, rollback, and a kill switch. Redact or omit prompts, retrieved content, credentials, secrets, and confidential, proprietary, restricted, or personal data from telemetry unless approved controls explicitly allow them.
6. **Plan delivery.** Define data/model/prompt/index versioning, migration and deletion behavior, staged rollout, human escalation, ownership, and operational runbooks. Ensure each important requirement has an implementation control and a way to verify it.

## Deliverable

For a substantive design, provide a concise decision record with: scope and assumptions; a context/data-flow diagram; chosen pattern and alternatives; component contracts; identity and trust boundaries; quality, reliability, and cost targets; threat mitigations; observability; rollout and rollback; and unresolved decisions with owners. Keep requirements, assumptions, and recommendations distinguishable. Do not claim compliance or approval without evidence.

Use companion skills when needed: `rag-engineering` for retrieval design, `agent-engineering` for agent loops and state, `mcp-engineering` for MCP integrations, `llm-evaluation` for thresholds and evaluation, `security-review` for adversarial review, and `python-production` for Python implementation.

## Current references

Check current official material when it affects a decision; use the deployed stack's pinned versions and policy as constraints.

When Context7 is configured, use it for focused, version-specific library documentation after inspecting the target's dependency and runtime versions. Verify consequential details against official documentation. Keep credentials, secrets, private source code, and restricted data out of Context7 queries; the integration is optional.

- [NIST AI RMF Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
