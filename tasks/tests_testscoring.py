from django.test import TestCase, Client
from .scoring import calculate_task_score, detect_cycles
import json
from datetime import date, timedelta


class ScoringTests(TestCase):
    def test_detect_cycles(self):
        tasks = [
            {"id": "a", "dependencies": ["b"]},
            {"id": "b", "dependencies": ["c"]},
            {"id": "c", "dependencies": ["a"]},
        ]
        cycles = detect_cycles(tasks)
        self.assertEqual(set(["a", "b", "c"]), set(cycles))

    def test_calculate_score_overdue_and_quick_win(self):
        t = {
            "id": "x",
            "due_date": (date.today() - timedelta(days=2)).isoformat(),
            "importance": 7,
            "estimated_hours": 1,
            "dependencies": [],
        }
        out = calculate_task_score(t)
        self.assertTrue(out["score"] > 0)
        self.assertIn("Overdue", out["explanation"] or "")

    def test_defaults_on_missing_fields(self):
        t = {"id": "y"}  # missing keys
        out = calculate_task_score(t)
        self.assertIn("No due date", out["explanation"])
        # importance default -> 5 used internally, so score contains 25 contribution
        self.assertTrue(out["meta"]["importance"] >= 0)


class ViewsIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_analyze_endpoint_returns_sorted_list(self):
        payload = [
            {
                "title": "T1",
                "due_date": None,
                "importance": 1,
                "estimated_hours": 1,
                "dependencies": [],
            },
            {
                "title": "T2",
                "due_date": None,
                "importance": 10,
                "estimated_hours": 1,
                "dependencies": [],
            },
        ]
        resp = self.client.post(
            "/api/tasks/analyze/", json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIsInstance(data, list)
        # T2 (importance 10) should score higher than T1 (importance 1)
        self.assertGreaterEqual(data[0]["score"], data[1]["score"])
