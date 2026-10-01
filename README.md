# AI Engineer Skill Stack

A portable, eight-skill engineering workflow for building and reviewing LLM, RAG, MCP, agent, and Python systems. Each skill is an independent `SKILL.md` with concise discovery metadata, an actionable workflow, deliverable expectations, and live primary references where standards evolve.

## Skills

| Skill | Use it for |
|---|---|
| `ai-system-design` | Requirements-to-architecture decisions, trust boundaries, operations, and rollout |
| `rag-engineering` | Authorized ingestion, retrieval, grounding, citations, quality, latency, and cost |
| `mcp-engineering` | MCP clients/servers, tool surfaces, auth, protocol security, and deployment |
| `llm-evaluation` | Golden datasets, judge calibration, metric selection, regression and release gates |
| `python-production` | Typed, secure, observable, maintainable Python services and APIs |
| `agent-engineering` | Bounded agent loops, tools, state, orchestration, interruption, and recovery |
| `security-review` | Evidence-based security review for AI systems and connected applications |
| `code-review` | Focused review of code changes for concrete correctness and maintainability defects |

See [STACK_GUIDE.md](STACK_GUIDE.md) for suggested combinations and handoffs.

## Install

### OpenCode project

Copy the `.agents/` directory from this package into the repository root. OpenCode discovers `.agents/skills/<skill-name>/SKILL.md` for the project. Restart or refresh the agent session if needed and confirm all eight skill IDs appear. OpenCode's skill permission settings can hide or restrict a skill.

### OpenCode global

Copy the eight skill directories into `~/.agents/skills/` (on Windows, typically `%USERPROFILE%\.agents\skills\`). Check for existing IDs first; merge deliberately to preserve local modifications.

### Codex global

Copy the eight skill directories into `$CODEX_HOME/skills/` (typically `%USERPROFILE%\.codex\skills\` on Windows). Check for existing IDs first and merge deliberately. `agents/openai.yaml` supplies Codex-facing UI metadata; `SKILL.md` remains the portable source of instructions.

The package is a ready-to-copy skill set; it has not been installed into a user profile or a target repository.

## Enterprise adoption boundary

This is a reusable engineering baseline, not an organization policy, security approval, legal opinion, or compliance certification. Organization-specific rules were not supplied, so the skills do not invent approved model/provider lists, data classifications, retention periods, residency rules, spend thresholds, evaluation cutoffs, or release authorities. Before use in a governed environment, connect the stack to applicable internal policies and approved environments. Put project-specific requirements in the repository's governed instructions/policy files and resolve any conflict with the responsible owner. The skills direct the agent to state assumptions and seek an authoritative answer where a missing control changes the design or authorization decision.

## Maintenance

Standards, protocol revisions, SDK APIs, model capabilities, and security taxonomies change. The skills direct users to current official sources and the versions pinned by the target repository. Recheck those sources when adopting or updating the package; do not treat the package's review date as proof of continuing currency.

Primary sources checked on 2026-09-27 include:

- [OpenCode Agent Skills](https://opencode.ai/docs/skills)
- [Model Context Protocol specifications](https://modelcontextprotocol.io/specification/)
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [A2A specification](https://a2a-protocol.org/latest/specification/)
- [NIST AI RMF Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Python documentation](https://docs.python.org/3/)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)

The RAG and MCP skills include focused companion references for metric interpretation and version-sensitive protocol/security decisions. Treat those as review notes, then verify the linked primary documentation and target SDK versions before implementation.
