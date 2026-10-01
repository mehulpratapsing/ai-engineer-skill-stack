# Contributing

Contributions are welcome when they make a skill more useful, accurate, or easier to adopt without turning the stack into a generic checklist.

## Before opening a pull request

- For a larger change, open an issue first and describe the use case and the skill it affects.
- Keep the eight specialist skills and the focused front-door interview skill unless a concrete workflow cannot fit an existing skill.
- Preserve the distinction between general engineering guidance and organization-specific policy. Do not add client or employer names, internal policies, secrets, or confidential examples.
- For version-sensitive advice, link primary documentation, name the applicable version when known, and explain what the guidance changes. Avoid copying large sections of upstream documentation.
- Keep optional integrations optional. A skill must still work when an external MCP server or security tool is unavailable.
- For security guidance, state the authorization boundary and distinguish code review from active testing.

## Validate changes

Review tracked primary references, refresh the file checksums, then run the packaging validator:

```sh
python scripts/update_manifest.py
python scripts/validate_stack.py
python scripts/check_sources.py --check
```

The source monitor compares normalized source text with `references/monitored-sources.lock.json`. If an upstream source changed, inspect the linked material and update any affected guidance first. Refresh the baseline only after review with `python scripts/check_sources.py --update-baseline`. The scheduled workflow opens one review issue on drift and never rewrites the baseline.

When preparing a new release, set the package version with `python scripts/update_manifest.py --version X.Y.Z` before validation.

If you changed installer behavior, smoke-test the relevant installer in a disposable project directory and confirm it skips an existing skill directory without overwriting it. Do not test against a profile containing valuable local skill changes.

For a demo or evaluation claim, use the same input and prompt in both conditions. If you report empirical results, record the model and version, system instructions, tool configuration, run count, scoring rubric, and limitations. Hand-written examples must be labeled as illustrative, not presented as measured model output.

For the interview skill, ask exactly one question per turn and make the final handoff, assumptions, risk list, and evaluation plan explicit.

## Pull request checklist

- [ ] Explain the user problem and the affected skill(s).
- [ ] Link primary sources for version-sensitive claims.
- [ ] Confirm examples contain no sensitive or proprietary data.
- [ ] Run `python scripts/validate_stack.py` and `python scripts/check_sources.py --check`; report the results.
- [ ] Describe checks actually performed; do not claim unrun checks.

## Good first issues

Look for issues labeled `good first issue`. Keep first contributions small and coordinate in the issue before starting work.
