import unittest
from datetime import datetime,timezone,timedelta
from jev_shadow import assess
N=datetime.now(timezone.utc)
P={"task_id":"synthetic-001","kind":"task-triage","generated_at":N.isoformat(),"sources":[{"id":"synthetic","observed_at":N.isoformat()}]}
D={"choice":"investigate","probability":0.63,"model":"typesafe-ai/jev"}
class Tests(unittest.TestCase):
 def test_advisory(self):
  r=assess(P,D);self.assertEqual(r["status"],"ADVISORY_ONLY");self.assertFalse(r["standing_authority"])
 def test_missing_evidence(self):self.assertEqual(assess({**P,"sources":[]},D)["status"],"STOP")
 def test_stale(self):self.assertEqual(assess({**P,"generated_at":(N-timedelta(days=2)).isoformat()},D)["status"],"STOP")
 def test_wrong_kind(self):self.assertEqual(assess({**P,"kind":"sign"},D)["status"],"STOP")
 def test_bad_choice(self):self.assertEqual(assess(P,{**D,"choice":"merge"})["status"],"STOP")
 def test_nan(self):self.assertEqual(assess(P,{**D,"probability":float("nan")})["status"],"STOP")
 def test_bool_probability(self):self.assertEqual(assess(P,{**D,"probability":True})["status"],"STOP")
 def test_wrong_model(self):self.assertEqual(assess(P,{**D,"model":"unknown"})["status"],"STOP")
 def test_expanded_schema(self):self.assertEqual(assess({**P,"run":True},D)["status"],"STOP")
 def test_bad_source(self):self.assertEqual(assess({**P,"sources":[{"id":"x"}]},D)["status"],"STOP")
 def test_unhashable_task_kind(self):self.assertEqual(assess({**P,"kind":[]},D)["status"],"STOP")
 def test_unhashable_choice(self):self.assertEqual(assess(P,{**D,"choice":[]})["status"],"STOP")
 def test_invalid_timestamp_type(self):self.assertEqual(assess({**P,"generated_at":[]},D)["status"],"STOP")
 def test_invalid_source_timestamp_type(self):self.assertEqual(assess({**P,"sources":[{"id":"x","observed_at":[]}]},D)["status"],"STOP")
if __name__=="__main__":unittest.main()
