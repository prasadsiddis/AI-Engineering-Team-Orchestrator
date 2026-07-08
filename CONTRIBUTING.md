# Contributing

This project is intentionally small and auditable. Changes should keep the workflow easy to run without external API keys.

## Workflow Changes

When changing role logic in `src/engineering_team_orchestrator/workflow.py`:

- Keep each role function focused on one responsibility.
- Preserve the final decision labels: `ready`, `revise`, and `block`.
- Update `data/feature_requests.json` if new behavior needs a representative example.
- Update tests when expected decisions change.

## Data Changes

When adding feature requests:

- Include a stable `request_id`.
- Fill all existing fields so the deterministic workflow can evaluate the request.
- Add an `expected_decision` that matches the intended baseline behavior.

## Prompt Changes

Prompt files under `prompts/` are upgrade paths for future LLM-based reviewers. Keep them role-specific, concise, and aligned with the deterministic workflow.

## Verification

Run the test suite before opening or merging changes:

```bash
python -m unittest discover tests
```

For runner-level verification, also run:

```bash
python run_orchestrator.py
```