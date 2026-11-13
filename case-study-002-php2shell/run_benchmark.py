"""Offline, synthetic, non-exploit PHP2Shell remediation triage benchmark. Python stdlib only."""
import csv,json,random,pathlib,collections
ROOT=pathlib.Path(__file__).parent
rng=random.Random(20261023)
fixed={'8.2':35,'8.3':36,'8.4':27,'8.5':12}
rows=[]
for i in range(240):
    branch=['8.2','8.3','8.4','8.5','8.1','8.0','7.4'][i%7]
    if branch in fixed:
        patch=max(0,fixed[branch]+[-2,-1,0,1][(i//7)%4])
    else: patch={'8.1':34,'8.0':30,'7.4':33}[branch]
    vendor_backport=bool(i%11==0)
    exposure=['internet-facing','internal-only','unknown'][i%3]
    evidence=['verified vendor bulletin','unverified claim','no bulletin'][i%3]
    # A supported branch with current/future patch is fixed; old branches need verified vendor backport.
    truth='patched' if (branch in fixed and patch>=fixed[branch]) or (vendor_backport and evidence=='verified vendor bulletin') else 'requires-action'
    rows.append(dict(id=f'CASE-{i+1:03}',php_version=f'{branch}.{patch}',vendor_backport_claim=str(vendor_backport).lower(),backport_evidence=evidence,exposure=exposure,ground_truth=truth,synthetic='true'))
def baseline(r):
    branch,patch=r['php_version'].rsplit('.',1);patch=int(patch)
    if branch in fixed and patch>=fixed[branch]:return 'patched'
    if r['vendor_backport_claim']=='true' and r['backport_evidence']=='verified vendor bulletin':return 'patched'
    return 'requires-action'
def naive(r):
    # Deliberately weak heuristic that ignores vendor backports.
    branch,patch=r['php_version'].rsplit('.',1)
    return 'patched' if branch in fixed and int(patch)>=fixed[branch] else 'requires-action'
for r in rows:r['rules_prediction']=baseline(r);r['naive_prediction']=naive(r)
with (ROOT/'synthetic_cases.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def metric(k):
    tp=sum(r[k]=='requires-action' and r['ground_truth']=='requires-action' for r in rows)
    fp=sum(r[k]=='requires-action' and r['ground_truth']=='patched' for r in rows)
    fn=sum(r[k]=='patched' and r['ground_truth']=='requires-action' for r in rows)
    tn=sum(r[k]=='patched' and r['ground_truth']=='patched' for r in rows)
    return {'TP':tp,'FP':fp,'FN':fn,'TN':tn,'accuracy':round((tp+tn)/len(rows),4),'precision_action':round(tp/(tp+fp),4) if tp+fp else None,'recall_action':round(tp/(tp+fn),4) if tp+fn else None,'false_positive_rate':round(fp/(fp+tn),4) if fp+tn else None}
results={'run_type':'synthetic offline rules benchmark; NOT OpenVals execution; NOT PHP exploitation test','cases':len(rows),'seed':20261023,'ground_truth_generation':'same public version thresholds and backport verification logic as rules baseline; not independent','rules_baseline':metric('rules_prediction'),'naive_baseline':metric('naive_prediction'),'limitations':['Labels are programmatically derived, causing circularity for rules baseline.','No AI/LLM model, OpenVals SDK, RedShield, PHP runtime, exploit, telemetry or production system was executed.','No statistical generalization to real security incidents.']}
(ROOT/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
