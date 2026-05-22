import json

with open('e:/Bao Cao Ha Dung/Tuan 2/Project/results/baseline_summary.json', encoding='utf-8') as f:
    data = json.load(f)

meta = data.get('meta', {})
print("--- META STATS ---")
print(f"Avg Latency Public (s): {meta.get('avg_latency_pub_s')}")
print(f"Avg Latency Hidden (s): {meta.get('avg_latency_hid_s')}")
print(f"Avg Latency Total (s): {meta.get('avg_latency_total_s')}")

results = data.get('results', [])
pub_latency = 0
hid_latency = 0
total_latency = 0
n = len(results)

if n > 0:
    for r in results:
        pub_latency += r.get('pub_latency', 0)
        hid_latency += r.get('hid_latency', 0)
        total_latency += r.get('avg_latency_total', 0)
    
    print("\n--- DETAILED CALCULATION ---")
    print(f"Avg Latency Public (s): {pub_latency / n}")
    print(f"Avg Latency Hidden (s): {hid_latency / n}")
    print(f"Avg Latency Total (s): {total_latency / n}")
