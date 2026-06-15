**KẾ HOẠCH TUẦN 5**

**Thời gian:** 01/6–08/6/2026  
**Hạn nộp:** Thứ 7, ngày 06/6/2026  
**Chủ đề:** Hoàn thiện sản phẩm, kiểm tra tái lập kết quả, chuẩn bị báo cáo cuối và demo

Tuần 5 là giai đoạn chuyển từ **tối ưu mô hình** sang **hoàn thiện sản phẩm học phần**. Các nhóm cần chứng minh được toàn bộ quy trình: dữ liệu đúng, code chạy được, có baseline, có phương pháp chính, có kết quả so sánh, có phân tích lỗi và có demo hoặc ví dụ chạy thử.

Quy trình nộp bài vẫn giữ như đã chốt: **thứ 7 nộp bài, chủ nhật giảng viên chấm và yêu cầu chỉnh sửa, thứ 2 tuần tiếp theo làm việc với từng nhóm**.

Tuần 5 kế thừa yêu cầu của các tuần trước về lịch sử làm việc, minh chứng cá nhân, bảng so sánh kết quả, phân tích lỗi và khai báo sử dụng AI.

**1\. Mục tiêu tuần 5**

| **Mục tiêu** | **Yêu cầu** |
| --- | --- |
| **Hoàn thiện pipeline** | Code/notebook chạy lại được từ dữ liệu gốc đến kết quả cuối |
| **Chốt mô hình/phương pháp tốt nhất** | Chọn mô hình dựa trên metric phù hợp, không chọn theo cảm tính |
| **So sánh đầy đủ** | Có bảng so sánh baseline, phương pháp chính và mô hình/cấu hình tốt nhất |
| **Khóa số liệu chính thức** | Các bảng metric, confusion matrix, biểu đồ và nhận xét phải khớp nhau |
| **Phân tích lỗi cuối cùng** | Chỉ ra mô hình còn sai ở đâu, nguyên nhân và hướng cải thiện |
| **Chuẩn bị demo** | Có notebook, script, giao diện nhỏ hoặc ví dụ chạy thử |
| **Hoàn thiện báo cáo** | Báo cáo gần hoàn chỉnh như báo cáo cuối kỳ |
| **Chuẩn bị thuyết trình** | Có dàn ý hoặc slide trình bày 5–7 phút |
| **Hoàn thiện minh chứng cá nhân** | Mỗi thành viên có file/code/notebook/sản phẩm cụ thể |

**2\. Mức hoàn thành tuần 5**

| **Mức** | **Yêu cầu** |
| --- | --- |
| **Đạt yêu cầu tối thiểu** | Có pipeline chạy được, bảng so sánh cuối, phân tích lỗi, demo đơn giản, minh chứng cá nhân |
| **Tốt** | Có số liệu rõ, metric phù hợp, kết quả khớp notebook, demo chạy được, báo cáo gần hoàn chỉnh |
| **Rất tốt** | Có kiểm tra tái lập, external/cross-validation nếu phù hợp, phân tích lỗi sâu, inference time, slide/demo rõ ràng |

Tuần 5 **không bắt buộc phải thêm mô hình mới** nếu pipeline hoặc số liệu chưa ổn định. Nhóm cần ưu tiên sửa lỗi, khóa số liệu chính thức, hoàn thiện báo cáo và demo.

**3\. Nội dung bắt buộc trong báo cáo tuần 5**

Báo cáo tuần 5 nên viết theo cấu trúc sau:

1.  Tóm tắt đề tài và mục tiêu tuần 5
2.  Lịch sử làm việc trong tuần 5
3.  Tóm tắt quá trình từ tuần 1 đến tuần 4
4.  Dữ liệu cuối cùng và pipeline xử lý
5.  Baseline và kết quả baseline
6.  Phương pháp chính và các cải tiến đã triển khai
7.  Kết quả thực nghiệm cuối cùng
8.  So sánh baseline – phương pháp chính – mô hình tối ưu
9.  Phân tích lỗi và hạn chế
10. Demo hoặc sản phẩm thử nghiệm
11. Phân công, minh chứng cá nhân và khai báo sử dụng AI
12. Kết luận và hướng phát triển
13. Tài liệu tham khảo

**4\. Lịch sử làm việc tuần 5**

Mỗi nhóm phải có mục **Lịch sử làm việc trong tuần 5**.

| **Thời điểm** | **Thành viên thực hiện** | **Nội dung công việc** | **Sản phẩm/minh chứng** | **Trạng thái** |
| --- | --- | --- | --- | --- |
| 01–02/6 | Thành viên A | Chạy lại toàn bộ pipeline, kiểm tra dữ liệu cuối | final_pipeline.ipynb | Hoàn thành |
| 02–03/6 | Thành viên B | Chốt mô hình tốt nhất, tổng hợp metric | final_results.csv, bảng metric | Hoàn thành |
| 03–04/6 | Thành viên C | Phân tích lỗi cuối cùng | error_analysis.csv, hình minh họa | Hoàn thành |
| 04–05/6 | Cả nhóm | Chuẩn bị demo và báo cáo tuần 5 | demo.py, report_week5.docx | Hoàn thành |
| 05–06/6 | Cả nhóm | Kiểm tra lại file nộp, tài liệu, khai báo AI | Thư mục nộp hoàn chỉnh | Hoàn thành |

Không ghi chung chung như **“làm báo cáo”**, **“làm code”**, **“hoàn thành 100%”**. Phải ghi rõ file, notebook, biểu đồ, bảng kết quả hoặc demo.

**5\. Yêu cầu kỹ thuật chung**

**5.1. Code phải chạy lại được**

Tuần 5, yêu cầu quan trọng nhất là **tái lập kết quả**.

| **Nội dung** | **Yêu cầu** |
| --- | --- |
| Đường dẫn dữ liệu | Không để đường dẫn máy cá nhân khó chạy lại |
| Notebook/code | Chạy được từ đầu đến cuối |
| Thư viện | Có requirements.txt hoặc ghi rõ thư viện dùng |
| Random seed | Ghi rõ nếu có dùng chia train/test hoặc mô hình ngẫu nhiên |
| Kết quả | Metric trong báo cáo phải khớp với notebook/code |
| Hình ảnh/bảng | Lưu trong thư mục results/ hoặc chèn rõ trong báo cáo |
| Model nếu có | Lưu model hoặc ghi rõ cách huấn luyện lại |
| Demo | Có hướng dẫn chạy ngắn gọn |

**5.2. Phải có bảng kết quả chính thức duy nhất**

Mỗi nhóm phải có **một bảng kết quả cuối chính thức**. Các số liệu trong bảng metric, confusion matrix, biểu đồ và phần nhận xét phải khớp nhau.

Nếu có nhiều lần chạy, nhóm phải ghi rõ:

| **Nội dung** | **Cần ghi** |
| --- | --- |
| Run chính thức | Run nào được chọn làm kết quả cuối |
| Tập test | Tập test nào được dùng |
| Mô hình cuối | Mô hình/cấu hình nào được chọn |
| Metric chính | Metric nào dùng để chọn mô hình |
| Confusion Matrix | Phải khớp với Precision/Recall/F1 |
| Ghi chú | Nếu có external test/cross-validation, phải tách riêng với test chuẩn |

Các lỗi như **số mẫu không khớp**, **metric mâu thuẫn**, **confusion matrix không khớp với bảng kết quả**, **nhãn bị đảo** sẽ bị trừ nặng.

**5.3. Phải chốt metric chính**

Mỗi nhóm phải ghi rõ **metric chính** dùng để chọn mô hình tốt nhất.

| **Loại đề tài** | **Metric chính nên dùng** |
| --- | --- |
| Phân loại cân bằng | Accuracy, F1-score |
| Phân loại mất cân bằng | Macro-F1, F1 lớp thiểu số, Recall lớp quan trọng |
| IDS / Phishing / DDoS | Recall attack/phishing, FPR, F1, MCC, Confusion Matrix |
| Hồi quy | MAE, RMSE, R² |
| Dự báo chuỗi thời gian | MAE, RMSE, sMAPE, lỗi tại peak/valley |
| Object detection | mAP50, mAP50-95, Precision, Recall theo lớp |
| Retrieval / Visual Search | Recall@K, Precision@K, mAP, MRR |
| Calibration | ECE, Brier Score, Reliability Diagram |
| Code grading | FPR, số bài sai bị lọt, số bài đúng bị chấm sai |
| Đạo văn code | Precision, Recall, F1 lớp đạo văn, FP/FN cụ thể |

Không chọn mô hình chỉ vì Accuracy cao nếu bài toán mất cân bằng hoặc có lớp quan trọng cần ưu tiên.

**6\. Bảng so sánh cuối cùng bắt buộc**

Mỗi nhóm cần có bảng so sánh tối thiểu 3 mức:

| **Phương pháp** | **Metric chính** | **Metric phụ** | **Ưu điểm** | **Hạn chế** |
| --- | --- | --- | --- | --- |
| Baseline tuần 2 |     |     | Đơn giản, dễ hiểu | Kết quả còn hạn chế |
| Phương pháp chính tuần 3 |     |     | Đúng hướng đề tài | Cần tối ưu |
| Mô hình/cấu hình tốt nhất tuần 5 |     |     | Kết quả tốt nhất hoặc ổn định nhất | Vẫn còn lỗi nào |

Ví dụ với bài toán phân loại:

| **Mô hình** | **Accuracy** | **Precision** | **Recall** | **F1/Macro-F1** | **Nhận xét** |
| --- | --- | --- | --- | --- | --- |
| Baseline |     |     |     |     |     |
| Phương pháp chính |     |     |     |     |     |
| Mô hình tốt nhất |     |     |     |     |     |

Với hồi quy dùng **MAE, RMSE, R²**.  
Với truy hồi dùng **Precision@K, Recall@K, mAP/MRR**.  
Với IDS dùng **Recall, FPR, F1-score, Confusion Matrix**.  
Với object detection dùng **mAP50, mAP50-95, Precision, Recall**.

**7\. Phân tích lỗi cuối cùng**

Tuần 5 không chỉ báo kết quả cao hay thấp. Mỗi nhóm phải phân tích lỗi rõ hơn.

| **Loại đề tài** | **Nội dung phân tích lỗi** |
| --- | --- |
| NLP | 10–20 câu dự đoán sai, đặc biệt lớp thiểu số |
| Ảnh | 5–10 ảnh sai, lớp dễ nhầm, điều kiện ảnh khó |
| Object detection | Ảnh detect sai, vật thể nhỏ, lớp mAP thấp |
| IDS | Attack bị bỏ sót, Benign bị báo động nhầm |
| Hồi quy | Mẫu có sai số lớn nhất, sai số theo nhóm/phân khúc |
| Dự báo | Khoảng thời gian dự báo sai nhiều, đỉnh/đáy không bắt được |
| Visual search | Query trả top-k sai |
| Code grading | Bài sai nhưng qua test, bài đúng bị chấm sai |
| Đạo văn code | Cặp đạo văn bị bỏ lọt, cặp tự làm bị bắt oan |
| Calibration | Nhóm xác suất nào còn lệch sau hiệu chỉnh |

Phần phân tích lỗi cần trả lời:

1.  Mô hình còn sai ở đâu?
2.  Nguyên nhân có thể là gì?
3.  Nhóm đã thử cách sửa nào?
4.  Nếu phát triển tiếp, nên cải thiện theo hướng nào?

Mẫu bảng phân tích lỗi:

| **Mẫu** | **Nhãn thật** | **Dự đoán** | **Điểm/xác suất** | **Loại lỗi** | **Nguyên nhân** | **Hướng xử lý** |
| --- | --- | --- | --- | --- | --- | --- |
| Mẫu 1 |     |     |     | FP/FN |     |     |
| Mẫu 2 |     |     |     | FP/FN |     |     |

**8\. Demo hoặc sản phẩm thử nghiệm**

Tuần 5 mỗi nhóm cần có demo đơn giản hoặc ví dụ chạy thử.

| **Loại demo** | **Ví dụ** |
| --- | --- |
| Notebook demo | Một cell nhập dữ liệu mẫu và in kết quả |
| Script Python | python predict.py --input sample.csv |
| Giao diện nhỏ | Streamlit hoặc Gradio nếu nhóm làm được |
| NLP | Nhập câu văn → dự đoán nhãn |
| Ảnh | Upload ảnh → dự đoán lớp |
| Object detection | Upload ảnh → vẽ bounding box |
| IDS | Upload mẫu flow → dự đoán normal/attack |
| Visual search | Nhập ảnh query → trả top-k ảnh giống |
| Code grading | Nộp code → pass/fail + loại lỗi |
| Đạo văn code | Nhập 2 file .py → similarity + cảnh báo |

Demo không cần đẹp, nhưng phải chạy được và nhóm phải giải thích được cách hoạt động.

**9\. Nhắc nhở riêng theo từng đề tài**

| **Đề tài / nhóm đề tài** | **Nhắc nhở đặc thù tuần 5** |
| --- | --- |
| **Phát hiện URL lừa đảo** | Chốt so sánh DistilBERT với TF-IDF char n-gram + Linear SVM/Logistic Regression. Có domain-level split hoặc external test nếu làm được. Báo F1, Recall, AUC, MCC và thời gian suy luận. |
| **Phân tích cảm xúc phản hồi sinh viên** | Không chọn mô hình theo Accuracy. Phải báo Macro-F1, Recall lớp Trung tính và Confusion Matrix. Nếu có phân loại chủ đề, phải có bảng kết quả riêng cho topic. |
| **Fake News** | Chốt bảng Text Only, Title Only, Title + Text. Phân tích top features để kiểm tra leakage. Không kết luận quá mạnh nếu dataset dễ. |
| **Spam Email / SMS Spam** | Làm rõ SMS hay Email trong tên đề tài. Tập trung Recall lớp Spam và phân tích spam bị bỏ lọt. |
| **Dự đoán học tập sinh viên** | Nên có kết quả cho bài toán nhị phân “Cần cảnh báo” vs “Đạt”. Metric chính là Recall/F1 của nhóm cần cảnh báo. |
| **Job Trend IT** | Báo per-class F1, phân tích nhóm Other IT Role, có demo nhập mô tả công việc → dự đoán vai trò IT nếu làm được. |
| **Dự đoán nguy cơ rời bỏ từ review** | Không gọi là churn thật nếu chưa có dữ liệu hành vi mua lại. Chốt tên bài toán là tín hiệu bất mãn/nguy cơ rời bỏ tiềm ẩn. Số liệu metric phải khớp. |
| **Bot Detection Twitter** | Nếu dữ liệu hai lớp đã sửa, chốt Random Forest/XGBoost và feature importance. Nếu vẫn chỉ có một lớp, chưa được kết luận mô hình nhị phân. |
| **DDoS / Anomaly Detection** | Chốt so sánh Isolation Forest/LOF/One-Class SVM với supervised baseline. Metric chính: Recall, FPR, F1, Confusion Matrix. |
| **Calibration IDS** | Chốt bảng Raw vs Platt vs Isotonic với Brier Score, ECE, Precision, Recall, F1. Có Reliability Diagram trước/sau. |
| **Dự đoán giá nhà** | Chốt mô hình tốt nhất, thường là Random Forest/XGBoost/Gradient Boosting. Phân tích sai số theo quận, loại bất động sản, phân khúc giá. Làm rõ đơn vị tiền. |
| **Dự báo tiêu thụ điện** | Chốt dữ liệu đúng và horizon. So sánh Naive Lag-1, Seasonal Naive, Linear/Random Forest/XGBoost. Chỉ dùng LSTM nếu dữ liệu đủ dài và baseline đã ổn. |
| **Nhận diện biển báo giao thông** | Báo per-class F1, confusion matrix, ảnh dự đoán sai. Có demo dự đoán ảnh. |
| **Rác thải YOLO** | Chốt mAP50, mAP50-95, Precision, Recall theo lớp. Có ảnh detect đúng/sai. Phân tích lớp yếu như Glass/Paper/Metal. |
| **Visual Search sản phẩm** | Báo Recall@K, Precision@K hoặc mAP. Có ví dụ query đúng/sai. Nếu dùng FAISS, phải nói rõ FAISS tăng tốc truy hồi, không tự làm embedding tốt hơn. |
| **Tái cấu trúc vật thể 3D** | Phải có hình input–ground truth–prediction. Làm rõ Chamfer Distance, F-score, số điểm point cloud, threshold. |
| **Nhận dạng từ viết tay tiếng Anh** | Không được chỉ dừng ở EMNIST. Cần có pipeline IAM, CRNN + CTC, và metric CER/WER. |
| **Đạo văn code** | Chốt so sánh Jaccard, token similarity, AST similarity nếu có. Báo Precision, Recall, F1 và phân tích FP/FN. |
| **Automated Python Grading** | Có runner ổn định, hidden test, phân loại lỗi, FPR rõ ràng và demo chạy một bài nộp. Nên có phản hồi tự động theo lỗi. |

**10\. Phân công và minh chứng cá nhân**

Mỗi nhóm cần nộp bảng phân công tuần 5.

| **Thành viên** | **Công việc đã làm** | **File/code/minh chứng** | **Mức độ hoàn thành** |
| --- | --- | --- | --- |
| Thành viên 1 | Hoàn thiện dữ liệu, pipeline, EDA cuối | 01_final_data_pipeline.ipynb | Hoàn thành |
| Thành viên 2 | Chốt mô hình, chạy kết quả cuối | 02_final_model.ipynb, final_results.csv | Hoàn thành |
| Thành viên 3 | Phân tích lỗi, demo, báo cáo | 03_error_demo.ipynb, demo.py, báo cáo | Hoàn thành |

Không chấp nhận phân công chỉ ghi **“làm mục 1, 2, 3”** hoặc **“100%”** mà không có file minh chứng.

**11\. Cấu trúc thư mục nộp khuyến nghị**

Mỗi nhóm nên nộp theo cấu trúc sau để dễ kiểm tra:

NhomXX_Tuan5/  
├── report/  
│ └── BaoCao_Tuan5_NhomXX.docx  
├── notebooks/  
│ ├── 01_final_data_pipeline.ipynb  
│ ├── 02_final_model.ipynb  
│ └── 03_error_analysis_demo.ipynb  
├── src/  
│ └── predict.py  
├── demo/  
│ └── demo.py hoặc demo.ipynb  
├── results/  
│ ├── final_results.csv  
│ ├── final_metrics.csv  
│ ├── confusion_matrix.png  
│ ├── error_analysis.csv  
│ └── figures/  
├── data_sample/  
│ └── sample_input.csv  
├── slides/  
│ └── outline_or_slides_week5.pptx  
├── README.md  
└── requirements.txt

Không bắt buộc phải đúng hoàn toàn cấu trúc này, nhưng các file quan trọng phải dễ tìm.

**12\. Chuẩn bị thuyết trình 5–7 phút**

Tuần 5, mỗi nhóm cần có **dàn ý hoặc slide sơ bộ** để chuẩn bị báo cáo cuối.

Gợi ý cấu trúc slide:

| **Slide** | **Nội dung** |
| --- | --- |
| Slide 1 | Tên đề tài, thành viên, mục tiêu bài toán |
| Slide 2 | Dữ liệu, nhãn, pipeline xử lý |
| Slide 3 | Baseline và phương pháp chính |
| Slide 4 | Kết quả so sánh baseline – phương pháp chính – mô hình tốt nhất |
| Slide 5 | Phân tích lỗi và hạn chế |
| Slide 6 | Demo hoặc sản phẩm thử nghiệm |
| Slide 7 | Kết luận và hướng phát triển |

Thời lượng trình bày nên khoảng **5–7 phút**. Nhóm cần tập trung vào kết quả chính, demo và bài học kỹ thuật, không đọc toàn bộ báo cáo.

**13\. Sản phẩm cần nộp vào thứ 7**

| **Thành phần** | **Yêu cầu** |
| --- | --- |
| Báo cáo tuần 5 | Gần hoàn chỉnh như báo cáo cuối |
| Notebook/code | Chạy được từ đầu đến cuối |
| Bảng kết quả cuối | Baseline – phương pháp chính – mô hình tốt nhất |
| Biểu đồ/Confusion Matrix | Tùy đề tài |
| Phân tích lỗi | Có mẫu sai cụ thể |
| Demo hoặc ví dụ chạy thử | Notebook/script/giao diện nhỏ |
| Minh chứng cá nhân | File/code/notebook theo từng người |
| Khai báo AI | Ghi rõ AI hỗ trợ phần nào |
| Tài liệu tham khảo | Chuẩn hóa theo IEEE/APA |
| Dàn ý/slide sơ bộ | Chuẩn bị thuyết trình 5–7 phút |

**14\. Rubric đánh giá tuần 5**

| **Tiêu chí** | **Tỷ trọng** | **Mô tả** |
| --- | --- | --- |
| **Pipeline hoàn chỉnh và code chạy lại được** | **20%** | Code/notebook chạy được, dữ liệu đúng, kết quả tái lập được |
| **Kết quả cuối và bảng so sánh đầy đủ** | **20%** | Có baseline, phương pháp chính, mô hình tốt nhất; số liệu rõ và khớp |
| **Phân tích lỗi, hạn chế và hướng phát triển** | **15%** | Có mẫu lỗi cụ thể, giải thích nguyên nhân và hướng cải thiện |
| **Demo hoặc sản phẩm thử nghiệm** | **15%** | Demo/notebook/script chạy được, có ví dụ input/output |
| **Báo cáo gần hoàn chỉnh, trình bày rõ** | **10%** | Cấu trúc rõ, bảng/hình đầy đủ, văn phong kỹ thuật |
| **Lịch sử làm việc và minh chứng cá nhân** | **10%** | Có phân công cụ thể, file minh chứng theo từng thành viên |
| **Tài liệu tham khảo và khai báo AI** | **5%** | Có tài liệu tham khảo phù hợp, khai báo AI rõ |
| **Chuẩn bị thuyết trình / slide / dàn ý** | **5%** | Có dàn ý/slide, sẵn sàng báo cáo 5–7 phút |
| **Tổng** | **100%** |     |

**15\. Quy định trừ điểm**

| **Lỗi** | **Mức xử lý** |
| --- | --- |
| Code không chạy được | Trừ nặng |
| Không có baseline hoặc không so sánh với baseline | Trừ nặng |
| Không có phương pháp chính | Trừ nặng |
| Chỉ báo Accuracy | Trừ điểm |
| Không có phân tích lỗi | Trừ điểm |
| Không có demo/ví dụ chạy thử | Trừ điểm |
| Không có lịch sử làm việc | Trừ điểm |
| Không có minh chứng cá nhân | Trừ điểm |
| Số liệu trong báo cáo không khớp notebook | Trừ nặng |
| Confusion matrix không khớp Precision/Recall/F1 | Trừ nặng |
| Dữ liệu sai nhãn hoặc sai bài toán | Trừ rất nặng |
| Dùng AI nhưng không khai báo | Trừ điểm |
| Không có dàn ý/slide chuẩn bị thuyết trình | Trừ điểm nhẹ |

**16\. Lưu ý cuối**

Các nhóm nộp bài vào **thứ 7 hằng tuần**. Chủ nhật, giảng viên chấm bài, nhận xét và yêu cầu chỉnh sửa nếu cần. Thứ 2 tuần tiếp theo, giảng viên làm việc với từng nhóm để kiểm tra phần chỉnh sửa, đánh giá tiến độ và giao kế hoạch mới.

Tuần 5 là tuần **hoàn thiện sản phẩm**. Báo cáo không chỉ cần có kết quả, mà phải cho thấy nhóm hiểu rõ dữ liệu, mô hình, metric, lỗi còn tồn tại và cách triển khai demo.

Nhóm cần ưu tiên:

1.  Chạy lại pipeline từ đầu đến cuối.
2.  Chốt một bảng kết quả cuối chính thức.
3.  Đảm bảo số liệu trong báo cáo khớp notebook/code.
4.  Hoàn thiện demo hoặc ví dụ chạy thử.
5.  Phân tích lỗi có mẫu cụ thể.
6.  Chuẩn bị dàn ý/slide thuyết trình 5–7 phút.