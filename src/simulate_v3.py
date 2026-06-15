"""
simulate_v3.py — Tạo 100 bài nộp mô phỏng từ file nguồn raw với phân bố lỗi Week 4
Nhóm 67 | Tuần 4 | Ngôn ngữ lập trình Python
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
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent

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
        
        # Đồng bộ hóa chủ đề bài tập
        if tid in topic_map:
            sub["topic"] = topic_map[tid]
            
        # 1. Update SV009 (factorial) to AC
        if sid == "SV009":
            sub["error_type"] = "AC"
            sub["submitted_code"] = "def factorial(n):\n    if n == 0:\n        return 1\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result\n"
            sub["note"] = "factorial - Solution đúng hoàn toàn"
            
        # 2. Update SV019 (count_words) to WA
        if sid == "SV019":
            sub["error_type"] = "WA"
            sub["submitted_code"] = "def count_words(s):\n    return len(s.split(' '))\n"
            sub["note"] = "Không xử lý chuỗi có khoảng trắng liên tiếp hoặc đầu/cuối - WA"
            
        # 3. Update SV028 (is_sorted) to WA
        if sid == "SV028":
            sub["error_type"] = "WA"
            sub["submitted_code"] = "def is_sorted(lst):\n    if len(lst) <= 1:\n        return False\n    for i in range(len(lst)-1):\n        if lst[i]>lst[i+1]:\n            return False\n    return True\n"
            sub["note"] = "Trả về False cho danh sách rỗng hoặc có 1 phần tử - WA"
            
        # 4. Update SV046 (MLE) to MLE
        if sid == "SV046":
            sub["error_type"] = "MLE"
            sub["submitted_code"] = "def starts_with_upper(s):\n    # Cố tình tạo chuỗi 200MB để kích hoạt MLE\n    x = ' ' * (200 * 1024 * 1024)\n    return s[0].isupper()\n"
            sub["note"] = "Tràn bộ nhớ (MLE) — Khai báo chuỗi 200MB"
            
        # 5. Update SV047 (TLE) to TLE
        if sid == "SV047":
            sub["error_type"] = "TLE"
            sub["submitted_code"] = "def last_n(lst, n):\n    # Vòng lặp vô hạn kích hoạt TLE\n    while True:\n        pass\n    return lst[-n:] if n else []\n"
            sub["note"] = "Quá thời gian (TLE) — Vòng lặp vô hạn"

        # 6. Update SV063 (is_samepatterns) to AC because it is functionally correct
        if sid == "SV063":
            sub["error_type"] = "AC"
            sub["note"] = "is_samepatterns - Solution đúng mặc dù có thay đổi dấu cộng thành dấu trừ (do tính chất đối xứng và chỉ mục âm)"

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)

    print(f"OK: Da tao {len(submissions)} bai nop mo phong -> {OUT_FILE}")

    # In phân bố lỗi để kiểm chứng
    counts = Counter(s["error_type"] for s in submissions)
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v} bai nop")

    # In phân bố chủ đề
    topic_counts = Counter(s["topic"] for s in submissions)
    print("\nSummary of topic distribution:")
    for k, v in sorted(topic_counts.items()):
        print(f"  {k}: {v} bai nop")


if __name__ == "__main__":
    generate()
