# AI Engineer Skill Stack

![AI Engineer Skill Stack social preview](assets/social-preview.png)

**Coding agents often give generic or stale advice on RAG, MCP, agents, and LLM evaluation. This stack gives them focused workflows for version-aware design, implementation, evaluation, and security review.**

Eight portable skills, each centered on a reusable `SKILL.md` workflow. They help the agent inspect the actual project, use evidence, check the target's versions, and report concrete decisions and risks. They are guidance, not a guarantee of correctness or a substitute for project policy.

## What is included

| Skill | Use it for |
|---|---|
| `ai-system-design` | Requirements-to-architecture decisions, trust boundaries, operations, and rollout |
| `rag-engineering` | Authorized ingestion, retrieval, grounding, citations, quality, latency, and cost |
| `mcp-engineering` | MCP clients/servers, tools, resources, authorization, security, and deployment |
| `llm-evaluation` | Golden datasets, judge calibration, metrics, regression tests, and release gates |
| `python-production` | Typed, secure, observable Python services and APIs |
| `agent-engineering` | Bounded agent loops, tool use, state, orchestration, interruption, and recovery |
| `security-review` | Evidence-based security review of AI systems and connected applications |
| `code-review` | Focused review for concrete correctness, security, compatibility, and maintainability defects |

See [STACK_GUIDE.md](STACK_GUIDE.md) for combinations and handoffs.

## See the difference

The [RAG review example](examples/rag-review/README.md) uses the same small pipeline and the same prompt, `review this RAG pipeline`, to show a generic review beside a skill-guided review. The second example ties findings to code, conditions severity on actual data boundaries, and proposes checks for authorization, injection, logging, citations, and abstention.

The outputs are hand-written illustrations of the stack's intended review shape, not recorded model runs or a benchmark. Model behavior depends on the model, version, surrounding instructions, tools, and task. For a measured comparison, run both conditions with the same model and configuration on a representative blinded set and score against a pre-agreed rubric.

## Install

Clone the repository, then run the installer for the agent and scope you want. The installer copies missing skill directories and skips existing IDs so local skill edits are not overwritten.

One-line global install from macOS/Linux (replace the final `codex` target with `opencode` or `claude` if needed):

```sh
git clone --depth 1 https://github.com/mehulpratapsing/ai-engineer-skill-stack.git ai-engineer-skill-stack && ./ai-engineer-skill-stack/scripts/install.sh codex --global
```

On Windows, use PowerShell:

```powershell
git clone --depth 1 https://github.com/mehulpratapsing/ai-engineer-skill-stack.git ai-engineer-skill-stack; if ($LASTEXITCODE -eq 0) { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ai-engineer-skill-stack\scripts\install.ps1 -Target codex -Scope global }
```

### OpenCode

Project install (run from the target repository root):

```sh
/path/to/ai-engineer-skill-stack/scripts/install.sh opencode --project
```

Global install:

```sh
/path/to/ai-engineer-skill-stack/scripts/install.sh opencode --global
```

OpenCode uses `.agents/skills` for project skills and supports `~/.agents/skills` globally.

### Codex

Project install uses `.agents/skills`:

```sh
/path/to/ai-engineer-skill-stack/scripts/install.sh codex --project
```

Global install uses `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset:

```sh
/path/to/ai-engineer-skill-stack/scripts/install.sh codex --global
```

### Claude Code

The skill content follows the open Agent Skills format. Other compatible agents may load it from their documented skill directories; installation guidance here covers OpenCode, Codex, and Claude Code.

Claude Code supports the Agent Skills format. Project skills live in `.claude/skills`; personal skills live in `~/.claude/skills`.

```sh
/path/to/ai-engineer-skill-stack/scripts/install.sh claude --project
/path/to/ai-engineer-skill-stack/scripts/install.sh claude --global
```

On Windows, use PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\path\to\ai-engineer-skill-stack\scripts\install.ps1 -Target claude -Scope global
```

Replace `claude` with `opencode` or `codex` as needed. Use `-Scope Project` for a project install. For a project install, run the command with the target repository as the current directory. The package keeps its portable source under `.agents/skills`; the installer maps it to each tool's documented discovery path. Codex-only `agents/openai.yaml` files supply UI metadata and are ignored by other tools.

To install without a script, copy the skill folders from `.agents/skills/` into the destination above. Review skill files before installing them. If a target already has a skill with the same ID, the installer skips it and reports the destination; compare or merge changes deliberately.

### Verify an installation

Restart or refresh the agent session, ask it to list available skills, and invoke one relevant skill explicitly. Tool configuration, the active working directory, or managed policy may affect discovery; consult the agent's docs if a skill is missing.

## Optional tool integrations

- **Context7:** When its MCP server is configured, use it for focused, version-specific library documentation in architecture and implementation work. Match the library and version to the repository's dependency files, verify important details against official documentation, and keep secrets, private source code, and restricted data out of queries. Context7 is optional; use official sources when it is unavailable. See [Context7 documentation](https://context7.com/docs/overview).
- **Strix:** The `security-review` skill may use Strix for dynamic testing only when the user explicitly authorizes a defined scope. Confirm target ownership, allowed actions, environment, data handling, and resource limits first; prefer staging or a disposable checkout. Strix can send exploit payloads and change target data. Review the [official Strix testing workflow](https://github.com/usestrix/strix/blob/main/skills/application-security-testing/SKILL.md) before use. Strix is optional and does not make a skill invocation permission to scan.

## Enterprise adoption boundary

This is a reusable engineering baseline, not an organization policy, security approval, legal opinion, or compliance certification. Organization-specific rules were not supplied, so the skills do not invent approved model/provider lists, data classifications, retention periods, residency rules, spend thresholds, evaluation cutoffs, or release authorities. Before use in a governed environment, connect the stack to applicable internal policies and approved environments. Put project-specific requirements in the repository's governed instruction and policy files and resolve conflicts with the responsible owner.

A skill does not grant permission to access data, call external systems, conduct intrusive security testing, or make production changes. Follow the user's authorization, repository policy, and target environment's controls.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for scope, source, review, and validation expectations. Good first issues are labeled in the [issue tracker](https://github.com/mehulpratapsing/ai-engineer-skill-stack/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

## References and maintenance

Standards, protocol revisions, SDK APIs, model capabilities, and security taxonomies change. Verify the target repository's pinned versions and primary documentation before implementation. The focused references in the RAG and MCP skills are orientation, not substitutes for those checks.

Sources for skill and installation format checked on 2026-10-02:

- [Agent Skills open specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills)
- [Codex skills documentation](https://github.com/openai/codex/blob/main/docs/skills.md)
- [Context7 documentation](https://context7.com/docs/overview)
- [Strix application security testing workflow](https://github.com/usestrix/strix/blob/main/skills/application-security-testing/SKILL.md)

Core technical references were last recorded as reviewed on 2026-09-27; installation and optional integration details were checked on 2026-10-02. Recheck live sources before relying on them for a consequential design or release.

## License

This project is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
