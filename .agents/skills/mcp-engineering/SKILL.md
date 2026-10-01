---
name: mcp-engineering
license: Apache-2.0
description: Design, implement, secure, test, and deploy Model Context Protocol clients and servers, including tools, resources, prompts, authorization, and interoperability.
---

# MCP Engineering

Use this skill for MCP protocol implementations and integrations. MCP standardizes context and capability exchange; it does not replace application authorization, consent, privacy, or operational controls.

## Workflow

1. **Resolve compatibility first.** Inspect the host/client/server, transport, SDK, and protocol revision already in use. Check the matching version of the official specification and SDK migration guidance. Implement only features and extensions supported by both peers. Do not copy examples for another protocol revision or assume session, handshake, transport, or authorization behavior.
2. **Design a narrow capability surface.** Decide whether each capability belongs in a tool (action), resource (context/data), or prompt (reusable template). Keep tools task-specific, bounded, typed, and explicit about side effects. Define input/output schemas, size limits, stable errors, pagination, cancellation, idempotency, and timeouts. Treat tool names, descriptions, annotations, resource content, and model-generated arguments as untrusted; descriptions and annotations are not enforcement controls.
3. **Enforce identity and authorization at the server.** For HTTP transports using MCP authorization, follow the matching protocol authorization requirements and trusted identity-provider configuration; for STDIO and other transports, follow their applicable credential model and security requirements. Validate issuer, audience, expiry, scopes, and resource binding as required by the chosen transport and revision. Authorize every operation against the authenticated principal and tenant at the point of access. Use least-privilege scopes and short-lived credentials. Never forward an incoming token to a downstream service without the required validation and delegation design. Bind opaque task/state handles to the authenticated principal; possession of a handle is not identity.
4. **Harden inputs and egress.** Validate types, lengths, paths, URLs, and resource identifiers on the server. Prevent path traversal, command injection, SQL injection, SSRF, unsafe deserialization, and uncontrolled filesystem/network access. Use parameterized queries, safe process APIs, destination allowlists or controlled egress, and minimal runtime privileges. Require explicit user awareness/authorization for consequential side effects in the host experience.
5. **Instrument without leaking data.** Trace request lifecycle, principal/tenant identifiers that are approved for telemetry, capability name, outcome, latency, rate limits, and dependency failures. Redact tokens, secrets, prompts, retrieved content, and PII by default. Keep audit records protected, access-controlled, and within the approved retention policy.
6. **Verify protocol and security behavior.** Cover matching-version conformance, malformed and oversized payloads, unknown methods/capabilities, authorization failures, cross-tenant access, expired/replayed credentials, malicious resource content, cancellation, timeout, retry/idempotency, and transport failures. Test proxy and OAuth discovery paths for SSRF and token confusion. Load-test using the intended deployment topology. Document supported revisions and deprecations.
7. **Deploy with bounded access.** Pin and track SDK versions, review transitive dependencies, isolate the process, restrict network/filesystem permissions, rotate credentials, and provide health checks, rate controls, alerts, and a rollback plan.

## MCP and A2A boundary

Use MCP for exposing tools and context to an AI host. Consider A2A when independent agent systems need a defined task/exchange protocol. Do not conflate the protocols; verify the official current specification and security model for each integration.

## Current references

Read [protocol and authorization notes](references/protocol-and-authorization.md) for version-sensitive orientation, then verify the target peers against their matching primary specifications and SDK docs. The notes are not a substitute for protocol negotiation or deployment-specific policy.

When Context7 is configured, use it for focused, version-specific SDK documentation after checking the host, server, transport, and protocol versions already in use. Resolve the exact library/version, verify consequential details against the official specification and SDK docs, and keep credentials, secrets, private source code, and restricted data out of queries. Context7 is optional.

- [MCP specifications](https://modelcontextprotocol.io/specification/)
- [MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [A2A specification](https://a2a-protocol.org/latest/specification/)
