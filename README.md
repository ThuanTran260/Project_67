# Automated Python Grading System với Kiểm thử ẩn và Phản hồi tự động

**Đề tài**: Hidden-Test-Based Automated Python Grading with Error-Type Feedback  
**Nhóm**: 67  
**Ngôn ngữ**: Python 3.10+

Hệ thống chấm điểm mã nguồn Python tự động được xây dựng dựa trên tập dữ liệu **100 bài toán MBPP** kết hợp với **100 bài nộp mô phỏng** (SV001–SV100) có chứa lỗi logic hoặc hành vi nguy hiểm để đánh giá độ chính xác, tính an toàn của Sandbox và giá trị sư phạm của phản hồi tự động.

---

## 1. Thành phần Hệ thống & Cấu trúc Thư mục

```
Project/
├── data/
│   ├── raw/                    # Dữ liệu raw MBPP và submissions ban đầu
│   └── processed/              # Dữ liệu đã đồng bộ
│       ├── hidden_v2.json      # 100 bài toán + public/hidden test cases
│       ├── mbpp_clean.json     # 100 bài toán + 6 hidden tests/bài (Set 2)
│       └── submissions_50.json # 100 bài nộp mô phỏng (SV001–SV100, tên file giữ nguyên để tương thích)
├── results/                    # Biểu đồ PNG và kết quả CSV/JSON
├── report/                     # Báo cáo tuần 3 và tuần 4
├── src/                        # Mã nguồn lõi
│   ├── runner_v3.py            # Sandbox v3: Fail-Fast + Docker + tách RE chi tiết
│   ├── feedback.py             # Sinh phản hồi tự động tiếng Việt
│   ├── diff_testing.py         # Property-based differential testing (sinh input ngẫu nhiên)
│   ├── harden_hidden_tests.py  # Làm khó hidden test cases tự động
│   ├── test_sandbox.py         # Stress-test bảo mật sandbox (13 kịch bản)
│   ├── comparison_3sets.py     # So sánh 4 cấu hình chấm → comparison_week4.csv
│   ├── generate_plots.py       # Vẽ 6 biểu đồ từ comparison_week4.csv
│   ├── run_grading_v2.py       # Chấm 100 bài nộp → error_analysis_v2.csv
│   ├── run_baseline.py         # Kiểm chứng solution chuẩn (50/50 PASS)
│   ├── regenerate_all.py       # Đồng bộ toàn bộ dataset + gọi harden_hidden_tests
│   ├── simulate_v3.py          # Đồng bộ bài nộp từ raw → processed
│   └── error_stats.py          # Tính FPR, FAR, thống kê lỗi, xuất CSV
├── notebooks/
│   ├── 00_setup_v3.ipynb       # Thiết lập môi trường
│   ├── 01_eda_v3.ipynb         # EDA: phân tích 100 bài MBPP
│   ├── 02_runner_v3.ipynb      # Demo Sandbox v3 (AST, TLE, MLE, feedback)
│   ├── 03_simulate_v3.ipynb    # Mô phỏng 100 bài nộp
│   ├── 05_comparison_v3.ipynb  # So sánh 4 cấu hình → comparison_week4.csv
│   ├── 06_baseline.ipynb       # Kiểm chứng baseline
│   ├── 07_all_in_one.ipynb     # Chạy toàn bộ pipeline end-to-end
│   └── 08_streamlit_app.ipynb  # Khởi chạy Streamlit app trên Colab
├── grade.py                    # CLI chấm bài đơn lẻ
├── app.py                      # Web Demo Streamlit
├── requirements.txt            # Thư viện cần thiết
└── README.md
```

---

## 2. Môi trường chạy

Dự án hỗ trợ **hai môi trường**: Google Colab (môi trường chính của nhóm) và Local Machine (để clone và chạy độc lập).

---

### 2A. Google Colab (Môi trường chính)

Toàn bộ pipeline của nhóm được phát triển và chạy trên **Google Colab** kết hợp **Google Drive**. Thư mục gốc mặc định là `/content/drive/MyDrive/Project`.

#### Bước 1 — Kết nối Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

#### Bước 2 — Upload toàn bộ project lên Drive

Tải thư mục `Project/` lên Google Drive tại đường dẫn `My Drive/Project/`. Đảm bảo cấu trúc thư mục giống hệt mục 1.

#### Bước 3 — Cài đặt thư viện

Chạy cell sau trong bất kỳ notebook nào trước khi bắt đầu:

```python
!pip install psutil pandas matplotlib seaborn -q
# Chỉ cần cho Web Demo (app.py):
!pip install streamlit streamlit-ace autopep8 -q
```

#### Bước 4 — Thiết lập BASE path

Tất cả script đã tự động resolve `BASE`:

```python
import os, sys
from pathlib import Path

BASE = Path("/content/drive/MyDrive/Project")
sys.path.insert(0, str(BASE / "src"))
```

Nếu chạy từ thư mục con (`notebooks/`, `src/`...), script sẽ tự detect và điều chỉnh.

#### Bước 5 — Chạy toàn bộ pipeline (khuyến nghị)

Mở và chạy `notebooks/07_all_in_one.ipynb` — notebook này chạy end-to-end toàn bộ pipeline theo thứ tự đúng:

```
regenerate_all.py  →  run_baseline.py  →  run_grading_v2.py
→  comparison_3sets.py  →  generate_plots.py
```

> **Lưu ý**: `regenerate_all.py` sẽ tự động bị bỏ qua nếu `hidden_v2.json` và `submissions_50.json` đã tồn tại, tránh ghi đè dữ liệu đang ổn định.

#### Chạy Web Demo trên Colab

Vì Colab không có localhost, dùng `pyngrok` để expose Streamlit:

```python
!pip install pyngrok streamlit streamlit-ace autopep8 -q
import subprocess, threading
from pyngrok import ngrok

def run_streamlit():
    subprocess.run(["streamlit", "run", "/content/drive/MyDrive/Project/app.py",
                    "--server.port", "8501", "--server.headless", "true"])

threading.Thread(target=run_streamlit, daemon=True).start()

import time; time.sleep(5)
public_url = ngrok.connect(8501)
print(f"Web Demo URL: {public_url}")
```

Hoặc chạy notebook `08_streamlit_app.ipynb` đã có sẵn.

---

### 2B. Local Machine (Máy tính cá nhân)

Dùng khi muốn clone repository và chạy độc lập, không cần Google Drive.

#### Yêu cầu hệ thống

- Python 3.10+
- pip
- (Tuỳ chọn) Docker Desktop — để bật chế độ Docker Sandbox thật trong `runner_v3.py`

#### Bước 1 — Clone và cài thư viện

```bash
git clone <repository_url>
cd Project
pip install -r requirements.txt
```

Nội dung `requirements.txt` cần có:

```
psutil
pandas
matplotlib
seaborn
streamlit
streamlit-ace
autopep8
```

#### Bước 2 — Khởi tạo dữ liệu

```bash
python src/regenerate_all.py
```

Lệnh này đồng bộ `hidden_v2.json`, `mbpp_clean.json`, `submissions_50.json` và tự động gọi `harden_hidden_tests.py`.

#### Bước 3 — Chạy pipeline thực nghiệm

```bash
# Kiểm chứng solution chuẩn (phải đạt 100/100 PASS)
python src/run_baseline.py

# Chấm 100 bài nộp mô phỏng → error_analysis_v2.csv
python src/run_grading_v2.py

# So sánh 4 cấu hình chấm → comparison_week4.csv
python src/comparison_3sets.py

# Vẽ 6 biểu đồ → results/*.png
python src/generate_plots.py
```

> **BASE path tự động**: Khi chạy từ thư mục gốc `Project/`, tất cả script tự detect `BASE = Path(os.getcwd())`. Không cần chỉnh đường dẫn thủ công.

#### Bước 4 — Stress-test bảo mật Sandbox

```bash
python src/test_sandbox.py
```

Kiểm tra 13 kịch bản tấn công. Kết quả mong đợi: `13/13 bài kiểm tra bảo mật PASS`.

---

## 3. CLI Chấm bài Đơn lẻ (`grade.py`)

Chấm nhanh một bài nộp cho một `task_id` bất kỳ:

```bash
# Chấm từ chuỗi code trực tiếp
python grade.py --task_id 86 --code "def check_integer(text): ..."

# Chấm từ file .py
python grade.py --task_id 4 --file solution.py

# Dừng khi gặp lỗi đầu tiên (Fail-Fast)
python grade.py --task_id 86 --code "..." --fail-fast

# Xuất kết quả dạng JSON thô
python grade.py --task_id 86 --code "..." --json

# Dùng Docker Sandbox thật (cần Docker Desktop đang chạy)
python grade.py --task_id 4 --file solution.py --use-docker
```

---

## 4. Web Demo Streamlit (`app.py`)

```bash
streamlit run app.py
```

Mở trình duyệt tại `http://localhost:8501`.

### Tính năng:
- Chọn bài tập từ 100 bài MBPP, lọc theo chủ đề (List / Math / String)
- Soạn thảo code Python trực tiếp trên ACE Editor (theme Monokai, hỗ trợ auto-indent)
- Nút Auto-fix thụt lề (autopep8)
- Bật/Tắt Fail-Fast và Docker Sandbox ở Sidebar
- Hiển thị kết quả Pass/Fail, chi tiết từng test case bị lỗi và phản hồi sư phạm tiếng Việt

---

## 5. Cấu hình 4 Bộ Test (Tuần 4)

| Set | Cấu hình | Số tests/bài | Ghi chú |
|-----|----------|-------------|---------|
| Set 1 | 3 public tests | 3 | Baseline (tuần 2) |
| Set 2 | 3 public + 6 hidden | 9 | Cải tiến tuần 3 |
| Set 3 | 3 public + 6–10 hidden | ~11 | Phân bố chuông |
| Set 4 | Set 3 + Fail-Fast | ~11 | Tối ưu tuần 4 |

---

## 6. Kết quả Thực nghiệm Chính (Tuần 4)

| Metric | Set 1 | Set 2 | Set 3 | Set 4 (Fail-Fast) |
|--------|-------|-------|-------|-------------------|
| False Positive Rate (FPR) | 38.0% | 12.0% | 8.0% | 8.0% |
| False Acceptance Rate (FAR) | 42.2% | 13.3% | 8.9% | 8.9% |
| Sandbox: kịch bản tấn công bị chặn | — | — | — | 13/13 |
| Baseline: solution chuẩn pass | 100% | 100% | 100% | 100% |

---

## 7. Thành viên & Phân công

| MSSV | Họ tên | Vai trò |
|------|--------|---------|
| 3124560085 | Nguyễn Lê Nhựt Thắng | Kỹ thuật chính: runner, sandbox, comparison, demo |
| 3124410350 | Trần Vĩnh Thuận | EDA, biểu đồ, notebooks phân tích |
| 3124410356 | Trần Bảo Tín | Dữ liệu bài nộp, tổng hợp báo cáo |

**Giảng viên hướng dẫn**: ThS.NCS. Hà Thanh Dũng  
**Trường**: Đại học Sài Gòn — Khoa Công nghệ Thông tin  
**Học phần**: Ngôn ngữ Lập trình Python | 2026
