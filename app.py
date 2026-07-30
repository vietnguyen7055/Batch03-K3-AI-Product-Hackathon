"""VLearn Clone — AI-Powered Learning Platform UI"""
import streamlit as st

st.set_page_config(page_title="VLearn", page_icon="📚", layout="wide")

# ── Mock slide data ──
SLIDES = [
    {"id": 1, "title": "Giới thiệu khóa học", "content": """# 🎓 Giới thiệu khóa học AI Thực Chiến

## Mục tiêu khóa học
- Hiểu và áp dụng AI vào sản phẩm thực tế
- Làm chủ quy trình Problem → Solution → Prototype
- Thành thạo prompt engineering & tool calling

## Lịch trình
| Ngày | Chủ đề |
|------|--------|
| Day 1 | LLM API & Token |
| Day 2 | AI Product Scoping |
| Day 3 | Chatbot vs Agent |
| Day 4 | Prompt Engineering |

## Giảng viên
- Thầy A — AI Engineer
- Cô B — Product Manager"""},
    {"id": 2, "title": "LLM API Cơ Bản", "content": """# 🔌 LLM API Cơ Bản

## OpenAI Chat Completions
```python
from openai import OpenAI
client = OpenAI(api_key="...")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Tham số quan trọng
- **temperature** (0.0–2.0): Độ sáng tạo
- **top_p** (0.0–1.0): Nucleus sampling
- **max_tokens**: Giới hạn độ dài output"""},
    {"id": 3, "title": "System Prompt & Token", "content": """# 🧠 System Prompt & Token

## System Prompt
Định hình persona cho model:
```python
messages = [
    {"role": "system", "content": "Bạn là giáo viên tiểu học..."},
    {"role": "user", "content": "Giải thích blockchain?"}
]
```

## Token Counting
- Dùng `tiktoken` để đếm token
- Giá input khác output
- 1 token ≈ 4 ký tự (ước lượng)"""},
    {"id": 4, "title": "Streaming & Retry", "content": """# ⚡ Streaming & Độ Bền

## Streaming
```python
stream = client.chat.completions.create(
    model="gpt-4o", messages=messages, stream=True
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

## Exponential Backoff
```python
for attempt in range(max_retries + 1):
    try: return fn()
    except: time.sleep(0.1 * 2**attempt)
```"""},
    {"id": 5, "title": "AI Product Scoping", "content": """# 🎯 AI Product Scoping

## 4 Lăng Kính Tìm Problem
1. **Lặp lại**: Việc gì xuất hiện đều đặn?
2. **Tốn thời gian**: Việc gì ngốn thời gian?
3. **AI có thể tốt hơn**: Việc gì AI làm tốt hơn?
4. **Pain từ người khác**: Ai đang kêu ca?

## Problem Statement 6-Field
- Actor · Workflow · Bottleneck
- Impact · Metric · Boundary"""},
    {"id": 6, "title": "ReAct Agent", "content": """# 🤖 ReAct Agent

## Thought → Action → Observation
1. **Thought**: Suy luận bước tiếp theo
2. **Action**: Gọi tool với tham số
3. **Observation**: Nhận kết quả từ tool

## Guardrails
- MAX_ITERATIONS: giới hạn vòng lặp
- Timeout: giới hạn thời gian mỗi tool"""},
]

# ── Custom CSS for VLearn-like layout ──
st.markdown("""
<style>
    .stApp { background: #f8f9fa; }
    .slide-nav { padding: 8px 4px; }
    .slide-nav-item {
        padding: 10px 12px; margin: 4px 0; border-radius: 8px; cursor: pointer;
        font-size: 13px; transition: all 0.15s;
    }
    .slide-nav-item:hover { background: #e9ecef; }
    .slide-nav-item.active { background: #dbeafe; font-weight: 600; border-left: 3px solid #2563eb; }
    .chat-msg { padding: 10px 12px; margin: 6px 0; border-radius: 10px; font-size: 13px; line-height: 1.5; }
    .chat-msg.user { background: #dbeafe; margin-left: 20px; }
    .chat-msg.bot { background: #f1f3f5; margin-right: 20px; }
    .chat-input input { font-size: 13px; }
    .slide-content { padding: 20px 30px; background: white; border-radius: 12px; min-height: 80vh; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    .slide-content h1 { font-size: 24px; margin-top: 0; }
    .slide-content pre { background: #1e293b; color: #e2e8f0; padding: 14px; border-radius: 8px; font-size: 13px; }
    .slide-content code { font-size: 13px; }
    hr { margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

# ── Initialize state ──
if "current_slide" not in st.session_state:
    st.session_state.current_slide = 1
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── 3-COLUMN LAYOUT ──
col1, col2, col3 = st.columns([1, 3, 2])

# ── LEFT: Slide Navigation ──
with col1:
    st.markdown("### 📑 Bài giảng")
    st.caption(f"{len(SLIDES)} slides")

    for slide in SLIDES:
        active = "active" if slide["id"] == st.session_state.current_slide else ""
        if st.button(
            f"{'🔵 ' if active else ''}{slide['id']}. {slide['title']}",
            key=f"nav_{slide['id']}",
            use_container_width=True,
            type="secondary" if slide["id"] != st.session_state.current_slide else "primary"
        ):
            st.session_state.current_slide = slide["id"]
            st.rerun()

# ── CENTER: Slide Content ──
current = next(s for s in SLIDES if s["id"] == st.session_state.current_slide)

with col2:
    with st.container():
        st.markdown(f'<div class="slide-content">{current["content"]}</div>', unsafe_allow_html=True)

# ── RIGHT: AI Chatbot ──
with col3:
    st.markdown("### 🤖 AI Tutor")

    with st.container(height=500):
        if not st.session_state.chat_history:
            st.caption("Chọn đoạn text ở slide bên trái, paste vào đây để AI tutor giải thích. Hoặc đặt câu hỏi bất kỳ về nội dung bài học.")

        for msg in st.session_state.chat_history:
            role = "user" if msg["role"] == "user" else "bot"
            st.markdown(f'<div class="chat-msg {role}"><b>{"Bạn" if role=="user" else "Tutor"}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

    with st.container():
        with st.form("chat_form", clear_on_submit=True):
            cols = st.columns([5, 1])
            with cols[0]:
                user_input = st.text_input("Hỏi AI Tutor...", key="chat_input", label_visibility="collapsed", placeholder="VD: Giải thích khái niệm temperature...")
            with cols[1]:
                submitted = st.form_submit_button("Gửi", use_container_width=True)

        if submitted and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Mock AI response based on current slide context
            mock_responses = {
                "temperature": "**Temperature** (0.0–2.0) kiểm soát độ ngẫu nhiên khi model sinh text. Temperature = 0.0 → output ổn định, lặp lại. Temperature = 1.0+ → sáng tạo, đa dạng nhưng dễ lan man. Với chatbot hỗ trợ khách hàng, nên dùng 0.2–0.3 để đảm bảo nhất quán.",
                "token": "**Token** là đơn vị text mà model xử lý. 1 token ≈ 4 ký tự tiếng Anh hoặc 0.75 từ. Tiếng Việt tốn nhiều token hơn vì dấu và ký tự Unicode. Dùng `tiktoken` để đếm chính xác.",
                "prompt": "**System Prompt** là chỉ thị đạo diễn — định hình toàn bộ giọng điệu và hành vi của model. Nó nằm ở đầu `messages` với `role: system`. Ví dụ: 'Bạn là giáo viên tiểu học...' sẽ khiến model giải thích mọi thứ đơn giản hơn.",
                "react": "**ReAct Agent** hoạt động theo vòng lặp: Thought → Action → Observation. Khác với Chatbot thường (chỉ sinh text tĩnh), ReAct Agent tự gọi công cụ (tool), nhận kết quả, rồi suy luận tiếp. Cần guardrail (MAX_ITERATIONS) để tránh lặp vô hạn.",
                "streaming": "**Streaming** cho phép model trả về từng token một thay vì đợi toàn bộ response. UX tốt hơn vì user thấy text xuất hiện dần. Dùng `stream=True` trong API call. Phù hợp cho chatbot, không cần cho xử lý batch.",
                "top_p": "**Top-p (nucleus sampling)** giới hạn token pool chỉ lấy những token có tổng xác suất ≥ p. Ví dụ top_p=0.9 → model chỉ chọn từ 90% token có khả năng cao nhất. Thường chỉ dùng 1 trong 2: temperature hoặc top_p.",
                "system": "**System Prompt** là tin nhắn đầu tiên trong `messages` với `role: 'system'`. Nó định nghĩa vai trò, giọng điệu, và ranh giới cho model. Khác với user prompt — system prompt không thay đổi giữa các lượt chat.",
            }

            response = "Tôi không có thông tin về câu hỏi này trong slide hiện tại. Bạn có thể hỏi về: temperature, token, system prompt, streaming, ReAct Agent, hoặc top-p."
            for keyword, answer in mock_responses.items():
                if keyword in user_input.lower():
                    response = answer
                    break

            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

st.divider()
st.caption("VLearn Clone · Mini Hackathon Prototype · Batch 03 K3")
