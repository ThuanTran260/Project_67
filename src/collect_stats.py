import json
from pathlib import Path
BASE = Path('.')

with open(BASE / 'results' / 'comparison_week4.json', encoding='utf-8') as f:
    comp = json.load(f)
stats = comp['stats']

print('=== COMPARISON WEEK4 STATS (100 submissions) ===')
for s in ['set1','set2','set3','set4']:
    st = stats[s]
    fpr  = st['fpr_pct']
    far  = st['far_pct']
    frr  = st['frr_pct']
    tpr  = st['avg_tpr']
    fp   = st['fp_count']
    fn   = st['fn_count']
    tot  = st['total_latency_sub_s']
    avg  = st['avg_latency_sub_ms']
    p95  = st['p95_latency_sub_ms']
    print(f"{s}: FPR={fpr}%  FAR={far}%  FRR={frr}%  avg_tpr={tpr}%  fp={fp}  fn={fn}  total_s={tot}  avg_sub_ms={avg}  p95={p95}")

print()
print('=== ERROR TYPES ===')
for s in ['set1','set2','set3','set4']:
    e = stats[s]['errors']
    se  = e.get('SE', 0)
    wa  = e.get('WA', 0)
    re  = e.get('RE', 0)
    tle = e.get('TLE', 0)
    mle = e.get('MLE', 0)
    idx = e.get('IndexError', 0)
    typ = e.get('TypeError', 0)
    val = e.get('ValueError', 0)
    nam = e.get('NameError', 0)
    atr = e.get('AttributeError', 0)
    rec = e.get('RecursionError', 0)
    skp = e.get('SKIPPED', 0)
    re_total = re + idx + typ + val + nam + atr + e.get('ZeroDivisionError',0) + rec + e.get('KeyError',0)
    print(f"{s}: SE={se} WA={wa} RE_total={re_total}(IndexErr={idx} TypeError={typ} ValueError={val} NameErr={nam} AttrErr={atr} RecursionErr={rec}) TLE={tle} MLE={mle} SKIPPED={skp}")

import pandas as pd
df_bl = pd.read_csv(BASE / 'results' / 'baseline_summary.csv')
print()
print('=== BASELINE ===')
print(f"Total tasks: {len(df_bl)}  Pass: {df_bl['baseline_ok'].sum()}")
print(f"Avg latency: {df_bl['avg_latency_total'].mean():.4f} s/test")
lat_by_topic = df_bl.groupby('topic')['avg_latency_total'].mean().round(4)
print(lat_by_topic.to_string())

speedup_total = stats['set3']['total_latency_sub_s'] / stats['set4']['total_latency_sub_s']
speedup_p95   = stats['set3']['p95_latency_sub_ms']  / stats['set4']['p95_latency_sub_ms']
print()
print(f"Fail-Fast speedup: total={speedup_total:.2f}x  p95={speedup_p95:.2f}x")
