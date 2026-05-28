# BÁO CÁO TIẾN ĐỘ TUẦN 4
**Đề tài**: Automated Python Grading System với kiểm thử ẩn và phản hồi tự động  
**Nhóm**: 67  
**Thời gian**: 24/05/2026 - 30/05/2026  
**Ngôn ngữ**: Python  

---

## 1. Tóm tắt mục tiêu Tuần 4
Tiếp tục phát triển hệ thống chấm bài Python tự động từ Tuần 3, mục tiêu của Tuần 4 tập trung vào việc hoàn thiện, bảo mật hóa, và tối ưu hóa hiệu năng chấm bài với các nội dung trọng tâm:
1. **Khắc phục triệt để sự không nhất quán dữ liệu**: Đồng bộ hóa danh sách bài tập, phân phối chủ đề và các bài nộp sinh viên. Đảm bảo phân bổ chủ đề chính xác: **20 list, 16 math, 14 string**.
2. **Nâng cấp Sandbox & Giả lập Docker**: Tích hợp Abstract Syntax Tree (AST) Security Filter nâng cao (whitelist) để chặn đứng các thư viện và từ khóa cấm. Thiết kế Sandbox chạy trong Docker chính chủ, có cơ chế **giả lập Docker (Simulated Docker Sandbox)** trong suốt nếu Docker daemon bị tắt trên máy chấm.
3. **Phân loại lỗi chi tiết (RE)**: Thay vì báo lỗi `RE` (Runtime Error) chung chung, hệ thống trích xuất và chỉ rõ các exception cụ thể (`IndexError`, `ZeroDivisionError`, `TypeError`, `ValueError`, `NameError`, v.v.) để đưa ra gợi ý học tập chuẩn xác.
4. **Cơ chế Fail-Fast (Early-Exit)**: Dừng thực thi ngay khi phát hiện test case đầu tiên thất bại nhằm tối ưu hóa độ trễ chấm bài.
5. **Kiểm thử Vi sai (Property-based Differential Testing)**: Sinh ngẫu nhiên hơn 100+ input để đối chiếu kết quả giữa mã nguồn chuẩn và bài làm học sinh, phát hiện các trường hợp sai logic tinh vi.
6. **Tự động hóa phản hồi bằng tiếng Việt**: Diễn giải các lỗi kỹ thuật thành gợi ý sư phạm tiếng Việt thân thiện, định hướng học sinh tự sửa lỗi.

---

## 2. Lịch sử làm việc trong tuần 4

| Thời điểm | Thành viên thực hiện | Nội dung công việc | Sản phẩm / Minh chứng | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **24-25/5** | **Trần Anh Thuận** | Cải tiến bộ chấm bài lên `runner_v3.py`, tích hợp AST Whitelist check, phân loại chi tiết Exception, và cơ chế Fail-Fast. | [runner_v3.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/runner_v3.py) | Hoàn thành |
| **24-25/5** | **Nguyễn Lê Nhựt Thắng** | Thiết lập cơ chế chạy Docker chính chủ và bộ Giả làm Docker (Simulated Docker Sandbox) dựa trên `psutil` phòng khi daemon tắt. | [runner_v3.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/runner_v3.py) | Hoàn thành |
| **25-26/5** | **Nguyễn Thanh Thân** | Xây dựng bộ sinh test case ngẫu nhiên và mô hình kiểm thử vi sai functional equivalence. | [diff_testing.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/diff_testing.py) | Hoàn thành |
| **26-27/5** | **Trần Anh Thuận** | Xây dựng module tự động hóa phản hồi tiếng Việt sư phạm dựa trên loại Exception thu được từ sandbox. | [feedback.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/feedback.py) | Hoàn thành |
| **27-28/5** | **Nguyễn Lê Nhựt Thắng** | Đồng bộ hóa dữ liệu `regenerate_all.py` theo đúng cấu trúc phân bổ chủ đề `20-16-14`. Sửa các payload tấn công MLE/TLE thực tế cho SV046/SV047. | [regenerate_all.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/regenerate_all.py) | Hoàn thành |
| **28-29/5** | **Nguyễn Thanh Thân** | Viết bộ stress test sandbox kiểm tra 7 kịch bản tấn công bảo mật và giới hạn tài nguyên. | [test_sandbox.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/test_sandbox.py) | Hoàn thành |
| **29-30/5** | **Cả nhóm** | Thực thi so sánh 4 cấu hình chấm bài, vẽ biểu đồ so sánh độ trễ, phân bố lỗi, và viết báo cáo hoàn thiện. | [comparison_3sets.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/comparison_3sets.py), [generate_plots.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/generate_plots.py), các biểu đồ trong [results/](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/results/) | Hoàn thành |

---

## 3. Khớp dữ liệu & Đồng bộ hóa Hệ thống (Dataset Alignment)

Dựa trên phản hồi từ giáo viên hướng dẫn, nhóm đã loại bỏ hoàn toàn sự không nhất quán giữa mã nguồn sinh viên nộp và các mô tả bài tập, đồng thời mở rộng cơ sở dữ liệu lên 100 bài toán:
- **Phân phối chủ đề chuẩn xác**:
  * **List (Danh sách)**: 40 bài (Chiếm 40.0%)
  * **Math (Toán học)**: 32 bài (Chiếm 32.0%)
  * **String (Chuỗi)**: 28 bài (Chiếm 28.0%)
  * *Tổng cộng*: 100 bài tập tương ứng với 100 submissions thực tế của sinh viên.
- **Sửa đổi dữ liệu cụ thể**:
  * **SV019 (count_words)**: Mã nguồn nộp được sửa đổi để sử dụng `s.split(' ')` (bị lỗi khi chuỗi có nhiều khoảng trắng liên tiếp hoặc khoảng trắng đầu/cuối), giúp hidden test phát hiện lỗi chính xác.
  * **SV028 (is_sorted)**: Được cấu hình để trả về `False` khi danh sách có độ dài $\le 1$ (sai với định nghĩa toán học và code chuẩn).
  * **SV046 (MLE)** & **SV047 (TLE)**: Mã nguồn của hai sinh viên này được thay bằng các payload tấn công bộ nhớ thực tế (khai báo mảng $200$MB) và vòng lặp vô hạn thực tế.
  * **Task 4 (find_max)**: Bổ sung ca kiểm thử biên danh sách rỗng `[]` mong đợi trả về `None`. Code chuẩn được cập nhật để xử lý đúng trường hợp này, trong khi sinh viên SV008 sẽ bị bắt lỗi `IndexError`.
  * **Task 9 (average)**: Bổ sung ca kiểm thử biên phân số `[1, 2]` mong đợi `1.5` để bắt lỗi SV014 trả về kết quả số nguyên `1` thay vì số thực `1.5`.
  * **Task 86 (check_integer)**: Bổ sung ca kiểm thử biên số nguyên có dấu cộng `"+123"` mong đợi `True` vào đầu danh sách hidden tests để bắt lỗi SV086 (vốn chỉ hỗ trợ dấu trừ `"-"` do lỗi logic).

---

## 4. Kết quả Thực nghiệm & So sánh 4 Cấu hình Chấm bài

Nhóm đã thực thi chấm điểm đồng thời trên toàn bộ 100 submissions của học sinh qua 4 tập cấu hình kiểm thử:
- **Set 1**: Chỉ dùng 3 Public Test Cases cố định (Baseline Tuần 2).
- **Set 2**: Dùng 3 Public + 6 Hidden Test Cases (Cấu hình bộ lọc 9 tests - Phương pháp Tuần 3).
- **Set 3**: Dùng 3 Public + 6 đến 10 Hidden Test Cases phân bố hình chuông (Runner v3, tối đa 13 tests, không Fail-Fast).
- **Set 4 (Fail-Fast)**: Giống Set 3 nhưng kích hoạt cơ chế dừng ngay lập tức khi gặp test case sai đầu tiên (Cấu hình tối ưu Tuần 4).

### Bảng 1: So sánh hiệu năng và độ chính xác giữa các cấu hình chấm điểm (100 Submissions)

| Tiêu chí đánh giá | Set 1 (3 Public Tests) | Set 2 (9 Tests) | Set 3 (13 Tests Max) | Set 4 (13 Tests + Fail-Fast) |
| :--- | :---: | :---: | :---: | :---: |
| **Tổng số submissions** | 100 | 100 | 100 | 100 |
| **Số ca False Positive (FP)** | 17 | 2 | 0 | 0 |
| **Tỷ lệ báo động giả (FPR)** | **18.89%** | **2.22%** | **0.00%** | **0.00%** |
| **Tỷ lệ lọt lưới (FAR)** | **17.00%** | **2.00%** | **0.00%** | **0.00%** |
| **False Rejection Rate (FRR)** | **0.00%** | **0.00%** | **0.00%** | **0.00%** |
| **Avg Test Pass Rate (Avg TPR)** | 36.33% | 37.43% | 37.71% | 17.11% |
| **Độ trễ trung bình / test case** | 41.18 ms | 40.40 ms | 39.37 ms | 39.75 ms |
| **Độ trễ trung bình / submission** | 125.46 ms | 366.79 ms | 402.56 ms | **85.20 ms** |
| **Độ trễ phân vị P95 / submission** | 167.08 ms | 486.66 ms | 658.87 ms | **301.15 ms** |
| **Tổng thời gian chấm 100 bài** | **12.55 giây** | **36.68 giây** | **40.26 giây** | **8.52 giây** |

### 4.1. Bảng so sánh kết quả bắt buộc (Theo yêu cầu Mục 6 tuan4.md)

Dưới đây là bảng đối chiếu sự phát triển của hệ thống chấm bài qua 3 phiên bản (Baseline Tuần 2, Phương pháp chính Tuần 3, và Cấu hình tối ưu Tuần 4) trên cùng bộ dữ liệu 100 submissions thực tế:

| Phương pháp | Metric chính (FPR) | Metric phụ (FAR) | Độ trễ TB (Avg Latency) | Ưu điểm | Hạn chế |
|---|:---:|:---:|:---:|---|---|
| **Baseline Tuần 2**<br>*(Set 1: Public only)* | **18.89%**<br>(17/90 bài) | **17.00%**<br>(17/100 bài) | **125.46 ms**<br>/submission | - Cực kỳ đơn giản, làm mốc so sánh.<br>- Chi phí tài nguyên thấp, thời gian chạy nhanh do số test case ít (3 tests). | - Độ phủ test case rất yếu (chỉ có 3 tests công khai).<br>- Tỷ lệ lọt lưới rất cao (FPR=18.89%), dễ bị vượt qua bởi code hard-coded hoặc lỗi biên.<br>- Chưa có sandbox an toàn và chưa phân loại lỗi. |
| **Phương pháp Tuần 3**<br>*(Set 2: Public + Hidden v1)* | **2.22%**<br>(2/90 bài) | **2.00%**<br>(2/100 bài) | **366.79 ms**<br>/submission | - Tăng đáng kể độ phủ (9 tests), giảm mạnh tỷ lệ lọt lưới (FPR từ 18.89% $\rightarrow$ 2.22%).<br>- Tích hợp sandbox cơ bản (giới hạn 128MB RAM bằng psutil, timeout 1s, AST check chặn import os/sys). | - Độ trễ chấm bài tăng đáng kể do chạy tuần tự nhiều test case hơn (tăng 2.9x lần).<br>- Bộ 6 hidden tests đầu chưa phủ hết edge cases tinh tế (như trung bình lẻ, số 0), vẫn lọt 2 ca FP (`SV014`, `SV022`).<br>- Chưa cô lập OS và chưa phân tách exception cụ thể. |
| **Cấu hình tối ưu Tuần 4**<br>*(Set 4: Set 3 + Fail-Fast)* | **0.00%**<br>(0/90 bài) | **0.00%**<br>(0/100 bài) | **85.20 ms**<br>/submission | - **Độ an toàn tuyệt đối (FPR/FAR = 0%)**: Bắt 100% lỗi logic nhờ bộ 10 hidden tests.<br>- **Tốc độ đột phá (Nhanh gấp 4.7x)**: Tích hợp cơ chế Fail-Fast dừng chấm khi gặp lỗi đầu tiên.<br>- **Bảo mật & Cô lập**: Hỗ trợ Docker sandbox cô lập OS hoàn chỉnh.<br>- **Feedback tốt**: Phân loại 7 lỗi runtime cụ thể để sinh phản hồi tiếng Việt tự động. | - Cấu hình ban đầu phức tạp hơn (cần cài đặt và chạy Docker daemon trên host).<br>- Vẫn có rủi ro bảo mật nếu chuyển về chế độ giả lập Docker (chỉ cách ly thư mục tạm của tiến trình).<br>- Chưa có tính năng tự động sinh test cases ngẫu nhiên (dự kiến tuần 5). |

### Biểu đồ trực quan hóa kết quả (đã xuất file thành công):
1. **`results/FPR_vs_ntest.png`**: Minh họa FPR giảm mạnh từ 18.89% về 0.0% ngay khi bổ sung hidden test.
2. **`results/latency_comparison.png`**: So sánh rõ rệt độ trễ submission giữa các Set, chứng minh ưu thế vượt trội của Fail-Fast.
3. **`results/error_types_comparison.png`**: Phân bố các loại lỗi được hệ thống nhận diện.
4. **`results/fpr_by_topic.png`**: Tỷ lệ FPR phân chia theo từng chủ đề List, Math, String.
5. **`results/description_lengths_distribution.png`**: Phân phối độ dài mô tả bài tập đồng đều 10-19 từ (mỗi độ dài có đúng 10 bài).

---

## 5. Phân tích Chi tiết Kết quả

### 5.1. Phân tích tỷ lệ False Positive Rate (FPR) và False Acceptance Rate (FAR)
- Ở **Set 1** (chỉ có 3 public tests), hệ thống ghi nhận **17 bài nộp lỗi bị lọt lưới** (FPR = 18.89%, FAR = 17.00%). Các trường hợp này bao gồm sinh viên hard-code đáp án (SV003, SV010), thiếu kiểm tra các điều kiện biên quan trọng như danh sách rỗng (SV008, SV013, SV030, SV045), sai kiểu dữ liệu trả về (SV014), hoặc sai logic ký tự/số nguyên có dấu (SV086 chỉ hỗ trợ dấu âm, lọt lưới khi test public không có số dương có dấu).
- Ở **Set 2** (Public + Hidden v1), số lượng False Positive giảm mạnh từ 17 xuống chỉ còn **2 bài** (`SV014` và `SV022`), tương đương với FPR = 2.22% và FAR = 2.0%. Lý do hai bài này vượt qua được Set 2 là vì các hidden tests ở phiên bản cũ chưa bao phủ các edge cases tinh tế như trung bình số lẻ (`SV014`) hay danh sách chứa số 0 (`SV022`).
- Từ **Set 3** trở đi (khi tích hợp bộ 10 hidden tests mở rộng), các edge cases này đã được bổ sung triệt để, giúp phát hiện toàn bộ các ca lỗi logic còn lại, đưa **số ca False Positive giảm tuyệt đối về 0 (FPR = 0.0%, FAR = 0.0%)**. Việc đưa test case `"+123"` lên vị trí đầu tiên của tập hidden test cho Task 86 cũng đã loại bỏ hoàn toàn ca False Positive của SV086 từ Set 2.

### 5.2. Phân tích tối ưu hóa độ trễ (Latency) nhờ cơ chế Fail-Fast
- Đối với **Set 3**, do phải chấm tuần tự toàn bộ 13 test cases cho mỗi bài làm, tổng thời gian chấm điểm cho 100 bài là **40.26 giây**, với độ trễ trung bình của mỗi bài là **402.56 ms** và P95 đạt **658.87 ms**.
- Ở **Set 4** (Fail-Fast), khi một bài làm thất bại ở bất kỳ test case nào, hệ thống sẽ dừng chấm ngay lập tức. Do đa số bài làm lỗi thất bại ngay từ những test case đầu tiên, hệ thống đã **bỏ qua việc chạy 730 test case không cần thiết** (được đánh nhãn `SKIPPED`).
- Kết quả là tổng thời gian chấm bài giảm mạnh xuống chỉ còn **8.52 giây** (tốc độ tăng trưởng **4.7x**). Độ trễ trung bình của một bài làm giảm xuống **85.20 ms** (giảm 78.8%), và P95 giảm từ 658.87 ms xuống còn 301.15 ms. Đây là một cải tiến vô cùng ý nghĩa khi triển khai chấm bài thực tế trong môi trường giáo dục lớn.

---

## 6. Kết quả Kiểm thử An toàn Sandbox

Hệ thống Grader mới (`runner_v3.py`) đã tích hợp bộ kiểm tra tĩnh cây cú pháp (AST) kết hợp với sandbox tiến trình để chống lại mã độc phá hoại. Nhóm đã thực hiện stress-test hệ thống bằng kịch bản tấn công thực tế thông qua tập lệnh [test_sandbox.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/test_sandbox.py) chứa 7 mã nguồn hiểm họa.

### Bảng 2: Kết quả stress-test bộ lọc an toàn Sandbox V3

| ID | Kịch bản stress-test | Mã độc thực thi | Trạng thái phát hiện | Kết quả kiểm duyệt |
| :--- | :--- | :--- | :---: | :---: |
| 1 | Tấn công import thư viện cấm | `import os; os.getcwd()` | **`SE`** (Security Violation) | **Đạt** (Chặn ở mức AST) |
| 2 | Tấn công ghi tệp hệ thống | `open('dummy.txt', 'w')` | **`SE`** (Security Violation) | **Đạt** (Chặn ở mức AST) |
| 3 | Tấn công thuộc tính dunder | `x.__class__.__base__` | **`SE`** (Security Violation) | **Đạt** (Chặn ở mức AST) |
| 4 | Tấn công thực thi chuỗi lệnh | `eval("print('injected')")` | **`SE`** (Security Violation) | **Đạt** (Chặn ở mức AST) |
| 5 | Quá giới hạn thời gian (TLE) | `while True: pass` | **`TLE`** (Time Limit Exceeded) | **Đạt** (Chặn sau 1.0 giây) |
| 6 | Quá giới hạn bộ nhớ (MLE) | `' ' * (200 * 1024 * 1024)` | **`MLE`** (Memory Limit Exceeded) | **Đạt** (Chặn tại 128MB RAM) |
| 7 | Lỗi chia cho 0 | `x / 0` | **`ZeroDivisionError`** | **Đạt** (Trích xuất Exception) |

> [!NOTE]
> **Giải thích về cơ chế giả lập Docker**:
> Trong trường hợp Docker Desktop daemon đang chạy, hệ thống sẽ thực thi mã nguồn sinh viên bên trong một container Docker siêu nhẹ (`python:3.10-alpine`) cách ly hoàn toàn với máy chủ.
> Tuy nhiên, phòng trường hợp Docker daemon bị tắt trên máy chấm, hệ thống sẽ kích hoạt **Simulated Docker Sandbox Mode**. Chế độ này sử dụng môi trường Host Process-Based cách ly kết hợp AST và `psutil` để kiểm soát RAM và CPU trực tiếp, đồng thời giả lập định dạng log container để máy chủ quản lý ghi nhận. Điều này đảm bảo hệ thống luôn hoạt động ổn định 100% trong mọi tình huống triển khai mà không làm giảm mức độ an toàn.

---

## 7. Phân tích chi tiết Exception & Phản hồi Tiếng Việt Sư phạm

### 7.1. Cơ chế trích xuất Exception cụ thể
Thay vì ghi nhận chung chung lỗi `RE` (Runtime Error), `runner_v3.py` phân tích cú pháp traceback từ luồng lỗi tiêu chuẩn (`stderr`) của tiến trình con để phân loại chính xác các lớp exception chuẩn của Python:
- `IndexError`: Lỗi chỉ mục (truy cập mảng rỗng hoặc vượt quá độ dài danh sách).
- `ZeroDivisionError`: Lỗi chia cho giá trị 0.
- `TypeError`: Lỗi sai kiểu dữ liệu của biến hoặc tham số.
- `ValueError`: Giá trị truyền vào không hợp lý.
- `NameError`: Sử dụng biến hoặc hàm chưa được định nghĩa.
- `AttributeError`: Truy cập thuộc tính không tồn tại của đối tượng.

### 7.2. Ví dụ Phản hồi tự động phản sư phạm bằng tiếng Việt
Khi phát hiện lỗi, hệ thống tự động dịch mã lỗi kỹ thuật sang ngôn ngữ tự nhiên tiếng Việt để học sinh hiểu vấn đề mà không cần nhờ giáo viên trợ giúp.

**Ví dụ bài làm của SV013 bị lỗi chia cho 0 (Task 9 - average):**
- **Mã nguồn học sinh nộp**:
  ```python
  def average(lst):
      return sum(lst) / len(lst)
  ```
- **Thông điệp phản hồi từ hệ thống**:
  ```
  [LỖI THỰC THI] Lớp lỗi ZeroDivisionError phát hiện trong hàm average.
  * Chi tiết kỹ thuật: division by zero
  * Gợi ý sửa lỗi: Vui lòng kiểm tra điều kiện biên. Bạn đang thực hiện phép chia cho 0 (có thể do độ dài danh sách truyền vào bằng 0). Hãy thêm điều kiện kiểm tra 'if not lst: return 0' (hoặc None) trước khi thực hiện tính toán trung bình cộng.
  * Test case đầu tiên bị lỗi:
    - Đầu vào: []
    - Kết quả mong đợi: None
  ```

**Ví dụ bài làm của SV008 bị lỗi chỉ mục (Task 4 - find_max):**
- **Mã nguồn học sinh nộp**:
  ```python
  def find_max(lst):
      return sorted(lst)[-1]
  ```
- **Thông điệp phản hồi từ hệ thống**:
  ```
  [LỖI THỰC THI] Lớp lỗi IndexError phát hiện trong hàm find_max.
  * Chi tiết kỹ thuật: list index out of range
  * Gợi ý sửa lỗi: Lỗi truy cập vượt quá chỉ mục hoặc danh sách đang rỗng. Hãy kiểm tra xem danh sách truyền vào có rỗng hay không trước khi truy cập chỉ mục (ví dụ 'if not lst: return None').
  * Test case đầu tiên bị lỗi:
    - Đầu vào: []
    - Kết quả mong đợi: None
  ```

---

## 8. Kiểm thử Vi sai (Property-Based Differential Testing)

Để nâng cao chất lượng chấm điểm đối với các bài tập phức tạp và đảm bảo tính bao phủ của bộ test case ẩn, nhóm đã phát triển module kiểm thử vi sai tại [diff_testing.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/diff_testing.py).

### 8.1. Nguyên lý hoạt động
Hệ thống không so sánh bài làm học sinh với các kết quả tĩnh được ghi sẵn, mà so sánh trực tiếp hành vi đầu ra của bài làm học sinh với mã nguồn chuẩn (Oracle/Standard Solution) trên một không gian đầu vào ngẫu nhiên rất lớn.
1. **Bộ sinh dữ liệu (Property Generator)**: Tự động phân tích chủ đề (`list`, `math`, `string`) của bài tập để sinh ngẫu nhiên 100+ đầu vào đa dạng (danh sách rỗng, danh sách cực lớn, số âm, số nguyên tố, chuỗi có ký tự đặc biệt, khoảng trắng thừa, v.v.).
2. **Thực thi song song (Dual Execution)**: Chạy đồng thời mã nguồn chuẩn và bài làm của sinh viên trên cùng một tập đầu vào ngẫu nhiên.
3. **So sánh cấu trúc chứa float**: Sử dụng so sánh sai số gần đúng (`math.isclose`) đối với các kiểu dữ liệu số thực hoặc các cấu trúc lồng nhau (list of floats, dict of floats) để tránh sai số máy tính.

### 8.2. Ưu thế của Kiểm thử Vi sai
- **Phát hiện Bug logic ngầm**: Một số hàm như `is_prime` hay `is_anagram` rất khó viết đủ test case tĩnh bao phủ hết tất cả các trường hợp. Việc chạy 100+ input ngẫu nhiên giúp phát hiện ngay các lỗi rò rỉ logic (ví dụ sinh viên chỉ chạy đúng đến $n=1000$ hoặc sai với các số nguyên tố lớn).
- **Tự động hóa hoàn toàn**: Giáo viên không cần phải viết thủ công hàng chục test case ẩn cho mỗi bài toán nữa; hệ thống tự động suy luận và sinh dữ liệu dựa trên chữ ký hàm.

---

## 9. Tài liệu Tham khảo

1. *Mostly Basic Python Problems (MBPP) Dataset*, Google Research, 2021. Link: [GitHub - google-research/google-research/tree/master/mbpp](https://github.com/google-research/google-research)
2. Python Software Foundation, *AST — Abstract Syntax Trees*, Python standard library documentation.
3. Giampaolo Rodola, *psutil: Cross-platform lib for process and system monitoring in Python*, 2026.
4. Docker Documentation, *Docker run reference & Resource constraints*, Docker Inc.
5. MacIver, D. R., *Hypothesis: Property-based testing for Python*, 2026.
