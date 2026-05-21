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
      "fpr": {compute_fpr output}
    }
    """
    stats = {
        "tong_submissions": len(results),
        "fp_count": 0,
        "fpr_pct": 0.0,
        "avg_tpr_public": 0.0,
        "avg_tpr_hidden": 0.0,
        "error_total_public": {"SE": 0, "WA": 0, "RE": 0, "TLE": 0},
        "error_total_hidden": {"SE": 0, "WA": 0, "RE": 0, "TLE": 0},
        "avg_latency_public": 0.0,
        "avg_latency_hidden": 0.0,
        "per_topic":  defaultdict(lambda: {
            "count": 0, "fp": 0,
            "pub_err": {"SE":0,"WA":0,"RE":0,"TLE":0},
            "hid_err": {"SE":0,"WA":0,"RE":0,"TLE":0},
        }),
        "false_positives": [],
    }

    for r in results:
        pub = r.get("public", {})
        hid = r.get("hidden", {})
        fpr = r.get("fpr", {})
        topic = r.get("topic", "unknown")

        if fpr.get("is_false_positive"):
            stats["fp_count"] += 1
            stats["false_positives"].append({
                "sv_id":    r.get("sv_id"),
                "task_id":  r.get("task_id"),
                "func":     r.get("func"),
                "pub_rate": fpr.get("public_rate"),
                "hid_rate": fpr.get("hidden_rate"),
                "mo_ta_loi": r.get("mo_ta_loi", "")
            })

        stats["avg_tpr_public"] += pub.get("test_pass_rate", 0)
        stats["avg_tpr_hidden"] += hid.get("test_pass_rate", 0)
        stats["avg_latency_public"] += pub.get("avg_latency", 0)
        stats["avg_latency_hidden"] += hid.get("avg_latency", 0)

        for err_type in ["SE", "WA", "RE", "TLE"]:
            stats["error_total_public"][err_type] += pub.get("error_counts", {}).get(err_type, 0)
            stats["error_total_hidden"][err_type] += hid.get("error_counts", {}).get(err_type, 0)

        # Theo topic
        stats["per_topic"][topic]["count"] += 1
        if fpr.get("is_false_positive"):
            stats["per_topic"][topic]["fp"] += 1
        for err_type in ["SE", "WA", "RE", "TLE"]:
            stats["per_topic"][topic]["pub_err"][err_type] += pub.get("error_counts", {}).get(err_type, 0)
            stats["per_topic"][topic]["hid_err"][err_type] += hid.get("error_counts", {}).get(err_type, 0)

    n = len(results)
    if n > 0:
        stats["fpr_pct"]           = round(stats["fp_count"] / n * 100, 2)
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
        "pub_SE", "pub_WA", "pub_RE", "pub_TLE",
        "hid_pass", "hid_total", "hid_tpr",
        "hid_SE", "hid_WA", "hid_RE", "hid_TLE",
        "is_false_positive",
        "avg_latency_pub", "avg_latency_hid",
    ]

    rows = []
    for r in results:
        pub = r.get("public", {})
        hid = r.get("hidden", {})
        fpr = r.get("fpr", {})
        pub_err = pub.get("error_counts", {})
        hid_err = hid.get("error_counts", {})

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
            "hid_pass":    hid.get("pass_count", 0),
            "hid_total":   hid.get("total_count", 0),
            "hid_tpr":     hid.get("test_pass_rate", 0),
            "hid_SE":      hid_err.get("SE", 0),
            "hid_WA":      hid_err.get("WA", 0),
            "hid_RE":      hid_err.get("RE", 0),
            "hid_TLE":     hid_err.get("TLE", 0),
            "is_false_positive": fpr.get("is_false_positive", False),
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
    print(f"  False Positive Rate     : {stats['fpr_pct']}% ({stats['fp_count']} bài)")
    print(f"  Avg TPR public (3 test) : {stats['avg_tpr_public']}%")
    print(f"  Avg TPR hidden (10 test): {stats['avg_tpr_hidden']}%")
    print(f"  Latency public          : {stats['avg_latency_public']}s/test")
    print(f"  Latency hidden          : {stats['avg_latency_hidden']}s/test")
    print(f"\n  Lỗi PUBLIC  → SE:{stats['error_total_public']['SE']}  WA:{stats['error_total_public']['WA']}  RE:{stats['error_total_public']['RE']}  TLE:{stats['error_total_public']['TLE']}")
    print(f"  Lỗi HIDDEN  → SE:{stats['error_total_hidden']['SE']}  WA:{stats['error_total_hidden']['WA']}  RE:{stats['error_total_hidden']['RE']}  TLE:{stats['error_total_hidden']['TLE']}")

    if stats.get("per_topic"):
        print(f"\n  Theo topic:")
        for topic, t in stats["per_topic"].items():
            fp_rate = round(t['fp'] / t['count'] * 100, 1) if t['count'] else 0
            print(f"    {topic:<10}: {t['count']} bài, FPR={fp_rate}%")

    if stats.get("false_positives"):
        print(f"\n  Bài False Positive chi tiết:")
        for fp in stats["false_positives"]:
            print(f"    [{fp['sv_id']}] task {fp['task_id']} {fp['func']}() — pub:{fp['pub_rate']}% hid:{fp['hid_rate']}%")
            if fp.get("mo_ta_loi"):
                print(f"      Lỗi: {fp['mo_ta_loi']}")
    print(f"{'='*60}\n")
