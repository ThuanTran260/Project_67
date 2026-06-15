**BỘ GIÁO DỤC VÀ ĐÀO TẠO**

**TRƯỜNG ĐẠI HỌC SÀI GÒN**

**KHOA CÔNG NGHỆ THÔNG TIN**

**\--------------🙦 🕮 🙤--------------**

**BÁO CÁO**

**NGHIÊN CỨU KHOA HỌC**

**HỌC PHẦN: NGÔN NGỮ LẬP TRÌNH PYTHON**

**ĐỀ TÀI: Xây dựng hệ thống chấm bài tự động nhằm giảm tải giảng viên**

**và tăng tính nhất quán trong đánh giá, đồng thời đánh giá hiệu quả của các cơ chế kiểm thử.**

**Sinh viên thực hiện: Trần Bảo Tín - 3124410356**

**Nguyễn Lê Nhựt Thắng - 3124560085**

**Trần Vĩnh Thuận - 3124410350**

**Giảng viên hướng dẫn: ThS.NCS. Hà Thanh Dũng**

_TP.HCM, tháng 5 năm 2026_

**Phân công nhiệm vụ:**

|     |     |
| --- | --- |
| **Họ và Tên** | **Nhiệm Vụ** |
| **Trần Bảo Tín** | **Mô tả bài toán, Thước đo đánh giá** |
| **Nguyễn Lê Nhựt Thắng** | **Hướng thực sơ bộ, Câu hỏi nghiên cứu** |
| **Trần Vĩnh Thuận** | **Tìm hiểu bộ dữ liệu, Tài liệu tham khảo** |

**TUẦN 1**

# 1\. MÔ TẢ BÀI TOÁN

## 1.1. Bài toán cần giải quyết

Trong bối cảnh giáo dục đại học hiện nay, số lượng sinh viên ngày càng tăng trong khi nguồn lực giảng viên có hạn, đặc biệt ở các môn học lập trình với lượng bài nộp lớn. Việc chấm bài thủ công không chỉ tốn nhiều thời gian mà còn dễ dẫn đến thiếu nhất quán giữa các lần chấm. Đề tài này hướng đến xây dựng một hệ thống chấm bài lập trình tự động (Automated Grading System) nhằm:

- Giảm tải khối lượng công việc chấm bài cho giảng viên.
- Đảm bảo tính nhất quán (consistency) trong đánh giá giữa các sinh viên và giữa các lần chấm.
- Hỗ trợ phản hồi nhanh, giúp sinh viên cải thiện kỹ năng ngay trong quá trình học.

Phạm vi chính của đề tài tập trung vào bài lập trình Python – loại bài phổ biến nhất trong các môn học lập trình nhập môn, đồng thời đánh giá hiệu quả của các cơ chế kiểm thử (test case) được sử dụng để chấm điểm tự động.

## 1.2. Đầu vào (Input)

Hệ thống nhận vào các thành phần sau:

- **Mã nguồn Python (.py)** do sinh viên nộp (code submission).
- **Bộ test case** gồm các cặp đầu vào/đầu ra chuẩn (input/output) được thiết kế trước bởi giảng viên hoặc lấy từ bộ dữ liệu chuẩn.
- **Đề bài và mô tả bài toán** (problem statement) kèm theo các ràng buộc về thời gian thực thi và bộ nhớ nếu có.
- **Đáp án mẫu hoặc rubric chấm điểm** (dùng để đối chiếu trong một số trường hợp có phân tích tĩnh).

## 1.3. Đầu ra (Output)

Sau khi xử lý, hệ thống trả về:

- **Điểm số** tổng hợp của bài nộp (ví dụ: 8/10).
- **Kết quả chi tiết từng test case**: Pass/Fail, kèm thông tin đầu vào, đầu ra mong đợi và đầu ra thực tế.
- **Phản hồi tự động (feedback)**: chỉ ra lỗi sai (runtime error, wrong answer, time limit exceeded) và gợi ý cải thiện nếu có.
- **Báo cáo tổng hợp cho giảng viên**: thống kê tỉ lệ pass/fail theo từng test case, phân phối điểm của cả lớp.

## 1.4. Ứng dụng thực tế

Hệ thống chấm bài tự động có thể được tích hợp vào nhiều môi trường giáo dục khác nhau. Trong phạm vi trường đại học, hệ thống phù hợp để triển khai trong các môn lập trình nhập môn (như học phần Ngôn ngữ lập trình Python) nơi số lượng bài nộp có thể lên tới hàng trăm bài mỗi buổi. Ở quy mô lớn hơn, hệ thống có thể tích hợp vào các nền tảng LMS như Moodle hay Canvas, hoặc phục vụ các khóa học trực tuyến đại trà (MOOC) nơi việc chấm thủ công là bất khả thi. Ngoài ra, các trung tâm đào tạo lập trình cũng có thể ứng dụng hệ thống này để đánh giá học viên theo thời gian thực.

## 1.5. Khó khăn chính

### 1.5.1. Thiết kế test case và vấn đề dương tính giả

Chất lượng của hệ thống chấm tự động phụ thuộc trực tiếp vào bộ test case. Nếu test case quá ít hoặc không bao phủ đủ các trường hợp biên (edge cases), hệ thống có thể chấm đúng cho những bài thực chất sai về mặt logic – đây gọi là hiện tượng dương tính giả (false positive). Ngược lại, test case quá nhiều làm tăng chi phí tính toán và thời gian chấm.

### 1.5.2. Đánh giá chất lượng code ngoài tính đúng đắn

Một bài code "đúng" theo test case chưa hẳn là một bài tốt. Các yếu tố như phong cách code (code style), độ phức tạp thuật toán, khả năng đọc hiểu và tái sử dụng là những tiêu chí quan trọng nhưng khó đưa vào chấm tự động một cách đầy đủ.

### 1.5.3. Gian lận học thuật

Sự phổ biến của các công cụ AI sinh code (như GitHub Copilot, ChatGPT) đặt ra thách thức mới trong việc phân biệt bài tự làm và bài do AI sinh ra. Bên cạnh đó, hành vi sao chép code (plagiarism) giữa sinh viên cũng cần được phát hiện, đòi hỏi tích hợp các thuật toán phát hiện trùng lặp như Winnowing.

### 1.5.4. Tính công bằng và nhất quán

Hệ thống phải đảm bảo chấm điểm nhất quán cho các bài nộp tương đương nhau, không phụ thuộc vào định dạng trình bày hay phong cách cá nhân của từng sinh viên. Đây là yêu cầu cốt lõi để hệ thống có thể thực sự thay thế được chấm tay trong thực tế.

# 2\. BỘ DỮ LIỆU

Do đề tài tập trung vào chấm bài lập trình Python, nhóm lựa chọn bốn bộ dữ liệu chuẩn được sử dụng rộng rãi trong cộng đồng nghiên cứu để phục vụ huấn luyện, đánh giá và so sánh hệ thống.

## 2.1. Mostly Basic Python Problems (MBPP)

**Nguồn:** Được xây dựng bởi nhóm nghiên cứu tại Google Research thông qua phương pháp crowd-sourcing từ người dùng có kiến thức Python cơ bản (Austin et al., 2021).

**Loại dữ liệu:** Văn bản mô tả bài toán và mã nguồn Python (.py).

**Nhãn:** Mỗi bài toán có một hàm Python hoàn chỉnh làm đáp án, vượt qua 3 test case do người tạo đề cung cấp.

**Đặc trưng chính:** Khoảng 1.000 bài toán cơ bản (xử lý chuỗi, toán học, list, dict). Tỉ lệ rò rỉ dữ liệu rất thấp (chỉ 3,3% bài có mã trùng lặp đáng kể với dữ liệu tiền huấn luyện), giúp đánh giá mô hình trung thực hơn.

**Hạn chế:** Bài toán đơn giản, thiếu đa dạng về chủ đề, mỗi bài chỉ có 3 test case nên dễ xảy ra false positive.

## 2.2. Automated Programming Progress Standard (APPS)

**Nguồn:** Thu thập từ các nền tảng lập trình cạnh tranh: Codeforces, Kattis, CodeWars (Hendrycks et al., 2021).

**Loại dữ liệu:** Văn bản đề bài và mã nguồn Python (.py).

**Nhãn:** Kết quả pass/fail theo từng test case; phân loại độ khó gồm ba mức: nhập môn (introductory), trung bình (interview), thi đấu (competition).

**Đặc trưng chính:** Đa dạng về độ khó và chủ đề thuật toán, phù hợp để đánh giá hệ thống trên nhiều mức năng lực sinh viên.

**Hạn chế:** Rủi ro false positive do test case hạn chế ở một số bài; nguy cơ mô hình ghi nhớ (memorization) thay vì suy luận logic.

## 2.3. LeetCode Dataset

**Nguồn:** Được giới thiệu bởi Xia et al. (2025), thu thập từ nền tảng LeetCode.

**Loại dữ liệu:** Mã nguồn Python (.py) kèm metadata văn bản và test case dạng JSON.

**Nhãn:** Độ khó (Dễ/Trung bình/Khó), chủ đề thuật toán (Array, DP, Math...), ngày phát hành để phân chia tập huấn luyện và kiểm tra theo thời gian.

**Đặc trưng chính:** 2.869 bài toán, bao phủ hơn 90% bài Python trên LeetCode. Mỗi bài có hơn 100 test case, giảm thiểu false positive. Phân chia theo mốc thời gian (tháng 7/2024) để tránh rò rỉ dữ liệu nghiêm ngặt.

**Hạn chế:** Chưa phân tích được độ phức tạp thời gian/không gian của giải pháp; bỏ qua một số dạng bài có nhiều điểm đầu vào.

## 2.4. HumanEval

**Nguồn:** Được xây dựng và phát hành bởi nhóm nghiên cứu OpenAI (Chen et al., 2021).

**Loại dữ liệu:** Mã nguồn Python, tập trung vào việc sinh các hàm độc lập từ docstring mô tả.

**Nhãn:** Mỗi bài gồm function signature, docstring, thân hàm và unit tests. Trung bình 7,7 test case/bài để xác định tính đúng đắn chức năng.

**Đặc trưng chính:** 164 bài toán được biên soạn thủ công hoàn toàn, đánh giá nhiều kỹ năng (thuật toán, toán học, đọc hiểu). Không có rò rỉ dữ liệu.

**Hạn chế:** Quy mô nhỏ (164 bài) và chỉ tập trung hàm độc lập, chưa phản ánh được thực tế lập trình trên codebase lớn.

# 3\. THƯỚC ĐO ĐÁNH GIÁ DỰ KIẾN

## 3.1. Vì sao không nên chỉ dùng Accuracy?

Accuracy đo tỉ lệ dự đoán đúng trên tổng số mẫu. Tuy nhiên, trong bài toán chấm điểm lập trình tự động, chỉ dùng Accuracy là chưa đủ vì một số lý do:

- Điểm số không phải nhị phân: kết quả chấm là điểm liên tục (ví dụ 0–10), không phải đúng/sai. Một bài bị chấm sai 1 điểm và sai 5 điểm đều bị tính như nhau nếu dùng Accuracy.
- Dữ liệu có thể mất cân bằng: nếu phần lớn bài đạt điểm cao, mô hình luôn đoán điểm cao cũng đạt Accuracy tốt nhưng thực chất vô dụng.
- Accuracy không đo được mức độ đồng thuận với giảng viên, không phản ánh được sai lệch hệ thống (systematic bias) trong chấm.

## 3.2. Các metric phù hợp

### 3.2.1. Pass@k (cho bài lập trình)

Pass@k đo xác suất ít nhất một trong k lời giải do hệ thống sinh ra vượt qua tất cả test case. Đây là metric chuẩn để đánh giá khả năng sinh code đúng. Trong bối cảnh chấm bài, Pass@1 (một lần nộp vượt qua tất cả test) là chỉ số quan trọng nhất.

### 3.2.2. Tỉ lệ pass test case (Test Pass Rate)

Đo phần trăm test case được vượt qua trên tổng số test case của một bài. Metric này phản ánh chính xác hơn mức độ đúng của một bài nộp thay vì chỉ cho điểm nhị phân đúng/sai. Ví dụ: bài pass 7/10 test case xứng đáng nhận điểm cao hơn bài pass 3/10.

### 3.2.3. Mean Absolute Error (MAE) và Root Mean Squared Error (RMSE)

Khi điểm số được coi là biến liên tục, MAE đo sai số tuyệt đối trung bình giữa điểm hệ thống và điểm giảng viên – dễ hiểu và phản ánh trực tiếp sai lệch. RMSE phạt nặng hơn các trường hợp sai lớn, phù hợp khi muốn hạn chế các lỗi chấm nghiêm trọng.

### 3.2.4. Cohen's Kappa (Quadratic Weighted Kappa – QWK)

Đo mức độ đồng thuận giữa hệ thống chấm và giảng viên, có tính đến yếu tố ngẫu nhiên. Phiên bản có trọng số bậc hai (QWK) phù hợp với thang điểm thứ bậc – sai lệch lớn bị phạt nặng hơn sai lệch nhỏ. Đây là metric chuẩn trong nhiều nghiên cứu đánh giá tự động.

### 3.2.5. Precision / Recall / F1-score

Áp dụng khi xem mỗi test case là một bài toán phân loại (pass/fail). Precision đo tỉ lệ những bài được chấm pass mà thực sự đúng; Recall đo khả năng phát hiện các bài thực sự đúng. F1-score là trung bình điều hòa của hai chỉ số trên, cân bằng giữa tránh bỏ sót và tránh chấm nhầm.

### 3.2.6. Latency (thời gian phản hồi)

Thời gian từ khi sinh viên nộp bài đến khi nhận kết quả. Đây không phải metric về độ chính xác nhưng ảnh hưởng trực tiếp đến khả năng triển khai thực tế. Một hệ thống cần hàng giờ để chấm sẽ không hữu ích trong môi trường lớp học.

## 3.3. Kết luận về lựa chọn metric

Nhóm dự kiến sử dụng kết hợp các metric sau: Pass@1 và Test Pass Rate làm chỉ số chính phản ánh chất lượng chấm; MAE/RMSE để đo sai lệch điểm; QWK để đo độ đồng thuận với giảng viên; và Latency để đánh giá tính khả dụng thực tế. Accuracy thuần túy sẽ không được dùng làm metric chính vì những lý do đã trình bày ở trên.

# 4.TÓM TẮT TÀI LIỆU THAM KHẢO

**5 Bài báo khoa học liên quan trực tiếp:**

## (Tan et al., 2025) A Comprehensive Review on Automated Grading Systems in STEM Using AI Techniques

Bài báo tổng quan hệ thống các phương pháp chấm điểm tự động trong lĩnh vực STEM, phân loại theo kỹ thuật AI sử dụng: machine learning truyền thống, deep learning và NLP. Phân tích ưu nhược điểm từng nhóm phương pháp theo từng môn học. Cung cấp bức tranh toàn cảnh về xu hướng nghiên cứu và các khoảng trống cần lấp đầy, là cơ sở lý thuyết quan trọng để nhóm xác định hướng tiếp cận.

##  (KEUNING et al., 2018) A Systematic Literature Review of Automated Feedback Generation for Programming Exercises

Khảo sát có hệ thống (SLR) các công trình về sinh phản hồi tự động cho bài tập lập trình theo chuẩn PRISMA. Phân loại các loại phản hồi: syntactic, semantic, hint-based và explanatory. Kết luận rằng phần lớn hệ thống hiện chỉ trả về phản hồi nhị phân (đúng/sai), thiếu tính sư phạm – đây là khoảng trống mà đề tài hướng đến bổ sung.

## (Paiva et al., 2022) Automated Assessment in Computer Science Education: A State-of-the-Art Review

Review toàn diện về đánh giá tự động trong giáo dục khoa học máy tính, bao gồm chấm code, trắc nghiệm và tự luận kỹ thuật. Phân tích các công cụ phổ biến (Web-CAT, BOSS, Praktomat) theo tiêu chí độ chính xác, khả năng mở rộng và tích hợp LMS. Nhấn mạnh sự cần thiết của phản hồi có ngữ cảnh thay vì chỉ cho điểm.

## (Mahdaoui et al., 2025)Automated Grading Method of Python Code Submission

Đề xuất phương pháp chấm tự động cho bài nộp Python kết hợp chạy test case với phân tích tĩnh mã nguồn bằng AST parsing. Thực nghiệm trên bài tập lập trình nhập môn đạt độ đồng thuận cao với giảng viên. Đây là công trình liên quan trực tiếp nhất đến pipeline kỹ thuật nhóm dự định triển khai.

## (Lee, 2021) Effectiveness of Real-time Feedback and Instructive Hints in Graduate CS Courses via Automated Grading System

Nghiên cứu thực nghiệm đánh giá hiệu quả của hệ thống chấm tự động tích hợp phản hồi thời gian thực trong lớp học cao học. Sinh viên nhận phản hồi tức thì có tỉ lệ sửa lỗi cao hơn và kết quả học tập cải thiện rõ rệt so với nhóm đối chứng. Cung cấp bằng chứng thực nghiệm trực tiếp ủng hộ giá trị của hệ thống trong giảng dạy thực tế.

**5 Tài liệu tham khảo về kỹ thuật và ứng dụng:**

**(Austin et al., 2021)** “**Program Synthesis with Large Language Models** ”: Nghiên cứu đánh giá Mô hình ngôn ngữ lớn trên “MBPP và MathQA-Python. Nghiên cứu cung cấp kỹ thuật sử dụng bài kiểm thử (test cases) để đánh giá mã nguồn

**(Chen et al., 2021)** “**Evaluating Large Language Models Trained on Code**”: Bài báo giới thiệu Codex, mô hình ngôn ngữ lớn tinh chỉnh từ GitHub để sinh mã Python. Đánh giá trên tập HumanEval cho thấy hiệu suất tỷ lệ thuận với kích thước mô hình và vượt trội 

**(Hendrycks et al., 2021)** “**Measuring Coding Challenge Competence With APPS**”: Nghiên cứu giới thiệu APPS, một bộ dữ liệu và nền tảng chuẩn đối sánh đo lường khả năng lập trình Python từ mô tả ngôn ngữ tự nhiên

**(Xia et al., 2025)** “**LeetCodeDataset: A Temporal Dataset for Robust Evaluation and Efficient Training of Code LLMs** ”: Cung cấp một bộ dữ liệu lớn gồm các bài toán Python thực tế trên nền tảng LeetCode, đi kèm hàng trăm ca kiểm thử mỗi bài để hạn chế tối đa rủi ro "dương tính giả"

(**Schleimer et al., 2003) “Winnowing: local algorithms for document fingerprinting”**:  Bài báo trình bày thuật toán Winnowing – thuật toán cốt lõi đứng sau hệ thống MOSS (Measure Of Software Similarity), MOSS là ứng dụng phát hiện đạo văn phổ biến nhất được tích hợp song song với các hệ thống chấm bài lập trình 

# 5\. HƯỚNG THỰC HIỆN SƠ BỘ

Nhóm dự kiến tiếp cận đề tài theo hướng xây dựng một pipeline chấm bài lập trình Python tự động dựa trên cơ chế kiểm thử (test-based grading), kết hợp với phân tích tĩnh mã nguồn và phản hồi tự động. Quá trình thực hiện được chia thành các giai đoạn cụ thể như sau.

## 5.1. Giai đoạn 1 – Chuẩn bị dữ liệu và môi trường

Nhóm sẽ tải và tiền xử lý các bộ dữ liệu đã chọn: MBPP, APPS, LeetCode Dataset và HumanEval. Với mỗi bài toán, nhóm chuẩn hóa định dạng đề bài, mã nguồn mẫu và bộ test case về một cấu trúc thống nhất để dễ xử lý ở các bước sau. Môi trường thực thi được thiết lập sử dụng Docker sandbox để đảm bảo an toàn khi chạy code sinh viên.

## 5.2. Giai đoạn 2 – Xây dựng cơ chế chấm dựa trên kiểm thử

Đây là nền tảng kỹ thuật của hệ thống. Với mỗi bài nộp, nhóm sẽ:

- Chạy toàn bộ test case và ghi lại kết quả pass/fail từng test.
- Tính điểm dựa trên tỉ lệ test case được vượt qua (Test Pass Rate).
- Ghi nhận các loại lỗi: Wrong Answer, Runtime Error, Time Limit Exceeded.

Bộ test case được đánh giá ở hai mức: test case công khai (hiển thị cho sinh viên) và test case ẩn (chỉ dùng khi chấm), nhằm tránh sinh viên tối ưu code chỉ theo test thấy được.

## 5.3. Giai đoạn 3 – Phân tích tĩnh mã nguồn

Song song với chấm test case, nhóm sẽ phân tích cấu trúc mã nguồn bằng thư viện ast của Python để trích xuất các đặc trưng: độ phức tạp cyclomatic, tuân thủ quy tắc đặt tên, số dòng code, sự hiện diện của docstring. Các đặc trưng này phục vụ cho việc đánh giá chất lượng code ngoài tính đúng đắn.

## 5.4. Giai đoạn 4 – Sinh phản hồi tự động

Dựa trên kết quả từ hai giai đoạn trên, hệ thống tự động sinh phản hồi cho sinh viên. Phản hồi bao gồm: test case nào fail kèm ví dụ đầu vào/đầu ra cụ thể, loại lỗi gặp phải, và gợi ý cải thiện ở mức cơ bản (ví dụ: "Kiểm tra lại xử lý trường hợp danh sách rỗng"). Nhóm sẽ đánh giá khả năng kết hợp LLM để sinh phản hồi chi tiết hơn nếu thời gian cho phép.

## 5.5. Giai đoạn 5 – Đánh giá và phân tích kết quả

Nhóm đánh giá hệ thống theo các metric đã trình bày ở Mục 3: Pass@1, Test Pass Rate, MAE/RMSE (so sánh với điểm giảng viên), QWK và Latency. Ngoài ra, nhóm thực hiện phân tích riêng về hiệu quả của cơ chế kiểm thử: so sánh kết quả chấm khi dùng ít test case (như MBPP: 3 test/bài) với nhiều test case (như LeetCode: 100+ test/bài) để trả lời câu hỏi nghiên cứu đặt ra.

# 6\. CÂU HỎI NGHIÊN CỨU BAN ĐẦU

Trong quá trình thực hiện đề tài, nhóm đặt ra ba câu hỏi nghiên cứu cốt lõi sau:

## RQ1: Số lượng và chất lượng test case ảnh hưởng như thế nào đến độ tin cậy của hệ thống chấm tự động?

Câu hỏi này xuất phát trực tiếp từ mục tiêu "đánh giá hiệu quả của các cơ chế kiểm thử" trong đề tài. Bộ dữ liệu được chọn (MBPP có 3 test/bài, LeetCode có 100+ test/bài) tạo điều kiện tự nhiên để so sánh. Nhóm kỳ vọng chứng minh được ngưỡng số lượng test case tối thiểu để hệ thống chấm có độ tin cậy chấp nhận được (false positive rate dưới một ngưỡng nhất định).

## RQ2: Hệ thống chấm tự động có đạt mức độ đồng thuận chấp nhận được với giảng viên khi chấm bài lập trình Python nhập môn hay không?

Đây là câu hỏi về tính khả dụng thực tế. Nhóm sẽ thu thập một tập bài nộp thực tế từ môn học, cho giảng viên chấm tay và so sánh với kết quả hệ thống qua các metric QWK, MAE. Mức QWK ≥ 0.7 thường được xem là đủ để hệ thống có thể hỗ trợ giảng viên, thay vì thay thế hoàn toàn.

## RQ3: Phản hồi tự động từ hệ thống có thực sự giúp sinh viên cải thiện bài làm trong các lần nộp tiếp theo hay không?

Câu hỏi này đánh giá tác động sư phạm của hệ thống. Nhóm dự kiến theo dõi hành vi nộp lại (resubmission) của sinh viên sau khi nhận phản hồi, so sánh tỉ lệ cải thiện điểm giữa hai nhóm: một nhóm nhận phản hồi chi tiết từ hệ thống và một nhóm chỉ nhận kết quả pass/fail. Câu hỏi này liên kết trực tiếp với mục tiêu "tăng tính nhất quán trong đánh giá và hỗ trợ phản hồi nhanh" của đề tài.

**Tài Liệu tham khảo**

Athiwaratkun, B., Gouda, S. K., Wang, Z., Li, X., Tian, Y., Tan, M., Ahmad, W. U., Wang, S., Sun, Q., Shang, M., Gonugondla, S. K., Ding, H., Kumar, V., Fulton, N., Farahani, A., Jain, S., Giaquinto, R., & Qian, H. (2023, 2 2). MULTI-LINGUAL EVALUATION OF CODE GENERATION MODEL. _ICLR_. https://openreview.net/forum?id=Bo7eeXm6An8

Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., & Sutton, C. (2021, 8 21). Program Synthesis with Large Language Models. https://doi.org/10.48550/arXiv.2108.07732

Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger, G., Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., & Gray, S. (2021, 7 14). Evaluating Large Language Models Trained on Code. https://doi.org/10.48550/arXiv.2107.03374

Hendrycks, D., Basart, S., Kadavath, S., Mazeika, M., Arora, A., Guo, E., Burns, C., Puranik, S., He, H., Song, D., & Steinhardt, J. (2021, 5 20). Measuring Coding Challenge Competence With APPS. _NeurIPS_. https://doi.org/10.48550/arXiv.2105.09938

KEUNING, H., JEURING, J., & HEEREN, B. (2018, 9 28). ASystematic Literature Review of Automated Feedback Generation for Programming Exercises. https://doi.org/10.1145/3231711

Lee, H. H. (2021, 3 5). Effectiveness of Real-time Feedback and Instructive Hints in Graduate CS Courses via Automated Grading System. https://doi.org/10.1145/3408877.3432463

Mahdaoui, M., Nouh, ,. S., Alaoui, M. S. E. K., & Kandali, K. (2025, 8 7). Automated Grading Method of Python Code Submissions Using Large Language Models and Machine Learning. _Information_. https://doi.org/10.3390/info16080674

Paiva, J. C., LEAL, J. P., & FIGUEIRA, Á. (2022, 6 9). Automated Assessment in Computer Science Education:A State-of-the-Art Review. _ACM_. https://doi.org/10.1145/3513140

Schleimer, S., Wilkerson, D. S., & Aiken, A. (2003, 6 9). Winnowing: local algorithms for document fingerprinting. _SIGMOD '03_. https://doi.org/10.1145/872757.872770

Tan, L. Y., Hu, S., Yeo, D. J., & Cheong, K. H. (2025, 9 2). AComprehensive Review on Automated Grading Systems in STEMUsingAITechniques. _Mathematics_. https://doi.org/10.3390/math13172828

Xia, Y., Shen, W., Wang, Y., Liu, J. K., Sun, H., Wu, S., Hu, J., & Xu, X. (2025, 4 20). LeetCodeDataset: A Temporal Dataset for Robust Evaluation and Efficient Training of Code LLMs. https://arxiv.org/html/2504.14655v1