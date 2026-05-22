"""
error_stats.py — Module thống kê lỗi tự động theo task
Nhóm 67 | Tuần 3

Chức năng:
  - Đếm SE/WA/RE/TLE theo từng task và toàn bộ
  - Tính FPR theo đơn vị bài nộp
  - Xuất báo cáo CSV và JSON tự động
"""

import json, csv, os
from collections import defaultdict
from typing import List, Dict

def compute_stats(results: List[Dict]) -> Dict:
    """
    Tính toàn bộ thống kê từ danh sách kết quả.

    Mỗi result có dạng:
    {
      "sv_id": ..., "task_id": ..., "func": ...,
      "public": {grade_submission output},
      "hidden": {grade_submission output},
      "fpr": {compute_fpr output} hoặc "leakage": {compute_leakage output}
    }
    """
    stats = {
        "tong_submissions": len(results),
        "fp_count": 0,
        "fpr_pct": 0.0,
        "leakage_count": 0,
        "leakage_rate_pct": 0.0,
        "avg_tpr_public": 0.0,
        "avg_tpr_hidden": 0.0,
        "error_total_public": {"SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0},
        "error_total_hidden": {"SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0},
        "avg_latency_public": 0.0,
        "avg_latency_hidden": 0.0,
        "per_topic":  defaultdict(lambda: {
            "count": 0, "fp": 0, "leakage": 0,
            "pub_err": {"SE":0,"WA":0,"RE":0,"TLE":0,"MLE":0},
            "hid_err": {"SE":0,"WA":0,"RE":0,"TLE":0,"MLE":0},
        }),
        "false_positives": [],
        "leakages": [],
    }

    for r in results:
        pub = r.get("public", {})
        hid = r.get("hidden", {})
        # Hỗ trợ cả key "leakage" mới và key "fpr" cũ
        leakage = r.get("leakage") or r.get("fpr") or {}
        topic = r.get("topic", "unknown")

        is_leak = leakage.get("is_public_test_leakage") or leakage.get("is_false_positive")

        if is_leak:
            stats["fp_count"] += 1
            stats["leakage_count"] += 1
            leak_info = {
                "sv_id":    r.get("sv_id"),
                "task_id":  r.get("task_id"),
                "func":     r.get("func"),
                "pub_rate": leakage.get("public_rate"),
                "hid_rate": leakage.get("hidden_rate"),
                "mo_ta_loi": r.get("mo_ta_loi", "")
            }
            stats["false_positives"].append(leak_info)
            stats["leakages"].append(leak_info)

        stats["avg_tpr_public"] += pub.get("test_pass_rate", 0)
        stats["avg_tpr_hidden"] += hid.get("test_pass_rate", 0)
        stats["avg_latency_public"] += pub.get("avg_latency", 0)
        stats["avg_latency_hidden"] += hid.get("avg_latency", 0)

        for err_type in ["SE", "WA", "RE", "TLE", "MLE"]:
            stats["error_total_public"][err_type] += pub.get("error_counts", {}).get(err_type, 0)
            stats["error_total_hidden"][err_type] += hid.get("error_counts", {}).get(err_type, 0)

        # Theo topic
        stats["per_topic"][topic]["count"] += 1
        if is_leak:
            stats["per_topic"][topic]["fp"] += 1
            stats["per_topic"][topic]["leakage"] += 1
        for err_type in ["SE", "WA", "RE", "TLE", "MLE"]:
            stats["per_topic"][topic]["pub_err"][err_type] += pub.get("error_counts", {}).get(err_type, 0)
            stats["per_topic"][topic]["hid_err"][err_type] += hid.get("error_counts", {}).get(err_type, 0)

    n = len(results)
    if n > 0:
        stats["fpr_pct"]           = round(stats["fp_count"] / n * 100, 2)
        stats["leakage_rate_pct"]   = round(stats["leakage_count"] / n * 100, 2)
        stats["avg_tpr_public"]    = round(stats["avg_tpr_public"] / n, 2)
        stats["avg_tpr_hidden"]    = round(stats["avg_tpr_hidden"] / n, 2)
        stats["avg_latency_public"]= round(stats["avg_latency_public"] / n, 4)
        stats["avg_latency_hidden"]= round(stats["avg_latency_hidden"] / n, 4)

    stats["per_topic"] = dict(stats["per_topic"])
    return stats


def save_stats_csv(results: List[Dict], filepath: str):
    """Lưu kết quả chi tiết ra CSV."""
    if not results:
        return

    fieldnames = [
        "sv_id", "task_id", "func", "topic", "mo_ta_loi",
        "pub_pass", "pub_total", "pub_tpr",
        "pub_SE", "pub_WA", "pub_RE", "pub_TLE", "pub_MLE",
        "hid_pass", "hid_total", "hid_tpr",
        "hid_SE", "hid_WA", "hid_RE", "hid_TLE", "hid_MLE",
        "is_false_positive",
        "is_public_test_leakage",
        "avg_latency_pub", "avg_latency_hid",
    ]

    rows = []
    for r in results:
        pub = r.get("public", {})
        hid = r.get("hidden", {})
        leakage = r.get("leakage") or r.get("fpr") or {}
        pub_err = pub.get("error_counts", {})
        hid_err = hid.get("error_counts", {})

        is_leak = leakage.get("is_public_test_leakage") or leakage.get("is_false_positive") or False

        rows.append({
            "sv_id":       r.get("sv_id", ""),
            "task_id":     r.get("task_id", ""),
            "func":        r.get("func", ""),
            "topic":       r.get("topic", ""),
            "mo_ta_loi":   r.get("mo_ta_loi", ""),
            "pub_pass":    pub.get("pass_count", 0),
            "pub_total":   pub.get("total_count", 0),
            "pub_tpr":     pub.get("test_pass_rate", 0),
            "pub_SE":      pub_err.get("SE", 0),
            "pub_WA":      pub_err.get("WA", 0),
            "pub_RE":      pub_err.get("RE", 0),
            "pub_TLE":     pub_err.get("TLE", 0),
            "pub_MLE":     pub_err.get("MLE", 0),
            "hid_pass":    hid.get("pass_count", 0),
            "hid_total":   hid.get("total_count", 0),
            "hid_tpr":     hid.get("test_pass_rate", 0),
            "hid_SE":      hid_err.get("SE", 0),
            "hid_WA":      hid_err.get("WA", 0),
            "hid_RE":      hid_err.get("RE", 0),
            "hid_TLE":     hid_err.get("TLE", 0),
            "hid_MLE":     hid_err.get("MLE", 0),
            "is_false_positive": is_leak,
            "is_public_test_leakage": is_leak,
            "avg_latency_pub": pub.get("avg_latency", 0),
            "avg_latency_hid": hid.get("avg_latency", 0),
        })

    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(stats: Dict, label: str = ""):
    """In bảng tổng hợp ra màn hình."""
    print(f"\n{'='*60}")
    if label:
        print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Tổng submissions        : {stats['tong_submissions']}")
    print(f"  Public Test Leakage Rate: {stats['leakage_rate_pct']}% ({stats['leakage_count']} bài)")
    print(f"  Avg TPR public (3 test) : {stats['avg_tpr_public']}%")
    print(f"  Avg TPR hidden (10 test): {stats['avg_tpr_hidden']}%")
    print(f"  Latency public          : {stats['avg_latency_public']}s/test")
    print(f"  Latency hidden          : {stats['avg_latency_hidden']}s/test")
    print(f"\n  Lỗi PUBLIC  → SE:{stats['error_total_public']['SE']}  WA:{stats['error_total_public']['WA']}  RE:{stats['error_total_public']['RE']}  TLE:{stats['error_total_public']['TLE']}  MLE:{stats['error_total_public']['MLE']}")
    print(f"  Lỗi HIDDEN  → SE:{stats['error_total_hidden']['SE']}  WA:{stats['error_total_hidden']['WA']}  RE:{stats['error_total_hidden']['RE']}  TLE:{stats['error_total_hidden']['TLE']}  MLE:{stats['error_total_hidden']['MLE']}")

    if stats.get("per_topic"):
        print(f"\n  Theo topic:")
        for topic, t in stats["per_topic"].items():
            leakage_rate = round(t['leakage'] / t['count'] * 100, 1) if t['count'] else 0
            print(f"    {topic:<10}: {t['count']} bài, Leakage Rate={leakage_rate}%")

    if stats.get("leakages"):
        print(f"\n  Bài Public Test Leakage chi tiết:")
        for l in stats["leakages"]:
            print(f"    [{l['sv_id']}] task {l['task_id']} {l['func']}() — pub:{l['pub_rate']}% hid:{l['hid_rate']}%")
            if l.get("mo_ta_loi"):
                print(f"      Lỗi: {l['mo_ta_loi']}")
    print(f"{'='*60}\n")
