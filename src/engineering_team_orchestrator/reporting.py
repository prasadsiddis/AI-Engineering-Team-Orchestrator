"""Markdown reporting helpers for engineering team reviews."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def escape_markdown_table_cell(value: object) -> str:
    """Escape characters that would break a markdown table cell."""
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def build_release_report(trace: pd.DataFrame) -> str:
    ready_count = int((trace["decision"] == "ready").sum())
    revise_count = int((trace["decision"] == "revise").sum())
    block_count = int((trace["decision"] == "block").sum())
    lines = [
        "# Engineering Team Review Report",
        "",
        "## Summary",
        "",
        f"- Ready: {ready_count}",
        f"- Needs revision: {revise_count}",
        f"- Blocked: {block_count}",
        "",
        "## Request Decisions",
        "",
        "| Request | Decision | Max Risk | Matched Expected |",
        "|---|---|---:|---|",
    ]
    for row in trace.to_dict(orient="records"):
        request_label = escape_markdown_table_cell(f"{row['request_id']} - {row['title']}")
        decision = escape_markdown_table_cell(row["decision"])
        decision_match = escape_markdown_table_cell(row["decision_match"])
        lines.append(
            f"| {request_label} | {decision} | "
            f"{row['max_risk_score']} | {decision_match} |"
        )
    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "Use this report as a release-readiness checkpoint before implementation. High-risk or blocked items should receive a human review and a rollback plan.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_release_report(trace: pd.DataFrame, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_release_report(trace), encoding="utf-8")
    return output_path