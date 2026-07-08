# Engineering Team Trace Schema

The orchestrator exports `outputs/engineering_team_trace.csv` when `run_engineering_team_orchestrator` is executed. The trace is intended to make each role review auditable and easy to compare across feature requests.

## Columns

| Column | Type | Description |
|---|---|---|
| `request_id` | string | Stable identifier from `data/feature_requests.json`. |
| `title` | string | Human-readable feature request title. |
| `role_signals` | string | Semicolon-delimited role outputs, formatted as `role:signal`. |
| `recommendations` | string | Concatenated role recommendations for implementation, testing, design, and release. |
| `max_risk_score` | integer | Highest risk score assigned by any role. Higher values mean stronger review concern. |
| `decision` | string | Final orchestrator decision: `ready`, `revise`, or `block`. |
| `expected_decision` | string | Expected baseline decision used by tests and sample-data validation. |
| `decision_match` | boolean | Whether the final decision matches the expected decision. |
| `review_count` | integer | Number of role reviews included in the trace. The current workflow expects five. |
| `trace_complete` | boolean | Whether all role reviews and final decision fields were produced. |

## Decision Meanings

- `ready`: the feature is low risk and has a clear implementation/test path.
- `revise`: the feature is promising but needs design, architecture, QA, or rollout changes.
- `block`: the feature has safety, privacy, or production-risk concerns that should stop implementation until reviewed.

## Audit Use

Use the trace to inspect why a request was approved, revised, or blocked. For portfolio review, the most useful fields are `role_signals`, `recommendations`, `max_risk_score`, and `decision`.