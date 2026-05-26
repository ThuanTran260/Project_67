# Automated Python Grading System với Kiểm thử ẩn và Phản hồi tự động

**Đề tài**: Hidden-Test-Based Automated Python Grading with Error-Type Feedback  
**Nhóm**: 67  
**Ngôn ngữ**: Python 3.10+

Hệ thống chấm điểm mã nguồn Python tự động được xây dựng dựa trên tập dữ liệu **100 bài toán MBPP** kết hợp với **100 bài nộp mô phỏng** có chứa lỗi logic hoặc hành vi nguy hiểm để đánh giá độ chính xác, tính an toàn của Sandbox và giá trị sư phạm của phản hồi tự động.

---

## 1. Thành phần Hệ thống & Cấu trúc Thư mục

```
Project/
├── data/
│   ├── raw/                 # Dữ liệu raw MBPP và submissions ban đầu
│   └── processed/           # Dữ liệu 100 bài tập và submissions sau khi đồng bộ
│       ├── hidden_v2.json   # Dữ liệu test cases ẩn mở rộng
│       └── submissions_50.json  # 100 bài nộp mô phỏng của học sinh
├── results/                 # Biểu đồ PNG thống kê và các tệp kết quả CSV/JSON
├── report/                  # Báo cáo tiến độ Tuần 3 và Tuần 4 bằng Tiếng Việt
├── src/                     # Mã nguồn lõi của hệ thống chấm bài
│   ├── runner_v3.py         # Sandbox chấm bài an toàn hỗ trợ Docker và Fail-Fast
│   ├── feedback.py          # Module sinh gợi ý phản hồi tự động bằng tiếng Việt
│   ├── diff_testing.py      # Module kiểm thử vi sai sinh input ngẫu nhiên
│   ├── test_sandbox.py      # Tập lệnh stress-test bảo mật sandbox (7 kịch bản)
│   ├── comparison_3sets.py  # Script chạy thực nghiệm đối chiếu 4 Set chấm điểm
│   └── generate_plots.py    # Script tự động vẽ và lưu trữ các biểu đồ
├── grade.py                 # Lệnh CLI chấm bài nộp đơn lẻ (Mới bổ sung)
├── app.py                   # Ứng dụng Web Demo Streamlit tương tác trực quan (Mới bổ sung)
├── requirements.txt         # Khai báo các thư viện phụ thuộc
└── README.md                # Tài liệu hướng dẫn sử dụng này
```

---

## 2. Hướng dẫn Cài đặt & Chuẩn bị Môi trường

1. **Cài đặt các thư viện phụ thuộc**:
   ```bash
   pip install -r requirements.txt
   ```
   *Để chạy Web Demo tương tác, vui lòng cài đặt thêm thư viện Streamlit*:
   ```bash
   pip install streamlit
   ```

2. **Khởi tạo dữ liệu sạch và đồng bộ hệ thống**:
   ```bash
   python src/regenerate_all.py
   ```
   *Lệnh này sẽ đồng bộ cấu trúc 100 bài toán (40 list, 32 math, 28 string), đồng bộ nhãn bài nộp và tự động chèn các ca kiểm thử biên (như `[]` cho Task 4, `[1, 2]` cho Task 9, và `"+123"` cho Task 86).*

---

## 3. Cách chạy Thực nghiệm & Chấm điểm hàng loạt

### 3.1. Chạy chấm điểm tự động & Xuất báo cáo CSV/JSON
Chạy lệnh sau để tự động chấm toàn bộ 100 bài nộp mô phỏng đối chiếu với các bộ test ẩn:
```bash
python src/run_grading_v2.py
```
Kết quả thống kê tổng hợp và danh sách traceback lỗi chi tiết sẽ được lưu tại `results/error_analysis_v2.csv` và `results/error_analysis_v2.json`.

### 3.2. Chạy So sánh 4 Cấu hình Chấm bài (Week 4 Evaluation)
Chạy script so sánh hiệu năng và tỷ lệ báo động giả (FPR/FAR) của 4 tập cấu hình kiểm thử (Public only, Public+Hidden v1, Public+Hidden v2, và Fail-Fast):
```bash
python src/comparison_3sets.py
```
Sau khi chạy xong, kết quả chi tiết sẽ xuất ra bảng so sánh chi tiết trên Terminal và lưu kết quả tại `results/comparison_week4.csv` và `results/comparison_week4.json`.

### 3.3. Tự động vẽ và cập nhật biểu đồ
Chạy script vẽ biểu đồ trực quan hóa dữ liệu và độ trễ (RQ1, RQ2, RQ5):
```bash
python src/generate_plots.py
```
Các biểu đồ dạng ảnh PNG sẽ được lưu tự động vào thư mục `results/`.

---

## 4. Chạy Stress-test Bảo mật Sandbox
Để kiểm tra độ an toàn của Sandbox V3 (AST Filter + Docker/Process limit), chạy script stress-test bảo mật:
```bash
python src/test_sandbox.py
```
Bộ stress-test giả lập 7 kịch bản tấn công thực tế bao gồm: import thư viện cấm, ghi tệp hệ thống, gọi hàm nguy hại `eval()`, truy cập thuộc tính dunder `__class__`, lặp vô hạn (TLE), bom bộ nhớ (MLE) và chia cho 0. Hệ thống sẽ phát hiện và ngăn chặn thành công 7/7 kịch bản.

---

## 5. Sử dụng CLI Chấm bài Đơn lẻ (`grade.py`)

Hệ thống cung cấp một CLI tool để chấm điểm nhanh một bài nộp bất kỳ của sinh viên cho một `task_id` cho trước:

*   **Chấm mã nguồn dạng chuỗi trực tiếp**:
    ```bash
    python grade.py --task_id 86 --code "def check_integer(text): text = text.strip(); return text.isdigit() or (len(text) > 1 and text[0] in '+-' and text[1:].isdigit())"
    ```
*   **Chấm mã nguồn chứa trong một tệp `.py`**:
    ```bash
    python grade.py --task_id 4 --file solution.py
    ```
*   **Chạy với chế độ Fail-Fast (dừng khi gặp lỗi đầu tiên để tối ưu thời gian)**:
    ```bash
    python grade.py --task_id 86 --code "..." --fail-fast
    ```
*   **Xuất kết quả chấm dưới dạng cấu trúc JSON thô để tích hợp hệ thống khác**:
    ```bash
    python grade.py --task_id 86 --code "..." --json
    ```

---

## 6. Trải nghiệm Web Demo Tương tác (`app.py`)

Ứng dụng cung cấp một giao diện web trực quan, thân thiện bằng **Streamlit** dành cho giảng viên và học sinh:

```bash
streamlit run app.py
```

### Các tính năng trên giao diện:
1. **Sidebar bài tập**: Chọn bài tập bất kỳ trong danh sách 100 bài MBPP (lọc theo chủ đề List, Math, String). Hệ thống tự động tải đề bài và các ví dụ công khai tương ứng.
2. **Trình soạn thảo mã nguồn**: Nhập hoặc sửa đổi mã nguồn Python trực tiếp trên trang.
3. **Cấu hình Sandbox**: Bật/Tắt Fail-Fast và Docker Sandbox tùy chọn ở Sidebar.
4. **Báo cáo trực quan**: Hiển thị trạng thái Pass/Fail (Bóng bay chúc mừng khi pass hết), phân loại lớp lỗi và hiển thị gợi ý sửa bài bằng tiếng Việt sinh động kèm theo chi tiết test case bị lỗi.
