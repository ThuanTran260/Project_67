"""
simulate_v2.py — Tạo 50 bài nộp mô phỏng từ file nguồn raw
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import sys
from pathlib import Path
from collections import Counter

# Thiết lập encoding UTF-8 cho Windows console
if sys.stdout.encoding != 'utf-8':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Auto-resolve BASE path
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebookes", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)

RAW_FILE = BASE / "data" / "raw" / "submissions_50.json"
HIDDEN_FILE = BASE / "data" / "processed" / "hidden_v2.json"
OUT_FILE = BASE / "data" / "processed" / "submissions_50.json"


def generate():
    if not RAW_FILE.exists():
        print(f"ERROR: Khong tim thay file nguon {RAW_FILE}")
        return
    if not HIDDEN_FILE.exists():
        print(f"ERROR: Khong tim thay file test cases {HIDDEN_FILE}")
        return

    with open(RAW_FILE, "r", encoding="utf-8") as f:
        submissions = json.load(f)

    with open(HIDDEN_FILE, "r", encoding="utf-8") as f:
        hidden_tasks = json.load(f)
        
    # Map task_id to its correct topic
    topic_map = {t["task_id"]: t["topic"] for t in hidden_tasks}
    
    for sub in submissions:
        sid = sub["submission_id"]
        tid = sub["task_id"]
        
        # 1. Update error_type to AC for SV009 and SV032
        if sid in ["SV009", "SV032"]:
            sub["error_type"] = "AC"
            
        # 2. Synchronize topic with hidden_v2.json
        if tid in topic_map:
            sub["topic"] = topic_map[tid]

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)

    print(f"OK: Da tao {len(submissions)} bai nop mo phong -> {OUT_FILE}")

    # In phân bố lỗi để kiểm chứng
    counts = Counter(s["error_type"] for s in submissions)
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v} bai nop")

    # In phân bố task_id để kiểm chứng đủ 50 task
    task_ids = sorted(set(s["task_id"] for s in submissions))
    print(f"  Task IDs ({len(task_ids)} tasks): {task_ids[0]} -> {task_ids[-1]}")


if __name__ == "__main__":
    generate()
