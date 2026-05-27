**Yêu cầu hoàn thiện Nhóm 67**

**Đề tài: Automated Python Grading System với kiểm thử ẩn và phản hồi tự động**

**1\. Định hướng chung**

Nhóm 67 không nên dừng ở mức **"chạy được hệ thống chấm code"**. Đề tài này có tiềm năng phát triển thành bài hội nghị nếu nhóm chứng minh được ba điểm:

| **Trục đóng góp**             | **Yêu cầu**                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------ |
| **Độ tin cậy khi chấm code**  | Hidden tests giúp giảm số bài sai nhưng vẫn được chấp nhận                     |
| **An toàn khi thực thi code** | Runner có kiểm soát timeout, memory, import nguy hiểm và hành vi bất thường    |
| **Giá trị giáo dục**          | Hệ thống không chỉ trả Pass/Fail mà còn phân loại lỗi và sinh phản hồi tự động |

Trong kế hoạch tuần 3, đề tài Automated Python Grading đã được nhắc riêng: cần mở rộng số bài MBPP và số bài nộp mô phỏng, định nghĩa rõ False Positive Rate, kiểm chứng hidden test, bổ sung sandbox an toàn hơn và thống kê lỗi tự động.

**2\. Tên hướng nghiên cứu nên chốt**

**Hidden-Test-Based Automated Python Grading with Error-Type Feedback**

Tên này thể hiện rõ hai điểm mạnh: **hidden test** và **feedback theo loại lỗi**.

**3\. Câu hỏi nghiên cứu cần trả lời**

Nhóm cần viết lại báo cáo theo các câu hỏi nghiên cứu sau:

| **Mã**  | **Câu hỏi nghiên cứu**                                              | **Cách kiểm chứng**                                        |
| ------- | ------------------------------------------------------------------- | ---------------------------------------------------------- |
| **RQ1** | Hidden tests có làm giảm số bài sai nhưng vẫn được chấm pass không? | So sánh Public only vs Public + Hidden vs Hidden v2        |
| **RQ2** | Runner có phát hiện được các lỗi phổ biến khi chấm Python không?    | Báo WA, RE, TLE, MLE, Security Error                       |
| **RQ3** | Sandbox hiện tại có ngăn được các hành vi nguy hiểm cơ bản không?   | Chạy test với open, os, socket, infinite loop, memory bomb |
| **RQ4** | Phản hồi tự động theo loại lỗi có hữu ích hơn Pass/Fail không?      | Tạo template feedback và minh họa trên bài sai             |
| **RQ5** | Chi phí chấm có chấp nhận được không?                               | Báo latency/test, latency/submission, P95 latency          |

**4\. Yêu cầu về dữ liệu**

**4.1. Quy mô dữ liệu tối thiểu**

Bản hiện tại dùng 50 bài MBPP và 50 bài nộp mô phỏng. Để đủ mạnh cho báo cáo cuối và có khả năng viết paper, nhóm cần mở rộng.

| **Thành phần**      | **Mức tối thiểu** | **Mức tốt** | **Mức paper** |
| ------------------- | ----------------- | ----------- | ------------- |
| Bài MBPP            | 50                | 75          | 100           |
| Bài nộp mô phỏng    | 50                | 100         | 150-200       |
| Public tests/bài    | 3                 | 3           | 3             |
| Hidden tests/bài    | 6-10              | 8-12        | 10-15         |
| Bài lỗi TLE         | 3-5               | 5-10        | ≥10           |
| Bài lỗi MLE         | 3-5               | 5-10        | ≥10           |
| Bài vi phạm sandbox | 5                 | 10          | ≥15           |

**Yêu cầu bắt buộc:** Nếu chưa đủ thời gian, ít nhất phải nâng từ **50 submissions lên 100 submissions**. Nhưng cố gắng đảm bảo dữ liệu theo yêu cầu

**4.2. Cấu trúc dữ liệu cần có**

Nhóm cần chuẩn hóa dữ liệu thành các file:

| **File**                      | **Nội dung**                                         |
| ----------------------------- | ---------------------------------------------------- |
| mbpp_tasks.json               | Danh sách bài MBPP, mô tả, hàm cần viết, test public |
| hidden_tests_v1.json          | Hidden tests cơ bản                                  |
| hidden_tests_v2.json          | Hidden tests mở rộng gồm edge cases                  |
| submissions.json              | Bài nộp mô phỏng                                     |
| submission_labels.csv         | Nhãn bài nộp: AC, WA, RE, TLE, MLE, SE               |
| grading_results_public.csv    | Kết quả chấm bằng public tests                       |
| grading_results_hidden.csv    | Kết quả chấm bằng hidden tests                       |
| grading_results_hidden_v2.csv | Kết quả chấm bằng hidden v2                          |
| error_analysis.csv            | Các bài sai nhưng lọt hoặc bài đúng bị chấm sai      |

**4.3. Phân loại bài nộp mô phỏng**

Không nên chỉ có bài đúng/sai logic. Cần có đủ các loại lỗi:

| **Loại bài nộp**      | **Ký hiệu** | **Ví dụ**                                |
| --------------------- | ----------- | ---------------------------------------- |
| Đúng hoàn toàn        | AC          | Pass public và hidden                    |
| Sai logic             | WA          | Sai edge case, sai điều kiện biên        |
| Runtime error         | RE          | IndexError, TypeError, ZeroDivisionError |
| Time limit exceeded   | TLE         | while True, recursion vô hạn             |
| Memory limit exceeded | MLE         | Tạo list rất lớn, chuỗi rất lớn          |
| Security violation    | SE          | Dùng open, os, subprocess, socket        |
| Bài hard-coded        | HC          | Chỉ đúng public tests, sai hidden        |
| Bài gần đúng          | PA          | Đúng phần lớn test nhưng sai edge case   |

**5\. Yêu cầu về baseline và các bộ test**

Nhóm cần có ít nhất ba cấu hình chấm:

| **Cấu hình**                                         | **Mô tả**                                   | **Vai trò**          |
| ---------------------------------------------------- | ------------------------------------------- | -------------------- |
| **Set 1: Public only**                               | Chỉ dùng 3 public tests                     | Baseline             |
| **Set 2: Public + Hidden v1**                        | Public tests + 6 hidden tests               | Phương pháp tuần 3   |
| **Set 3: Public + Hidden v2**                        | Public tests + 6-10 hoặc 10-15 hidden tests | Phương pháp cải tiến |
| **Set 4: Public + Hidden v2 + Property-based tests** | Nếu làm được                                | Mức paper            |

Bảng kết quả bắt buộc:

| **Bộ test**        | **Tổng submissions** | **Bài đúng** | **Bài sai** | **False Acceptance** | **False Rejection** | **FAR** | **FRR** | **Avg latency/ submission** |
| ------------------ | -------------------- | ------------ | ----------- | -------------------- | ------------------- | ------- | ------- | --------------------------- |
| Public only        |                      |              |             |                      |                     |         |         |                             |
| Public + Hidden v1 |                      |              |             |                      |                     |         |         |                             |
| Public + Hidden v2 |                      |              |             |                      |                     |         |         |                             |
| \+ Property-based  |                      |              |             |                      |                     |         |         |                             |

**6\. Chuẩn hóa metric**

**6.1. Không nên gọi chung là FPR nếu chưa giải thích**

Trong chấm code, nên dùng thuật ngữ chính xác hơn:

| **Thuật ngữ**                  | **Công thức**                               | **Ý nghĩa**                    |
| ------------------------------ | ------------------------------------------- | ------------------------------ |
| **False Acceptance Rate, FAR** | Bài sai nhưng được chấm pass / tổng bài sai | Tỷ lệ bài sai lọt qua hệ thống |
| **False Rejection Rate, FRR**  | Bài đúng nhưng bị chấm fail / tổng bài đúng | Tỷ lệ bài đúng bị chấm oan     |
| **Pass Rate**                  | Số bài pass / tổng bài nộp                  | Tỷ lệ pass chung               |
| **Error Detection Rate**       | Số bài lỗi bị phát hiện / tổng bài lỗi      | Khả năng phát hiện bài lỗi     |
| **Error-Type Accuracy**        | Lỗi được phân loại đúng / tổng lỗi          | Độ đúng của phân loại lỗi      |
| **Average Latency**            | Tổng thời gian / số submissions             | Chi phí chấm trung bình        |

**6.2. Bảng metric bắt buộc**

| **Metric**             | **Bắt buộc?** | **Ghi chú**                 |
| ---------------------- | ------------- | --------------------------- |
| FAR                    | Có            | Metric chính                |
| FRR                    | Có            | Tránh chấm oan bài đúng     |
| Error Detection Rate   | Có            | Đo khả năng phát hiện lỗi   |
| WA/RE/TLE/MLE/SE count | Có            | Thống kê lỗi                |
| Latency/test           | Có            | Chi phí từng test           |
| Latency/submission     | Có            | Quan trọng hơn latency/test |
| P95 latency            | Khuyến khích  | Đánh giá trường hợp chậm    |
| Error-Type Accuracy    | Khuyến khích  | Cần nếu có nhãn lỗi chuẩn   |
| Feedback Coverage      | Khuyến khích  | Bao nhiêu lỗi có feedback   |

**7\. Yêu cầu về runner và sandbox**

**7.1. Runner phải có các chức năng tối thiểu**

| **Chức năng**         | **Yêu cầu**                                                     |
| --------------------- | --------------------------------------------------------------- |
| Timeout               | Có, ví dụ 1-2 giây/test hoặc 5 giây/submission                  |
| Memory limit          | Có, ví dụ 128 MB hoặc 256 MB                                    |
| AST safety check      | Có                                                              |
| Chặn import nguy hiểm | os, sys, subprocess, socket, ctypes, multiprocessing, threading |
| Chặn hàm nguy hiểm    | eval, exec, open, compile, \__import_\_, globals, locals        |
| Temporary directory   | Có                                                              |
| Capture stdout/stderr | Có                                                              |
| Error classification  | Có                                                              |
| Result logging        | Có CSV/JSON output                                              |

**7.2. Bài kiểm thử sandbox bắt buộc**

Nhóm phải tạo ít nhất 10 bài test sandbox:

| **Loại tấn công/lỗi** | **Ví dụ**                       |
| --------------------- | ------------------------------- |
| Infinite loop         | while True: pass                |
| Infinite recursion    | Hàm gọi lại chính nó không dừng |
| Memory bomb           | Tạo list hoặc string cực lớn    |
| File access           | open("secret.txt")              |
| OS command            | os.system("...")                |
| Network access        | socket.socket(...)              |
| Subprocess            | subprocess.run(...)             |
| Dynamic import        | \__import_\_("os")              |
| Eval/exec             | eval("..."), exec("...")        |
| Excessive output      | In ra chuỗi rất dài             |

Bảng báo cáo bắt buộc:

| **Test** | **Loại lỗi**  | **Expected** | **Detected?** | **Error type** | **Ghi chú** |
| -------- | ------------- | ------------ | ------------- | -------------- | ----------- |
| TLE_01   | Infinite loop | TLE          | Có/Không      | TLE            |             |
| MLE_01   | Memory bomb   | MLE          | Có/Không      | MLE            |             |
| SE_01    | os.system     | SE           | Có/Không      | SE             |             |

**7.3. Nếu có thể, dùng Docker**

Mức tối thiểu: AST + timeout + memory.  
Mức tốt: Docker container.  
Mức paper: Docker + resource limit + no network + mounted temp dir.

Nếu chưa làm Docker, phải ghi rõ:

Sandbox hiện tại là sandbox mức cơ bản, chưa phải cô lập hệ điều hành hoàn chỉnh.

**8\. Yêu cầu về hidden tests**

**8.1. Hidden tests phải có phân loại**

Không nên chỉ viết hidden test thủ công. Cần phân loại hidden tests:

| **Loại hidden test**      | **Ví dụ**                         |
| ------------------------- | --------------------------------- |
| Empty input               | \[\], "", {}                      |
| Single element            | \[1\], "a"                        |
| Negative numbers          | \[-1, -2, -3\]                    |
| Duplicate values          | \[1, 1, 2\]                       |
| Boundary value            | 0, 1, large number                |
| Wrong type / special case | None, mixed list nếu bài cho phép |
| Long input                | List/string dài                   |
| Randomized input          | Sinh test ngẫu nhiên              |
| Property-based            | Dùng Hypothesis hoặc rule         |

**8.2. Mỗi bài MBPP nên có bảng test coverage**

| **Task ID** | **Public tests** | **Hidden basic** | **Hidden edge** | **Hidden random/property** | **Tổng test** |
| ----------- | ---------------- | ---------------- | --------------- | -------------------------- | ------------- |
| MBPP_001    | 3                | 4                | 4               | 2                          | 13            |
| MBPP_002    | 3                | 3                | 5               | 2                          | 13            |

**8.3. Phân tích các bài còn lọt**

Nhóm phải có bảng:

| **Submission ID** | **Task**    | **Lỗi thật**          | **Vì sao lọt public** | **Vì sao lọt hidden**          | **Hidden test cần bổ sung** |
| ----------------- | ----------- | --------------------- | --------------------- | ------------------------------ | --------------------------- |
| SV008             | find_max    | Không xử lý list rỗng | Public không có \[\]  | Hidden chưa có \[\]            | Thêm find_max(\[\])         |
| SV019             | count_words | Sai chuỗi trắng       | Public không có " "   | Hidden chưa có whitespace-only | Thêm " "                    |

**9\. Yêu cầu về phản hồi tự động**

Đây là điểm giúp đề tài có giá trị giáo dục và có khả năng viết paper.

**9.1. Không chỉ trả Pass/Fail**

Mỗi bài fail cần có:

| **Thành phần phản hồi** | **Ví dụ**                                                     |
| ----------------------- | ------------------------------------------------------------- |
| Trạng thái              | Fail                                                          |
| Loại lỗi                | Wrong Answer / Runtime Error / Timeout / Memory / Unsafe Code |
| Test bị fail            | Hidden test #3                                                |
| Input gây lỗi           | \[1, 2, 2, 3\]                                                |
| Expected output         | 3                                                             |
| Actual output           | 2                                                             |
| Gợi ý                   | "Kiểm tra lại trường hợp có phần tử trùng lặp."               |

**9.2. Template feedback theo lỗi**

| **Loại lỗi** | **Feedback mẫu**                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| WA           | "Code chạy được nhưng kết quả sai ở một số test. Hãy kiểm tra lại điều kiện biên hoặc công thức xử lý." |
| RE           | "Code phát sinh lỗi khi chạy. Hãy kiểm tra kiểu dữ liệu đầu vào và truy cập chỉ số."                    |
| TLE          | "Code chạy quá thời gian cho phép. Hãy kiểm tra vòng lặp vô hạn hoặc độ phức tạp thuật toán."           |
| MLE          | "Code dùng quá nhiều bộ nhớ. Hãy tránh tạo cấu trúc dữ liệu quá lớn không cần thiết."                   |
| SE           | "Code sử dụng thao tác không an toàn hoặc không được phép trong hệ thống chấm."                         |

**9.3. Bảng đánh giá feedback**

| **Submission** | **Error type thật** | **Error type dự đoán** | **Feedback sinh ra** | **Đúng loại?** |
| -------------- | ------------------- | ---------------------- | -------------------- | -------------- |
| SV001          | WA                  | WA                     | Có                   | Có             |
| SV002          | RE                  | RE                     | Có                   | Có             |
| SV003          | TLE                 | TLE                    | Có                   | Có             |

**10\. Yêu cầu về demo**

Nhóm bắt buộc phải có demo chạy được.

**10.1. Demo tối thiểu**

Dạng notebook:

Input:  
\- Chọn Task ID  
\- Dán code bài nộp  
<br/>Output:  
\- Pass/Fail  
\- Số test pass/fail  
\- Loại lỗi  
\- Feedback

**10.2. Demo tốt hơn**

Dạng script:

python grade.py --task_id MBPP_001 --submission submissions/SV001.py

Output:

{  
"status": "fail",  
"passed": 7,  
"failed": 2,  
"error_type": "Wrong Answer",  
"failed_test": "hidden_03",  
"feedback": "Check the empty-list case."  
}

**10.3. Demo mức tốt nhất**

Dạng Streamlit/Gradio:

- Chọn bài.
- Nhập code.
- Bấm Grade.
- Hiển thị kết quả.
- Hiển thị feedback.

**11\. Bảng kết quả cuối cần có**

Nhóm phải có ít nhất 5 bảng sau.

**Bảng 1. Dữ liệu**

| **Thành phần**      | **Số lượng** |
| ------------------- | ------------ |
| MBPP tasks          |              |
| Submissions         |              |
| Correct submissions |              |
| Buggy submissions   |              |
| WA                  |              |
| RE                  |              |
| TLE                 |              |
| MLE                 |              |
| SE                  |              |

**Bảng 2. So sánh bộ test**

| **Test set**       | **FAR** | **FRR** | **Error detection** | **Avg latency/submission** | **Nhận xét** |
| ------------------ | ------- | ------- | ------------------- | -------------------------- | ------------ |
| Public only        |         |         |                     |                            |              |
| Public + Hidden v1 |         |         |                     |                            |              |
| Public + Hidden v2 |         |         |                     |                            |              |
| \+ Property-based  |         |         |                     |                            |              |

**Bảng 3. Phân loại lỗi**

| **Error type** | **Số bài thật** | **Phát hiện đúng** | **Phát hiện sai** | **Accuracy** |
| -------------- | --------------- | ------------------ | ----------------- | ------------ |
| WA             |                 |                    |                   |              |
| RE             |                 |                    |                   |              |
| TLE            |                 |                    |                   |              |
| MLE            |                 |                    |                   |              |
| SE             |                 |                    |                   |              |

**Bảng 4. Sandbox test**

| **Loại test**  | **Số test** | **Phát hiện đúng** | **Tỷ lệ** |
| -------------- | ----------- | ------------------ | --------- |
| Infinite loop  |             |                    |           |
| Memory bomb    |             |                    |           |
| Unsafe import  |             |                    |           |
| File access    |             |                    |           |
| Network access |             |                    |           |

**Bảng 5. Các bài còn lọt**

| **Submission** | **Task** | **Lỗi** | **Vì sao lọt** | **Cách bổ sung test** |
| -------------- | -------- | ------- | -------------- | --------------------- |
|                |          |         |                |                       |

**12\. Yêu cầu về báo cáo**

Báo cáo cuối của nhóm nên có cấu trúc:

- Giới thiệu bài toán
- Động cơ: public tests không đủ
- Dữ liệu MBPP và bài nộp mô phỏng
- Thiết kế hệ thống grading
- Public tests, hidden tests và hidden v2
- Runner và sandbox
- Phân loại lỗi và phản hồi tự động
- Thực nghiệm
- Kết quả
- Phân tích lỗi
- Demo
- Hạn chế
- Kết luận và hướng phát triển

**13\. Yêu cầu về bài hội nghị/paper**

Nếu muốn nâng lên thành paper, nhóm cần chuẩn bị thêm:

| **Thành phần**  | **Yêu cầu**                                                  |
| --------------- | ------------------------------------------------------------ |
| Title           | Có đóng góp rõ, không quá chung                              |
| Abstract        | Nêu vấn đề public test yếu, hidden test, sandbox, feedback   |
| Related Work    | Automated grading, MBPP, hidden tests, sandbox, feedback     |
| Method          | Mô tả pipeline grading                                       |
| Experiments     | Public vs Hidden vs Hidden v2                                |
| Error Analysis  | Bài sai bị lọt, bài đúng bị fail                             |
| Demo            | Có ví dụ chạy thử                                            |
| Limitation      | Dữ liệu còn mô phỏng, sandbox chưa hoàn toàn nếu chưa Docker |
| Reproducibility | Có code, config, data sample                                 |

**14\. Sản phẩm bắt buộc nhóm phải nộp**

| **Sản phẩm**                              | **Bắt buộc?**                    |
| ----------------------------------------- | -------------------------------- |
| Báo cáo hoàn chỉnh                        | Có                               |
| Notebook hoặc script chạy pipeline        | Có                               |
| mbpp_tasks.json                           | Có                               |
| submissions.json hoặc thư mục submissions | Có                               |
| hidden_tests_v1.json                      | Có                               |
| hidden_tests_v2.json                      | Có                               |
| grading_results.csv                       | Có                               |
| error_analysis.csv                        | Có                               |
| sandbox_tests.csv                         | Có                               |
| Demo notebook/script                      | Có                               |
| README hướng dẫn chạy                     | Có                               |
| requirements.txt                          | Khuyến khích                     |
| Slide 5-7 phút                            | Có nếu chuẩn bị báo cáo/hội nghị |

**15\. Tiêu chí chấm riêng cho Nhóm 67**

| **Tiêu chí**                                        | **Điểm** |
| --------------------------------------------------- | -------- |
| Dữ liệu MBPP và submissions đủ, phân loại lỗi rõ    | 15       |
| Public/Hidden/Hidden v2 được thiết kế hợp lý        | 15       |
| Runner chạy ổn định, có timeout/memory/safety check | 15       |
| Metric chuẩn: FAR, FRR, error detection, latency    | 15       |
| Phân tích bài sai bị lọt và bài đúng bị chấm sai    | 15       |
| Feedback tự động theo lỗi                           | 10       |
| Demo chạy được                                      | 10       |
| Minh chứng cá nhân, README, khai báo AI             | 5        |
| **Tổng**                                            | **100**  |

**16\. Kết luận yêu cầu**

Nhóm 67 cần hoàn thiện theo hướng:

**Không chỉ là hệ thống chấm Python, mà là hệ thống chấm Python có kiểm thử ẩn, sandbox, phân loại lỗi và phản hồi tự động.**

Để đủ mức báo cáo tốt, nhóm phải có:

- Ít nhất **100 bài nộp mô phỏng**.
- So sánh **Public only vs Public + Hidden v1 vs Public + Hidden v2**.
- Metric chính là **False Acceptance Rate**, không chỉ pass rate.
- Kiểm thử sandbox bằng bài lỗi cố ý.
- Bảng các bài sai còn lọt và hidden test cần bổ sung.
- Phản hồi tự động theo loại lỗi.
- Demo chạy được với một bài nộp Python.
