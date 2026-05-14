# Nhóm 67 — Tuần 2 | Ngôn ngữ Lập trình Python

## Đề tài
Xây dựng hệ thống chấm bài Python tự động dựa trên test case, có sandbox, timeout,
phản hồi lỗi cơ bản và đánh giá ảnh hưởng của số lượng test case đến độ tin cậy của điểm chấm.

## Thành viên
| MSSV | Họ tên | Nhiệm vụ tuần 2 |
|---|---|---|
| 3124410356 | Trần Vĩnh Thuận | Đọc & phân tích dữ liệu, biểu đồ |
| 3124560085 | Nguyễn Lê Nhựt Thắng | Kỹ thuật & Baseline (runner) |
| 3124410350 | Trần Bảo Tín | Tổng hợp, nhận xét, kế hoạch tuần 3 |

## Cấu trúc thư mục
```
nhom67_tuan2/
├── data/
│   ├── raw/           ← Dữ liệu gốc MBPP subset (JSON)
│   └── processed/     ← Dữ liệu đã làm sạch
├── src/
│   └── runner.py      ← Engine chấm bài (subprocess + timeout)
├── notebooks/
│   ├── 00_setup.ipynb          ← Cài đặt môi trường
│   ├── 01_load_data.ipynb      ← Đọc & làm sạch dữ liệu
│   ├── 02_baseline.ipynb       ← Chạy baseline
│   ├── 03_simulate.ipynb       ← Mô phỏng bài nộp sinh viên
│   └── 04_visualize.ipynb      ← Vẽ biểu đồ
├── results/           ← Kết quả CSV, JSON, PNG
├── report/            ← File báo cáo Word/PDF
├── requirements.txt
└── README.md
```

## Cách chạy trên Google Colab
Xem file `notebooks/00_setup.ipynb` để bắt đầu.

## Dataset
- **Chính:** MBPP subset (~50 bài, task_id 1–100) — `data/raw/mbpp_subset.json`
- **Mở rộng (tuần 4):** LeetCode subset
