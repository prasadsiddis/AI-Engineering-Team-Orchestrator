# Workflow Design Notes

## Goal

The orchestrator is designed as a transparent baseline for AI-assisted engineering review. It does not try to replace human judgment. Instead, it makes the review process explicit enough to inspect, test, and improve.

## Agent Roles

| Role | Responsibility | Example Output |
|---|---|---|
| Product agent | Checks user value and success clarity | `clear_user_value` |
| Engineering agent | Checks architecture and implementation risk | `implementation_path_clear` |
| Design agent | Checks user-facing workflow and visibility | `user_flow_visible` |
| QA agent | Checks testability and failure coverage | `test_plan_clear` |
| Release agent | Checks rollout, rollback, and safety readiness | `release_ready` |

## Decision Policy

- `ready`: risk is low and testability is clear.
- `revise`: the feature is promising but needs a design, test, or rollout revision.
- `block`: safety, privacy, or irreversible production risk is too high.

## Future Integrations

- GitHub Issues: load feature requests directly from issue labels and body text.
- Pull Requests: attach release-readiness reports to PR comments.
- LLM Reviewers: replace deterministic role functions with prompt-driven reviewers.
- Human Approval: require manual signoff before high-risk release decisions.