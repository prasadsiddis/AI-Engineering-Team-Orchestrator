# AI Engineering Team Orchestrator

A small end-to-end Agentic AI project that simulates an AI-assisted engineering team. It routes product requests through product, engineering, design, QA, and release agents, then produces a traceable build decision.

## Inspiration

This project is inspired by the role-based AI workflow idea in [garrytan/gstack](https://github.com/garrytan/gstack). The code, data, prompts, and project structure here are original and intentionally lightweight so they can run without external API keys.

## Workflow

1. Load feature requests from `data/feature_requests.json`.
2. Run five specialist review agents.
3. Aggregate role signals, recommendations, and risk scores.
4. Decide whether each request is `ready`, `revise`, or `block`.
5. Export `outputs/engineering_team_trace.csv`.

## Run

```bash
pip install -r requirements.txt
python run_orchestrator.py
python -m unittest discover tests
```

## Project Structure

- `src/engineering_team_orchestrator/`: reusable workflow code
- `data/`: sample feature requests
- `configs/`: decision policy configuration
- `prompts/`: prompt template for future LLM-based role reviews
- `tests/`: workflow regression tests

## Documentation

- [Engineering Team Trace Schema](docs/trace-schema.md)
- [Contributing Guide](CONTRIBUTING.md)

## Upgrade Ideas

- Replace deterministic agents with LLM role reviewers.
- Add GitHub issue ingestion and PR readiness scoring.
- Generate markdown release reports for each reviewed request.
- Add human approval gates for high-risk features.