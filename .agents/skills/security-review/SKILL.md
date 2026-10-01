---
name: security-review
license: Apache-2.0
description: Conduct evidence-based security reviews of LLM, RAG, agent, MCP, and conventional application code or architecture, prioritizing exploitable risks and actionable fixes.
---

# Security Review

Use this skill for a focused security assessment of code, configuration, architecture, or a proposed AI integration. Establish the authorized review scope and inspect the actual implementation and surrounding trust boundaries. A checklist is a way to find evidence, not proof that a control exists.

## Review workflow

1. **Map the attack surface.** Identify assets, data classifications, principals, trust boundaries, entry points, model/provider calls, retrieval sources, tools, MCP/A2A connections, persistence/memory, secrets, and egress. Trace how attacker-controlled input can influence data access, code paths, model instructions, or side effects.
2. **Verify conventional application controls.** Check authentication and per-object authorization; tenant isolation; least privilege; secret handling; input validation; SQL/command injection; path traversal; SSRF and egress; unsafe deserialization; file upload; CSRF/CORS where relevant; dependency/build supply chain; rate/resource limits; error handling; and sensitive logging/retention.
3. **Check AI-specific paths.** Look for direct and indirect prompt injection through user input, retrieved content, files, images, and tool results; unsafe model output use; sensitive-data disclosure; retrieval ACL bypass; poisoned sources or memory; over-broad tool scope; identity/privilege confusion; unsafe delegation; unverified tool or agent metadata; weak human approval; uncontrolled loops/cost; and lack of auditability. Model instructions and output filters do not replace server-side controls.
4. **Prove the finding safely.** Follow data and control flow to a concrete vulnerable sink or missing enforcement. State prerequisites and impact. Validate only with read-only inspection or tests in an explicitly authorized, isolated environment. Do not probe production or extract/display real secrets or personal data. Redact sensitive values in all notes.
5. **Prioritize and recommend.** Follow the organization's severity rubric. If none is supplied, label a provisional severity and explain the impact/preconditions; avoid false precision. Recommend the smallest durable fix and a regression check. Distinguish confirmed findings, plausible risks requiring evidence, and controls that could not be assessed.

## Finding format

For each confirmed issue provide: severity; file and line or precise architecture location; affected asset/boundary; concrete attack or failure path; prerequisites; business/security impact; evidence; and actionable remediation. Order by risk. Cite only evidence visible in scope. Do not report generic checklist entries as vulnerabilities. If none are found, state what was reviewed and material coverage limits.

Keep the review read-only unless the user separately requests remediation. Pair with `code-review` for general change correctness and `mcp-engineering`, `rag-engineering`, or `agent-engineering` for implementation-specific workflows.

## Optional dynamic testing

Use Strix only when the user explicitly authorizes a defined active-testing scope. Before a run, confirm target ownership, in-scope assets and actions, environment, credentials, data handling, resource limits, and stop conditions. Prefer staging; use a clean disposable checkout for local source targets because the tool may modify them. Strix sends real exploit payloads and can change target data. Do not test production or third-party assets without explicit authorization, and use hosted mode only when the target/source data may be sent to the service under applicable policy. Manually validate and redact findings; do not apply fixes automatically. If authorization or scope is missing, keep the review read-only.

## Current references

Check the latest applicable editions and the organization's control mapping; Top 10 lists are guidance, not assurance.

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [NIST AI RMF Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)
- [Strix application security testing workflow](https://github.com/usestrix/strix/blob/main/skills/application-security-testing/SKILL.md)
