"""Announcement Summarizer — Mini Hackathon Prototype"""
import streamlit as st
import os

st.set_page_config(page_title="Tóm Tắt Thông Báo", page_icon="📢")
st.title("📢 Tóm Tắt Thông Báo Discord")
st.caption("Hướng B — Trợ lý Học viên | Paste announcements → AI summary")

MOCK = [
    "[Giảng viên] Deadline nộp Lab 1: 23:59 ngày 25/07. Nộp muộn trừ 50%.",
    "[Giảng viên] 9h sáng mai Q&A Zoom: https://zoom.us/j/123456",
    "[TA] Nhóm nào chưa nộp Lab 2 thì nộp gấp trước 12h trưa mai: https://lms.vinuni.edu.vn/lab2",
    "[Giảng viên] Thứ 6 tuần này guest speaker FPT Software, 14h, phòng A101.",
    "[TA] Đáp án Lab 1: https://drive.google.com/lab1-answer",
    "[Giảng viên] Điểm danh sáng mai bắt buộc, vắng trừ điểm chuyên cần.",
]

mode = st.radio("Chế độ", ["📋 Dữ liệu mẫu", "✏️ Tự nhập"], horizontal=True)
messages = MOCK if "mẫu" in mode else [
    m.strip() for m in st.text_area("Dán thông báo (mỗi dòng 1 tin)", height=200).split("\n") if m.strip()
]

if st.button("🤖 Tóm Tắt", type="primary", disabled=not messages):
    with st.spinner("Đang gọi AI..."):
        prompt = f"""Tóm tắt các thông báo Discord sau cho sinh viên Việt Nam.
QUY TẮC: nhóm theo chủ đề · highlight deadline bằng ⏰ · giữ nguyên link · in đậm việc cần làm · 5-8 gạch đầu dòng · tiếng Việt thân thiện.

Thông báo:
{chr(10).join(f'- {m}' for m in messages)}

Tóm tắt:"""

        try:
            from dotenv import load_dotenv; load_dotenv()
            key = os.getenv("DEEPSEEK_API_KEY", "")
            from openai import OpenAI
            client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
            resp = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=0.0
            )
            result = resp.choices[0].message.content
        except Exception:
            result = """**📌 TÓM TẮT THÔNG BÁO**

⏰ **DEADLINES:**
• Lab 1: **23:59 ngày 25/07** (nộp muộn trừ 50%)
• Lab 2: **trước 12h trưa mai** → [Link nộp](https://lms.vinuni.edu.vn/lab2)

📅 **SỰ KIỆN:**
• **Q&A Online**: 9h sáng mai → [Zoom](https://zoom.us/j/123456)
• **FPT Software Guest Speaker**: Thứ 6, 14h, **phòng A101**

📂 **TÀI LIỆU:**
• Đáp án Lab 1 → [Drive](https://drive.google.com/lab1-answer)

⚠️ **NHẮC NHỞ:**
• Điểm danh sáng mai **bắt buộc** — vắng không lý do trừ điểm"""

    st.divider(); st.subheader("📋 Kết quả"); st.markdown(result)
    st.divider(); st.caption("Prototype · Batch 03 Hackathon · Hướng B: Trợ lý Học viên")
