import importlib.util
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'case-studies/001-llm-judge-reliability/experiment.py'
spec=importlib.util.spec_from_file_location('case001_experiment',P)
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
class TestCase001(unittest.TestCase):
    def setUp(self):
        self.cases=json.loads((P.parent/'test_cases.json').read_text())
    def test_unbiased_oracle(self):
        r=mod.evaluate(self.cases,mod.JudgeConfig())
        self.assertEqual(r['accuracy_ab'],1.0)
        self.assertEqual(r['order_swap_inconsistency_rate'],0.0)
    def test_position_bias_detectable(self):
        r=mod.evaluate(self.cases,mod.JudgeConfig(first_position_bonus=1.2))
        self.assertGreater(r['order_swap_inconsistency_rate'],0)
    def test_verbosity_bias_detectable(self):
        r=mod.evaluate(self.cases,mod.JudgeConfig(per_word_bonus=0.14))
        self.assertGreater(r['incorrect_approval_rate_ab'],0)
    def test_critical_case_metric(self):
        r=mod.evaluate(self.cases,mod.JudgeConfig(per_word_bonus=0.14))
        self.assertEqual(r['critical_case_count'],4)
        self.assertIsNotNone(r['critical_incorrect_approval_rate_ab'])
    def test_dataset_validity(self):
        self.assertEqual(len({x['id'] for x in self.cases}),len(self.cases))
        for x in self.cases:
            self.assertEqual({z['id'] for z in x['responses']},{'safe','unsafe'})
            self.assertIn(x['expert_preferred_id'],{z['id'] for z in x['responses']})
    def test_empty_data_fails(self):
        with self.assertRaises(ValueError):mod.evaluate([],mod.JudgeConfig())
if __name__=='__main__':unittest.main()
