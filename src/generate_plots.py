"""
generate_plots.py — Vẽ các biểu đồ trực quan hóa kết quả FPR, lỗi và độ trễ (Week 4)
Dùng số liệu THỰC TẾ từ comparison_week4.csv và comparison_week4.json — không hardcode.
Nhóm 67 | Tuần 4
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path

# Thiết lập encoding UTF-8 để vẽ chữ tiếng Việt không lỗi trên Windows
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

try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

COMPARISON_CSV  = BASE / "results" / "comparison_week4.csv"
COMPARISON_JSON = BASE / "results" / "comparison_week4.json"
HIDDEN_V2_JSON  = BASE / "data" / "processed" / "hidden_v2.json"
OUT_DIR         = BASE / "results"

def load_data():
    """Đọc số liệu thực tế từ CSV và JSON."""
    if not COMPARISON_CSV.exists():
        print(f"[LỖI] Không tìm thấy {COMPARISON_CSV}")
        return None, None
    df = pd.read_csv(COMPARISON_CSV)
    
    stats = None
    if COMPARISON_JSON.exists():
        with open(COMPARISON_JSON, encoding="utf-8") as f:
            stats = json.load(f).get("stats", {})
            
    return df, stats

def apply_styling(ax):
    """Áp dụng style tối giản, hiện đại."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_alpha(0.3)
    ax.spines["bottom"].set_alpha(0.3)
    ax.grid(axis="y", alpha=0.2, linestyle="--")

def plot_fpr_vs_ntest(df, stats, out_dir):
    """
    Biểu đồ 1: FPR theo số lượng test case (RQ1).
    So sánh 4 cấu hình: Set 1, Set 2, Set 3, Set 4
    """
    if not stats:
        return
        
    avg_t1 = df["set1_total"].mean() if df is not None and "set1_total" in df.columns else 3.0
    avg_t2 = df["set2_total"].mean() if df is not None and "set2_total" in df.columns else 9.0
    avg_t3 = df["set3_total"].mean() if df is not None and "set3_total" in df.columns else 13.0
    avg_t4 = df["set4_total"].mean() if df is not None and "set4_total" in df.columns else 13.0
    
    x_tests = [avg_t1, avg_t2, avg_t3, avg_t4]
    y_fpr = [
        stats["set1"]["fpr_pct"],
        stats["set2"]["fpr_pct"],
        stats["set3"]["fpr_pct"],
        stats["set4"]["fpr_pct"]
    ]
    
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    
    # Vẽ đường biểu diễn
    ax.plot(x_tests[:3], y_fpr[:3], marker="o", markersize=8, linewidth=2.5,
            color="#E24B4A", label="FPR (%) - No FailFast", zorder=3)
    # Điểm Set 4 riêng biệt (vì cùng số test case với Set 3 nhưng có fail fast)
    ax.scatter([avg_t4], [y_fpr[3]], color="#3CB371", edgecolor="black", s=120, 
               label="FPR (%) - Set 4 (FailFast)", zorder=4)
    ax.fill_between(x_tests[:3], y_fpr[:3], alpha=0.1, color="#E24B4A")
    
    # Annotate từng điểm
    for i, (x, y, fp_count) in enumerate(zip(x_tests, y_fpr, [stats["set1"]["fp_count"], stats["set2"]["fp_count"], stats["set3"]["fp_count"], stats["set4"]["fp_count"]])):
        offset = (0, 10) if i != 3 else (25, -5)
        ax.annotate(
            f"{y}% ({fp_count}/50)",
            xy=(x, y),
            xytext=offset,
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#C82323" if i != 3 else "#2E8B57"
        )
        
    ax.set_title("Biểu đồ 1: Tỉ lệ báo động giả (FPR) theo số lượng test case", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Số lượng test case trung bình mỗi bài toán", fontsize=9.5, labelpad=8)
    ax.set_ylabel("FPR (%)", fontsize=9.5, labelpad=8)
    ax.set_xlim(min(x_tests) - 1.5, max(x_tests) + 2.0)
    ax.set_ylim(-3, max(y_fpr) + 8)
    ax.set_xticks(sorted(list(set(x_tests))))
    
    labels = [
        f"{int(avg_t1)} tests\n(S1: Public)",
        f"{int(avg_t2)} tests\n(S2: 3P+6H)",
        f"{int(avg_t3)} tests\n(S3: 3P+6-10H)\n& (S4: FailFast)"
    ]
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.legend(loc="upper right", fontsize=8.5)
    apply_styling(ax)
    
    path = out_dir / "FPR_vs_ntest.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] Da ve va luu: {path}")

def plot_error_types_comparison(df, stats, out_dir):
    """
    Biểu đồ 2: So sánh số lỗi SE/WA/RE/TLE/MLE phát hiện được qua 4 bộ test.
    """
    if not stats:
        return
        
    err_types = ["SE", "WA", "RE", "TLE", "MLE"]
    set1_vals = [stats["set1"]["errors"].get(e, 0) for e in err_types]
    set2_vals = [stats["set2"]["errors"].get(e, 0) for e in err_types]
    set3_vals = [stats["set3"]["errors"].get(e, 0) for e in err_types]
    set4_vals = [stats["set4"]["errors"].get(e, 0) for e in err_types]
    
    x = np.arange(len(err_types))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    
    rects1 = ax.bar(x - 1.5*width, set1_vals, width, label="Set 1 (3 Public)", color="#5C9BD1")
    rects2 = ax.bar(x - 0.5*width, set2_vals, width, label="Set 2 (3P+6H)", color="#F29C38")
    rects3 = ax.bar(x + 0.5*width, set3_vals, width, label="Set 3 (3P+6-10H)", color="#3CB371")
    rects4 = ax.bar(x + 1.5*width, set4_vals, width, label="Set 4 (Set 3 + FailFast)", color="#E55B5B")
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f"{int(height)}",
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha="center", va="bottom", fontsize=7.5, fontweight="bold")
                             
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)
    
    ax.set_title("Biểu đồ 2: So sánh số lượng lỗi phát hiện qua các cấu hình", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Loại lỗi", fontsize=9.5, labelpad=8)
    ax.set_ylabel("Số lỗi phát hiện", fontsize=9.5, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(err_types, fontsize=9)
    ax.set_ylim(0, max(max(set1_vals), max(set2_vals), max(set3_vals), max(set4_vals)) + 15)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=8.5)
    apply_styling(ax)
    
    path = out_dir / "error_types_comparison.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] Da ve va luu: {path}")

def plot_fpr_by_topic(df, out_dir):
    """
    Biểu đồ 3: FPR của Set 1 theo chủ đề bài toán.
    """
    topics = df["topic"].unique() if "topic" in df.columns else []
    if len(topics) == 0:
        return
        
    topic_stats = []
    for t in sorted(topics):
        sub = df[df["topic"] == t]
        n = len(sub)
        fp = sub["is_fp_set1"].sum()
        topic_stats.append({
            "topic": t,
            "n": n,
            "fp": fp,
            "fpr": round(fp / n * 100, 1) if n else 0
        })
        
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
    colors = {"list": "#5C9BD1", "math": "#E55B5B", "string": "#9B59B6"}
    
    names = [s["topic"].capitalize() for s in topic_stats]
    fprs = [s["fpr"] for s in topic_stats]
    cols = [colors.get(s["topic"], "#95A5A6") for s in topic_stats]
    
    bars = ax.bar(names, fprs, color=cols, width=0.4)
    
    for bar, s in zip(bars, topic_stats):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                f"{h}%\n({s['fp']}/{s['n']} bài)",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold")
                
    ax.set_title("Biểu đồ 3: False Positive Rate (Set 1) theo chủ đề bài toán", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Chủ đề bài toán", fontsize=9.5, labelpad=8)
    ax.set_ylabel("FPR (%)", fontsize=9.5, labelpad=8)
    ax.set_ylim(0, max(fprs) + 12)
    apply_styling(ax)
    
    path = out_dir / "fpr_by_topic.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] Da ve va luu: {path}")

def plot_latency_comparison(stats, out_dir):
    """
    Biểu đồ 4: So sánh tổng thời gian graded và độ trễ P95 (Set 3 vs Set 4 FailFast)
    Để chứng minh sự cải tiến vượt bậc về mặt latency của Week 4.
    """
    if not stats:
        return
        
    sets = ["Set 1", "Set 2", "Set 3", "Set 4 (FF)"]
    total_times = [
        stats["set1"]["total_latency_sub_s"],
        stats["set2"]["total_latency_sub_s"],
        stats["set3"]["total_latency_sub_s"],
        stats["set4"]["total_latency_sub_s"]
    ]
    p95_lats = [
        stats["set1"]["p95_latency_sub_ms"],
        stats["set2"]["p95_latency_sub_ms"],
        stats["set3"]["p95_latency_sub_ms"],
        stats["set4"]["p95_latency_sub_ms"]
    ]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)
    
    # Subplot 1: Tổng thời gian chấm 50 submissions (giây)
    bars1 = ax1.bar(sets, total_times, color=["#5C9BD1", "#F29C38", "#3CB371", "#E55B5B"], width=0.4)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + (max(total_times)*0.02),
                 f"{h:.3f} s", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax1.set_title("Tổng thời gian chấm 50 bài nộp (giây)", fontsize=11, fontweight="bold", pad=10)
    ax1.set_ylabel("Thời gian (giây)", fontsize=9.5)
    ax1.set_ylim(0, max(total_times) * 1.15)
    apply_styling(ax1)
    
    # Subplot 2: Độ trễ P95 trên mỗi submission (ms)
    bars2 = ax2.bar(sets, p95_lats, color=["#5C9BD1", "#F29C38", "#3CB371", "#E55B5B"], width=0.4)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, h + (max(p95_lats)*0.02),
                 f"{h:.1f} ms", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax2.set_title("Độ trễ P95 trên mỗi bài nộp (mili-giây)", fontsize=11, fontweight="bold", pad=10)
    ax2.set_ylabel("Độ trễ (ms)", fontsize=9.5)
    ax2.set_ylim(0, max(p95_lats) * 1.15)
    apply_styling(ax2)
    
    path = out_dir / "latency_comparison.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] Da ve va luu bieu do latency: {path}")

def plot_description_lengths(out_dir):
    """
    Biểu đồ 5: Phân phối độ dài mô tả bài tập và số lượng test cases.
    """
    if not os.path.exists(HIDDEN_V2_JSON):
        return
        
    with open(HIDDEN_V2_JSON, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
        
    word_lengths = [len(t['text'].split()) for t in tasks]
    total_test_counts = [len(t['public_tests']) + len(t['hidden_tests']) for t in tasks]
    
    avg_word = sum(word_lengths) / len(tasks)
    avg_total = sum(total_test_counts) / len(tasks)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)
    
    # Subplot 1: Phân bố số từ trong mô tả (đều đặn từ 10-19 từ)
    unique_w, counts_w = np.unique(word_lengths, return_counts=True)
    bars1 = ax1.bar(unique_w, counts_w, color="#4682B4", edgecolor="white", alpha=0.85, width=0.6, zorder=2)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.1,
                 f"{int(h)} bài", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax1.axvline(avg_word, color="red", linestyle="--", linewidth=1.5, label=f"TB: {avg_word:.1f} từ", zorder=3)
    ax1.legend(loc="upper right", fontsize=8.5)
    ax1.set_title("Phân bố số từ trong câu lệnh mô tả bài tập", fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlabel("Số lượng từ", fontsize=9)
    ax1.set_ylabel("Số lượng bài toán", fontsize=9)
    ax1.set_xticks(range(10, 20))
    ax1.set_ylim(0, max(counts_w) + 1)
    apply_styling(ax1)
    
    # Subplot 2: Tổng số test case (public + hidden) mỗi bài toán
    unique_tests, test_counts = np.unique(total_test_counts, return_counts=True)
    bars2 = ax2.bar(unique_tests, test_counts, color="#FF7F50", width=0.6, alpha=0.85, edgecolor="white", zorder=2)
    for bar in bars2:
        h = bar.get_height()
        if h > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.3,
                     f"{int(h)} bài", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax2.axvline(avg_total, color="green", linestyle="--", linewidth=1.5, label=f"TB: {avg_total:.1f} tests", zorder=3)
    ax2.legend(loc="upper right", fontsize=8.5)
    ax2.set_title("Số lượng test case (Public + Hidden) của mỗi bài toán", fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("Số lượng test case", fontsize=9)
    ax2.set_ylabel("Số lượng bài toán", fontsize=9)
    ax2.set_xticks(range(min(total_test_counts) - 1, max(total_test_counts) + 2))
    ax2.set_ylim(0, max(test_counts) + 3)
    apply_styling(ax2)
    
    path = out_dir / "description_lengths_distribution.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] Da ve va luu bieu do mo ta ghep: {path}")

def plot_full_vs_failfast_comparison(stats, out_dir):
    """
    Biểu đồ 6: So sánh chi tiết hiệu năng giữa Full-run (Set 3) và Fail-Fast (Set 4).
    """
    if not stats:
        return
        
    categories = ["Tổng thời gian chạy (s)", "Độ trễ TB/bài (ms)", "Độ trễ P95/bài (ms)"]
    full_run = [
        stats["set3"]["total_latency_sub_s"],
        stats["set3"]["avg_latency_sub_ms"],
        stats["set3"]["p95_latency_sub_ms"]
    ]
    fail_fast = [
        stats["set4"]["total_latency_sub_s"],
        stats["set4"]["avg_latency_sub_ms"],
        stats["set4"]["p95_latency_sub_ms"]
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
    
    rects1 = ax.bar(x - width/2, full_run, width, label="Full-Run (Không dừng sớm)", color="#3CB371")
    rects2 = ax.bar(x + width/2, fail_fast, width, label="Fail-Fast (Dừng khi gặp lỗi)", color="#E55B5B")
    
    def add_labels(rects):
        for idx, rect in enumerate(rects):
            h = rect.get_height()
            unit = " s" if idx == 0 else " ms"
            ax.annotate(f"{h:.2f}{unit}",
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=8.5, fontweight="bold")
                        
    add_labels(rects1)
    add_labels(rects2)
    
    speedup_total = full_run[0] / fail_fast[0] if fail_fast[0] > 0 else 0
    speedup_avg = full_run[1] / fail_fast[1] if fail_fast[1] > 0 else 0
    speedup_p95 = full_run[2] / fail_fast[2] if fail_fast[2] > 0 else 0
    
    ax.text(0, max(full_run[0], fail_fast[0]) * 0.5, f"Nhanh hơn\n{speedup_total:.1f}x", ha="center", va="center", color="#C82323", fontweight="bold", fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))
    ax.text(1, max(full_run[1], fail_fast[1]) * 0.5, f"Nhanh hơn\n{speedup_avg:.1f}x", ha="center", va="center", color="#C82323", fontweight="bold", fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))
    ax.text(2, max(full_run[2], fail_fast[2]) * 0.5, f"Nhanh hơn\n{speedup_p95:.1f}x", ha="center", va="center", color="#C82323", fontweight="bold", fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))
    
    ax.set_title("Biểu đồ 6: So sánh Hiệu năng giữa Full-Run (Set 3) và Fail-Fast (Set 4)", fontsize=11, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5)
    ax.set_ylabel("Giá trị thực tế", fontsize=9.5)
    ax.set_ylim(0, max(max(full_run), max(fail_fast)) * 1.15)
    ax.legend(loc="upper right", frameon=True, fontsize=9)
    apply_styling(ax)
    
    path = out_dir / "full_vs_failfast_latency.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] Da ve va luu bieu do so sanh rieng: {path}")

def main():
    if not HAS_PLOT:
        print("[LỖI] Không thể import matplotlib.")
        return
        
    print("=" * 60)
    print("  BAT DAU VE CAC BIEU DO TRUC QUAN HOA KET QUA WEEK 4")
    print("=" * 60)
    
    df, stats = load_data()
    if df is None or stats is None:
        print("[LỖI] Thiếu tệp dữ liệu so sánh.")
        return
        
    print(f"  [OK] Du lieu tai thanh cong: {len(df)} hang.")
    os.makedirs(OUT_DIR, exist_ok=True)
    
    plot_fpr_vs_ntest(df, stats, OUT_DIR)
    plot_error_types_comparison(df, stats, OUT_DIR)
    plot_fpr_by_topic(df, OUT_DIR)
    plot_latency_comparison(stats, OUT_DIR)
    plot_description_lengths(OUT_DIR)
    plot_full_vs_failfast_comparison(stats, OUT_DIR)
    
    print(f"\n  [OK] Hoan tat! Tat ca bieu do da duoc luu trong: {OUT_DIR}")

if __name__ == "__main__":
    main()
