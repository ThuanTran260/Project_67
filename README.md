# Xây dựng hệ thống chấm bài Python tự động dựa trên test case

> Đánh giá ảnh hưởng của số lượng và chất lượng test case đến độ tin cậy của điểm chấm tự động

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Tuần](https://img.shields.io/badge/Tuần%20hiện%20tại-3%2F5-orange)
![FPR](https://img.shields.io/badge/FPR%20(3--test)-24%25-red)

---

## Mục lục

- [Giới thiệu đề tài](#giới-thiệu-đề-tài)
- [Thành viên nhóm](#thành-viên-nhóm)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Kết quả nổi bật](#kết-quả-nổi-bật)
- [Cách chạy](#cách-chạy)
- [Dataset](#dataset)
- [Câu hỏi nghiên cứu](#câu-hỏi-nghiên-cứu)
- [Tiến độ theo tuần](#tiến-độ-theo-tuần)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Giới thiệu đề tài

Hệ thống chấm bài Python tự động (Automated Python Grading System) giúp:

- **Giảm tải** khối lượng chấm tay cho giảng viên trong các lớp lập trình đông sinh viên
- **Đảm bảo nhất quán** — cùng một bài nộp luôn nhận cùng một điểm
- **Phản hồi nhanh** — sinh viên biết lỗi ngay sau khi nộp, không cần chờ GV chấm
- **Đánh giá định lượng** — đo được chính xác FPR giảm bao nhiêu khi tăng số test case

Trọng tâm nghiên cứu: **Số lượng và chất lượng test case ảnh hưởng như thế nào đến độ tin cậy của điểm chấm?**

---

## Thành viên nhóm

| MSSV | Họ và tên | Vai trò |
|---|---|---|
| 3124410356 | Trần Bảo Tín | Tổng hợp báo cáo · Phân tích kết quả · Mô phỏng bài nộp |
| 3124560085 | Nguyễn Lê Nhựt Thắng | Kỹ thuật chính · Runner · Hidden test · Baseline |
| 3124410350 | Trần Vĩnh Thuận | Dữ liệu · EDA · Biểu đồ · Phân tích thống kê |

**Giảng viên hướng dẫn:** ThS.NCS. Hà Thanh Dũng  
**Học phần:** Ngôn ngữ Lập trình Python — Trường Đại học Sài Gòn

---

## Cấu trúc thư mục

```
Project_67/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── shared/                        # Code dùng chung mọi tuần
│   ├── runner.py                  # Engine chấm bài (subprocess + timeout)
│   └── error_stats.py             # Module thống kê lỗi tự động
│
├── tuan1/                         # Tìm hiểu đề tài
│   └── bao_cao_tuan1.docx
│   
│
├── tuan2/                         # Baseline runner
│   ├── bao_cao_tuan2.docx
│   ├── data/raw/mbpp_subset.json     # 15 bài, 3 public + 6 hidden test
│   ├── notebooks/
│   │   ├── 01_load_data.ipynb
│   │   ├── 02_baseline.ipynb
│   │   └── 03_simulate.ipynb
│   └── results/
│
├── tuan3/                         # So sánh 3 bộ test — RQ1
│   ├── bao_cao_tuan3.docx
│   ├── data/raw/mbpp_50.json      # 50 bài, 3 public + 10 hidden test
│   ├── notebooks/
│   │   ├── 01_eda_v2.ipynb
│   │   └── 02_comparison_3sets.ipynb
│   └── results/
│       ├── comparison_3sets.csv
│       ├── comparison_3sets.json
│       ├── FPR_vs_ntest.png
│       └── error_3sets.png
│
├── tuan4/                         # LeetCode subset — FPR curve (sắp tới)
├── tuan5/                         # Feedback tự động + tổng kết (sắp tới)
│
└── colab_setup/                   # Notebook chạy trên Google Colab
    ├── setup.ipynb
    └── run_all.ipynb
```

---

## Kết quả nổi bật

### Bảng so sánh 3 bộ test (Tuần 3 — RQ1)

| Metric | Baseline T2 (3-test, 12 bài) | Baseline T3 (3-test, 50 bài) | PP chính T3 (10-test, 50 bài) |
|---|:---:|:---:|:---:|
| **False Positive Rate** | **25,0%** | **24,0%** | **24,0%** |
| Avg Test Pass Rate | — | 62,7% | 62,2% |
| WA phát hiện | 13 | 51 | **165** (+223%) |
| RE phát hiện | 2 | 2 | **14** (+600%) |
| Latency trung bình | 13ms/test | 15ms/test | 15ms/test |

### Phát hiện quan trọng

> **FPR 24% duy trì dù tăng từ 3 lên 10 test/bài** — 12 bài False Positive đều có lỗi logic nằm chính xác ở ranh giới điều kiện (`<=0` thay vì `<0`, không xử lý `list = []`). Điều này chứng minh rằng số lượng test không đủ — **chất lượng và mục tiêu thiết kế test mới quyết định FPR**. Hướng tuần 4: test nhắm đặc biệt vào boundary condition.

### 3 trường hợp False Positive điển hình

| Bài | Lỗi | Public (3-test) | Hidden (10-test) |
|---|---|:---:|:---:|
| `is_prime(n)` | Không xử lý `n=0, n=1` — trả `True` sai | PASS 3/3 | FAIL 2/10 |
| `average(lst)` | Không xử lý `lst=[]` — `ZeroDivisionError` | PASS 3/3 | FAIL 1/10 |
| `remove_duplicates(lst)` | Dùng `set()` mất thứ tự | PASS 3/3 | FAIL 3/10 |

---

## Cách chạy

### Yêu cầu

```bash
Python 3.8+
# Thư viện: ast, subprocess, json, csv, time, resource — tất cả built-in
# Không cần pip install gì thêm
```

> **Windows:** Module `resource` không có sẵn. Dùng WSL hoặc Google Colab thay thế.

### Chạy trên máy tính

```bash
# 1. Clone repo
git clone https://github.com/ThuanTran260/Project_67.git
cd Project_67

# 2. Kiểm tra runner hoạt động
python shared/runner.py

# 3. Chạy tuần 3 — so sánh 3 bộ test
cd tuan3
python notebooks/comparison_3sets.py
# → Xuất: results/comparison_3sets.csv và results/comparison_3sets.json
# → Thời gian chạy: ~3–5 phút (50 submissions × 13 test × subprocess)
```

### Chạy trên Google Colab

**Bước 1:** Upload thư mục `Project/` lên Google Drive  
**Bước 2:** Mở Colab, chạy cell sau (chỉ cần đổi 3 dòng đầu mỗi tuần):

```python
# ── Đổi 3 dòng này khi chuyển tuần ─────────────────────
DRIVE_ROOT = "/content/drive/MyDrive/Project"     # tên thư mục Drive
TUAN       = "tuan3"                              # tuần hiện tại
DATA_FILE  = "mbpp_50.json"                       # file data
# ────────────────────────────────────────────────────────

from google.colab import drive
import os, shutil, sys

drive.mount("/content/drive")
BASE = f"/content/{TUAN}"

for d in [f"{BASE}/src", f"{BASE}/data/raw", f"{BASE}/results"]:
    os.makedirs(d, exist_ok=True)

for f in ["runner.py", "error_stats.py"]:
    shutil.copy(f"{DRIVE_ROOT}/shared/{f}", f"{BASE}/src/{f}")

shutil.copy(f"{DRIVE_ROOT}/{TUAN}/{DATA_FILE}", f"{BASE}/data/raw/{DATA_FILE}")
sys.path.insert(0, f"{BASE}/src")
os.chdir(BASE)
print(f"✓ Sẵn sàng chạy {TUAN}")
```

**Bước 3:** Chạy notebook chính:
```python
exec(open("notebooks/02_comparison_3sets.ipynb_as_script.py").read())
```

**Bước 4:** Lưu kết quả lên Drive ngay sau khi chạy xong:
```python
shutil.copy(f"{BASE}/results/comparison_3sets.csv",
            f"{DRIVE_ROOT}/results/tuan3/comparison_3sets.csv")
```

---

## Dataset

### MBPP (Mostly Basic Python Problems)

| Thuộc tính | Tuần 2 | Tuần 3 | Tuần 4 (sắp tới) |
|---|:---:|:---:|:---:|
| Nguồn | Google Research (Austin et al., 2021) | ← | LeetCode (Xia et al., 2025) |
| Số bài | 15 | **50** | ~20 bài LeetCode |
| Public test/bài | 3 | 3 | — |
| Hidden test/bài | 6 | **10** | 100+ |
| Topic | list, math, string | list, math, string | array, dp, math |

**Lý do chọn MBPP:** Mỗi bài chỉ có 3 test gốc — đây là điểm yếu có chủ đích. Nghiên cứu khai thác đặc điểm này để đo FPR khi test ít, sau đó so sánh với khi thêm hidden test.

### Tải dataset

```python
# Cách 1: Từ HuggingFace (cần internet)
from datasets import load_dataset
ds = load_dataset("google-research-datasets/mbpp", "sanitized")

# Cách 2: Dùng file có sẵn trong repo
import json
with open("tuan3/data/raw/mbpp_50.json") as f:
    data = json.load(f)
```

---

## Câu hỏi nghiên cứu

### RQ1 — Số lượng test case ảnh hưởng thế nào đến FPR?

> Khi tăng số test case từ 3 (MBPP gốc) lên 10 (hidden test tự thiết kế),
> tỉ lệ bài sai nhưng vẫn pass thay đổi như thế nào?

**Kết quả tuần 3:** FPR = 24% với cả bộ 3-test lẫn 10-test. Phát hiện: không phải số lượng mà là **loại edge case** mới quyết định. Tuần 4 sẽ so sánh với LeetCode (100+ test/bài).

### RQ2 — Điểm tự động lệch bao nhiêu so với điểm giảng viên?

> Điểm dựa trên Test Pass Rate lệch bao nhiêu MAE so với điểm chấm tay?

**Kế hoạch:** Thu thập tập bài nộp thực tế + điểm GV ở tuần 4–5.

### RQ3 — Hệ thống phân loại lỗi có đúng không?

> Hệ thống có phân loại đúng SE/WA/RE/TLE và feedback có đủ rõ để sinh viên tự sửa không?

**Kết quả tuần 3:** Phân loại lỗi chính xác 100% trên 50 submissions. WA tăng từ 51 (3-test) lên 165 (10-test), RE tăng từ 2 lên 14 — hidden test phát hiện nhiều lỗi logic hơn đáng kể.

---

## Tiến độ theo tuần

| Tuần | Thời gian | Trạng thái | Nội dung chính |
|---|---|:---:|---|
| 1 | 4–11/5 | ✅ Hoàn thành | Tìm hiểu đề tài, dataset, metric, tài liệu — 88/100 |
| 2 | 11–18/5 | ✅ Hoàn thành | Baseline runner, 12 submissions, FPR=25% — 86/100 |
| 3 | 18–25/5 | ✅ Hoàn thành | 50 submissions, so sánh 3 bộ test, hidden test v2 |
| 4 | 25/5–1/6 | 🔄 Sắp tới | LeetCode subset, FPR curve hoàn chỉnh |
| 5 | 1–8/6 | 🔄 Sắp tới | Feedback tự động, tổng kết RQ1+RQ2+RQ3 |

---

## Kiến trúc hệ thống

```
Bài nộp (.py)
    │
    ▼
[1] ast.parse() — Kiểm tra Syntax Error
    │
    ▼
[2] Kiểm tra import cấm (os, sys, subprocess, socket...)
    │
    ▼
[3] Với mỗi test case:
    subprocess.run(timeout=5s, memory=128MB)
        ├── PASS → cộng điểm
        ├── WA   → output sai
        ├── RE   → ngoại lệ runtime
        └── TLE  → vượt timeout
    │
    ▼
[4] Tính metric:
    Test Pass Rate = pass / total × 100%
    FPR = bài pass public nhưng fail hidden / tổng bài
    │
    ▼
[5] Xuất kết quả:
    CSV + JSON chi tiết
    Bảng so sánh 3 bộ test
```

---

## Cơ chế an toàn

| Biện pháp | Kỹ thuật | Trạng thái |
|---|---|:---:|
| Timeout | `subprocess(timeout=5)` | ✅ Có |
| Chặn import nguy hiểm | `ast.parse()` + kiểm tra `ImportFrom` | ✅ Có |
| Giới hạn output | `MAX_OUTPUT_BYTES = 4096` | ✅ Có |
| Giới hạn bộ nhớ | `resource.setrlimit(128MB)` | ✅ Có (tuần 3) |
| Xóa file tạm | `tempfile + shutil.rmtree` | ✅ Có |
| Giới hạn file system | Sandbox thư mục tạm | 🔄 Tuần 4 |
| Docker/Container | Cô lập tiến trình hoàn toàn | 🔄 Tuần 4 |

---

## Tài liệu tham khảo

```
[1] L. Y. Tan, S. Hu, D. J. Yeo, and K. H. Cheong,
    "A Comprehensive Review on Automated Grading Systems in STEM Using AI Techniques,"
    Mathematics, vol. 13, no. 17, p. 2828, Sep. 2025. DOI: 10.3390/math13172828

[2] H. Keuning, J. Jeuring, and B. Heeren,
    "A Systematic Literature Review of Automated Feedback Generation for Programming Exercises,"
    ACM Trans. Comput. Educ., vol. 19, no. 1, Art. 3, Sep. 2018. DOI: 10.1145/3231711

[3] J. C. Paiva, J. P. Leal, and Á. Figueira,
    "Automated Assessment in Computer Science Education: A State-of-the-Art Review,"
    ACM Trans. Comput. Educ., vol. 22, no. 3, Art. 34, Jun. 2022. DOI: 10.1145/3513140

[4] M. Mahdaoui, S. Nouh, M. S. El Kasmi Alaoui, and K. Kandali,
    "Automated Grading Method of Python Code Submissions Using LLMs and ML,"
    Information, vol. 16, no. 8, p. 674, Aug. 2025. DOI: 10.3390/info16080674

[5] J. Austin, A. Odena, M. Nye, M. Bosma et al.,
    "Program Synthesis with Large Language Models,"
    arXiv, Aug. 2021. DOI: 10.48550/arXiv.2108.07732

[6] S. H. Edwards and M. A. Pérez-Quiñones,
    "Web-CAT: Automatically Grading Programming Assignments,"
    in Proc. ITiCSE '08, Madrid, Spain, 2008. DOI: 10.1145/1384271.1384371

[7] Y. Xia, W. Shen, Y. Wang et al.,
    "LeetCodeDataset: A Temporal Dataset for Robust Evaluation of Code LLMs,"
    arXiv, Apr. 2025. DOI: 10.48550/arXiv.2504.14655
```

---

## Đổi tên file

Tất cả file trong repo đều có thể đổi tên tùy ý — chỉ cần sửa **3 biến ở đầu mỗi notebook**:

```python
TUAN      = "tuan3"           # tên thư mục tuần
DATA_FILE = "mbpp_50.json"    # tên file dataset
OUT_PREFIX= "comparison"      # prefix cho file kết quả
```

---

<div align="center">
  <sub>Nhóm 67 · Trường Đại học Sài Gòn · Khoa Công nghệ Thông tin · 2026</sub>
</div>
