import datetime as dt
import unittest
from accountability import assess, digest_lines

NOW = dt.datetime(2026, 10, 12, 1, tzinfo=dt.timezone.utc)
REG = ({"name":"Test","owner":"Agent","next":"Investigate",
        "kind":"issues","number":9,"threshold_hours":24},)

class AccountabilityTests(unittest.TestCase):
    def test_stale(self):
        rows=assess(NOW, {"issues/9":{"state":"open","updated_at":"2026-10-10T23:00:00Z"}},REG)
        self.assertEqual(rows[0]["status"],"STALE")
        self.assertIn("ATTENTION",digest_lines(rows))
    def test_recent_not_claimed_complete(self):
        rows=assess(NOW, {"issues/9":{"state":"open","updated_at":"2026-10-12T00:00:00Z"}},REG)
        self.assertEqual(rows[0]["status"],"OPEN")
        self.assertIn("does NOT certify",digest_lines(rows))
    def test_unknown_fails_closed(self):
        self.assertEqual(assess(NOW,{},REG)[0]["status"],"UNKNOWN")
    def test_closed_record(self):
        rows=assess(NOW, {"issues/9":{"state":"closed","updated_at":"2026-10-12T00:00:00Z"}},REG)
        self.assertEqual(rows[0]["status"],"CLOSED")
    def test_future_timestamp(self):
        rows=assess(NOW, {"issues/9":{"state":"open","updated_at":"2026-10-14T00:00:00Z"}},REG)
        self.assertEqual(rows[0]["status"],"UNKNOWN")

if __name__=="__main__":
    unittest.main()
