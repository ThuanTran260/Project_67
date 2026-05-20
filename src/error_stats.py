"""
error_stats.py — Module thống kê lỗi tự động theo task
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Union

# Auto-resolve BASE path
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebooks", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)


def analyze_errors(submissions_results: List[Dict]) -> Dict:
    """
    Phân tích danh sách kết quả chấm bài của sinh viên và trả về thống kê chi tiết.
    
    Args:
        submissions_results: Danh sách kết quả chấm bài. Mỗi kết quả chứa:
            - task_id, func, topic, is_false_positive
            - error_type (loại lỗi thực tế của bài nộp)
            - status (kết quả test thực tế: PASS, WA, RE, TLE, MLE, SE)
    """
    total_submissions = len(submissions_results)
    
    # 1. Thống kê theo loại lỗi thực tế (error_type) vs Kết quả chấm (status)
    error_type_stats = defaultdict(lambda: defaultdict(int))
    # 2. Thống kê theo chủ đề (topic)
    topic_stats = defaultdict(lambda: defaultdict(int))
    # 3. Thống kê theo Task ID
    task_stats = defaultdict(lambda: defaultdict(int))
    
    false_positives = 0
    
    for sub in submissions_results:
        # Nhận diện thông tin
        task_id = sub.get("task_id")
        topic = sub.get("topic", "unknown")
        err_type = sub.get("mo_ta_loi", "").split(" - ")[0].replace("Lỗi ", "").strip()
        if not err_type:
            err_type = sub.get("error_type", "unknown")
            
        status = sub.get("status", "")
        # Nếu từ file student_simulation.json, kiểm tra kết quả trên bộ test
        is_fp = sub.get("is_false_positive", False)
        if is_fp:
            false_positives += 1
            
        # Xác định status đại diện cho bài nộp (ví dụ nếu có bất kỳ lỗi nào)
        # Hoặc đếm số lượng lỗi cụ thể
        if "hid_errors" in sub:
            # Nếu là kết quả tổng hợp của bài
            # Trích xuất lỗi từ dict hid_errors
            try:
                err_counts = eval(sub["hid_errors"]) if isinstance(sub["hid_errors"], str) else sub["hid_errors"]
                if err_counts.get("SE", 0) > 0:
                    rep_status = "SE"
                elif err_counts.get("TLE", 0) > 0:
                    rep_status = "TLE"
                elif err_counts.get("MLE", 0) > 0:
                    rep_status = "MLE"
                elif err_counts.get("RE", 0) > 0:
                    rep_status = "RE"
                elif err_counts.get("WA", 0) > 0:
                    rep_status = "WA"
                else:
                    rep_status = "PASS"
            except Exception:
                rep_status = "unknown"
        else:
            rep_status = status if status else "unknown"
            
        # Cập nhật thống kê
        error_type_stats[err_type][rep_status] += 1
        topic_stats[topic][rep_status] += 1
        task_stats[task_id][rep_status] += 1
        if is_fp:
            task_stats[task_id]["false_positive"] += 1
            topic_stats[topic]["false_positive"] += 1
            error_type_stats[err_type]["false_positive"] += 1
            
    return {
        "total": total_submissions,
        "false_positives": false_positives,
        "fpr_rate": round(false_positives / total_submissions * 100, 2) if total_submissions > 0 else 0.0,
        "by_error_type": error_type_stats,
        "by_topic": topic_stats,
        "by_task": task_stats
    }


def print_ascii_report(stats: Dict):
    """In bao cao thong ke dinh dang ASCII ra console."""
    print("=" * 70)
    print("           BAO CAO THONG KE LOI TU DONG THEO TASK")
    print("=" * 70)
    print(f" Tong so bai nop duoc phan tich: {stats['total']}")
    print(f" So luong False Positive: {stats['false_positives']}")
    print(f" Ty le False Positive Rate (FPR): {stats['fpr_rate']}%")
    print("-" * 70)
    
    # 1. Thống kê theo Chủ đề (Topic)
    print("\n[1] THONG KE LOI THEO CHU DE (TOPIC):")
    print(f" {'Topic':<12} | {'PASS':<6} | {'WA':<6} | {'RE':<6} | {'TLE':<6} | {'MLE':<6} | {'SE':<6} | {'FPs':<6}")
    print("-" * 70)
    for topic, s in sorted(stats["by_topic"].items()):
        print(f" {topic:<12} | {s['PASS']:<6} | {s['WA']:<6} | {s['RE']:<6} | {s['TLE']:<6} | {s['MLE']:<6} | {s['SE']:<6} | {s['false_positive']:<6}")
    print("-" * 70)
    
    # 2. Thống kê theo Loại lỗi sinh viên thiết kế (Error Type)
    print("\n[2] THONG KE THEO LOAI LOI THUC TE:")
    print(f" {'Loai loi goc':<15} | {'PASS':<6} | {'WA':<6} | {'RE':<6} | {'TLE':<6} | {'MLE':<6} | {'SE':<6} | {'FPs':<6}")
    print("-" * 70)
    for err_type, s in sorted(stats["by_error_type"].items()):
        print(f" {err_type:<15} | {s['PASS']:<6} | {s['WA']:<6} | {s['RE']:<6} | {s['TLE']:<6} | {s['MLE']:<6} | {s['SE']:<6} | {s['false_positive']:<6}")
    print("-" * 70)


def export_stats_to_csv(stats: Dict, output_path: Union[str, Path]):
    """Xuất báo cáo thống kê chi tiết theo từng task ra file CSV."""
    # Gom tất cả task_id
    all_tasks = sorted(list(stats["by_task"].keys()))
    
    rows = []
    for tid in all_tasks:
        s = stats["by_task"][tid]
        rows.append({
            "task_id": tid,
            "total_submissions": sum(v for k, v in s.items() if k != "false_positive"),
            "PASS": s["PASS"],
            "WA": s["WA"],
            "RE": s["RE"],
            "TLE": s["TLE"],
            "MLE": s["MLE"],
            "SE": s["SE"],
            "false_positives": s["false_positive"],
            "fpr_pct": round(s["false_positive"] / sum(v for k, v in s.items() if k != "false_positive") * 100, 2) if sum(v for k, v in s.items() if k != "false_positive") > 0 else 0.0
        })
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "task_id", "total_submissions", "PASS", "WA", "RE", "TLE", "MLE", "SE", "false_positives", "fpr_pct"
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"OK: Da xuat thong ke loi theo task ra file: {output_path}")


def analyze_file(json_file_path: Union[str, Path], csv_output_path: Union[str, Path] = None):
    """Đọc dữ liệu từ file kết quả mô phỏng và xuất báo cáo."""
    if not os.path.exists(json_file_path):
        print(f"ERROR: File {json_file_path} khong ton tai.")
        return
        
    with open(json_file_path, encoding="utf-8") as f:
        data = json.load(f)
        
    # Hỗ trợ cả định dạng bọc ngoài {"submissions": [...]} và list gốc
    if isinstance(data, dict) and "submissions" in data:
        subs = data["submissions"]
    elif isinstance(data, list):
        subs = data
    else:
        print("ERROR: Dinh dang file khong hop le (can la list hoac dict submissions)")
        return
        
    stats = analyze_errors(subs)
    print_ascii_report(stats)
    
    if csv_output_path:
        export_stats_to_csv(stats, csv_output_path)


if __name__ == "__main__":
    # Chạy thử với dữ liệu hiện tại nếu có
    sim_path = BASE / "results" / "student_simulation.json"
    out_csv = BASE / "results" / "error_analysis_v2.csv"
    if sim_path.exists():
        analyze_file(sim_path, out_csv)
    else:
        print(f"Chua co file {sim_path}. Hay chay file simulation truoc.")
