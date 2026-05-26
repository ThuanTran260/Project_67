# Yêu cầu hoàn thiện Nhóm 67

**Đề tài**: Automated Python Grading System với kiểm thử ẩn và phản hồi tự động

## 1. Định hướng chung
Nhóm 67 cần phát triển hệ thống chấm code chứng minh được ba trục đóng góp chính:
*   **Độ tin cậy khi chấm code**: Hidden tests giúp giảm số bài sai nhưng vẫn được chấp nhận (FAR = 0%).
*   **An toàn khi thực thi code**: Runner có kiểm soát timeout, memory, whitelist imports/builtins và sandbox cô lập.
*   **Giá trị giáo dục**: Phân loại lỗi chi tiết (RE) và sinh phản hồi tự động (Feedback) bằng tiếng Việt sư phạm.

## 2. Tên hướng nghiên cứu
**Hidden-Test-Based Automated Python Grading with Error-Type Feedback**

## 3. Câu hỏi nghiên cứu (Research Questions)
*   **RQ1**: Hidden tests có làm giảm số bài sai nhưng vẫn được chấm pass không? (So sánh Set 1 vs Set 2 vs Set 3 vs Set 4)
*   **RQ2**: Runner có phát hiện được các lỗi phổ biến khi chấm Python không? (WA, RE, TLE, MLE, SE)
*   **RQ3**: Sandbox hiện tại có ngăn được các hành vi nguy hiểm cơ bản không? (Stress-test với open, os, socket, infinite loop, memory bomb)
*   **RQ4**: Phản hồi tự động theo loại lỗi có hữu ích hơn Pass/Fail không? (Template feedback sư phạm kèm chi tiết lỗi)
*   **RQ5**: Chi phí chấm có chấp nhận được không? (Đo latency/submission, P95 latency, Fail-Fast speedup)

## 4. Yêu cầu về dữ liệu
*   **Số lượng bài MBPP**: Ít nhất 100 bài (Mức paper).
*   **Số bài nộp mô phỏng**: Ít nhất 100 bài (Mức tốt/paper).
*   **Số test cases**: 3 Public tests, 10-15 Hidden tests.
*   **Phân loại bài nộp**: Có đủ nhãn lỗi AC, WA, RE, TLE, MLE, SE, HC (Hard-coded), PA (Partially Accepted).

## 5. Các tập cấu hình chấm điểm
*   **Set 1**: Public only (3 tests).
*   **Set 2**: Public + Hidden v1 (9 tests).
*   **Set 3**: Public + Hidden v2 (13 tests max, không Fail-Fast).
*   **Set 4**: Set 3 + Fail-Fast (Dừng ngay khi gặp lỗi).
*   **Property-based**: So sánh vi sai với input ngẫu nhiên.

## 6. Các chỉ số đo lường (Metrics)
*   **FAR (False Acceptance Rate)**: Tỷ lệ bài lỗi lọt qua hệ thống.
*   **FRR (False Rejection Rate)**: Tỷ lệ bài đúng bị chấm oan.
*   **Error Detection Rate**: Khả năng phát hiện bài lỗi.
*   **Latency**: Chi phí chấm trung bình (Average Latency/submission, P95 Latency).

## 7. Yêu cầu về Runner & Sandbox
*   Chức năng: Timeout (1.0s/test), Memory limit (128MB), AST safety whitelist check, Capture stdout/stderr, Result logging.
*   Sandbox tests: Ít nhất 10 bài stress-test cố ý chứa mã độc và lỗi tài nguyên.
*   Docker: Cách ly hệ điều hành hoàn chỉnh hoặc Giả lập Docker Sandbox nếu daemon tắt.

## 8. Phân loại Hidden Tests
*   Hidden tests cần có độ bao phủ đa dạng: edge cases (danh sách rỗng, số âm, số 0, biên lớn, trùng lặp) và stress-test.

## 9. Phản hồi tự động (Feedback)
*   Cung cấp thông tin chi tiết: Trạng thái, Loại lỗi, Test bị fail, Input gây lỗi, Expected/Actual output, Gợi ý sửa lỗi sư phạm bằng tiếng Việt.

## 10. Demo
*   Dạng notebook / dạng CLI / hoặc dạng giao diện web (Streamlit/Gradio).

## 11. Các bảng kết quả cần có trong báo cáo
*   Bảng 1: Thống kê quy mô và phân bố lỗi dữ liệu.
*   Bảng 2: So sánh FAR, FRR và Latency giữa 4 Set chấm bài.
*   Bảng 3: Độ chính xác phân loại lỗi (Accuracy).
*   Bảng 4: Kết quả stress-test Sandbox.
*   Bảng 5: Phân tích các bài nộp lỗi còn lọt và phương án bổ sung test.
