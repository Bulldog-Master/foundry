import datetime as dt
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))
spec = importlib.util.spec_from_file_location("digest", Path(__file__).with_name("digest.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

now = dt.datetime(2026, 10, 11, 20, 0, tzinfo=dt.timezone.utc)


class Response:
    def __init__(self, value):
        self.data = io.BytesIO(json.dumps(value).encode())
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def read(self, *args): return self.data.read(*args)


def fetch(request, timeout):
    path = request.full_url
    if "/commits?" in path:
        return Response([{"commit": {"committer": {"date": "2026-10-11T18:00:00Z"}}}])
    if "/issues?" in path:
        return Response([
            {"number": 29, "state": "open", "updated_at": "2026-10-11T18:00:00Z"},
            {"number": 28, "state": "open", "pull_request": {},
             "updated_at": "2026-10-11T18:00:00Z"}])
    if "/pulls/30/reviews?" in path:
        return Response([{"state": "APPROVED", "submitted_at": "2026-10-11T19:00:00Z"}])
    if "/pulls?" in path:
        return Response([{"number": 30, "state": "open", "draft": True,
                          "updated_at": "2026-10-11T18:00:00Z", "merged_at": None}])
    raise ValueError("unexpected URL")


class DigestTests(unittest.TestCase):
    def test_daily_bounds(self):
        a, b = m.period("daily", now)
        self.assertEqual(b - a, dt.timedelta(hours=24))

    def test_weekly_bounds(self):
        a, b = m.period("weekly", now)
        self.assertEqual(b - a, dt.timedelta(days=7))

    def test_previous_calendar_month(self):
        a, b = m.period("monthly", now)
        self.assertEqual((a.year, a.month, a.day), (2026, 9, 1))
        self.assertEqual((b.year, b.month, b.day), (2026, 10, 1))

    def test_no_issue_pr_double_count(self):
        a, b = m.period("daily", now)
        c, i, p = m.gather(a, b, fetch)
        self.assertEqual((len(c), len(i), len(p)), (1, 1, 1))

    def test_summary_explicit_coverage(self):
        value = m.run("daily", now, fetch)
        self.assertIn("Host/agent/evaluator activity not yet connected", value)
        self.assertIn("Submitted reviews: 1", value)
        self.assertIn("Review APPROVED on PR #30", value)
        self.assertIn("pull/30", value)
        self.assertIn("issues/29", value)
        self.assertIn("Commits: 1", value)

    def test_month_excludes_outside_window(self):
        a, b = m.period("monthly", now)
        c, i, p = m.gather(a, b, fetch)
        self.assertEqual((len(c), len(i), len(p)), (0, 0, 0))

    def test_actual_merge_events(self):
        start, end = m.period("daily", now)
        pr = {"number": 28, "state": "closed", "draft": False,
              "merged_at": "2026-10-11T19:00:00Z",
              "updated_at": "2026-10-11T19:00:00Z"}
        msg = m.summary("daily", start, end, [], [], [pr], [])
        self.assertIn("Merged: 1", msg)
        self.assertIn("MERGED PR #28", msg)

    def test_daily_progress_and_inactivity(self):
        start, end = m.period("daily", now)
        report = m.summary("daily", start, end, [], [], [], [])
        self.assertIn("Progress & blockers:", report)
        self.assertIn("No new activity evidenced", report)
        self.assertIn("Blocker status not fully verified", report)

    def test_daily_review_flags_not_called_all_clear(self):
        start, end = m.period("daily", now)
        report = m.summary("daily", start, end, [], [], [], [(30, "CHANGES_REQUESTED", "2026-10-11T19:00:00Z")])
        self.assertIn("Review flags: 1", report)

    def test_weekly_has_no_daily_progress_claim(self):
        start, end = m.period("weekly", now)
        report = m.summary("weekly", start, end, [], [], [], [])
        self.assertNotIn("Progress & blockers:", report)

    def test_bad_response_fails_closed(self):
        with self.assertRaises(ValueError):
            m.api_page("commits", 1, lambda *args, **kw: Response({"error": "limited"}))


if __name__ == "__main__":
    unittest.main()
