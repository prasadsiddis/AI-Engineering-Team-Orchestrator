from pathlib import Path

from src.engineering_team_orchestrator import run_engineering_team_orchestrator


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    trace = run_engineering_team_orchestrator(repo_root)
    print(trace[["request_id", "decision", "max_risk_score", "decision_match"]].to_string(index=False))