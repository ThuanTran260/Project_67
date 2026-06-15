**Nhận xét báo cáo tuần 2 của Nhóm 67 - Đề tài 18: Automated Python Grading System với kiểm thử ẩn và phản hồi tự động**

Nhìn chung, **Nhóm 67 làm tốt trong tuần 2**. Đây là một trong các nhóm có hướng triển khai kỹ thuật rõ: không chỉ mô tả ý tưởng, mà đã xây dựng được **baseline runner** để chạy bài nộp Python qua test case, phân loại lỗi và so sánh giữa **public test** và **hidden test**. Cách xác định baseline là **test-case runner**, thay vì mô hình học máy, là hợp lý vì bài toán chấm code có thể xác minh trực tiếp bằng thực thi chương trình.

Tuy nhiên, báo cáo vẫn còn một số hạn chế: tập MBPP mới dùng **15 mẫu**, bài nộp sinh viên là **12 bài mô phỏng**, hidden test do nhóm tự tạo nên cần kiểm chứng chất lượng, và phần tài liệu tham khảo / khai báo AI / minh chứng file-code cá nhân chưa thật đầy đủ.

**Điểm đề xuất theo rubric mới: 86/100 - Mức Tốt.**

**1\. Nhận xét tổng quan**

| **Nội dung**              | **Đánh giá**                                            |
| ------------------------- | ------------------------------------------------------- |
| Cấu trúc báo cáo          | Khá tốt                                                 |
| Mô tả dữ liệu             | Có, nhưng tập mẫu còn nhỏ                               |
| Làm sạch dữ liệu          | Tốt, phù hợp với dữ liệu code                           |
| Phân tích dữ liệu ban đầu | Tốt                                                     |
| Baseline tuần 2           | Rất đúng hướng: test-case runner                        |
| Kết quả                   | Có số liệu rõ, có public/hidden comparison              |
| Metric                    | Phù hợp: pass rate, FPR, WA, RE, SE, latency            |
| Phân tích lỗi             | Tốt, có ví dụ cụ thể                                    |
| Minh chứng cá nhân        | Có phân công, nhưng thiếu file/code minh chứng chi tiết |
| Tài liệu tham khảo / AI   | Chưa thấy trình bày đầy đủ trong báo cáo tuần 2         |

**2\. Điểm mạnh**

**2.1. Nhóm xác định đúng baseline cho đề tài**

Điểm mạnh nhất là nhóm không cố ép bài toán thành mô hình học máy. Với hệ thống chấm bài Python, baseline hợp lý nhất là:

**Runner chạy bài nộp qua test case và ghi nhận kết quả pass/fail, loại lỗi và thời gian chạy.**

Nhóm giải thích đúng rằng bài toán chấm bài lập trình có đáp án có thể xác minh qua thực thi, nên giai đoạn đầu không nhất thiết cần mô hình ML.

**2.2. Kiến trúc runner khá rõ**

Runner có hai lớp kiểm tra:

| **Thành phần**                 | **Vai trò**                                                   |
| ------------------------------ | ------------------------------------------------------------- |
| Kiểm tra tĩnh bằng ast         | Phát hiện lỗi cú pháp trước khi chạy                          |
| Kiểm tra import nguy hiểm      | Chặn các thư viện rủi ro như os, sys, subprocess              |
| Thực thi bằng subprocess.run() | Chạy từng test case có timeout                                |
| Chuẩn hóa output               | So sánh số thực, danh sách, boolean tốt hơn so sánh chuỗi thô |

Nhóm cũng phân loại lỗi thành **SE, WA, RE, TLE**, phù hợp với hệ thống chấm lập trình tự động.

**2.3. Có thiết kế public test và hidden test**

Nhóm giữ 3 test gốc của MBPP làm **public test**, đồng thời tự thiết kế thêm 5-7 **hidden test** cho mỗi bài, tập trung vào các trường hợp biên như danh sách rỗng, số âm, chuỗi đặc biệt, giá trị min/max. Đây là điểm rất tốt vì đúng bản chất của hệ thống chấm code: public test giúp sinh viên kiểm tra cơ bản, hidden test giúp chống code đối phó.

**2.4. Có kết quả thực nghiệm rõ**

Nhóm chạy solution mẫu của 15 bài MBPP và tất cả đạt 100% trên cả public và hidden test. Điều này giúp xác nhận runner và hidden test không làm sai đáp án chuẩn. Đồng thời, nhóm mô phỏng 12 bài nộp có lỗi để kiểm tra khả năng phát hiện lỗi.

Kết quả quan trọng:

| **Metric**              | **Public test** | **Hidden test** |
| ----------------------- | --------------- | --------------- |
| Số bài pass toàn bộ     | 5/12            | 2/12            |
| False Positive          | -               | 3/12            |
| Wrong Answer phát hiện  | 13              | 22              |
| Runtime Error phát hiện | 2               | 7               |
| Latency trung bình      | 0,013s/test     | 0,012s/test     |

Những số liệu này cho thấy hidden test phát hiện thêm nhiều lỗi logic và lỗi runtime mà public test bỏ sót.

**2.5. Phân tích lỗi có ví dụ cụ thể**

Báo cáo phân tích tốt 3 trường hợp false positive:

| **Mẫu** | **Lỗi**               | **Nhận xét**                                      |
| ------- | --------------------- | ------------------------------------------------- |
| SV007   | return list(set(lst)) | Qua public test nhưng sai vì set không giữ thứ tự |
| SV008   | sum(lst) / len(lst)   | Không xử lý danh sách rỗng, gây ZeroDivisionError |
| SV009   | Kiểm tra số nguyên tố | Không xử lý n = 0, n = 1                          |

Đây là phần rất tốt vì cho thấy nhóm hiểu rõ vì sao hidden test cần thiết, không chỉ báo số liệu chung chung.

**3\. Vấn đề cần chỉnh sửa**

**3.1. Tập dữ liệu tuần 2 còn quá nhỏ**

Nhóm mới dùng:

| **Thành phần**   | **Số lượng** |
| ---------------- | ------------ |
| Bài MBPP subset  | 15 bài       |
| Bài nộp mô phỏng | 12 bài       |

Quy mô này đủ để chứng minh pipeline chạy được trong tuần 2, nhưng chưa đủ để kết luận mạnh về độ tin cậy của hệ thống chấm tự động.

Tuần 3 nên mở rộng ít nhất:

| **Hướng mở rộng** | **Gợi ý**                            |
| ----------------- | ------------------------------------ |
| MBPP              | 50-100 bài                           |
| Bài nộp mô phỏng  | 50-100 bài với nhiều dạng lỗi        |
| Hidden test       | Chuẩn hóa số lượng và loại edge case |
| Nếu có thể        | Thêm một số bài LeetCode/APPS nhỏ    |

**3.2. Cần làm rõ định nghĩa False Positive Rate**

Báo cáo ghi FPR = 25% với 3/12 bài. Tuy nhiên, cần diễn đạt chính xác hơn:

Đây là tỷ lệ bài **được public test cho qua nhưng bị hidden test phát hiện sai**.

Không nên gọi chung chung là FPR nếu chưa định nghĩa rõ đơn vị tính là **bài nộp**, không phải **test case**.

Nên bổ sung công thức:

![](data:image/png;base64,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)

Hoặc diễn đạt đơn giản hơn:

Public false-positive rate = số bài sai logic nhưng vẫn pass public test / tổng số bài mô phỏng.

**3.3. Hidden test do nhóm tự tạo cần có kiểm chứng**

Hidden test là đóng góp quan trọng, nhưng do nhóm tự thiết kế nên cần đảm bảo:

| **Cần kiểm tra**                                  | **Lý do**               |
| ------------------------------------------------- | ----------------------- |
| Hidden test có đúng expected output không         | Tránh chấm sai bài đúng |
| Hidden test có bao phủ nhiều loại edge case không | Tăng độ tin cậy         |
| Có trùng hoặc quá giống public test không         | Tránh dư thừa           |
| Có quá khó hoặc vượt yêu cầu đề bài không         | Tránh không công bằng   |
| Có được review độc lập bởi thành viên khác không  | Giảm lỗi thiết kế test  |

Tuần 3 nên thêm bảng mô tả hidden test theo từng task: loại edge case, mục tiêu bắt lỗi, expected output.

**3.4. Cần bổ sung phần an toàn thực thi rõ hơn**

Nhóm có kiểm tra import nguy hiểm và dùng timeout, đây là tốt. Tuy nhiên, chạy code sinh viên bằng subprocess vẫn có rủi ro nếu không sandbox kỹ.

Cần làm rõ:

| **Vấn đề**                  | **Cần bổ sung**                                                  |
| --------------------------- | ---------------------------------------------------------------- |
| Giới hạn thời gian          | Đã có 5 giây                                                     |
| Giới hạn bộ nhớ             | Chưa thấy                                                        |
| Giới hạn file system        | Chưa thấy                                                        |
| Chặn network                | Chưa thấy                                                        |
| Chạy trong Docker/container | Chưa thấy                                                        |
| Xóa file tạm sau chạy       | Cần ghi rõ                                                       |
| Import cấm                  | Cần cân nhắc không chặn quá rộng như sys nếu bài hợp lệ cần dùng |

Tuần 3 nên ưu tiên sandbox an toàn hơn, vì đây là hệ thống chạy code không tin cậy.

**3.5. Cần bổ sung tài liệu tham khảo và khai báo AI**

Trong nội dung tuần 2 đã trích xuất, chưa thấy phần tài liệu tham khảo và khai báo sử dụng AI rõ ràng. Với đề tài này, nên có tối thiểu:

- MBPP / Program Synthesis with Large Language Models;
- HumanEval / Codex;
- APPS;
- tài liệu về automated grading;
- tài liệu về test-based grading;
- tài liệu về sandboxing khi chạy code không tin cậy.

Nếu nhóm có sử dụng AI, cần ghi rõ AI dùng để làm gì: gợi ý code runner, viết test case, diễn giải metric hay chỉnh báo cáo.

**3.6. Minh chứng cá nhân cần cụ thể hơn**

Báo cáo có phân công:

- Trần Vĩnh Thuận: đọc và phân tích dữ liệu, biểu đồ;
- Nguyễn Lê Nhựt Thắng: kỹ thuật và baseline runner;
- Trần Bảo Tín: tổng hợp, nhận xét, kế hoạch tuần 3.

Tuy nhiên, theo yêu cầu mới, cần bổ sung bảng minh chứng:

| **Thành viên**       | **Công việc**                                         | **File/minh chứng**                          |
| -------------------- | ----------------------------------------------------- | -------------------------------------------- |
| Trần Vĩnh Thuận      | EDA, biểu đồ độ dài đề bài, số test case, pass rate   | eda_mbpp.ipynb, hình biểu đồ                 |
| Nguyễn Lê Nhựt Thắng | Runner, AST check, subprocess, timeout, phân loại lỗi | src/runner.py, tests_runner.py               |
| Trần Bảo Tín         | Tổng hợp kết quả, phân tích FP, kế hoạch tuần 3       | results/error_summary.csv, report_week2.docx |

**4\. Đánh giá theo rubric mới**

| **Tiêu chí**                                | **Tỷ trọng** | **Điểm**   | **Nhận xét**                                                    |
| ------------------------------------------- | ------------ | ---------- | --------------------------------------------------------------- |
| 1\. Cấu trúc và hình thức báo cáo           | 10%          | 8/10       | Cấu trúc rõ, nhưng thiếu rõ tài liệu tham khảo và AI note       |
| 2\. Mô tả dữ liệu                           | 15%          | 12/15      | Có MBPP, đặc trưng, test case; nhưng chỉ dùng 15 mẫu            |
| 3\. Làm sạch và tiền xử lý dữ liệu          | 15%          | 13/15      | Có kiểm tra task_id, mô tả rỗng, syntax, test case rỗng         |
| 4\. Phân tích dữ liệu ban đầu               | 15%          | 14/15      | EDA tốt: độ dài đề, số test, pass rate, loại lỗi                |
| 5\. Baseline hoặc phương pháp tuần 2        | 15%          | 15/15      | Runner là baseline rất đúng với đề tài                          |
| 6\. Kết quả ban đầu và metric               | 10%          | 9/10       | Có pass rate, FPR, WA/RE/SE, latency; cần định nghĩa FPR rõ hơn |
| 7\. Phân tích lỗi, hạn chế, kế hoạch tuần 3 | 10%          | 9/10       | Phân tích FP rất tốt, kế hoạch hidden test v2 hợp lý            |
| 8\. Phân công và minh chứng cá nhân         | 7%           | 5/7        | Có phân công, thiếu file/code minh chứng theo từng người        |
| 9\. Ghi chú AI và tài liệu tham khảo        | 3%           | 1/3        | Cần bổ sung rõ tài liệu và khai báo AI                          |
| **Tổng**                                    | **100%**     | **86/100** | **Tốt**                                                         |

**5\. Yêu cầu nhóm cần sửa trước tuần 3**

| **Việc cần làm**                                                             | **Mức độ ưu tiên** |
| ---------------------------------------------------------------------------- | ------------------ |
| Mở rộng số bài MBPP từ 15 lên ít nhất 50 bài                                 | Rất cao            |
| Tăng số bài nộp mô phỏng có lỗi                                              | Rất cao            |
| Định nghĩa rõ FPR theo đơn vị bài nộp hay test case                          | Rất cao            |
| Bổ sung bảng hidden test theo từng task và loại edge case                    | Rất cao            |
| Kiểm chứng expected output của hidden test                                   | Rất cao            |
| Bổ sung sandbox an toàn hơn: memory, file, network, container nếu có thể     | Cao                |
| Làm rõ danh sách import cấm và lý do cấm                                     | Cao                |
| Bổ sung tài liệu tham khảo chính thức về MBPP, HumanEval, APPS, auto-grading | Cao                |
| Bổ sung khai báo sử dụng AI                                                  | Cao                |
| Gắn file/code minh chứng theo từng thành viên                                | Rất cao            |

**6\. Định hướng tuần 3**

| **Ưu tiên** | **Nội dung**                                | **Mục tiêu**                        |
| ----------- | ------------------------------------------- | ----------------------------------- |
| 1           | Hidden test v2                              | Tăng độ phủ edge case               |
| 2           | Mở rộng MBPP subset                         | Kết quả đáng tin hơn                |
| 3           | Chuẩn hóa metric FPR/Test Pass Rate         | Đánh giá rõ hơn                     |
| 4           | Phân tích lỗi tự động                       | Thống kê SE/WA/RE/TLE theo task     |
| 5           | Sandbox an toàn hơn                         | Giảm rủi ro khi chạy code lạ        |
| 6           | So sánh public vs hidden theo từng dạng lỗi | Chứng minh hidden test hữu ích      |
| 7           | Thử LeetCode subset nhỏ                     | So sánh với hệ thống nhiều test hơn |
| 8           | Sinh phản hồi tự động theo lỗi              | Tiến gần mục tiêu đề tài            |

**7\. Kết luận**

Báo cáo tuần 2 của **Nhóm 67** đạt mức **Tốt - 86/100**. Nhóm có điểm mạnh rõ ràng: đã xây dựng được runner, có phân loại lỗi, có public/hidden test, có kết quả phát hiện false positive và có phân tích lỗi cụ thể. Đây là hướng triển khai đúng bản chất của hệ thống chấm bài Python tự động.

Nhận xét:

Nhóm làm tốt tuần 2, baseline runner đúng hướng và có kết quả public/hidden test rất có ý nghĩa. Tuy nhiên, tập thử nghiệm còn nhỏ, cần định nghĩa FPR rõ hơn, mở rộng số bài MBPP, kiểm chứng hidden test và bổ sung sandbox an toàn hơn. Tuần 3 nên tập trung vào hidden test v2, mở rộng dữ liệu và tự động hóa phân tích lỗi.