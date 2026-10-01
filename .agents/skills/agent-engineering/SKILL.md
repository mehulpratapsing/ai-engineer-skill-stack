---
name: agent-engineering
license: Apache-2.0
description: Design or improve tool-using AI agents, including planning, routing, orchestration, bounded state, memory, approvals, evaluation, and failure recovery.
---

# Agent Engineering

Use this skill when a system can choose and sequence actions at runtime. First confirm that an agent is warranted for the required variability; use a simpler deterministic workflow when it meets the need with lower risk and operating cost.

## Workflow

1. **Define the contract and authority.** State the user goal, allowed actions, data boundaries, identity, tools, success criteria, failure cases, and which effects require explicit human approval. The model may propose actions; trusted application code must enforce identity, authorization, scope, and policy on every tool call.
2. **Model execution as bounded state.** Define typed states and transitions for plan, action, observation, completion, failure, and interruption. Set use-case-based limits for steps, tool calls, wall time, tokens/spend, concurrency, and retries. Validate tool arguments and results. Use idempotency keys, checkpoints, deduplication, and compensating actions where repeated or partial execution can mutate external state.
3. **Choose orchestration intentionally.** Use routing, hand-offs, parallel work, or multiple agents only where decomposition or specialization yields a measurable benefit. Bound fan-out, isolate permissions and state, define merge/conflict handling, and prevent cycles or uncontrolled delegation. Use MCP for tool/context access; evaluate A2A when independent agent systems need to exchange task work.
4. **Control memory and context.** Define what is ephemeral versus persisted, how it is scoped to a principal/tenant, how it is updated/deleted, and what may be retrieved later. Treat conversation, retrieved documents, tool results, and agent-to-agent messages as untrusted. Do not let memory or model text grant access, change policy, or silently widen scope.
5. **Design interruption and recovery.** Handle user cancellation, timeouts, provider/tool failure, malformed output, partial side effects, and process restart. Persist only the minimum state needed for recovery, protect it with authorization and expiry, and make uncertain outcomes visible rather than silently repeating actions. Provide a safe stop path and human handoff.
6. **Observe the trajectory safely.** Trace decisions, state transitions, tool names, validated outcomes, retries, duration, resource use, and failure categories. Avoid recording raw chain-of-thought, credentials, sensitive prompts, retrieved content, or PII by default. Maintain protected audit events for consequential actions.
7. **Evaluate beyond the final answer.** Create cases for goal completion, tool choice/arguments, policy compliance, step efficiency, side effects, interruption, recovery, and adversarial context. Replay deterministically where possible; compare trajectories and task outcomes against a baseline. Use human review for high-impact outcomes.

## Deliverable

Document the state machine, tool contracts, identity/authorization enforcement, limits, approval points, persistence/expiry, retry and compensation behavior, telemetry, evaluation cases, and failure/stop semantics. For implementation, pair with `python-production`; for connected tools, `mcp-engineering`; for release criteria, `llm-evaluation`; and for adversarial risks, `security-review`.

## Current references

- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [A2A specification](https://a2a-protocol.org/latest/specification/)
- [NIST AI RMF Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)
