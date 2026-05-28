import json
from pathlib import Path
BASE = Path('.')

with open(BASE / 'results' / 'comparison_week4.json', encoding='utf-8') as f:
    comp = json.load(f)
stats = comp['stats']

print('=== XAC NHAN SO SUBMISSIONS DUOC DUNG TRONG comparison_week4.json ===')
print()
for s in ['set1','set2','set3','set4']:
    st = stats[s]
    total_s = st['total_latency_sub_s']
    avg_ms  = st['avg_latency_sub_ms']
    fp      = st['fp_count']
    fpr     = st['fpr_pct']

    n_from_latency = round(total_s / (avg_ms / 1000))
    n_from_fpr     = round(fp / (fpr / 100)) if fpr > 0 else 'N/A (fpr=0)'

    print(f'{s}:')
    print(f'  total_latency_sub_s = {total_s}')
    print(f'  avg_latency_sub_ms  = {avg_ms}')
    print(f'  => n (tinh nguoc tu total/avg) = {n_from_latency}')
    print(f'  fp_count={fp}  fpr_pct={fpr}%')
    print(f'  => n (tinh nguoc tu FP/FPR)    = {n_from_fpr}')
    print()
