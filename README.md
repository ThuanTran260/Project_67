# Nhóm 67  | Ngôn ngữ Lập trình Python

## Đề tài
Xây dựng hệ thống chấm bài Python tự động dựa trên test case, có sandbox, timeout,
phản hồi lỗi cơ bản và đánh giá ảnh hưởng của số lượng test case đến độ tin cậy của điểm chấm.

## Thành viên
| MSSV | Họ tên | Nhiệm vụ tuần 2 |
|---|---|---|
| 3124410350 | Trần Vĩnh Thuận | Đọc & phân tích dữ liệu, biểu đồ |
| 3124560085 | Nguyễn Lê Nhựt Thắng | Kỹ thuật & Baseline (runner)|
| 3124410356 | Trần Bảo Tín | Tổng hợp, nhận xét, kế hoạch        |

## Cấu trúc thư mục
```
Project_67/                              ← Tên GitHub repo (đổi tùy ý)
│
├── README.md                                  ← Mô tả đề tài, cách chạy, thành viên
├── .gitignore                                 ← __pycache__, *.pyc, .DS_Store
├── requirements.txt                           ← pandas, matplotlib (không cần pip gì thêm)
│
├── shared/                                    ← Code dùng chung cho mọi tuần
│   ├── runner.py                              ← Engine chấm bài (tuần nào cũng import)
│   └── error_stats.py                         ← Module thống kê lỗi tự động
│
├── tuan1/                                     ─────────── TUẦN 1 ───────────
│   ├── bao_cao_tuan1.docx                     ← Báo cáo Word (đổi tên tùy ý)
│   └── data/
│       └── mbpp_subset.json                   ← Dataset 15 bài (tuần 1 chưa chạy code)
│
├── tuan2/                                     ─────────── TUẦN 2 ───────────
│   ├── bao_cao_tuan2.docx
│   ├── data/
│   │   ├── raw/
│   │   │   └── mbpp_15.json                   ← 15 bài, 3 public + 6 hidden test
│   │   └── processed/
│   │       └── mbpp_clean.json                ← Sau khi làm sạch
│   ├── notebooks/
│   │   ├── 01_load_data.ipynb                 ← Đọc + làm sạch + EDA + 4 biểu đồ
│   │   ├── 02_baseline.ipynb                  ← Chạy runner trên 15 bài
│   │   └── 03_simulate.ipynb                  ← Mô phỏng 12 bài nộp có lỗi
│   └── results/
│       ├── baseline_summary.csv
│       ├── student_simulation.csv
│       └── metric_summary.json
│
├── tuan3/                                     ─────────── TUẦN 3 ───────────
│   ├── bao_cao_tuan3.docx
│   ├── data/
│   │   └── raw/
│   │       └── mbpp_50.json                   ← 50 bài, 3 public + 10 hidden test
│   ├── notebooks/
│   │   ├── 01_eda_v2.ipynb                    ← EDA cập nhật 50 bài
│   │   └── 02_comparison_3sets.ipynb          ← So sánh 3 bộ test, bảng RQ1
│   └── results/
│       ├── comparison_3sets.csv
│       ├── comparison_3sets.json
│       ├── FPR_vs_ntest.png                   ← Biểu đồ đường cong FPR (RQ1)
│       └── error_3sets.png                    ← Biểu đồ phân loại lỗi 3 bộ
│
├── tuan4/                                     ─────────── TUẦN 4 (sắp tới) ──
│   ├── bao_cao_tuan4.docx
│   ├── data/
│   │   └── raw/
│   │       ├── mbpp_50.json                   ← Dùng lại từ tuan3/ (symlink hoặc chép)
│   │       └── leetcode_subset.json           ← Dataset mới: LeetCode 100+ test/bài
│   ├── notebooks/
│   │   ├── 01_leetcode_eda.ipynb
│   │   └── 02_mbpp_vs_leetcode.ipynb         ← So sánh FPR: 3-test vs 10-test vs 100-test
│   └── results/
│       └── FPR_curve.png                      ← Đường cong FPR hoàn chỉnh cho RQ1
│
├── tuan5/                                     ─────────── TUẦN 5 (sắp tới) ──
│   ├── bao_cao_tuan5.docx
│   ├── notebooks/
│   │   ├── 01_feedback_module.ipynb           ← Module phản hồi lỗi tự động (RQ3)
│   │   └── 02_final_evaluation.ipynb          ← Đánh giá tổng hợp RQ1+RQ2+RQ3
│   └── results/
│       └── final_report.json
│
└── colab_setup/                               ← Notebook chạy trên Colab
    ├── setup.ipynb                            ← Kết nối Drive, tạo thư mục, chép file
    └── run_all.ipynb                          ← Chạy tuần nào thì gọi notebook đó

```

## Cách chạy trên Google Colab
Xem file `notebooks/00_setup.ipynb` để bắt đầu.

## Dataset
- **Chính:** MBPP subset (~50 bài, task_id 1–100) — `data/raw/mbpp_subset.json`
- **Mở rộng (tuần 4):** LeetCode subset
