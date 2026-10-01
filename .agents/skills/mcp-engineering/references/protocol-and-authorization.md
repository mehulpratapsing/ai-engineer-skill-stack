# MCP Protocol and Authorization Notes

Reviewed 2026-09-27 against official sources. The published `2026-07-28` protocol revision includes material compatibility changes, while deployed clients and servers may still implement earlier revisions. Confirm the negotiated protocol, transport, exact SDK versions, and supported features for both peers before applying any note below. Follow the matching official specification and migration guide when they differ from this summary.

## Version and transport compatibility

- Pin and inventory the client, server, transport, and SDK versions. Test the actual deployment path, including proxies and gateways. Do not infer wire behavior from a package name, an example, or another SDK's migration guide.
- In the `2026-07-28` revision, the protocol core is stateless: the `initialize`/`initialized` exchange and `Mcp-Session-Id` transport header are retired. Each request carries protocol/version metadata; `server/discover` is available when a client needs capability discovery but is not required. Older revisions have different behavior, so do not silently apply this profile to a legacy peer.
- For the `2026-07-28` Streamable HTTP revision, `Mcp-Method` and `Mcp-Name` headers are required and support routing; verify they agree with the JSON-RPC body. Routing metadata is not an identity credential, authorization decision, or permission check.
- Deprecation and extension status are versioned. Check the matching specification's deprecation policy and the SDK's release/migration notes before adopting or removing a capability.

## Mid-call input and long-running work

- The `2026-07-28` Multi Round-Trip Requests (MRTR) flow can return `resultType: "input_required"`, including requests the client must surface or satisfy, then retry the original request with `inputResponses` and `requestState`. Treat received request payloads and state as untrusted protocol data; validate shape, bind state to the right request/principal, expire it, and prevent replay or cross-caller reuse.
- If an operation has consequential side effects, require the product's authorized confirmation flow and validate the final action server-side. Never treat model-generated rationale or protocol state as proof of user consent.
- MCP Tasks is a separate extension, not an assumption of core MCP. Its specification page was labelled **Draft** on the review date. Check its current status, exact extension identifier, and support at both peers; use capability negotiation and handle ordinary results as well as task results where the extension requires it. Task handles are sensitive state: authenticate and authorize each read, update, and cancel request, and do not rely on obscurity alone.
- Do not build around deprecated capabilities simply because an old example uses them. Check status in the exact target revision and use a supported alternative where appropriate.

## Authorization and data boundaries

- Treat MCP as a protocol for exchanging context/capabilities, not as the application's authorization system. For HTTP deployments using MCP authorization, implement the matching authorization specification and validate the required issuer, audience/resource binding, expiry, scopes, and other token claims before acting. Do not accept a token intended for another resource or pass an inbound access token through to a downstream service.
- Authorize every tool/resource operation against the authenticated principal and tenant at the point of access, including task lifecycle calls and cached results. Use least privilege; make side effects explicit and bounded. Tools, prompts, annotations, resource text, headers, and model-produced arguments are not trusted policy inputs.
- Treat URLs, redirects, resource identifiers, file paths, and server-provided requests as untrusted. Apply egress controls and SSRF defenses to discovery and fetch paths; validate schemas and sizes; constrain filesystem/process/database access; rate-limit and audit sensitive actions.
- Minimize telemetry. Capability name, outcome, latency, approved correlation identifiers, and security-relevant audit events are often enough. Do not record tokens, credentials, raw prompts, private resource content, or personal data by default. Apply approved access, retention, and deletion controls to necessary audit records.

## Primary references

- [MCP specifications and version index](https://modelcontextprotocol.io/specification/)
- [MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP 2026-07-28 specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [MCP Tasks extension specification](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
- [MCP TypeScript SDK migration guide for 2026-07-28](https://ts.sdk.modelcontextprotocol.io/v2/migration/support-2026-07-28) (SDK-specific; use the matching SDK guide for other implementations.)
