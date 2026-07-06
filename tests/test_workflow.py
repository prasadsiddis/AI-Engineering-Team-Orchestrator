from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.engineering_team_orchestrator import run_engineering_team_orchestrator


class EngineeringTeamWorkflowTests(unittest.TestCase):
    def test_orchestrator_matches_expected_decisions(self):
        trace = run_engineering_team_orchestrator(REPO_ROOT)

        self.assertEqual(len(trace), 4)
        self.assertTrue(trace["decision_match"].all())
        self.assertTrue(trace["trace_complete"].all())
        self.assertGreaterEqual(trace["review_count"].min(), 5)


if __name__ == "__main__":
    unittest.main()