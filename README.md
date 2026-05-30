# Nhóm 67 — Automated Python Grading System
## Tuần 2: Xây dựng Baseline Runner

**Môn:** Ngôn ngữ Lập trình Python  
**GV:** ThS.NCS. Hà Thanh Dũng  
**Mốc báo cáo:** 18/5/2026

---

## Thành viên

| MSSV | Họ tên | Vai trò |
|---|---|---|
| 3124410356 | Trần Bảo Tín (A) | EDA + Biểu đồ + Báo cáo |
| 3124560085 | Nguyễn Lê Nhựt Thắng (B) | Runner + Kỹ thuật |
| 3124410350 | Trần Vĩnh Thuận (C) | Dữ liệu + Môi trường |

---

## Mục tiêu tuần 2

Xây dựng **baseline test-case runner** — chấm bài Python tự động qua subprocess, phân loại lỗi SE/WA/RE/TLE, đo False Positive Rate trên tập bài nộp mô phỏng.

---

## Kết quả chính

### Baseline — Solution mẫu (15 bài MBPP)

| Metric | Bộ Public (3 test/bài) | Bộ Hidden (6 test/bài) |
|---|:---:|:---:|
| Pass rate | 15/15 (100%) | 15/15 (100%) |
| Latency trung bình | 0,013s/test | 0,012s/test |
| Lỗi WA/RE/TLE | 0 | 0 |

→ Bộ test hợp lệ, runner hoạt động đúng.

### Mô phỏng bài nộp sinh viên (12 bài có lỗi cố ý)

| Metric | Bộ Public (3 test/bài) | Bộ Hidden (6 test/bài) |
|---|:---:|:---:|
| Bài pass toàn bộ | 5/12 (41,67%) | 2/12 (16,67%) |
| **False Positive Rate** | — | **25,0% (3/12)** |
| Lỗi WA phát hiện | 13 | 22 |
| Lỗi RE phát hiện | 2 | 7 |
| Lỗi SE phát hiện | 3 | 6 |

### 3 bài False Positive (pass public, fail hidden)

| ID | Task | Lỗi | Nguyên nhân |
|---|---|---|---|
| SV007 | remove_duplicates | `list(set(lst))` | `set` không giữ thứ tự |
| SV008 | average | `sum(lst)/len(lst)` | Không xử lý list rỗng → ZeroDivisionError |
| SV009 | is_prime | range(2,n) không check n<2 | n=0,1 trả True sai |

---

## Cấu trúc thư mục (branch Tuan2)

```
Project_67/
├── data/
│   ├── raw/
│   │   └── mbpp_subset.json        # 15 bài MBPP · 3 public + 6 hidden/bài
│   └── processed/
│       └── mbpp_clean.json         # Dataset sau làm sạch
│
├── notebooks/
│   ├── 00_setup.ipynb              # Thiết lập môi trường Colab
│   ├── 01_load_data.ipynb          # Đọc và làm  MBPP  
│   ├── 02_baseline.ipynb           # Chạy runner trên 15 bài solution mẫu
│   ├── 03_simulate.ipynb           # Mô phỏng 12 bài nộp có lỗi
|   ├── 04_visualize.ipynb          # EDA + 4 biểu đồ
|   └── Runner.ipynb                # Chạy tất cả
│
├── src/
│   └── runner.py                   # Engine chấm bài (subprocess · timeout 5s)
│
├── results/
│   ├── baseline_summary.csv        # 15/15 pass · lat=0.013s/test
│   ├── metric_summary.json         # FPR=0% (solution mẫu)
│   ├── student_simulation.csv      # FPR=25% (12 bài nộp)
│   ├── student_simulation.json
│   ├── bieu_do_1_tpr.png           # Test Pass Rate public vs hidden
│   ├── bieu_do_2_loi.png           # Phân loại lỗi SE/WA/RE/TLE
│   └── data_analysis.png           # Phân bố dữ liệu
│
└── Nhom67_Tuan2_18.docx
```

---

## Cách chạy (Google Colab)

```python
# Bước 1: Chạy 00_setup.ipynb — kết nối Drive, tạo thư mục
# Bước 2: Chạy 01_load_data.ipynb — EDA + làm sạch dữ liệu
# Bước 3: Chạy 02_baseline.ipynb — baseline solution mẫu
# Bước 4: Chạy 03_simulate.ipynb — mô phỏng bài nộp + tính FPR
```

> **Yêu cầu:** Folder `Project` nằm trong `MyDrive` của Google Drive.

---

## Kỹ thuật nổi bật

- **Runner:** Python `subprocess` + `timeout=5s` + phân loại SE/WA/RE/TLE
- **AST check:** Cơ bản (kiểm tra syntax)
- **FPR:** Đo theo đơn vị bài nộp — `FP / tổng bài nộp`
- **Dataset:** MBPP subset 15 bài · topic: list=5, math=5, string=5

---

## Hạn chế và hướng tuần 3

| Hạn chế tuần 2 | Cải tiến tuần 3 |
|---|---|
| 15 bài MBPP, 12 bài nộp | Mở rộng lên 50 bài MBPP, 50 bài nộp |
| Hidden test 6/bài cố định | Hidden test v2: 6–10/bài (Bell Curve) |
| Không giới hạn memory | Thêm memory limit bằng `psutil` (128MB) |
| AST check cơ bản | Thêm danh sách import cấm và banned functions |
| FPR 25,0% | Mục tiêu giảm FPR qua hidden test tốt hơn |
