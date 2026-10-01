---
name: python-production
description: Build or harden production Python services, APIs, workers, and AI integrations with project-aligned typing, validation, async behavior, security, observability, and operational controls.
---

# Python Production

Use this skill when implementing or changing Python services, APIs, workers, or production integrations. Follow the target repository's supported Python and dependency versions and established conventions.

## Workflow

1. **Inspect before changing.** Read the project instructions, `pyproject.toml` or equivalent, lockfile, supported Python versions, architecture, lint/type/test commands, and adjacent code. Confirm the framework and deployment model already in use. Do not introduce a framework or dependency without a concrete need.
2. **Make boundaries explicit.** Use type annotations on public and cross-module interfaces. Validate untrusted HTTP, queue, file, and model/tool inputs at the boundary with the project's schema mechanism (Pydantic where appropriate); keep internal domain types and validation rules clear. Treat model output as untrusted and validate before using it in control flow or side effects.
3. **Keep configuration and dependencies controlled.** Use typed, validated configuration and the approved secret manager/environment path. Never commit secrets, log them, or use defaults that silently weaken production security. Inject network, model, storage, clock, and other external dependencies at clear boundaries where that improves control and testing.
4. **Handle concurrency and failure deliberately.** Use `async` only along genuinely asynchronous paths. Bound concurrency, request sizes, queue growth, and timeouts; propagate cancellation and clean up resources. Retry only transient failures and only when the operation is safe to repeat or protected by idempotency. Translate expected failures into stable domain/API errors; preserve diagnostic context in protected logs without exposing internals to clients.
5. **Apply security at each boundary.** Authenticate and authorize every protected operation. Use parameterized queries and safe process APIs; validate paths and URLs; limit outbound network access; protect file uploads and deserialization; use least privilege. Avoid broad exception handling that converts security or data-integrity failures into success-shaped responses.
6. **Make the service operable.** Add structured logs, request/trace correlation, relevant metrics, health/readiness behavior, and alerts according to project conventions. Redact secrets, credentials, prompts, retrieved text, and confidential, proprietary, restricted, or personal data by default. Set retention and access according to approved policy. For AI calls, record model/version, latency, usage, and outcome only to the extent permitted and useful.
7. **Verify proportionately.** Use the repository's formatter, linter, type checker, and focused tests when requested or required by the delivery workflow. Cover boundary validation, authorization, failure/cancellation, and idempotency cases affected by the change. Report the exact checks run and any not run; never claim a check passed without its result.

## Output

Summarize the behavior changed, key contracts and operational/security choices, dependency changes, checks and outcomes, and any deployment/configuration steps. Keep implementation aligned with existing project patterns unless a concrete defect justifies a change.

## Current references

Confirm APIs and migration notes against the installed version before coding.

- [Python documentation](https://docs.python.org/3/)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
