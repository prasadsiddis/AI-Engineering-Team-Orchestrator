import argparse
from pathlib import Path

from src.engineering_team_orchestrator import run_engineering_team_orchestrator, write_release_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the engineering team review workflow.")
    parser.add_argument(
        "--report-path",
        type=Path,
        default=None,
        help="Optional markdown report path. Defaults to outputs/engineering_team_report.md.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    trace = run_engineering_team_orchestrator(repo_root)
    print(trace[["request_id", "decision", "max_risk_score", "decision_match"]].to_string(index=False))
    report_path = args.report_path or repo_root / "outputs" / "engineering_team_report.md"
    report_path = write_release_report(trace, report_path)
    print(f"Release report written to {report_path}")