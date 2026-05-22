"""
comparison_3sets.py — So sánh 3 bộ test trên 50 bài nộp mô phỏng
Nhóm 67 | Tuần 3

Đồng bộ dữ liệu đầu vào từ submissions_50.json.
So sánh 3 bộ test:
  - Set 1 (3 public tests)
  - Set 2 (3 public + 6 hidden = 9 tests, từ mbpp_clean.json)
  - Set 3 (3 public + 10 hidden = 13 tests, từ hidden_v2.json)
"""

import json
import sys
import os
import csv
from typing import Dict, List

# Đồng bộ hệ thống file để hiển thị được tiếng Việt có dấu trên Windows console
# try:
#     sys.stdout.reconfigure(encoding='utf-8')
#     sys.stderr.reconfigure(encoding='utf-8')
# except AttributeError:
#     pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMISSIONS_FILE = os.path.join(BASE, 'data', 'processed', 'submissions_50.json')
HIDDEN_V2_FILE = os.path.join(BASE, 'data', 'processed', 'hidden_v2.json')
MBPP_CLEAN_FILE = os.path.join(BASE, 'data', 'processed', 'mbpp_clean.json')
OUT_DIR = os.path.join(BASE, 'results')
os.makedirs(OUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE, 'src'))
from runner_v2 import grade_submission

def main():
    print("=" * 75)
    print("  HỆ THỐNG SO SÁNH 3 BỘ TEST TRÊN BÀI NỘP THỰC TẾ CỦA SINH VIÊN (RQ1)")
    print("=" * 75)
    
    # ── 1. Đọc dữ liệu đầu vào ────────────────────────────────────────────────
    if not os.path.exists(SUBMISSIONS_FILE):
        print(f"[LỖI] Không tìm thấy file bài nộp: {SUBMISSIONS_FILE}")
        sys.exit(1)
        
    if not os.path.exists(HIDDEN_V2_FILE) or not os.path.exists(MBPP_CLEAN_FILE):
        print(f"[LỖI] Không tìm thấy file dữ liệu test cases!")
        sys.exit(1)
        
    with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
        submissions = json.load(f)
        
    with open(HIDDEN_V2_FILE, 'r', encoding='utf-8') as f:
        problems_v2 = {p['task_id']: p for p in json.load(f)}
        
    with open(MBPP_CLEAN_FILE, 'r', encoding='utf-8') as f:
        problems_clean = {p['task_id']: p for p in json.load(f)}
        
    print(f"  ✓ Đã load {len(submissions)} bài nộp của sinh viên.")
    print(f"  ✓ Đã load bộ dữ liệu 10 hidden: {len(problems_v2)} bài.")
    print(f"  ✓ Đã load bộ dữ liệu 6 hidden: {len(problems_clean)} bài.")
    print("\n  Bắt đầu chấm bài trên 3 tập cấu hình test cases...")
    print()

    # ── 2. Chạy chấm bài và so sánh ───────────────────────────────────────────
    results = []
    
    # Khởi tạo bộ đếm lỗi cho các set
    set1_counts = {"SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0, "FP": 0}
    set2_counts = {"SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0, "FP": 0}
    set3_counts = {"SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0, "FP": 0}
    
    set1_latencies = []
    set2_latencies = []
    set3_latencies = []
    
    set1_tprs = []
    set2_tprs = []
    set3_tprs = []
    
    # Danh sách chi tiết các bài FP
    fp_details_set1 = []
    fp_details_set2 = []
    fp_details_set3 = []

    for i, sub in enumerate(submissions):
        sv_id = sub["submission_id"]
        tid = sub["task_id"]
        func_name = sub["func_name"]
        code = sub["submitted_code"]
        topic = sub.get("topic", "")
        err_type_actual = sub.get("error_type", "")
        note = sub.get("note", "")
        
        prob_v2 = problems_v2.get(tid)
        prob_clean = problems_clean.get(tid)
        
        if not prob_v2 or not prob_clean:
            continue
            
        # Trích xuất các test case
        pub_tests = prob_v2["public_tests"]
        hid_6_tests = prob_clean["hidden_tests"]
        hid_10_tests = prob_v2["hidden_tests"]
        
        # Chấm trên Set 1: 3 public tests
        r_set1 = grade_submission(code, func_name, pub_tests, "set1_public")
        # Chấm trên Set 2: 3 public + 6 hidden = 9 tests
        r_set2 = grade_submission(code, func_name, pub_tests + hid_6_tests, "set2_clean")
        # Chấm trên Set 3: 3 public + 10 hidden = 13 tests
        r_set3 = grade_submission(code, func_name, pub_tests + hid_10_tests, "set3_v2")
        
        # Kiểm tra trạng thái False Positive (bài làm bị lỗi nhưng lại PASS hết test)
        is_buggy = (err_type_actual != "AC")
        
        is_fp_set1 = is_buggy and (r_set1["pass_count"] == r_set1["total_count"])
        is_fp_set2 = is_buggy and (r_set2["pass_count"] == r_set2["total_count"])
        is_fp_set3 = is_buggy and (r_set3["pass_count"] == r_set3["total_count"])
        
        # Cập nhật thống kê Set 1
        set1_tprs.append(r_set1["test_pass_rate"])
        set1_latencies.append(r_set1["avg_latency"])
        for k in r_set1["error_counts"]:
            set1_counts[k] += r_set1["error_counts"][k]
        if is_fp_set1:
            set1_counts["FP"] += 1
            fp_details_set1.append({"sv_id": sv_id, "task_id": tid, "func": func_name, "topic": topic, "note": note})
            
        # Cập nhật thống kê Set 2
        set2_tprs.append(r_set2["test_pass_rate"])
        set2_latencies.append(r_set2["avg_latency"])
        for k in r_set2["error_counts"]:
            set2_counts[k] += r_set2["error_counts"][k]
        if is_fp_set2:
            set2_counts["FP"] += 1
            fp_details_set2.append({"sv_id": sv_id, "task_id": tid, "func": func_name, "topic": topic, "note": note})
            
        # Cập nhật thống kê Set 3
        set3_tprs.append(r_set3["test_pass_rate"])
        set3_latencies.append(r_set3["avg_latency"])
        for k in r_set3["error_counts"]:
            set3_counts[k] += r_set3["error_counts"][k]
        if is_fp_set3:
            set3_counts["FP"] += 1
            fp_details_set3.append({"sv_id": sv_id, "task_id": tid, "func": func_name, "topic": topic, "note": note})
            
        # In tiến trình chạy
        fp_flag = ""
        if is_fp_set1: fp_flag += "[FP Set1]"
        if is_fp_set2: fp_flag += "[FP Set2]"
        if is_fp_set3: fp_flag += "[FP Set3]"
        
        print(f"  [{sv_id}] {func_name}() (Topic: {topic:<8}) | Actual: {err_type_actual:<4} | Set1 Pass: {r_set1['pass_count']}/{r_set1['total_count']} | Set2 Pass: {r_set2['pass_count']}/{r_set2['total_count']} | Set3 Pass: {r_set3['pass_count']}/{r_set3['total_count']} {fp_flag}")
        
        results.append({
            "sv_id": sv_id,
            "task_id": tid,
            "func": func_name,
            "topic": topic,
            "mo_ta_loi": note,
            "actual_error_type": err_type_actual,
            
            "set1_pass": r_set1["pass_count"],
            "set1_total": r_set1["total_count"],
            "set1_tpr": r_set1["test_pass_rate"],
            "is_fp_set1": is_fp_set1,
            
            "set2_pass": r_set2["pass_count"],
            "set2_total": r_set2["total_count"],
            "set2_tpr": r_set2["test_pass_rate"],
            "is_fp_set2": is_fp_set2,
            
            "set3_pass": r_set3["pass_count"],
            "set3_total": r_set3["total_count"],
            "set3_tpr": r_set3["test_pass_rate"],
            "is_fp_set3": is_fp_set3
        })

    # ── 3. Tính toán các metric trung bình ──────────────────────────────────────
    n = len(submissions)
    
    stats = {
        "tong_submissions": n,
        "set1": {
            "fp_count": set1_counts["FP"],
            "fpr_pct": round(set1_counts["FP"] / n * 100, 2),
            "avg_tpr": round(sum(set1_tprs) / n, 2),
            "avg_latency": round(sum(set1_latencies) / n, 4),
            "errors": {k: v for k, v in set1_counts.items() if k != "FP"}
        },
        "set2": {
            "fp_count": set2_counts["FP"],
            "fpr_pct": round(set2_counts["FP"] / n * 100, 2),
            "avg_tpr": round(sum(set2_tprs) / n, 2),
            "avg_latency": round(sum(set2_latencies) / n, 4),
            "errors": {k: v for k, v in set2_counts.items() if k != "FP"}
        },
        "set3": {
            "fp_count": set3_counts["FP"],
            "fpr_pct": round(set3_counts["FP"] / n * 100, 2),
            "avg_tpr": round(sum(set3_tprs) / n, 2),
            "avg_latency": round(sum(set3_latencies) / n, 4),
            "errors": {k: v for k, v in set3_counts.items() if k != "FP"}
        }
    }

    # ── 4. In bảng so sánh RQ1 ──────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("  KẾT QUẢ SO SÁNH 3 TẬP TEST CASES (RQ1)")
    print("=" * 80)
    
    avg_t1 = sum(r["set1_total"] for r in results) / len(results)
    avg_t2 = sum(r["set2_total"] for r in results) / len(results)
    avg_t3 = sum(r["set3_total"] for r in results) / len(results)
    
    print(f"  {'Metric':<32} | {f'Set 1 (Avg {avg_t1:.1f}t)':<15} | {f'Set 2 (Avg {avg_t2:.1f}t)':<15} | {f'Set 3 (Avg {avg_t3:.1f}t)'}")
    print("  " + "-" * 78)
    print(f"  {'Số bài nộp mô phỏng':<32} | {n:<15} | {n:<15} | {n}")
    print(f"  {'Số lượng False Positives':<32} | {stats['set1']['fp_count']:<15} | {stats['set2']['fp_count']:<15} | {stats['set3']['fp_count']}")
    print(f"  {'False Positive Rate (FPR)':<32} | {stats['set1']['fpr_pct']}%{''*10:<11} | {stats['set2']['fpr_pct']}%{''*10:<11} | {stats['set3']['fpr_pct']}%")
    print(f"  {'Tỉ lệ pass trung bình (Avg TPR)':<32} | {stats['set1']['avg_tpr']}%{''*10:<11} | {stats['set2']['avg_tpr']}%{''*10:<11} | {stats['set3']['avg_tpr']}%")
    print(f"  {'Lỗi WA phát hiện':<32} | {stats['set1']['errors']['WA']:<15} | {stats['set2']['errors']['WA']:<15} | {stats['set3']['errors']['WA']}")
    print(f"  {'Lỗi RE phát hiện':<32} | {stats['set1']['errors']['RE']:<15} | {stats['set2']['errors']['RE']:<15} | {stats['set3']['errors']['RE']}")
    print(f"  {'Lỗi TLE phát hiện':<32} | {stats['set1']['errors']['TLE']:<15} | {stats['set2']['errors']['TLE']:<15} | {stats['set3']['errors']['TLE']}")
    print(f"  {'Lỗi MLE phát hiện':<32} | {stats['set1']['errors']['MLE']:<15} | {stats['set2']['errors']['MLE']:<15} | {stats['set3']['errors']['MLE']}")
    print(f"  {'Lỗi SE phát hiện':<32} | {stats['set1']['errors']['SE']:<15} | {stats['set2']['errors']['SE']:<15} | {stats['set3']['errors']['SE']}")
    print(f"  {'Độ trễ trung bình/test (s)':<32} | {stats['set1']['avg_latency']}s{''*10:<12} | {stats['set2']['avg_latency']}s{''*10:<12} | {stats['set3']['avg_latency']}s")
    print("=" * 80)
    print()

    # ── 5. In chi tiết danh sách False Positives ────────────────────────────────
    print("  CHI TIẾT CÁC BÀI FALSE POSITIVE:")
    print("  " + "-" * 78)
    
    print(f"  * Tập 1 (3 Public Tests) có {len(fp_details_set1)} bài FP:")
    for fp in fp_details_set1:
        print(f"    - [{fp['sv_id']}] Task {fp['task_id']} {fp['func']}() ({fp['topic']}) | Lỗi: {fp['note']}")
        
    print(f"\n  * Tập 2 (3 Public + 6 Hidden) có {len(fp_details_set2)} bài FP:")
    for fp in fp_details_set2:
        print(f"    - [{fp['sv_id']}] Task {fp['task_id']} {fp['func']}() ({fp['topic']}) | Lỗi: {fp['note']}")
        
    print(f"\n  * Tập 3 (3 Public + 6-10 Hidden) có {len(fp_details_set3)} bài FP:")
    for fp in fp_details_set3:
        print(f"    - [{fp['sv_id']}] Task {fp['task_id']} {fp['func']}() ({fp['topic']}) | Lỗi: {fp['note']}")
    print("-" * 80 + "\n")

    # ── 6. Lưu kết quả ra CSV & JSON ───────────────────────────────────────────
    csv_path = os.path.join(OUT_DIR, "comparison_3sets.csv")
    fieldnames = [
        "sv_id", "task_id", "func", "topic", "mo_ta_loi", "actual_error_type",
        "set1_pass", "set1_total", "set1_tpr", "is_fp_set1",
        "set2_pass", "set2_total", "set2_tpr", "is_fp_set2",
        "set3_pass", "set3_total", "set3_tpr", "is_fp_set3"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"✓ Lưu kết quả chi tiết CSV tại: {csv_path}")

    json_path = os.path.join(OUT_DIR, "comparison_3sets.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "results": results}, f, ensure_ascii=False, indent=2)
    print(f"✓ Lưu kết quả chi tiết JSON tại: {json_path}")
    print()

if __name__ == "__main__":
    main()
