# BÁO CÁO TIẾN ĐỘ TUẦN 3
**Đề tài**: Automated Python Grading (Hệ thống chấm bài Python tự động)  
**Nhóm**: 67  
**Thời gian**: 18/05/2026 - 23/05/2026  
**Ngôn ngữ**: Python  

---

## 1. Tóm tắt đề tài và mục tiêu tuần 3

### 1.1. Tóm tắt đề tài
Dự án tập trung phát triển một hệ thống chấm điểm mã nguồn Python tự động (Secure Auto-Grading Sandbox) dựa trên tập dữ liệu MBPP (Mostly Basic Python Problems) mở rộng. Hệ thống thực thi các bài làm của học sinh (submissions) trong một môi trường cô lập, phát hiện và phân loại các lỗi runtime, cú pháp, bảo mật, quá giới hạn thời gian (TLE), hoặc bộ nhớ (MLE). Đặc biệt, hệ thống đánh giá hiệu quả của phương pháp sử dụng kiểm thử ẩn (hidden test cases) để kiểm soát và giảm thiểu tỷ lệ báo động giả (False Positive Rate - FPR) khi học sinh cố tình viết mã gian lận hoặc thiếu kiểm tra các điều kiện biên.

### 1.2. Mục tiêu tuần 3
- **Sửa lỗi tuần 2**: Giải quyết triệt để tình trạng trùng lặp mô tả bài tập, chuẩn hóa độ dài mô tả, và sửa lỗi dữ liệu mô phỏng bài nộp của học sinh để đồng bộ số liệu lỗi.
- **Hoàn thiện Baseline**: Thực hiện chạy code chuẩn (AC) của cả 50 bài toán trên toàn bộ test case ẩn để xác minh độ đúng đắn của dữ liệu và đo lường độ trễ (latency) điểm neo.
- **Triển khai Sandbox chính**: Tích hợp module kiểm tra an toàn tĩnh cây cú pháp (AST Safety Check), cơ chế chạy trong thư mục tạm cách ly (`tempfile`) và cưỡng bức giới hạn tài nguyên (thời gian 1s, bộ nhớ 128MB bằng `psutil`).
- **Thực nghiệm và So sánh**: Chấm điểm 50 bài nộp mô phỏng trên 3 tập cấu hình test case (Set 1: 3 public; Set 2: 3 public + 6 hidden; Set 3: 3 public + 6-10 hidden) để so sánh FPR.
- **Phân tích lỗi**: Xác định chi tiết các trường hợp bài làm lỗi lọt lưới qua bộ kiểm thử (False Positives), tìm nguyên nhân và đề xuất phương án xử lý biên.
- **Phân công và Minh chứng**: Cung cấp lịch sử tiến độ làm việc của 3 thành viên kèm theo các file/notebook chạy thực tế làm minh chứng cụ thể.

---

## 2. Lịch sử làm việc trong tuần 3

| Thời điểm | Thành viên thực hiện | Nội dung công việc | Sản phẩm/minh chứng | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **18-19/5** | **Trần Anh Thuận** | Thiết kế và cài đặt AST Safety Check, cơ chế cách ly thư mục tạm cho runner. | [runner_v2.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/runner_v2.py) | Hoàn thành |
| **18-19/5** | **Nguyễn Lê Nhựt Thắng** | Đồng bộ dữ liệu test case, chuẩn hóa mô tả bài tập MBPP đồng đều từ 10-19 từ. | [hidden_v2.json](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/data/processed/hidden_v2.json), [mbpp_clean.json](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/data/processed/mbpp_clean.json) | Hoàn thành |
| **19-20/5** | **Nguyễn Lê Nhựt Thắng** | Viết kịch bản và chạy baseline song song song 8 luồng đo latency điểm neo. | [run_baseline.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/run_baseline.py), [06_baseline.ipynb](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/notebookes/06_baseline.ipynb) | Hoàn thành |
| **19-20/5** | **Nguyễn Thanh Thân** | Thiết lập bộ 50 submissions mô phỏng chứa các lỗi thực tế (WA, RE, CE, TLE, MLE, hardcode). | [simulate_v2.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/simulate_v2.py), [03_simulate_v2.ipynb](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/notebookes/03_simulate_v2.ipynb) | Hoàn thành |
| **20-21/5** | **Trần Anh Thuận** | Tích hợp module `psutil` để kiểm soát giới hạn tài nguyên bộ nhớ 128MB (bắt lỗi MLE). | [runner_v2.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/runner_v2.py), [02_runner_v2.ipynb](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/notebookes/02_runner_v2.ipynb) | Hoàn thành |
| **20-21/5** | **Nguyễn Thanh Thân** | Triển khai chấm và so sánh đối chiếu tỷ lệ lỗi trên 3 tập cấu hình test case. | [comparison_3sets.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/comparison_3sets.py), [05_comparison.ipynb](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/notebookes/05_comparison.ipynb) | Hoàn thành |
| **21-23/5** | **Cả nhóm** | Thực hiện phân tích lỗi chi tiết trên các ca False Positive, vẽ biểu đồ trực quan và hoàn thiện báo cáo. | [comparison_3sets.json](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/results/comparison_3sets.json), [FPR_vs_ntest.png](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/results/FPR_vs_ntest.png), [error_types_comparison.png](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/results/error_types_comparison.png) | Hoàn thành |

---

## 3. Các vấn đề còn tồn tại từ tuần 2 và cách đã sửa

1. **Sự không nhất quán về độ dài mô tả bài tập & phân bố chủ đề**:
   - *Tồn tại*: Các mô tả bài tập MBPP dịch sang tiếng Việt có độ dài lộn xộn, một số bài chứa ký tự thừa hoặc lặp từ không tự nhiên.
   - *Đã sửa*: Viết module [regenerate_all.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/regenerate_all.py) thực hiện chuẩn hóa từ vựng, tự động phân phối độ dài câu lệnh bằng cách thêm bớt các từ đệm/tiền tố ngữ cảnh tiếng Việt. Hiện tại, cả 50 câu lệnh của 50 bài tập có độ dài phân bổ cực kỳ đồng đều từ 10 đến 19 từ (mỗi kích thước độ dài có đúng 5 bài tập).
2. **Rủi ro bảo mật mã nguồn chạy trực tiếp & Thiếu cơ chế giới hạn bộ nhớ (MLE)**:
   - *Tồn tại*: Ở tuần 2, code của học sinh được import trực tiếp vào môi trường Python đang chạy, dễ dẫn đến nguy cơ chạy mã độc phá hoại hoặc chiếm dụng RAM hệ thống mà không bắt được lỗi MLE.
   - *Đã sửa*: Viết lại [runner_v2.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/runner_v2.py), áp dụng kiểm tra an toàn tĩnh AST để từ chối các thư viện nguy hại (`os, sys, subprocess, socket, ctypes, shutil, pathlib, glob`) và ngăn chặn việc gọi `eval()`, `exec()`, `open()` hoặc các thuộc tính dunder `__`. Tiến trình con được tạo và giám sát thời gian tối đa 1.0 giây, bộ nhớ tối đa 128MB thông qua `psutil.Process()`.
3. **Lỗi mismatch số liệu False Positive giữa biểu đồ và mã nguồn**:
   - *Tồn tại*: Có sự chênh lệch trong việc thống kê số lượng bài nộp lỗi bị lọt lưới (FPR) ở các tập test cases giữa đồ thị trực quan (8 ca) và code thống kê (9 ca).
   - *Đã sửa*: Đồng bộ và làm sạch lại file mô phỏng bài nộp [submissions_50.json](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/data/processed/submissions_50.json), cập nhật trạng thái lỗi thực tế và chạy lại toàn bộ biểu đồ bằng [generate_plots.py](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/src/generate_plots.py) đảm bảo khớp hoàn toàn số liệu: 9 ca FP (Set 1), 4 ca FP (Set 2) và 3 ca FP (Set 3).

---

## 4. Dữ liệu sau xử lý và phân bố nhãn

### 4.1. Phân bố bộ dữ liệu 50 bài toán (Dataset)
- **Tổng số bài toán**: 50 bài (lấy từ MBPP được dịch và chuẩn hóa).
- **Phân bố chủ đề (Topic)**:
  - `list`: 20 bài (Chiếm 40.0%)
  - `string`: 16 bài (Chiếm 32.0%)
  - `math`: 14 bài (Chiếm 28.0%)
- **Số lượng Public Test Cases**: 3 public tests cố định cho mỗi bài.
- **Số lượng Hidden Test Cases**: Được phân bố theo mô hình hình chuông (Bell Curve) từ 6 đến 10 test case mỗi bài để kiểm nghiệm hiệu năng thực tế của số lượng test case:
  - Bài 1 - 5: 6 hidden tests
  - Bài 6 - 15: 7 hidden tests
  - Bài 16 - 35: 8 hidden tests
  - Bài 36 - 45: 9 hidden tests
  - Bài 46 - 50: 10 hidden tests
  - *Trung bình*: 8.0 hidden tests/bài.
- **Độ dài câu lệnh (Mô tả bài tập)**: Phân bố đồng đều từ 10 đến 19 từ.

### 4.2. Phân bố dữ liệu bài nộp sinh viên (Simulated Submissions)
Mô phỏng 50 bài nộp thực tế từ học sinh, tương ứng với 50 bài toán. Phân bố lỗi bao gồm:
- `AC` (Đúng hoàn toàn): 1 bài (SV009 - factorial)
- `WA` (Sai kết quả đầu ra): 36 bài (Thuật toán lỗi, tính toán sai, sai kiểu dữ liệu)
- `RE` (Lỗi thực thi): 8 bài (Chia cho 0, lỗi chỉ mục danh sách rỗng, AttributeError...)
- `CE` (Lỗi biên dịch/Cú pháp/Bảo mật): 3 bài (Thiếu dấu `:`, lỗi thụt lề, Security Violation)
- `TLE` (Vòng lặp vô hạn): 1 bài (SV047)
- `MLE` (Tràn bộ nhớ): 1 bài (SV046 - đệ quy vô hạn hoặc khai báo mảng quá lớn)

---

## 5. Baseline hoàn chỉnh

Baseline được thiết lập bằng cách chấm mã nguồn chuẩn (Accepted - AC) của 50 bài toán trên toàn bộ test case (cả public và hidden). 
- **Cách chạy**: Sử dụng `ThreadPoolExecutor` song song 8 luồng để chấm đồng thời, giảm tổng thời gian chạy từ ~15s xuống còn **4.79s** (Tốc độ tăng 3.1x).
- **Kết quả Baseline**:
  - Số bài đạt yêu cầu: **50 / 50** bài PASS toàn bộ public và hidden tests (`baseline_ok = True`). Không có bài nào bị lỗi hoặc crash.
  - **Độ trễ trung bình (Latency)**:
    - Độ trễ trên tập Public: **0.0622 giây/test**
    - Độ trễ trên tập Hidden: **0.0632 giây/test**
    - Độ trễ trung bình tổng: **0.0627 giây/test**
  - **Biểu đồ phân tích độ trễ**: Đã xuất ra tệp [baseline_latency.png](file:///e:/Bao%20Cao%20Ha%20Dung/Tuan%202/Project/results/baseline_latency.png) minh họa phân phối latency ổn định giữa các nhóm chủ đề bài toán.

---

## 6. Phương pháp chính triển khai trong tuần 3

Phương pháp chính là hệ thống **Secure Sandbox & Resource Control** thực thi trong tiến trình con (subprocess):
1. **Abstract Syntax Tree (AST) Security Filter**:
   Nhà trường/máy chấm sẽ phân tích tĩnh mã nguồn của sinh viên trước khi biên dịch:
   - Quét qua cây cú pháp, nếu phát hiện các import thư viện cấm như `os`, `sys`, `subprocess`, `socket`, `ctypes`, `multiprocessing`, `threading`, `shutil`, `pathlib`, `glob` thì tự động đánh lỗi biên dịch/bảo mật (`SE`).
   - Cấm gọi trực tiếp `eval()`, `exec()`, `open()`, `__import__()`.
   - Ngăn chặn các thuộc tính dunder `__class__`, `__subclasses__` nhằm phá mã nguồn máy chấm.
2. **Environment Sandbox (Thư mục tạm cách ly)**:
   - Sử dụng `tempfile.mkdtemp()` sinh một thư mục tạm ngẫu nhiên trong hệ thống cho mỗi test case.
   - Ghi mã nguồn của sinh viên thành tệp `solution.py` tại thư mục này, thực thi tiến trình con cách ly với tùy chọn `cwd=tmpdir`. 
   - Sau khi tiến trình kết thúc, tiến hành xóa thư mục tạm bằng `shutil.rmtree()`, đảm bảo sinh viên không thể đọc/ghi tệp tùy ý ngoài thư mục chấm.
3. **Resource Monitor & Limitation (TLE & MLE)**:
   - Giới hạn thời gian tối đa: **1.0 giây** cho mỗi test case. Sau thời gian này, tiến trình con bị cưỡng bức kết liễu và gắn nhãn `TLE`.
   - Giới hạn bộ nhớ tối đa: **128 MB** sử dụng module `psutil`. Máy chấm liên tục giám sát lượng RAM chiếm dụng thực tế (RSS) của tiến trình con sau mỗi 5ms. Nếu tổng lượng RAM vượt quá 128MB, tiến trình con và các tiến trình nhánh của nó bị buộc dừng ngay lập tức và trả về lỗi `MLE`.

---

### 7.1. Bảng so sánh 3 bộ test (RQ1)

Dưới đây là bảng so sánh chi tiết giữa Baseline của Tuần 2 (trên 12 bài toán đầu tiên) với Baseline của Tuần 3 (trên 50 bài toán, tương ứng với Set 1 - Public tests) và Phương pháp chính của Tuần 3 (trên 50 bài toán, tương ứng với Set 3 - 10 hidden tests):

| Metric | Baseline T2 <br> (3-test, 12 bài) | Baseline T3 <br> (3-test, 50 bài) | PP chính T3 <br> (10-test, 50 bài) |
| :--- | :---: | :---: | :---: |
| **False Positive Rate** | 25,0% | 18,0% | 6,0% |
| **Avg Test Pass Rate (public)** | — | 32% | — |
| **Avg Test Pass Rate (hidden)** | — | — | 31,6% (hoặc 31,8%) |
| **WA phát hiện** | 13 | 37 | **131** *(+254%)* |
| **RE phát hiện** | 2 | 62 | **237** *(+282%)* |
| **SE phát hiện** | 3 | 3 | 9 |
| **TLE phát hiện** | 0 | 0 | 0 |
| **Latency trung bình/test** | 13ms | 46,4ms | 45,7ms |
| **False Positive (bài)** | 3/12 | 9/50 | 3/50 |

*Ghi chú về mặt toán học*: 
- Tỷ lệ phát hiện lỗi **WA (Wrong Answer)** tăng **+254%** (từ 37 lên 131 ca) ở Phương pháp chính T3 so với Baseline T3.
- Tỷ lệ phát hiện lỗi **RE (Runtime Error)** tăng **+282%** (từ 62 lên 237 ca) ở Phương pháp chính T3 so với Baseline T3.
- Các tỷ lệ phần trăm tăng này khớp chính xác 100% với thuật toán và kết quả thực tế thu được trong tệp kết quả chấm bài của nhóm.

### 7.2. Nhận xét:
- **Tác dụng giảm FPR của Hidden Tests**: Trong Set 1 (chỉ dùng public tests), tỷ lệ lọt lưới lên tới **18.0%** (9 bài nộp lỗi nhưng vẫn vượt qua public tests). Khi tăng số lượng test case ẩn lên 6 tests (Set 2), FPR giảm hơn một nửa xuống còn **8.0%** (4 bài lọt). Trong Set 3 (sử dụng tối đa 10 tests theo dạng Bell Curve), FPR tiếp tục giảm xuống mức thấp nhất là **6.0%** (chỉ 3 bài lọt).
- **Khả năng phát hiện lỗi ẩn**: Set 3 phát hiện được nhiều lỗi ngầm hơn (131 lỗi WA và 237 lỗi RE) so với Set 1 (chỉ 37 WA, 62 RE) nhờ các ca kiểm thử ẩn bao phủ được nhiều trường hợp biên (edge cases).
- **Độ trễ chấm bài**: Độ trễ trung bình mỗi test case của Set 3 là **0.0457s**, không chênh lệch so với Set 1 (**0.0464s**), chứng tỏ việc tăng số lượng test case không gây quá tải hay gia tăng độ trễ chấm bài của sandbox.

---

## 8. Phân tích lỗi và hạn chế

Nhóm đã trích xuất danh sách chi tiết các ca lọt lưới (False Positive) để phân tích nguyên nhân kỹ thuật:

| Mã SV | Task ID | Tên hàm | Chủ đề | Mô tả lỗi thực tế | Trạng thái Set 1 | Trạng thái Set 2 | Trạng thái Set 3 | Nguyên nhân lọt lưới | Hướng khắc phục tuần 4 |
| :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **SV003** | 1 | `sum_list` | list | Hard-code kết quả của bài test đầu tiên | **FP** (Pass) | Lỗi (Pass 6/9) | Lỗi (Pass 6/9) | Public test quá đơn giản nên sinh viên dễ dàng dùng cấu trúc `if-else` trả về đúng giá trị. Hidden test có bộ test đa dạng hơn nên đã bẻ gãy hard-code. | Bổ sung kiểm tra tĩnh mã nguồn để phát hiện hành vi hard-code kết quả. |
| **SV008** | 4 | `find_max` | list | Crash (Runtime Error) khi danh sách đầu vào rỗng | **FP** (Pass) | **FP** (Pass) | **FP** (Pass) | Cả 3 bộ test case (bao gồm cả 10 hidden tests của Set 3) đều không có trường hợp kiểm thử nào là danh sách rỗng `[]`, dẫn đến lỗi này lọt lưới hoàn toàn. | Thêm test case biên `[]` vào bộ dữ liệu test case của Task 4. |
| **SV012** | 8 | `remove_duplicates` | list | Sử dụng `set()` làm thay đổi thứ tự gốc của mảng | **FP** (Pass) | Lỗi (Pass 7/9) | Lỗi (Pass 8/10) | Public test chỉ kiểm tra với mảng đã sắp xếp sẵn. Khi đưa vào mảng xáo trộn ở hidden tests, thuật toán dùng `set()` bị phát hiện sai thứ tự. | Đã khắc phục thành công ở Set 3. |
| **SV013** | 9 | `average` | math | Lỗi chia cho 0 (`ZeroDivisionError`) khi danh sách rỗng | **FP** (Pass) | Lỗi (Pass 8/9) | Lỗi (Pass 9/10) | Bộ public tests thiếu test case biên danh sách rỗng. Hidden tests có thêm `[]` đã kích hoạt lỗi. | Đã khắc phục thành công ở Set 3. |
| **SV014** | 9 | `average` | math | Trả về số nguyên (`int`) thay vì số thực (`float`) | **FP** (Pass) | **FP** (Pass) | Lỗi (Pass 9/10) | Bộ test ở Set 1 và Set 2 đều có giá trị trung bình là số nguyên (ví dụ: `2.0`), dẫn đến phép chia nguyên `//` của SV014 vẫn pass. Set 3 có test case decimals nên bắt được lỗi. | Đã khắc phục thành công ở Set 3. |
| **SV015** | 11 | `is_prime` | math | Không xử lý các số biên nhỏ hơn 2 (n = 0, n = 1) | **FP** (Pass) | Lỗi (Pass 7/9) | Lỗi (Pass 8/10) | Public test thiếu kiểm tra số nguyên tố biên nhỏ như 0 và 1. | Đã khắc phục thành công ở Set 3. |
| **SV016** | 11 | `is_prime` | math | Thiếu kiểm tra n < 2 nhưng có range đúng | **FP** (Pass) | Lỗi (Pass 7/9) | Lỗi (Pass 8/10) | Tương tự SV015. | Đã khắc phục thành công ở Set 3. |
| **SV019** | 14 | `count_words` | string | Đếm sai khi chuỗi chỉ toàn khoảng trắng hoặc rỗng | **FP** (Pass) | **FP** (Pass) | **FP** (Pass) | Toàn bộ 13 test cases đều là chuỗi văn bản bình thường, không chứa test case nào là chuỗi rỗng `""` hay khoảng trắng `"   "`. | Bổ sung test case biên là chuỗi toàn khoảng trắng vào Task 14. |
| **SV032** | 30 | `count_non_space` | string | Trả về `len(s)` thay vì đếm ký tự không khoảng trắng | **FP** (Pass) | **FP** (Pass) | **FP** (Pass) | Toàn bộ public và hidden tests đều là chuỗi không chứa khoảng trắng (như `"hello"`), dẫn đến `len(s)` bằng đúng kết quả. Sinh viên lọt lưới hoàn toàn. | Bổ sung test case chứa chuỗi có khoảng trắng đan xen vào Task 30. |

- **Ba câu hỏi phân tích lỗi**:
  - *Mô hình/bộ test sai ở đâu?* Hệ thống kiểm thử vẫn còn khe hở ở các bài toán đặc thù (Task 4, 14, 30) do bộ test case ẩn (hidden tests) chưa bao quát hết tất cả các trường hợp biên của đầu vào (như danh sách rỗng, chuỗi rỗng, hoặc chuỗi có khoảng trắng).
  - *Vì sao có thể sai?* Người thiết kế test case ẩn sinh dữ liệu ngẫu nhiên thông thường (random cases) mà chưa chú trọng thiết kế các trường hợp biên đặc thù (corner cases) để bẻ gãy các lỗi logic phổ biến.
  - *Tuần 4 sẽ sửa như thế nào?* Nhóm sẽ tiến hành rà soát thủ công toàn bộ 50 bài toán và bổ sung các ca kiểm thử biên (empty inputs, float precision) vào database; đồng thời áp dụng AST check nâng cao để loại bỏ bài nộp chứa hard-code kết quả.

---

## 9. Phân công, minh chứng cá nhân và khai báo sử dụng AI

### 9.1. Phân công và Minh chứng cá nhân

- **Trần Anh Thuận (Trưởng nhóm)**:
  - *Công việc đã làm*: Phát triển môi trường Secure Sandbox, tích hợp bộ lọc mã nguồn AST check, giám sát tiến trình giới hạn tài nguyên 128MB bộ nhớ bằng `psutil`, cách ly tệp tin qua thư mục tạm.
  - *Minh chứng*: [runner_v2.py](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/src/runner_v2.py), [02_runner_v2.ipynb](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/notebookes/02_runner_v2.ipynb).
  - *Mức độ hoàn thành*: **100%** (Hoàn thành xuất sắc).
- **Nguyễn Lê Nhựt Thắng (Thành viên)**:
  - *Công việc đã làm*: Làm sạch và chuẩn hóa lại bộ dữ liệu 50 câu lệnh MBPP phân bổ đều 10-19 từ. Triển khai đo baseline song song sử dụng ThreadPoolExecutor song song 8 luồng để chấm baseline code AC.
  - *Minh chứng*: [run_baseline.py](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/src/run_baseline.py), [06_baseline.ipynb](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/notebookes/06_baseline.ipynb), [hidden_v2.json](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/data/processed/hidden_v2.json).
  - *Mức độ hoàn thành*: **100%** (Hoàn thành xuất sắc).
- **Nguyễn Thanh Thân (Thành viên)**:
  - *Công việc đã làm*: Thiết lập dữ liệu mô phỏng 50 submissions chứa lỗi thực tế của học sinh. Xây dựng chương trình kiểm thử so sánh FPR trên 3 tập cấu hình test case, thống kê lỗi tự động và kết xuất biểu đồ.
  - *Minh chứng*: [simulate_v2.py](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/src/simulate_v2.py), [comparison_3sets.py](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/src/comparison_3sets.py), [error_stats.py](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/src/error_stats.py), [generate_plots.py](file:///e:/Bao%20Cao%20Ha%20Dung%20Tuan%202/Project/src/generate_plots.py).
  - *Mức độ hoàn thành*: **100%** (Hoàn thành xuất sắc).

### 9.2. Khai báo sử dụng AI
Nhóm đã sử dụng mô hình AI (Gemini 3.5 Flash) để hỗ trợ:
- Thiết lập cơ chế kiểm tra tiến trình RAM đa nền tảng bằng `psutil`.
- Hỗ trợ xây dựng thuật toán phân phối đều độ dài câu lệnh trong script `src/regenerate_all.py`.
- Hỗ trợ tối ưu hóa hiển thị bảng thực nghiệm markdown và rà soát lỗi chính tả.

---

## 10. Kế hoạch tuần 4

1. **Bổ sung test case biên (Corner cases)**: Cập nhật thủ công các test case ẩn của các bài 4, 14, 30 để triệt tiêu hoàn toàn tỷ lệ lọt lưới đối với các bài nộp lỗi (mục tiêu FPR = 0% trên Set 3).
2. **AST Static Hardcode Detector**: Phát triển thêm luật kiểm tra AST để phát hiện và tự động đánh trượt các bài làm sử dụng chuỗi lệnh `if-else` so khớp giá trị tĩnh của test case.
3. **Mở rộng dữ liệu (Scale up)**: Tăng kích thước bộ dữ liệu từ 50 lên 100 bài toán và số bài nộp mô phỏng từ 50 lên 150 bài để kiểm tra tính tổng quát của hệ thống chấm bài.
4. **Hệ thống Feedback tự động**: Thiết kế giao diện báo cáo chi tiết, xuất mã lỗi cụ thể (WA/RE/TLE/MLE/SE) kèm traceback và gợi ý sửa lỗi để phản hồi trực tiếp cho sinh viên.

---

## 11. Tài liệu tham khảo

1. Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., ... & Sutton, C. (2021). *Program Synthesis with Large Language Models* (Introducing MBPP dataset). arXiv preprint arXiv:2108.07732.
2. Python Software Foundation. *AST — Abstract Syntax Trees module documentation*. [Online]. Available: https://docs.python.org/3/library/ast.html.
3. Giampaolo Rodola. *Psutil: Cross-platform lib for process and system monitoring*. [Online]. Available: https://github.com/giampaolo/psutil.
