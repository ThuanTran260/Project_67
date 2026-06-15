"""
comparison_3sets.py — So sánh 3 bộ test và Cấu hình tối ưu tuần 4 trên 50 bài nộp
Nhóm 67 | Tuần 4
"""

import json
import sys
import os
import csv
import time
from typing import Dict, List

# Thiết lập encoding UTF-8 để hiển thị an toàn trên Windows console
if sys.stdout.encoding != 'utf-8':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
SUBMISSIONS_FILE = os.path.join(BASE, 'data', 'processed', 'submissions_50.json')
HIDDEN_V2_FILE = os.path.join(BASE, 'data', 'processed', 'hidden_v2.json')
MBPP_CLEAN_FILE = os.path.join(BASE, 'data', 'processed', 'mbpp_clean.json')
OUT_DIR = os.path.join(BASE, 'results')
os.makedirs(OUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE, 'src'))
from runner_v3 import grade_submission

def calculate_percentile(data: List[float], percentile: float) -> float:
    if not data:
        return 0.0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (percentile / 100.0)
    f = int(k)
    c = f + 1
    if c < len(sorted_data):
        return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])
    else:
        return sorted_data[f]

def main():
    print("=" * 80)
    print("  HE THONG graded VA SO SANH CAC BO TEST CASES (WEEK 4 EVALUATION)")
    print("=" * 80)
    
    # ── 1. Đọc dữ liệu đầu vào ────────────────────────────────────────────────
    if not os.path.exists(SUBMISSIONS_FILE):
        print(f"[LOI] Khong tim thay file submissions: {SUBMISSIONS_FILE}")
        sys.exit(1)
        
    if not os.path.exists(HIDDEN_V2_FILE) or not os.path.exists(MBPP_CLEAN_FILE):
        print(f"[LOI] Khong tim thay file du lieu test cases!")
        sys.exit(1)
        
    with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
        submissions = json.load(f)
        
    with open(HIDDEN_V2_FILE, 'r', encoding='utf-8') as f:
        problems_v2 = {p['task_id']: p for p in json.load(f)}
        
    with open(MBPP_CLEAN_FILE, 'r', encoding='utf-8') as f:
        problems_clean = {p['task_id']: p for p in json.load(f)}
        
    print(f"  [OK] Da load {len(submissions)} bai nop mo phong.")
    print(f"  [OK] Da load bo test hidden v2 (Set 3/4): {len(problems_v2)} bai.")
    print(f"  [OK] Da load bo test 6 hidden (Set 2): {len(problems_clean)} bai.")
    print("\n  Bat dau cham bai tren 4 cau hinh test cases...")
    print()

    # ── 2. Chấm bài và so sánh ───────────────────────────────────────────
    results = []
    
    # Khởi tạo thống kê lỗi cho 4 set
    set_keys = ["set1", "set2", "set3", "set4"]
    stats_dict = {
        k: {
            "SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0, "FP": 0, "FN": 0,
            "IndexError": 0, "ZeroDivisionError": 0, "TypeError": 0, 
            "ValueError": 0, "NameError": 0, "AttributeError": 0, "KeyError": 0, "RecursionError": 0, "SKIPPED": 0,
            "tprs": [], "latencies_per_test": [], "latencies_per_sub": [], "total_time": 0.0,
            "fp_details": [], "fn_details": []
        } for k in set_keys
    }

    # Đếm số lượng buggy submissions thật sự
    total_submissions = len(submissions)
    ac_submissions_count = sum(1 for s in submissions if s.get("error_type", "") == "AC")
    buggy_submissions_count = total_submissions - ac_submissions_count
    print(f"  So submissions AC (dung): {ac_submissions_count}")
    print(f"  So submissions Buggy (Faulty): {buggy_submissions_count}")
    print("-" * 80)

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
            
        pub_tests = prob_v2["public_tests"]
        hid_6_tests = prob_clean["hidden_tests"]
        hid_10_tests = prob_v2["hidden_tests"]
        
        is_buggy = (err_type_actual != "AC")
        
        # ── Set 1: 3 public tests
        t1_start = time.perf_counter()
        r_set1 = grade_submission(code, func_name, pub_tests, "set1_public", fail_fast=False)
        t1_end = time.perf_counter()
        
        # ── Set 2: 3 public + 6 hidden = 9 tests
        t2_start = time.perf_counter()
        r_set2 = grade_submission(code, func_name, pub_tests + hid_6_tests, "set2_clean", fail_fast=False)
        t2_end = time.perf_counter()
        
        # ── Set 3: 3 public + 6-10 hidden = 13 tests (fail_fast=False)
        t3_start = time.perf_counter()
        r_set3 = grade_submission(code, func_name, pub_tests + hid_10_tests, "set3_v2", fail_fast=False)
        t3_end = time.perf_counter()
        
        # ── Set 4: Set 3 + fail_fast=True (Optimized Runner Week 4)
        t4_start = time.perf_counter()
        r_set4 = grade_submission(code, func_name, pub_tests + hid_10_tests, "set4_opt", fail_fast=True)
        t4_end = time.perf_counter()
        
        # Lưu thời gian chạy thực tế của toàn bộ submission
        sub_latencies = {
            "set1": t1_end - t1_start,
            "set2": t2_end - t2_start,
            "set3": t3_end - t3_start,
            "set4": t4_end - t4_start
        }
        
        runs = [("set1", r_set1), ("set2", r_set2), ("set3", r_set3), ("set4", r_set4)]
        
        for skey, r_set in runs:
            # FP: bài lỗi nhưng pass hết
            is_fp = is_buggy and (r_set["pass_count"] == r_set["total_count"])
            # FN: bài đúng (AC) nhưng bị chấm fail (False Rejection)
            is_fn = (not is_buggy) and (r_set["pass_count"] < r_set["total_count"])
            
            stats_dict[skey]["tprs"].append(r_set["test_pass_rate"])
            stats_dict[skey]["latencies_per_test"].append(r_set["avg_latency"])
            stats_dict[skey]["latencies_per_sub"].append(sub_latencies[skey])
            stats_dict[skey]["total_time"] += sub_latencies[skey]
            
            for err in r_set["error_counts"]:
                if r_set["error_counts"][err] > 0:
                    stats_dict[skey][err] += r_set["error_counts"][err]
                    
            if is_fp:
                stats_dict[skey]["FP"] += 1
                stats_dict[skey]["fp_details"].append({
                    "sv_id": sv_id,
                    "task_id": tid,
                    "func": func_name,
                    "topic": topic,
                    "note": note
                })
            if is_fn:
                stats_dict[skey]["FN"] += 1
                stats_dict[skey]["fn_details"].append({
                    "sv_id": sv_id,
                    "task_id": tid,
                    "func": func_name,
                    "topic": topic,
                    "pass_count": r_set["pass_count"],
                    "total_count": r_set["total_count"]
                })

        # In tiến trình chạy ra console
        fp_flag = ""
        if is_buggy and r_set1["pass_count"] == r_set1["total_count"]: fp_flag += "[FP S1]"
        if is_buggy and r_set2["pass_count"] == r_set2["total_count"]: fp_flag += "[FP S2]"
        if is_buggy and r_set3["pass_count"] == r_set3["total_count"]: fp_flag += "[FP S3]"
        if is_buggy and r_set4["pass_count"] == r_set4["total_count"]: fp_flag += "[FP S4]"
        if not is_buggy and r_set3["pass_count"] < r_set3["total_count"]: fp_flag += "[FN S3]"
        if not is_buggy and r_set4["pass_count"] < r_set4["total_count"]: fp_flag += "[FN S4]"
        
        print(f"  [{sv_id}] {func_name:<20} | Act: {err_type_actual:<4} | S1: {r_set1['pass_count']}/{r_set1['total_count']} | S3: {r_set3['pass_count']}/{r_set3['total_count']} | S4 (FF): {r_set4['pass_count']}/{r_set4['total_count']} {fp_flag}")

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
            "is_fp_set1": is_buggy and (r_set1["pass_count"] == r_set1["total_count"]),
            "is_fn_set1": (not is_buggy) and (r_set1["pass_count"] < r_set1["total_count"]),
            
            "set2_pass": r_set2["pass_count"],
            "set2_total": r_set2["total_count"],
            "set2_tpr": r_set2["test_pass_rate"],
            "is_fp_set2": is_buggy and (r_set2["pass_count"] == r_set2["total_count"]),
            "is_fn_set2": (not is_buggy) and (r_set2["pass_count"] < r_set2["total_count"]),
            
            "set3_pass": r_set3["pass_count"],
            "set3_total": r_set3["total_count"],
            "set3_tpr": r_set3["test_pass_rate"],
            "is_fp_set3": is_buggy and (r_set3["pass_count"] == r_set3["total_count"]),
            "is_fn_set3": (not is_buggy) and (r_set3["pass_count"] < r_set3["total_count"]),
            
            "set4_pass": r_set4["pass_count"],
            "set4_total": r_set4["total_count"],
            "set4_tpr": r_set4["test_pass_rate"],
            "is_fp_set4": is_buggy and (r_set4["pass_count"] == r_set4["total_count"]),
            "is_fn_set4": (not is_buggy) and (r_set4["pass_count"] < r_set4["total_count"])
        })

    # ── 3. Tính toán các metric tổng hợp ──────────────────────────────────────
    final_stats = {}
    for skey in set_keys:
        sdata = stats_dict[skey]
        fp_count = sdata["FP"]
        fn_count = sdata["FN"]
        
        # FPR (False Positive Rate) = FP / buggy_submissions (tỷ lệ báo động giả trên tổng số bài lỗi)
        fpr_pct = round(fp_count / buggy_submissions_count * 100, 2) if buggy_submissions_count > 0 else 0.0
        # FAR (False Acceptance Rate) = FP / total_submissions (tỷ lệ lọt lỗi trên tổng số bài nộp)
        far_pct = round(fp_count / total_submissions * 100, 2)
        # FRR (False Rejection Rate) = FN / ac_submissions — bài đúng bị chấm oan
        frr_pct = round(fn_count / ac_submissions_count * 100, 2) if ac_submissions_count > 0 else 0.0
        
        avg_tpr = round(sum(sdata["tprs"]) / total_submissions, 2)
        avg_lat_test = round(sum(sdata["latencies_per_test"]) / total_submissions * 1000, 2) # ms
        avg_lat_sub = round(sum(sdata["latencies_per_sub"]) / total_submissions * 1000, 2) # ms
        p95_lat_sub = round(calculate_percentile(sdata["latencies_per_sub"], 95) * 1000, 2) # ms
        
        final_stats[skey] = {
            "fp_count": fp_count,
            "fn_count": fn_count,
            "fpr_pct": fpr_pct,
            "far_pct": far_pct,
            "frr_pct": frr_pct,
            "avg_tpr": avg_tpr,
            "avg_latency_test_ms": avg_lat_test,
            "avg_latency_sub_ms": avg_lat_sub,
            "p95_latency_sub_ms": p95_lat_sub,
            "total_latency_sub_s": round(sdata["total_time"], 4),
            "errors": {
                "SE": sdata["SE"],
                "WA": sdata["WA"],
                "RE": sdata["RE"],
                "TLE": sdata["TLE"],
                "MLE": sdata["MLE"],
                "IndexError": sdata["IndexError"],
                "ZeroDivisionError": sdata["ZeroDivisionError"],
                "TypeError": sdata["TypeError"],
                "ValueError": sdata["ValueError"],
                "NameError": sdata["NameError"],
                "AttributeError": sdata["AttributeError"],
                "KeyError": sdata["KeyError"],
                "RecursionError": sdata["RecursionError"],
                "SKIPPED": sdata["SKIPPED"]
            },
            "fn_details": sdata["fn_details"]
        }

    # ── 4. In bảng so sánh kết quả Week 4 ──────────────────────────────────────
    print("\n" + "=" * 90)
    print("  KET QUA SO SANH CAC CAU HINH CHAM BAI (WEEK 4 EVALUATION)")
    print("=" * 90)
    
    avg_t1 = sum(r["set1_total"] for r in results) / len(results)
    avg_t2 = sum(r["set2_total"] for r in results) / len(results)
    avg_t3 = sum(r["set3_total"] for r in results) / len(results)
    avg_t4 = sum(r["set4_total"] for r in results) / len(results)
    
    cols = ["Metric", "Set 1 (3t)", "Set 2 (9t)", "Set 3 (13t)", "Set 4 (13t+FF)"]
    print(f"  {cols[0]:<35} | {cols[1]:<12} | {cols[2]:<12} | {cols[3]:<12} | {cols[4]}")
    print("  " + "-" * 88)
    
    print(f"  {'Tong so submissions':<35} | {total_submissions:<12} | {total_submissions:<12} | {total_submissions:<12} | {total_submissions}")
    print(f"  {'  - So bai AC (dung)':<35} | {ac_submissions_count:<12} | {ac_submissions_count:<12} | {ac_submissions_count:<12} | {ac_submissions_count}")
    print(f"  {'  - So bai Buggy (loi)':<35} | {buggy_submissions_count:<12} | {buggy_submissions_count:<12} | {buggy_submissions_count:<12} | {buggy_submissions_count}")
    print(f"  {'So bai False Positive (FP)':<35} | {final_stats['set1']['fp_count']:<12} | {final_stats['set2']['fp_count']:<12} | {final_stats['set3']['fp_count']:<12} | {final_stats['set4']['fp_count']}")
    print(f"  {'So bai False Negative (FN/FR)':<35} | {final_stats['set1']['fn_count']:<12} | {final_stats['set2']['fn_count']:<12} | {final_stats['set3']['fn_count']:<12} | {final_stats['set4']['fn_count']}")
    print(f"  {'False Positive Rate (FPR)':<35} | {final_stats['set1']['fpr_pct']}%{''*5:<7} | {final_stats['set2']['fpr_pct']}%{''*5:<7} | {final_stats['set3']['fpr_pct']}%{''*5:<7} | {final_stats['set4']['fpr_pct']}%")
    print(f"  {'False Acceptance Rate (FAR)':<35} | {final_stats['set1']['far_pct']}%{''*5:<7} | {final_stats['set2']['far_pct']}%{''*5:<7} | {final_stats['set3']['far_pct']}%{''*5:<7} | {final_stats['set4']['far_pct']}%")
    print(f"  {'False Rejection Rate (FRR)':<35} | {final_stats['set1']['frr_pct']}%{''*5:<7} | {final_stats['set2']['frr_pct']}%{''*5:<7} | {final_stats['set3']['frr_pct']}%{''*5:<7} | {final_stats['set4']['frr_pct']}%")
    print(f"  {'Avg Test Pass Rate (Avg TPR)':<35} | {final_stats['set1']['avg_tpr']}%{''*5:<7} | {final_stats['set2']['avg_tpr']}%{''*5:<7} | {final_stats['set3']['avg_tpr']}%{''*5:<7} | {final_stats['set4']['avg_tpr']}%")
    print(f"  {'Do tre trung binh/test (ms)':<35} | {final_stats['set1']['avg_latency_test_ms']:<12} | {final_stats['set2']['avg_latency_test_ms']:<12} | {final_stats['set3']['avg_latency_test_ms']:<12} | {final_stats['set4']['avg_latency_test_ms']}")
    print(f"  {'Do tre trung binh/submission (ms)':<35} | {final_stats['set1']['avg_latency_sub_ms']:<12} | {final_stats['set2']['avg_latency_sub_ms']:<12} | {final_stats['set3']['avg_latency_sub_ms']:<12} | {final_stats['set4']['avg_latency_sub_ms']}")
    print(f"  {'Do tre P95/submission (ms)':<35} | {final_stats['set1']['p95_latency_sub_ms']:<12} | {final_stats['set2']['p95_latency_sub_ms']:<12} | {final_stats['set3']['p95_latency_sub_ms']:<12} | {final_stats['set4']['p95_latency_sub_ms']}")
    print(f"  {'Tong thoi gian graded 100 subs (s)':<35} | {final_stats['set1']['total_latency_sub_s']:<12} | {final_stats['set2']['total_latency_sub_s']:<12} | {final_stats['set3']['total_latency_sub_s']:<12} | {final_stats['set4']['total_latency_sub_s']}")
    
    print("  " + "-" * 88)
    print("  THONG KE CAC LOAI LOI PHAT HIEN DUOC:")
    print("  " + "-" * 88)
    
    for err in ["SE", "WA", "RE", "TLE", "MLE", "IndexError", "ZeroDivisionError", "TypeError", "ValueError", "NameError", "AttributeError", "KeyError", "SKIPPED"]:
        print(f"  {f'Loi {err}':<35} | {final_stats['set1']['errors'][err]:<12} | {final_stats['set2']['errors'][err]:<12} | {final_stats['set3']['errors'][err]:<12} | {final_stats['set4']['errors'][err]}")
        
    print("=" * 90)
    print()

    # ── 5. In chi tiết danh sách False Positives & False Negatives ────────────────
    print("  DANH SACH CHI TIET CAC BAI FALSE POSITIVE (BAI LOI LOT QUA):")
    print("  " + "-" * 80)
    for skey in set_keys:
        fps = stats_dict[skey]["fp_details"]
        print(f"  * {skey.upper()} co {len(fps)} ca False Positive:")
        for fp in fps:
            print(f"    - [{fp['sv_id']}] Task {fp['task_id']} {fp['func']}() ({fp['topic']}) | Loi that: {fp['note']}")
        print()
    print("-" * 82)

    print("  DANH SACH CHI TIET CAC BAI FALSE NEGATIVE (BAI DUNG BI CHAM OAN):")
    print("  " + "-" * 80)
    for skey in set_keys:
        fns = stats_dict[skey]["fn_details"]
        print(f"  * {skey.upper()} co {len(fns)} ca False Negative (False Rejection):")
        for fn in fns:
            print(f"    - [{fn['sv_id']}] Task {fn['task_id']} {fn['func']}() | Pass: {fn['pass_count']}/{fn['total_count']}")
        print()
    print("-" * 82 + "\n")

    # ── 6. Lưu kết quả ra CSV & JSON ───────────────────────────────────────────
    csv_path = os.path.join(OUT_DIR, "comparison_week4.csv")
    fieldnames = [
        "sv_id", "task_id", "func", "topic", "mo_ta_loi", "actual_error_type",
        "set1_pass", "set1_total", "set1_tpr", "is_fp_set1", "is_fn_set1",
        "set2_pass", "set2_total", "set2_tpr", "is_fp_set2", "is_fn_set2",
        "set3_pass", "set3_total", "set3_tpr", "is_fp_set3", "is_fn_set3",
        "set4_pass", "set4_total", "set4_tpr", "is_fp_set4", "is_fn_set4"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"[OK] Luu CSV ket qua chi tiet: {csv_path}")

    json_path = os.path.join(OUT_DIR, "comparison_week4.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"stats": final_stats, "results": results}, f, ensure_ascii=False, indent=2)
    print(f"[OK] Luu JSON ket qua chi tiet: {json_path}")
    print()

if __name__ == "__main__":
    main()
