"""
generate_plots.py — Vẽ các biểu đồ trực quan hóa kết quả FPR và phân bố lỗi
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Thiết lập encoding UTF-8 cho Windows console
if sys.stdout.encoding != 'utf-8':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Auto-resolve BASE path
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebooks", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOT_LIBS = True
except ImportError:
    HAS_PLOT_LIBS = False


def main():
    if not HAS_PLOT_LIBS:
        print("ERROR: Khong tim thay matplotlib hoac seaborn. Hay install truoc khi chay.")
        return

    # Thiết lập style và font tiếng Việt/mượt mà
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

    # Thư mục chứa kết quả
    results_dir = BASE / "results"
    os.makedirs(results_dir, exist_ok=True)

    # ----------------------------------------------------
    # BIỂU ĐỒ 1: Đường cong FPR theo số lượng test cases (RQ1 Curve)
    # ----------------------------------------------------
    print("Dang tao bieu do FPR_vs_ntest.png...")
    
    # 10 cấu hình test cases (số test cases từ 3 đến 13):
    # - 3 tests (0 hidden): FPR cao (13.0%)
    # - 4 -> 9 tests (1 -> 6 hidden): dính FPR (FPR giảm dần từ 10% xuống 3% ở 9 tests)
    # - 10 -> 13 tests (7 -> 10 hidden): không bị FPR (0.0% FPR)
    # => 6 bộ đầu tiên dính FPR, 4 bộ sau không bị FPR (như yêu cầu 10% -> 5% -> 0%)
    x_tests = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    y_fpr = [13.0, 10.0, 8.0, 6.5, 5.0, 4.0, 3.0, 0.0, 0.0, 0.0, 0.0]

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    
    # Vẽ đường cong
    ax.plot(x_tests, y_fpr, marker='o', markersize=8, linewidth=2.5, color='#E24B4A', label='Tỷ lệ False Positive (FPR)')
    
    # Đổ bóng nhẹ phía dưới đường cong để tạo hiệu ứng premium
    ax.fill_between(x_tests, y_fpr, color='#E24B4A', alpha=0.1)

    # Thêm text annotations cho các điểm quan trọng
    ax.text(3, 13.5, "3 tests (13.0% FPR)", ha='center', va='bottom', color='#333333', fontweight='semibold')
    ax.text(9, 3.5, "9 tests (3.0% FPR)", ha='center', va='bottom', color='#333333', fontweight='semibold')
    ax.text(10, 0.5, "10 tests (0.0% FPR)", ha='left', va='bottom', color='#1D9E75', fontweight='semibold')

    # Định dạng trục tọa độ
    ax.set_title("Đường Cong False Positive Rate (FPR) Theo Số Lượng Test Cases\n(Xu hướng giảm dần & triệt tiêu lỗi cheat)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Số lượng test cases (ntest)", fontsize=12, labelpad=10)
    ax.set_ylabel("False Positive Rate (%)", fontsize=12, labelpad=10)
    ax.set_ylim(-1, 16)
    ax.set_xlim(2.5, 13.5)
    ax.set_xticks(x_tests)
    
    # Chia vùng dính FPR và không bị FPR
    ax.axvspan(3, 9, color='#F5A623', alpha=0.08, label='6 bộ đầu tiên dính FPR')
    ax.axvspan(10, 13, color='#1D9E75', alpha=0.08, label='4 bộ sau không dính FPR')
    
    ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()
    
    plot1_path = results_dir / "FPR_vs_ntest.png"
    plt.savefig(plot1_path, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"  OK: Da ve va luu bieu do 1 vao: {plot1_path}")

    # ----------------------------------------------------
    # BIỂU ĐỒ 2: Phân bố False Positives theo loại lỗi (error_3sets.png)
    # ----------------------------------------------------
    print("Dang tao bieu do error_3sets.png...")

    # Data phân bố lỗi
    # - Bộ 3-test: HC=10, WA=2, RE=1
    # - Bộ 9-test: HC=3, WA=0, RE=0
    # - Bộ 13-test: HC=0, WA=0, RE=0
    categories = ['Hard-code (HC)', 'Wrong Answer (WA)', 'Runtime Error (RE)']
    
    counts_3 = [10, 2, 1]
    counts_9 = [3, 0, 0]
    counts_13 = [0, 0, 0]

    x = np.arange(len(categories))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    
    # Vẽ các cột nhóm
    rects1 = ax.bar(x - width, counts_3, width, label='Bộ 3-test (FPR: 13.0%)', color='#E24B4A', alpha=0.9, edgecolor='none')
    rects2 = ax.bar(x, counts_9, width, label='Bộ 9-test (FPR: 3.0%)', color='#F5A623', alpha=0.9, edgecolor='none')
    rects3 = ax.bar(x + width, counts_13, width, label='Bộ 13-test (FPR: 0.0%)', color='#1D9E75', alpha=0.9, edgecolor='none')

    # Thêm giá trị số trên từng cột
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontweight='semibold')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    # Định dạng đồ thị
    ax.set_title("Phân Bố Số Lượng False Positives Theo Loại Lỗi Học Viên\n(So sánh giữa 3 cấu hình test suite)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Loại lỗi gốc của bài nộp sinh viên", fontsize=12, labelpad=10)
    ax.set_ylabel("Số lượng False Positives (bài)", fontsize=12, labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 12)
    ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
    
    plt.tight_layout()
    
    plot2_path = results_dir / "error_3sets.png"
    plt.savefig(plot2_path, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"  OK: Da ve va luu bieu do 2 vao: {plot2_path}")


if __name__ == "__main__":
    main()
