# Reflection - 2A202601737 - Nguyễn Quốc Việt

## My owned part

Tôi chịu trách nhiệm phần prototype và validation. Tôi xây dựng `codebase/` để cho Tutor chạy trên dữ liệu slide, triển khai đường dẫn prompt, và đảm bảo ít nhất một luồng AI thực tế hoạt động. Tôi cũng dẫn chương trình demo và thu thập phản hồi người dùng để đánh giá độ tin cậy của prototype trong bối cảnh học tập.

## What changed because of evidence or testing

Trong quá trình validation, chúng tôi nhận thấy prototype hoạt động tốt với câu hỏi có context rõ ràng nhưng dễ mất điểm với câu hỏi mơ hồ hoặc khi slide chỉ chứa hình ảnh. Do đó, tôi giúp điều chỉnh luồng demo và checklist kiểm tra để bao gồm các trường hợp: câu hỏi ngắn, nhu cầu yêu cầu rõ ràng, và câu hỏi nằm ngoài nội dung slide.

## One technical/product decision I can explain

Quyết định tôi giải thích được là chọn mức prototype "working" với ít nhất một truy vấn AI thật thay vì làm mock toàn bộ. Điều này giúp nhóm chứng minh được tính khả thi: code thực sự gọi model, xử lý prompt, và phản hồi theo ngữ cảnh slide chứ không chỉ dựng kịch bản giả.

## What failed or stayed weak

Codebase hiện vẫn thiếu OCR cho slide ảnh và chưa có bộ xử lý riêng cho câu hỏi quá ngắn. Phản hồi từ validation cho thấy flow demo cần thêm hướng dẫn cho học sinh khi Tutor trả lời "không đủ thông tin" để tránh mất trải nghiệm.

## If we had one more week

Chúng tôi sẽ hoàn thiện tính năng nhận diện slide ảnh/OCR, bổ sung logic xử lý câu hỏi ngắn, và nâng cấp demo flow để học sinh hiểu rõ khi nào Tutor cần thêm thông tin. Ngoài ra, sẽ thêm dashboard kết quả eval để dễ so sánh các lượt chạy và chỉ ra những case chưa đạt chất lượng.

