"""AI engineering team orchestrator baseline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class RoleReview:
    role: str
    signal: str
    risk_score: int
    recommendation: str


def load_feature_requests(project_dir: Path) -> list[dict]:
    with (project_dir / "data" / "feature_requests.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def product_agent(request: dict) -> RoleReview:
    if request["user_value"] == "high":
        return RoleReview("product_agent", "clear_user_value", 1, "Proceed with scoped requirements.")
    return RoleReview("product_agent", "needs_value_clarification", 2, "Clarify user value and success metrics.")


def engineering_agent(request: dict) -> RoleReview:
    if request["complexity"] == "high" and request["data_sensitivity"] == "high":
        return RoleReview("engineering_agent", "unsafe_architecture_risk", 4, "Require human approval and rollback design before implementation.")
    if request["complexity"] == "high":
        return RoleReview("engineering_agent", "architecture_needs_design_doc", 3, "Write a technical design and compare provider/runtime tradeoffs.")
    return RoleReview("engineering_agent", "implementation_path_clear", 1, "Build behind a small feature flag.")


def design_agent(request: dict) -> RoleReview:
    if request["ui_surface"] in {"dashboard", "settings"}:
        return RoleReview("design_agent", "user_flow_visible", 1, "Add clear states, owner notes, and reversible actions.")
    return RoleReview("design_agent", "limited_user_visibility", 2, "Add operational status and audit visibility.")


def qa_agent(request: dict) -> RoleReview:
    if request["testability"] == "low":
        return RoleReview("qa_agent", "insufficient_test_strategy", 3, "Define acceptance tests, regression coverage, and measurable checks.")
    if request["testability"] == "medium":
        return RoleReview("qa_agent", "needs_edge_case_tests", 2, "Add simulation tests and dry-run mode.")
    return RoleReview("qa_agent", "test_plan_clear", 1, "Cover core workflow, export behavior, and failure states.")


def release_agent(request: dict, reviews: list[RoleReview]) -> RoleReview:
    max_risk = max(review.risk_score for review in reviews)
    if request["data_sensitivity"] == "high" and max_risk >= 4:
        return RoleReview("release_agent", "release_blocked", 4, "Block release until safety review, audit log, and manual approval exist.")
    if max_risk >= 3:
        return RoleReview("release_agent", "release_needs_revision", 3, "Revise scope and add staged rollout criteria.")
    return RoleReview("release_agent", "release_ready", 1, "Release behind monitoring and rollback plan.")


def decide(reviews: list[RoleReview]) -> str:
    max_risk = max(review.risk_score for review in reviews)
    signals = {review.signal for review in reviews}
    if "release_blocked" in signals or max_risk >= 4:
        return "block"
    if max_risk >= 3 or "insufficient_test_strategy" in signals:
        return "revise"
    return "ready"


def run_engineering_team_orchestrator(project_dir: Path) -> pd.DataFrame:
    requests = load_feature_requests(project_dir)
    rows = []

    for request in requests:
        reviews = [
            product_agent(request),
            engineering_agent(request),
            design_agent(request),
            qa_agent(request),
        ]
        reviews.append(release_agent(request, reviews))
        final_decision = decide(reviews)
        rows.append(
            {
                "request_id": request["request_id"],
                "title": request["title"],
                "role_signals": ";".join(f"{review.role}:{review.signal}" for review in reviews),
                "recommendations": " | ".join(f"{review.role}: {review.recommendation}" for review in reviews),
                "max_risk_score": max(review.risk_score for review in reviews),
                "decision": final_decision,
                "expected_decision": request["expected_decision"],
                "decision_match": final_decision == request["expected_decision"],
                "review_count": len(reviews),
                "trace_complete": len(reviews) == 5 and bool(final_decision),
            }
        )

    trace = pd.DataFrame(rows)
    output_dir = project_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    trace.to_csv(output_dir / "engineering_team_trace.csv", index=False)
    return trace