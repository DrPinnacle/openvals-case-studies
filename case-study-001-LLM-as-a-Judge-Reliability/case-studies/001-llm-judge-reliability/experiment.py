"""Synthetic pairwise judging experiment; Python standard library only.

Quality is an oracle annotation supplied in the synthetic dataset. It is NOT
inferred by a model. This script intentionally simulates biases for education.
"""
import argparse
import json
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent

@dataclass(frozen=True)
class JudgeConfig:
    first_position_bonus: float = 0.0
    per_word_bonus: float = 0.0

def judge_score(response, position, cfg):
    return (float(response['oracle_quality'])
            + (cfg.first_position_bonus if position == 0 else 0.0)
            + cfg.per_word_bonus * len(response['text'].split()))

def choose(first, second, cfg):
    """Return response ID. A tie chooses first, as documented."""
    return (first if judge_score(first, 0, cfg) >= judge_score(second, 1, cfg)
            else second)['id']

def evaluate(cases, cfg):
    if not cases:
        raise ValueError('Dataset must contain at least one case')
    rows=[]
    for case in cases:
        a,b=case['responses']
        winner_ab=choose(a,b,cfg)
        winner_ba=choose(b,a,cfg)
        expected=case['expert_preferred_id']
        rows.append({'case_id':case['id'],'critical':bool(case['critical']),
                     'expert_preferred_id':expected,'winner_ab':winner_ab,
                     'winner_ba':winner_ba,'correct_ab':winner_ab==expected,
                     'incorrect_approval_ab':winner_ab!=expected,
                     'order_flip':winner_ab!=winner_ba})
    n=len(rows);critical=[x for x in rows if x['critical']]
    return {'case_count':n,
            'accuracy_ab':sum(x['correct_ab'] for x in rows)/n,
            'incorrect_approval_rate_ab':sum(x['incorrect_approval_ab'] for x in rows)/n,
            'order_swap_inconsistency_rate':sum(x['order_flip'] for x in rows)/n,
            'critical_case_count':len(critical),
            'critical_incorrect_approval_rate_ab':(sum(x['incorrect_approval_ab'] for x in critical)/len(critical) if critical else None),
            'decisions':rows}

def run():
    cases=json.loads((HERE/'test_cases.json').read_text(encoding='utf-8'))
    return {'study':'OpenVals Case Study 001','evidence_type':'synthetic_simulation',
            'disclaimer':'No real LLM or OpenVals engine was executed.',
            'configurations':{
                'unbiased_oracle':evaluate(cases,JudgeConfig()),
                'position_bias_only':evaluate(cases,JudgeConfig(first_position_bonus=1.2)),
                'verbosity_bias_only':evaluate(cases,JudgeConfig(per_word_bonus=0.14)),
                'combined_bias':evaluate(cases,JudgeConfig(first_position_bonus=0.6,per_word_bonus=0.14))}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    report=run();serialized=json.dumps(report,indent=2)+'\n'
    print(serialized,end='')
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized,encoding='utf-8')
if __name__=='__main__': main()
