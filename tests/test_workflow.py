from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.engineering_team_orchestrator import build_release_report, run_engineering_team_orchestrator


class EngineeringTeamWorkflowTests(unittest.TestCase):
    def test_orchestrator_matches_expected_decisions(self):
        trace = run_engineering_team_orchestrator(REPO_ROOT)

        self.assertEqual(len(trace), 4)
        self.assertTrue(trace["decision_match"].all())
        self.assertTrue(trace["trace_complete"].all())
        self.assertGreaterEqual(trace["review_count"].min(), 5)

    def test_release_report_summarizes_decisions(self):
        trace = run_engineering_team_orchestrator(REPO_ROOT)
        report = build_release_report(trace)

        self.assertIn("Engineering Team Review Report", report)
        self.assertIn("Ready: 2", report)
        self.assertIn("Needs revision: 1", report)
        self.assertIn("Blocked: 1", report)

    def test_release_report_escapes_markdown_table_cells(self):
        trace = run_engineering_team_orchestrator(REPO_ROOT)
        trace.loc[0, "title"] = "Review data | export"

        report = build_release_report(trace)

        self.assertIn("FR1 - Review data \\| export", report)

if __name__ == "__main__":
    unittest.main()