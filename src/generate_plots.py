"""
generate_plots.py — Vẽ các biểu đồ trực quan hóa kết quả FPR và phân bố lỗi
Dùng số liệu THỰC TẾ từ comparison_3sets.csv và comparison_3sets.json — không hardcode.
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path

# Auto-resolve BASE path
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebooks", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)

try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

COMPARISON_CSV  = BASE / "results" / "comparison_3sets.csv"
COMPARISON_JSON = BASE / "results" / "comparison_3sets.json"
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
    So sánh 3 bộ test: Set 1 (3 tests), Set 2 (9 tests), Set 3 (13 tests)
    """
    if not stats:
        return
        
    x_tests = [3, 9, 13]
    y_fpr = [
        stats["set1"]["fpr_pct"],
        stats["set2"]["fpr_pct"],
        stats["set3"]["fpr_pct"]
    ]
    
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    
    # Vẽ đường biểu diễn
    ax.plot(x_tests, y_fpr, marker="o", markersize=8, linewidth=2.5,
            color="#E24B4A", label="False Positive Rate (%)", zorder=3)
    ax.fill_between(x_tests, y_fpr, alpha=0.1, color="#E24B4A")
    
    # Annotate từng điểm
    for x, y, fp_count in zip(x_tests, y_fpr, [stats["set1"]["fp_count"], stats["set2"]["fp_count"], stats["set3"]["fp_count"]]):
        ax.annotate(
            f"{y}% ({fp_count}/50)",
            xy=(x, y),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#C82323"
        )
        
    ax.set_title("Biểu đồ 1: False Positive Rate (FPR) Giảm Dần Theo Số Lượng Test Case", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Số lượng test case mỗi bài toán", fontsize=10, labelpad=8)
    ax.set_ylabel("FPR (%)", fontsize=10, labelpad=8)
    ax.set_xlim(1.5, 14.5)
    ax.set_ylim(-2, max(y_fpr) + 8)
    ax.set_xticks(x_tests)
    ax.set_xticklabels(["3 tests\n(Set 1: Public)", "9 tests\n(Set 2: 3P+6H)", "13 tests\n(Set 3: 3P+10H)"], fontsize=9)
    apply_styling(ax)
    
    path = out_dir / "FPR_vs_ntest.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Đã vẽ và lưu: {path}")

def plot_error_types_comparison(stats, out_dir):
    """
    Biểu đồ 2: So sánh số lỗi SE/WA/RE/TLE/MLE phát hiện được qua 3 bộ test.
    """
    if not stats:
        return
        
    err_types = ["SE", "WA", "RE", "TLE", "MLE"]
    set1_vals = [stats["set1"]["errors"].get(e, 0) for e in err_types]
    set2_vals = [stats["set2"]["errors"].get(e, 0) for e in err_types]
    set3_vals = [stats["set3"]["errors"].get(e, 0) for e in err_types]
    
    x = np.arange(len(err_types))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    
    rects1 = ax.bar(x - width, set1_vals, width, label="Set 1 (3 Public)", color="#5C9BD1")
    rects2 = ax.bar(x, set2_vals, width, label="Set 2 (3P+6H)", color="#F29C38")
    rects3 = ax.bar(x + width, set3_vals, width, label="Set 3 (3P+10H)", color="#3CB371")
    
    # Add values on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f"{int(height)}",
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha="center", va="bottom", fontsize=8, fontweight="bold")
                            
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    
    ax.set_title("Biểu đồ 2: Phân Phối Lỗi SE, WA, RE, TLE, MLE Phát Hiện Bởi 3 Tập Test Cases", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Loại lỗi", fontsize=10, labelpad=8)
    ax.set_ylabel("Số lỗi phát hiện", fontsize=10, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(err_types, fontsize=9)
    ax.set_ylim(0, max(max(set1_vals), max(set2_vals), max(set3_vals)) + 8)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#DDDDDD")
    apply_styling(ax)
    
    path = out_dir / "error_types_comparison.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Đã vẽ và lưu: {path}")

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
                ha="center", va="bottom", fontsize=9, fontweight="bold")
                
    ax.set_title("Biểu đồ 3: False Positive Rate của Bộ 3 Public Theo Chủ Đề Bài Toán", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Chủ đề bài toán", fontsize=10, labelpad=8)
    ax.set_ylabel("FPR (%)", fontsize=10, labelpad=8)
    ax.set_ylim(0, max(fprs) + 12)
    apply_styling(ax)
    
    path = out_dir / "fpr_by_topic.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Đã vẽ và lưu: {path}")

def plot_description_lengths(out_dir):
    """
    Biểu đồ 4: Phân phối độ dài mô tả (ký tự) và số lượng test cases mỗi bài (gồm public và hidden).
    """
    if not os.path.exists(HIDDEN_V2_JSON):
        return
        
    with open(HIDDEN_V2_JSON, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
        
    # Tính toán các giá trị trung bình
    char_lengths = [len(t['text']) for t in tasks]
    word_lengths = [len(t['text'].split()) for t in tasks]
    pub_test_counts = [len(t['public_tests']) for t in tasks]
    hid_test_counts = [len(t['hidden_tests']) for t in tasks]
    total_test_counts = [len(t['public_tests']) + len(t['hidden_tests']) for t in tasks]
    
    avg_char = sum(char_lengths) / len(tasks)
    avg_word = sum(word_lengths) / len(tasks)
    avg_pub = sum(pub_test_counts) / len(tasks)
    avg_hid = sum(hid_test_counts) / len(tasks)
    avg_total = sum(total_test_counts) / len(tasks)
    
    print("\n  THÔNG SỐ TRUNG BÌNH THỰC TẾ:")
    print(f"    - Độ dài mô tả trung bình (ký tự)  : {avg_char:.2f} ký tự")
    print(f"    - Độ dài mô tả trung bình (từ)     : {avg_word:.2f} từ")
    print(f"    - Số public test case trung bình   : {avg_pub:.2f} tests")
    print(f"    - Số hidden test case trung bình   : {avg_hid:.2f} tests")
    print(f"    - Tổng số test case trung bình/bài : {avg_total:.2f} tests")
    print()
    
    # Tạo hình ảnh lớn chứa 2 subplot side-by-side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)
    
    # ── Subplot 1: Phân bố độ dài Description (Số ký tự) ──────────────────
    n_bins = 20
    counts_hist, bins, patches = ax1.hist(char_lengths, bins=n_bins, color="#4682B4", edgecolor="white", alpha=0.85, zorder=2)
    ax1.axvline(avg_char, color="red", linestyle="--", linewidth=1.5, label=f"TB: {int(avg_char)}", zorder=3)
    ax1.legend(loc="upper right")
    ax1.set_title("Bieu do 1: Phan bo do dai Description", fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlabel("So ky tu", fontsize=9, labelpad=5)
    ax1.set_ylabel("So bai toan", fontsize=9, labelpad=5)
    apply_styling(ax1)
    
    # ── Subplot 2: Số Test Case mỗi bài (bao gồm cả public + hidden) ─────
    unique_tests, test_counts = np.unique(total_test_counts, return_counts=True)
    bars = ax2.bar(unique_tests, test_counts, color="#FF7F50", width=0.6, alpha=0.85, edgecolor="white", zorder=2)
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                     f"{int(h)} bài", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax2.axvline(avg_total, color="green", linestyle="--", linewidth=1.5, label=f"TB: {avg_total:.1f}", zorder=3)
    ax2.legend(loc="upper right")
    ax2.set_title("Bieu do 2: So Test Case moi bai (public & hidden)", fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("So test case", fontsize=9, labelpad=5)
    ax2.set_ylabel("So bai toan", fontsize=9, labelpad=5)
    ax2.set_xlim(min(total_test_counts) - 1.5, max(total_test_counts) + 1.5)
    ax2.set_xticks(range(min(total_test_counts) - 1, max(total_test_counts) + 2))
    ax2.set_ylim(0, max(test_counts) + 3)
    apply_styling(ax2)
    
    # Lưu biểu đồ ghép
    path = out_dir / "description_lengths_distribution.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Đã vẽ và lưu biểu đồ ghép: {path}")

def main():
    if not HAS_PLOT:
        print("[LỖI] Không thể import matplotlib.")
        return
        
    print("=" * 60)
    print("  BẮT ĐẦU VẼ CÁC BIỂU ĐỒ TRỰC QUAN HÓA KẾT QUẢ")
    print("=" * 60)
    
    df, stats = load_data()
    if df is None:
        return
        
    print(f"  ✓ Dữ liệu tải thành công: {len(df)} hàng.")
    os.makedirs(OUT_DIR, exist_ok=True)
    
    plot_fpr_vs_ntest(df, stats, OUT_DIR)
    plot_error_types_comparison(stats, OUT_DIR)
    plot_fpr_by_topic(df, OUT_DIR)
    plot_description_lengths(OUT_DIR)
    
    print(f"\n  ✓ Hoàn tất! Tất cả biểu đồ đã được lưu trong: {OUT_DIR}")

if __name__ == "__main__":
    main()
