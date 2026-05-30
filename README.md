# Nhóm 67 — Automated Python Grading System
## Tuần 3: Hidden Test v2 + Runner v2 + So sánh 3 bộ test

**Môn:** Ngôn ngữ Lập trình Python  
**GV:** ThS.NCS. Hà Thanh Dũng  
**Mốc báo cáo:** 25/5/2026  


---

## Thành viên

| MSSV | Họ tên | Vai trò |
|---|---|---|
| 3124410356 | Trần Bảo Tín  | Demo + Feedback + Báo cáo |
| 3124560085 | Nguyễn Lê Nhựt Thắng  | Kỹ thuật chính |
| 3124410350 | Trần Vĩnh Thuận  | Dữ liệu + Biểu đồ |

---

## Mục tiêu tuần 3

So sánh 3 bộ test để trả lời **RQ1**: tăng số lượng hidden test có giúp phát hiện bài sai tốt hơn không?

---

## Kết quả chính

### FPR giảm dần theo số lượng test case (RQ1)

| Bộ test | Số test/bài | False Positive | FPR (tổng) | FAR (FP/47 buggy) |
|---|:---:|:---:|:---:|:---:|
| Set 1 — 3 Public | 3,0 | 8/50 | **16,0%** | 17,0% |
| Set 2 — 3P+6H | 9,0 | 3/50 | **6,0%** | 6,4% |
| Set 3 — 3P+6-10H | 10,7 | 2/50 | **4,0%** | 4,3% |

→ Tăng hidden test từ 0 lên 10 giúp FPR giảm 75% (từ 16% xuống 4%).

### Baseline — Solution mẫu (50 bài MBPP)

| Metric | Giá trị |
|---|---|
| Pass rate | 50/50 (100%) |
| Latency public | 0,062s/test |
| Latency hidden | 0,063s/test |
| Elapsed | 4,79s (ThreadPoolExecutor 8 luồng) |

### Phân bố lỗi phát hiện được

| Loại lỗi | Set 1 | Set 2 | Set 3 |
|---|:---:|:---:|:---:|
| SE | 3 | 9 | 9 |
| WA | 37 | 114 | 131 |
| RE | 62 | 185 | 237 |
| TLE | 0 | 0 | 0 |
| MLE | 0 | 0 | 0 |

---

## Cấu trúc thư mục (branch Tuan3)

```
Project_67/
├── Nhom67_Tuan3_18.docx
│
├── data/
│   ├── raw/
│   │   └── mbpp_50.json              # 50 bài · 3 public + 6 hidden/bài  
│   └── processed/
│       ├── hidden_v2.json            # Set 3: 3 pub + 6–10 hidden (Bell Curve)
│       ├── mbpp_clean.json           # Set 2: 3 pub + 6 hidden cố định
│       └── submissions_50.json       # 50 bài nộp mô phỏng (func_name khớp hidden_v2)
│
├── notebooks/
│   ├── 00_setup.ipynb                # Thiết lập môi trường Colab
│   ├── 01_eda_v2.ipynb               # EDA 50 bài MBPP
│   ├── 02_runner_v2.ipynb            # So sánh 3 bộ test → kết quả RQ1
│   ├── 03_simulate_v2.ipynb          # Mô phỏng 50 bài nộp sinh viên
│   ├── 04_visualize_v3.ipynb         # Vẽ biểu đồ từ CSV thực tế
│   ├── 05_comparison.ipynb           # So sánh hiệu quả phát hiện lỗi
│   ├── 06_baseline.ipynb             # Baseline evaluation 8 bước
│   └── All_Run_final.ipynb           # Chạy toàn bộ pipeline (52 cells)
│
├── src/
│   ├── runner_v2.py                  # Engine: psutil · 1s timeout · 128MB · _classify_re()
│   ├── error_stats.py                # Thống kê lỗi tự động · hỗ trợ MLE
│   ├── comparison_3sets.py           # So sánh 3 bộ test → RQ1
│   ├── simulate_v2.py                # Copy submissions_50_v2 raw → processed
│   ├── run_grading_v2.py             # Chấm 50 bài nộp → error_analysis_v2
│   ├── run_baseline.py               # Baseline song song (ThreadPoolExecutor 8 luồng)
│   ├── generate_plots.py             # Vẽ biểu đồ từ CSV thực tế
│   └── compare_topics.py             # Phân tích phân bố topic
│
└── results/
    ├── comparison_3sets.csv/json     # FPR: 16% → 6% → 4%
    ├── baseline_summary.csv/json     # 50/50 pass · elapsed=4.79s
    ├── error_analysis_v2.csv/json    # Chi tiết chấm bài + traceback
    ├── FPR_vs_ntest.png              # Đường cong FPR giảm dần (RQ1)
    ├── error_types_comparison.png    # SE/WA/RE/TLE so sánh 3 bộ
    ├── fpr_by_topic.png              # FPR theo topic
    ├── description_lengths_distribution.png
    ├── topic_distribution.png
    └── baseline_latency.png
```

---

## Cách chạy (Google Colab)

```python
# Upload All_Run_final.ipynb lên Drive rồi mở bằng Colab
# Chạy từ trên xuống — không bỏ qua bước nào

# Hoặc chạy tuần tự từng notebook:
# 00_setup → 01_eda_v2 → 03_simulate_v2 → 06_baseline → 02_runner_v2 → 04_visualize_v3
```

> **Yêu cầu:** Folder `Project` nằm trong `MyDrive`. FOLDER_ID đã được cấu hình trong `00_setup.ipynb`.

---

## Kỹ thuật nổi bật

### runner_v2.py — Cải tiến so với tuần 2

| Tính năng | Tuần 2 | Tuần 3 |
|---|---|---|
| Memory limit | Không | psutil 128MB |
| Timeout | 5s | 1s |
| Import check | Cơ bản | 10 module cấm + banned_names |
| Tách RE chi tiết | Không | `_classify_re()` → ZeroDivision/IndexError/TypeError/... |
| Thư mục tạm | Không | `tempfile.mkdtemp()` |
| Thống kê lỗi | Thủ công | `error_stats.py` tự động theo task |

### hidden_v2.json — Bell Curve distribution

```
Task  1– 5  →  6 hidden tests  (5 bài)
Task  6–15  →  7 hidden tests  (10 bài)
Task 16–35  →  8 hidden tests  (20 bài)
Task 36–45  →  9 hidden tests  (10 bài)
Task 46–50  → 10 hidden tests  (5 bài)
Trung bình: 8,0 test/bài
```

---

## Câu hỏi nghiên cứu

**RQ1:** Tăng số lượng hidden test có giảm FPR không?  
→ **Có.** FPR giảm từ 16,0% (3 test) → 6,0% (9 test) → 4,0% (10,7 test trung bình).

**RQ3:** Loại lỗi nào phổ biến nhất?  
→ **RE** chiếm tỷ lệ cao nhất trong hidden test (237 lỗi ở Set 3) do nhiều bài không xử lý edge case (list rỗng, n=0, chuỗi rỗng).

