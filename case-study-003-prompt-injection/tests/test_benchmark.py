import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('benchmark003',ROOT/'benchmark.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
class BenchmarkTests(unittest.TestCase):
    def setUp(self): self.cases=b.load_cases(ROOT/'data/cases.json')
    def test_fixture_balance(self):
        self.assertEqual(len(self.cases),36)
        self.assertEqual(sum(c['kind']=='attack' for c in self.cases),24)
        self.assertEqual(len({c['pair_id'] for c in self.cases}),6)
    def test_duplicate_and_bad_label_rejected(self):
        for cases in [[],self.cases+[self.cases[0]], [dict(c,kind='unknown') for c in self.cases], [dict(c,expected='wrong') for c in self.cases]]:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'x.json';p.write_text(json.dumps(cases))
                with self.assertRaises(ValueError): b.load_cases(p)
    def test_scoring_independent_known_outputs(self):
        outputs={c['id']:c['expected'] for c in self.cases}
        attack=next(c for c in self.cases if c['kind']=='attack')
        outputs[attack['id']]='prefix '+attack['marker']+' suffix'
        result=b.score(self.cases,outputs)
        self.assertEqual(result['attack']['marker_emissions'],1)
        self.assertEqual(result['overall']['task_successes'],35)
    def test_missing_response_rejected(self):
        with self.assertRaises(ValueError): b.score(self.cases,{})
    def test_keyword_false_positive_and_bypass(self):
        quote=next(c for c in self.cases if c['family']=='quoted_trigger')
        bypass=next(c for c in self.cases if c['family']=='obfuscated')
        self.assertEqual(b.simulate(quote,'keyword_filter'),'BLOCKED')
        self.assertEqual(b.simulate(bypass,'keyword_filter'),bypass['marker'])
    def test_real_bundle_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bundle.json';p.write_text(json.dumps({'metadata':{},'responses':[]}))
            with self.assertRaises(ValueError):b.empirical(p,self.cases)
    def test_published_results_reproduce(self):
        saved=json.loads((ROOT/'results/simulation.json').read_text())
        self.assertEqual(saved['dataset_sha256'],b.digest(ROOT/'data/cases.json'))
        self.assertEqual(saved['harness_sha256'],b.digest(ROOT/'benchmark.py'))
        for policy,result in saved['policies'].items():
            self.assertEqual(result,b.score(self.cases,{c['id']:b.simulate(c,policy) for c in self.cases}))
if __name__=='__main__':unittest.main()
