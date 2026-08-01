# Reflection - 2A202601873 - Nguyễn Quang Huy

## My owned part

Tôi chịu trách nhiệm evidence mining: phân tích lịch sử chat của VLearn, xác định các câu hỏi học sinh thường gặp và các tình huống gây nhầm lẫn. Tôi trích xuất ví dụ có ngữ cảnh rõ ràng để xây dựng golden test set, đồng thời chuyển đổi bằng chứng đó thành các kịch bản đánh giá và hướng dẫn prompt để giảm sai thông tin.

## What changed because of evidence or testing

Từ dữ liệu chat, tôi nhận ra hai nhóm vấn đề chính: học sinh hỏi quá ngắn/không rõ ràng và học sinh hỏi thông tin vượt ra ngoài slide hiện tại. Vì vậy nhóm đã điều chỉnh prompt để: 1) kiểm tra xem context đủ không; 2) yêu cầu làm rõ khi câu hỏi mơ hồ; 3) từ chối trả lời nếu câu hỏi không được hỗ trợ bởi tài liệu hiện có.

## One technical/product decision I can explain

Quyết định quan trọng là khóa Tutor vào dữ liệu slide hiện tại/thông tin đã upload và cấm trả lời bằng kiến thức LLM chung. Điều này giảm hallucination rõ rệt và làm rõ chất lượng sản phẩm: nếu không có bằng chứng từ tài liệu, Tutor phải trả lời "không đủ thông tin" chứ không bịa đặt.

## What failed or stayed weak

Phần evidence mining còn yếu ở chỗ chúng tôi chưa đầy đủ kịch bản cho slide ảnh (image-only PDF) và các câu hỏi quá ngắn. Mặc dù đã xây được golden set, baseline đầu tiên chỉ đạt 52/67 test case, cho thấy prompt và cách trích xuất context vẫn cần tinh chỉnh.

## If we had one more week

Chúng tôi sẽ mở rộng evidence mining sang dữ liệu OCR và các slide ảnh, bổ sung thêm kịch bản câu hỏi mơ hồ, và thắt chặt tiêu chí "supported claim" trong evaluation. Ngoài ra, sẽ mở rộng golden set bằng thêm các đoạn chat thực tế để tăng độ bao phủ.

