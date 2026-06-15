**Nhận xét báo cáo tuần 3 của Nhóm 67 - Đề tài 18: Automated Python Grading System với kiểm thử ẩn và phản hồi tự động**

Căn cứ theo báo cáo tuần 3, báo cáo tuần 2 revised và kế hoạch tuần 3, **Nhóm 67 có tiến bộ rất rõ so với tuần 2**. Tuần 2, nhóm mới thử nghiệm trên 15 bài MBPP và 12 bài nộp mô phỏng; baseline runner cho thấy FPR = 25,0% với 3/12 bài sai logic nhưng vẫn pass public test. Sang tuần 3, nhóm đã mở rộng lên **50 bài MBPP**, **50 bài nộp mô phỏng**, thiết kế **hidden test v2**, bổ sung **runner_v2** với memory limit bằng psutil, AST safety check, module thống kê lỗi tự động và bảng so sánh 3 bộ test.

Báo cáo bám sát yêu cầu riêng của kế hoạch tuần 3 cho đề tài **Automated Python Grading**: mở rộng số bài MBPP và bài nộp mô phỏng, định nghĩa rõ False Positive Rate, kiểm chứng hidden test, bổ sung sandbox an toàn hơn và thống kê lỗi tự động.

**Điểm đánh giá: 90/100 - Mức Tốt mạnh.**

**1\. Nhận xét tổng quan**

| **Nội dung**            | **Đánh giá**                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Cấu trúc báo cáo tuần 3 | Tốt, đầy đủ các mục chính                                                                                                 |
| Sửa lỗi tuần 2          | Tốt, mở rộng dữ liệu và sửa nhiều hạn chế kỹ thuật                                                                        |
| Dữ liệu                 | 50 bài MBPP, 50 bài nộp mô phỏng                                                                                          |
| Baseline                | Bộ 3 public tests trên 50 bài nộp                                                                                         |
| Phương pháp chính       | Hidden Test v2 + Runner v2 + thống kê lỗi tự động                                                                         |
| Metric                  | FPR, Avg Test Pass Rate, WA/RE/SE/TLE/MLE, latency                                                                        |
| Kết quả chính           | FPR giảm từ 18,0% ở Set 1 xuống 6,0% ở Set 3                                                                              |
| Phân tích lỗi           | Tốt, có danh sách 9 false positive và 3 bài còn lọt Set 3                                                                 |
| Minh chứng cá nhân      | Rõ, có nhiều file/code/notebook cụ thể                                                                                    |
| Vấn đề chính            | Cần thống nhất một số số liệu theo topic, làm rõ định nghĩa FPR, kiểm thử MLE/TLE thực tế và nâng cấp sandbox bằng Docker |

**2\. Điểm mạnh**

**2.1. Nhóm đã mở rộng thực nghiệm đúng yêu cầu**

Tuần 2 chỉ có 15 bài MBPP và 12 bài nộp mô phỏng. Tuần 3, nhóm mở rộng lên:

| **Thành phần**    | **Tuần 2** | **Tuần 3** |
| ----------------- | ---------- | ---------- |
| Bài MBPP          | 15         | 50         |
| Bài nộp mô phỏng  | 12         | 50         |
| Public test       | 3/bài      | 3/bài      |
| Hidden test       | 6/bài      | 6-10/bài   |
| Solution mẫu pass | 15/15      | 50/50      |

Đây là cải thiện lớn, đúng với yêu cầu của kế hoạch tuần 3 là mở rộng số bài MBPP và số bài nộp mô phỏng cho đề tài Automated Python Grading.

**2.2. Baseline được định nghĩa đúng với bản chất đề tài**

Nhóm giải thích hợp lý rằng baseline của đề tài này không phải Logistic Regression hay Decision Tree, mà là **test-case runner với 3 public tests**. Đây là đúng, vì bài toán chấm code có đáp án xác minh được qua thực thi, không phải bài toán phân loại học máy.

Baseline tuần 3 được chạy lại trên 50 bài nộp:

| **Metric**              | **Baseline tuần 2** | **Baseline tuần 3** |
| ----------------------- | ------------------- | ------------------- |
| FPR                     | 25,0%               | 18,0%               |
| False Positive          | 3/12                | 9/50                |
| Latency trung bình/test | 13 ms               | 45,7 ms             |

Nhóm cũng nhận xét đúng rằng FPR giảm từ 25,0% xuống 18,0% chủ yếu do thay đổi phân bố tập dữ liệu, không phải do baseline tốt hơn. Đây là cách diễn giải trung thực.

**2.3. Phương pháp chính có ý nghĩa rõ ràng**

Phương pháp chính tuần 3 gồm ba thành phần:

| **Thành phần** | **Vai trò**                                       |
| -------------- | ------------------------------------------------- |
| Hidden Test v2 | Tăng độ phủ edge case, 6-10 hidden test/bài       |
| Runner v2      | Sandbox an toàn hơn, có AST check và memory limit |
| error_stats.py | Thống kê lỗi tự động, FPR, WA/RE/SE/TLE/MLE       |

Cách thiết kế này phù hợp với đề tài. Nhóm không chỉ tăng số lượng test, mà còn nâng cấp hạ tầng chấm code và thống kê lỗi.

**2.4. Kết quả thực nghiệm trả lời được RQ1**

Bảng so sánh 3 bộ test là điểm mạnh nhất của báo cáo:

| **Bộ test**                   | **Tổng bài nộp** | **False Positive** | **FPR** | **WA phát hiện** | **RE phát hiện** |
| ----------------------------- | ---------------- | ------------------ | ------- | ---------------- | ---------------- |
| Set 1: 3 public               | 50               | 9                  | 18,0%   | 37               | 62               |
| Set 2: 3 public + 6 hidden    | 50               | 4                  | 8,0%    | 89               | 148              |
| Set 3: 3 public + 6-10 hidden | 50               | 3                  | 6,0%    | 131              | 237              |

Kết quả này cho thấy hidden tests giúp giảm FPR từ **18,0% xuống 6,0%**, đồng thời phát hiện nhiều lỗi WA và RE hơn. Đây là bằng chứng tốt cho nhận định: public test quá ít dễ bỏ sót bài sai, còn hidden test giúp bắt lỗi edge case tốt hơn.

**2.5. Phân tích false positive rất tốt**

Nhóm đã liệt kê 9 bài false positive ở Set 1 và chỉ ra bài nào bị bắt ở Set 2/Set 3. Đặc biệt, nhóm xác định rõ 3 bài vẫn lọt Set 3:

| **Bài**                 | **Lỗi**                         | **Vì sao còn lọt**            |
| ----------------------- | ------------------------------- | ----------------------------- |
| SV008 - find_max        | Không xử lý list rỗng           | Hidden test còn thiếu \[\]    |
| SV019 - count_words     | Sai với chuỗi rỗng/khoảng trắng | Hidden test còn thiếu " "     |
| SV032 - get_list_length | len(lst)+1                      | Test chưa phát hiện logic này |

Phần này đáp ứng rất tốt yêu cầu phân tích lỗi của tuần 3: mô hình/hệ thống sai ở đâu, vì sao sai, và tuần 4 sửa thế nào.

**2.6. Nâng cấp sandbox là điểm cộng kỹ thuật**

Tuần 3, nhóm bổ sung:

- kiểm tra bộ nhớ bằng psutil;
- giới hạn RAM 128 MB;
- timeout 1 giây;
- AST safety check;
- chặn os, sys, subprocess, socket, ctypes, multiprocessing, threading, shutil, pathlib, glob;
- chặn eval, exec, open, \__import_\_, compile, globals, locals;
- chạy trong thư mục tạm riêng.

Đây là tiến bộ rõ so với tuần 2, khi giới hạn bộ nhớ và kiểm soát sandbox vẫn còn là kế hoạch.

**2.7. Lịch sử làm việc và minh chứng cá nhân tốt**

Bảng lịch sử làm việc tuần 3 có thời điểm, thành viên, nội dung công việc, sản phẩm/minh chứng và trạng thái. Phần minh chứng cá nhân cũng liệt kê rõ file như mbpp_50.json, hidden_v2.json, runner_v2.py, error_stats.py, comparison_3sets.py, comparison_3sets.csv, generate_plots.py, submissions_50.json.

Đây là một trong những nhóm có phần minh chứng cá nhân rõ hơn nhiều so với yêu cầu tối thiểu.

**3\. Vấn đề cần chỉnh sửa**

**3.1. Cần làm rõ lại định nghĩa FPR**

Nhóm định nghĩa FPR theo đơn vị bài nộp:

FPR = số bài nộp có lỗi nhưng pass toàn bộ test / tổng số bài nộp × 100%.

Cách định nghĩa này có thể dùng được trong báo cáo nội bộ, nhưng cần ghi rõ đây là **False Acceptance Rate trên toàn bộ bài nộp**, vì FPR trong học máy thường được hiểu là:

FP / số mẫu âm thật.

Trong dữ liệu tuần 3, có 47 bài buggy và 3 bài AC. Vì vậy, ngoài cách tính hiện tại, nhóm nên báo thêm:

| **Bộ test** | **FP / tổng bài** | **FP / bài buggy** |
| ----------- | ----------------- | ------------------ |
| Set 1       | 9/50 = 18,0%      | 9/47 = 19,1%       |
| Set 2       | 4/50 = 8,0%       | 4/47 = 8,5%        |
| Set 3       | 3/50 = 6,0%       | 3/47 = 6,4%        |

Điều này giúp metric rõ ràng hơn và tránh tranh luận về thuật ngữ.

**3.2. Có mâu thuẫn nhỏ ở số lượng bài theo chủ đề**

Ở phần dữ liệu, báo cáo ghi phân bố chủ đề:

| **Chủ đề** | **Số bài** |
| ---------- | ---------- |
| list       | 20         |
| math       | 14         |
| string     | 16         |

Nhưng phần FPR theo chủ đề Set 1 lại ghi:

| **Chủ đề** | **Số bài nộp** |
| ---------- | -------------- |
| math       | 16             |
| list       | 20             |
| string     | 14             |

Như vậy **math/string bị đổi số lượng 14 và 16**. Nhóm cần kiểm tra lại topic trong mbpp_50.json và submissions_50.json, sau đó thống nhất tất cả bảng và biểu đồ.

**3.3. Trường hợp SV032 cần kiểm tra lại logic**

Báo cáo ghi SV032 dùng len(lst)+1 nhưng vẫn lọt Set 3. Đây là điểm cần kiểm tra kỹ, vì nếu test case kiểm tra đúng độ dài danh sách, hàm len(lst)+1 gần như chắc chắn phải sai với mọi input bình thường.

Có ba khả năng:

| **Khả năng**                                    | **Cần kiểm tra**                |
| ----------------------------------------------- | ------------------------------- |
| Mô tả lỗi của SV032 bị ghi sai                  | Code thật không phải len(lst)+1 |
| Expected output của Task 30 bị sai              | Test case thiết kế nhầm         |
| Hàm/test runner gọi sai function hoặc sai input | Runner không kiểm tra đúng hàm  |

Đây là lỗi cần ưu tiên sửa vì nó liên quan trực tiếp đến độ tin cậy của hidden test và runner.

**3.4. MLE/TLE chưa được kiểm chứng bằng ca lỗi thực tế**

Báo cáo nói runner v2 hỗ trợ MLE bằng psutil và timeout 1 giây, nhưng kết quả thực nghiệm TLE = 0 và MLE = 0. Điều này có thể hợp lý vì MBPP nhỏ, nhưng chưa chứng minh hệ thống thật sự bắt được MLE/TLE.

Tuần 4 cần bổ sung test kiểm chứng:

| **Loại lỗi**           | **Bài nộp mô phỏng cần thêm**    |
| ---------------------- | -------------------------------- |
| TLE                    | while True: pass, đệ quy vô hạn  |
| MLE                    | tạo list cực lớn, nhân chuỗi lớn |
| Output overflow        | in ra chuỗi rất dài              |
| File/network violation | thử open, socket, subprocess     |
| Import violation       | thử os, sys, pathlib             |

Nếu có module sandbox, cần có ca kiểm thử chứng minh sandbox hoạt động.

**3.5. Latency cần báo theo bài nộp, không chỉ theo test**

Báo cáo ghi latency trung bình/test ổn định khoảng 44-45 ms/test. Tuy nhiên, khi tăng số test từ 3 lên 9-13, thời gian chấm **mỗi bài nộp** chắc chắn tăng.

Cần bổ sung:

| **Metric**                     | **Ý nghĩa**                                  |
| ------------------------------ | -------------------------------------------- |
| Latency/test                   | Chi phí từng test                            |
| Latency/submission             | Thời gian sinh viên chờ kết quả              |
| Latency toàn bộ 50 submissions | Chi phí batch grading                        |
| P95 latency                    | Đánh giá trường hợp chậm                     |
| Early-exit latency             | Tách riêng bài fail sớm và bài chạy hết test |

Hiện tại, kết luận "latency ổn định" đúng ở mức per-test, nhưng chưa đủ cho trải nghiệm chấm bài thực tế.

**3.6. Sandbox hiện tại vẫn chưa phải cô lập hoàn toàn**

AST safety check và psutil là cải thiện tốt, nhưng vẫn chưa thay thế được sandbox thật. Một số rủi ro còn lại:

| **Rủi ro**                              | **Ghi chú**                                                        |
| --------------------------------------- | ------------------------------------------------------------------ |
| AST blacklist dễ bị bypass              | Cách gọi gián tiếp hoặc object introspection có thể vượt blacklist |
| Chưa tắt network ở mức hệ điều hành     | Chỉ chặn import chưa đủ tuyệt đối                                  |
| Chưa giới hạn filesystem bằng container | Thư mục tạm giúp giảm rủi ro nhưng chưa cô lập hoàn toàn           |
| psutil là giám sát mềm                  | Có độ trễ polling 5 ms                                             |
| Chưa có Docker/namespace/seccomp        | Cần cho triển khai thật                                            |

Nhóm đã ghi kế hoạch dùng Docker ở tuần 4, đây là hướng đúng.

**3.7. Dữ liệu bài nộp vẫn là mô phỏng**

Bộ 50 bài nộp mô phỏng tốt hơn tuần 2, nhưng vẫn do nhóm tự tạo. Vì vậy, kết quả FPR hiện tại phản ánh chất lượng trên **kịch bản lỗi do nhóm thiết kế**, chưa đại diện cho hành vi sinh viên thật.

Tuần 4 nên bổ sung:

| **Dữ liệu cần thêm**                       | **Mục tiêu**            |
| ------------------------------------------ | ----------------------- |
| Bài nộp thật từ sinh viên nếu có           | Đánh giá thực tế hơn    |
| Bài sinh bởi LLM với prompt khác nhau      | Mô phỏng lỗi đa dạng    |
| Bài có thuật toán chậm                     | Kiểm tra TLE            |
| Bài cố tình tấn công sandbox               | Kiểm tra bảo mật        |
| Bài đúng nhưng khác cách viết solution mẫu | Kiểm tra false negative |

**3.8. Tài liệu tham khảo cần rà lại một số nguồn mới**

Tài liệu tham khảo có các nguồn phù hợp như MBPP/program synthesis, automated assessment, Web-CAT. Tuy nhiên, một số nguồn năm 2025 cần kiểm tra lại metadata và mức độ liên quan. Nên ưu tiên thêm tài liệu về:

| **Nhóm tài liệu**                     | **Nên bổ sung**                     |
| ------------------------------------- | ----------------------------------- |
| Secure code execution                 | sandbox, container, seccomp         |
| Mutation testing                      | tạo bài sai có chủ đích             |
| Property-based testing                | Hypothesis/QuickCheck               |
| Automated feedback                    | phân tích lỗi và phản hồi sinh viên |
| Hidden tests in programming education | độ tin cậy của public/hidden tests  |

**4\. Đánh giá theo rubric tuần 3**

| **Tiêu chí**                                               | **Điểm**   | **Nhận xét**                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1\. Sửa lỗi và hoàn thiện dữ liệu từ tuần 2**            | **14/15**  | Nhóm mở rộng từ 15 bài/12 submissions lên 50 bài/50 submissions, có phân bố topic, phân bố error type, sanity check 50/50 solution mẫu pass. Điểm trừ nhỏ vì số lượng math/string trong các bảng topic chưa thống nhất và dữ liệu vẫn là mô phỏng.                 |
| **2\. Baseline chạy đúng và có metric phù hợp**            | **14/15**  | Baseline 3 public tests được định nghĩa đúng với bài toán chấm code, chạy lại trên 50 bài nộp, có FPR, pass rate, WA/RE/SE và latency. Điểm trừ vì cần làm rõ FPR theo tổng submissions và theo faulty submissions.                                                |
| **3\. Triển khai phương pháp chính**                       | **23/25**  | Hidden Test v2, runner_v2, memory limit bằng psutil, AST safety check và error_stats.py phù hợp đề tài. Điểm trừ vì sandbox chưa cô lập hoàn toàn bằng Docker và MLE/TLE chưa được kiểm chứng bằng ca lỗi thực tế.                                                 |
| **4\. So sánh baseline với phương pháp chính**             | **14/15**  | Có bảng so sánh Set 1, Set 2, Set 3 trên cùng 50 bài nộp; FPR giảm từ 18,0% xuống 6,0%, WA/RE phát hiện tăng rõ. Điểm trừ nhỏ vì cần thêm latency theo submission và giải thích kỹ tác động fail-fast.                                                             |
| **5\. Phân tích lỗi và nhận xét kết quả**                  | **13/15**  | Phân tích 9 false positive của Set 1 và 3 bài còn lọt Set 3 rất tốt. Điểm trừ vì trường hợp SV032 có dấu hiệu không hợp lý, cần kiểm tra lại test/runner/mô tả lỗi; feedback tự động mới là kế hoạch, chưa có kết quả.                                             |
| **6\. Lịch sử làm việc và minh chứng cá nhân**             | **10/10**  | Lịch sử làm việc đầy đủ theo thời điểm, có phân công rõ và file minh chứng cụ thể cho từng thành viên. Phần này đạt tốt yêu cầu tuần 3.                                                                                                                            |
| **7\. Khai báo AI, tài liệu tham khảo, hình thức báo cáo** | **2/5**    | Có khai báo AI theo từng thành viên và có tài liệu tham khảo. Tuy nhiên hình thức còn vài lỗi số liệu/topic chưa thống nhất, một số nhận xét hơi mạnh, và tài liệu tham khảo cần bổ sung nguồn trực tiếp hơn về sandbox/property-based testing/automated feedback. |
| **Tổng**                                                   | **90/100** | **Tốt mạnh**                                                                                                                                                                                                                                                       |

**Tổng điểm:**  
**14 + 14 + 23 + 14 + 13 + 10 + 2 = 90/100**

**5\. So sánh với tuần 2**

| **Nội dung**     | **Tuần 2 revised**               | **Tuần 3**                                          |
| ---------------- | -------------------------------- | --------------------------------------------------- |
| Quy mô MBPP      | 15 bài                           | 50 bài                                              |
| Bài nộp mô phỏng | 12 bài                           | 50 bài                                              |
| Baseline         | Runner public/hidden ban đầu     | Baseline 3 public chạy trên 50 bài                  |
| Hidden test      | 6 hidden test/bài                | 6-10 hidden test/bài theo độ khó                    |
| FPR              | 25,0% trên 12 bài                | 18,0% Set 1, 8,0% Set 2, 6,0% Set 3                 |
| Sandbox          | Timeout, AST/import check cơ bản | Thêm psutil, memory limit, AST safety check mở rộng |
| Thống kê lỗi     | WA/RE/SE/TLE cơ bản              | WA/RE/SE/TLE/MLE, FPR theo set/topic, latency       |
| Phân tích lỗi    | 3 false positive cụ thể          | 9 FP Set 1, 4 FP Set 2, 3 FP Set 3                  |
| Minh chứng       | Có file cơ bản                   | Có nhiều script/notebook/CSV/PNG rõ hơn             |

**Kết luận:** Tuần 3 tốt hơn tuần 2 rõ rệt về quy mô dữ liệu, độ chặt của hidden test, bảo mật runner, thống kê lỗi và phân tích false positive.

**6\. Yêu cầu nhóm cần sửa trước tuần 4**

| **Việc cần làm**                                                                  | **Mức độ ưu tiên** |
| --------------------------------------------------------------------------------- | ------------------ |
| Thống nhất số lượng topic: math/list/string trong tất cả bảng và biểu đồ          | Rất cao            |
| Làm rõ FPR là trên tổng submissions hay trên faulty submissions                   | Rất cao            |
| Báo thêm faulty acceptance rate = FP / số bài buggy                               | Rất cao            |
| Kiểm tra lại SV032 vì len(lst)+1 mà vẫn pass là bất thường                        | Rất cao            |
| Bổ sung test chứng minh MLE/TLE thật sự hoạt động                                 | Rất cao            |
| Báo latency theo submission, không chỉ theo test                                  | Cao                |
| Báo P95 latency và tổng thời gian chấm 50 submissions                             | Cao                |
| Thêm các bài nộp tấn công sandbox: open, os, socket, infinite loop, memory bomb   | Rất cao            |
| Chuyển sandbox sang Docker hoặc container nhẹ                                     | Cao                |
| Bổ sung property-based testing hoặc sinh hidden test tự động bằng rule            | Cao                |
| Tách lỗi RE thành IndexError, ZeroDivisionError, TypeError                        | Cao                |
| Tạo module feedback thật, không chỉ thống kê WA/RE/SE                             | Cao                |
| Rà soát tài liệu tham khảo về sandbox, automated feedback, property-based testing | Trung bình         |

**7\. Định hướng tuần 4**

| **Ưu tiên** | **Nội dung**                        | **Mục tiêu**                            |
| ----------- | ----------------------------------- | --------------------------------------- |
| 1           | Sửa 3 bài còn lọt Set 3             | Đưa FPR về gần 0%                       |
| 2           | Sinh hidden test tự động theo topic | Giảm phụ thuộc viết test thủ công       |
| 3           | Dùng property-based testing         | Bắt edge case tốt hơn                   |
| 4           | Kiểm thử sandbox bằng bài tấn công  | Xác minh an toàn hệ thống               |
| 5           | Docker/container sandbox            | Cô lập môi trường thực thi              |
| 6           | Tách RE thành lỗi cụ thể            | Tạo feedback hữu ích hơn                |
| 7           | Mở rộng submissions lên 100-150     | Đánh giá ổn định hơn                    |
| 8           | Báo latency theo submission/P95     | Đánh giá triển khai thực tế             |
| 9           | Sinh phản hồi tự động               | Chuyển từ chấm điểm sang hỗ trợ học tập |
| 10          | Chuẩn hóa lại bảng số liệu/topic    | Làm báo cáo cuối chắc hơn               |

**8\. Kết luận**

**Điểm đánh giá: 90/100 - Mức Tốt mạnh.**

Báo cáo tuần 3 của **Nhóm 67** có chất lượng tốt và tiến bộ rõ so với tuần 2. Nhóm đã mở rộng dữ liệu từ 12 bài nộp lên 50 bài nộp, chạy lại baseline, triển khai hidden test v2, nâng cấp sandbox, định nghĩa FPR, thống kê lỗi tự động và phân tích false positive khá sâu.

Mức điểm 90/100 phản ánh đúng chất lượng hiện tại: nhóm hoàn thành tốt các yêu cầu chính của tuần 3 và có minh chứng rõ. Các điểm cần hoàn thiện nằm ở việc thống nhất số liệu topic, làm rõ cách tính FPR, kiểm tra lại trường hợp SV032, bổ sung kiểm thử thực tế cho MLE/TLE và nâng sandbox lên mức cô lập mạnh hơn bằng Docker/container trong tuần 4.