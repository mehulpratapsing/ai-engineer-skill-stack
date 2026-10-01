# Stack Guide

Choose skills by the decision or artifact required. Start with `break-my-agent` when system context is incomplete; then use only the specialist skills needed for the decision or artifact.

## Suggested workflows

### Early design discovery

`break-my-agent` → `ai-system-design` → the relevant specialist skill(s) → `llm-evaluation` → `security-review` → `code-review`

The interview should ask one question at a time, then hand off a concise system summary, a risk list, and an evaluation plan. It does not certify the design or authorize production testing.

### New AI product or major architecture change

`ai-system-design` → the relevant implementation skill(s) (`rag-engineering`, `agent-engineering`, `mcp-engineering`, `python-production`) → `llm-evaluation` → `security-review` → `code-review`

Start with the architecture skill to define constraints, trust boundaries, measurable quality targets, and ownership. Run evaluation and security review before a production decision.

### RAG feature

`ai-system-design` (when system boundaries or storage choices change) → `rag-engineering` → `python-production` (if Python changes) → `llm-evaluation` → `security-review` → `code-review`

### MCP integration or server

`ai-system-design` (when identity/deployment architecture changes) → `mcp-engineering` → `agent-engineering` (if agents decide when/how to call tools) → `python-production` (if applicable) → `llm-evaluation` → `security-review` → `code-review`

### Agent workflow

`ai-system-design` (for system boundaries) → `agent-engineering` → relevant tool/integration and runtime skills → `llm-evaluation` → `security-review` → `code-review`

### Routine Python change

`python-production` as implementation guidance → `code-review`. Add `security-review` when the change touches identity, sensitive data, untrusted content, network/file/process boundaries, or consequential tools.

## Handoffs

- Architecture records the requirements, constraints, and explicit decisions downstream implementation must preserve.
- Implementation records interfaces, version pins, data flows, and known failure modes for evaluation and security review.
- Evaluation records the tested system/data/config versions and release decision against pre-agreed thresholds.
- Security review reports evidence-based findings and residual coverage limits.
- Code review focuses on defects in the proposed change and identifies checks actually performed.

A skill does not grant permission to access data, call external systems, conduct intrusive security testing, or make production changes. Follow the user's authorization, repository policy, and the target environment's controls.
