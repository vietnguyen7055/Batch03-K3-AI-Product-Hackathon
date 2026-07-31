"""VLearn-style study page with slide context and an AI tutor."""

from __future__ import annotations

import html
import json
import os
import re
import base64
import textwrap
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional in some deployments
    load_dotenv = None

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - app still works in mock mode
    OpenAI = None

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover - app still works with demo slide cards
    fitz = None


ROOT = Path(__file__).parent
EXTERNAL_DECKS_PATH = ROOT / "slides" / "decks.json"
SLIDE_PDF_DIR = ROOT.parent / "Slide-AIThucChien"
LOGO_PATH = ROOT.parent / "images.png"


def load_local_env() -> None:
    env_path = ROOT / ".env"
    if load_dotenv:
        load_dotenv(env_path, override=True)
        return

    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


load_local_env()

st.set_page_config(page_title="VLearn Tutor", page_icon="VL", layout="wide")


DEMO_DECKS: list[dict[str, Any]] = [
    {
        "id": "day01",
        "title": "Day01",
        "summary": "2 tài liệu · PUBLISHED",
        "status": "PUBLISHED",
        "materials": [
            {
                "id": "day01-foundation",
                "title": "day01-llm-foundation.pdf",
                "filename": "day01-llm-foundation.pdf",
                "pages": 38,
                "slides": [
                    {
                        "page": 1,
                        "layout": "concept",
                        "title": "LLM Foundation",
                        "subtitle": "Mô hình ngôn ngữ lớn hoạt động như thế nào?",
                        "eyebrow": "Day01 · Foundation",
                        "key_points": [
                            "LLM dự đoán token tiếp theo dựa trên ngữ cảnh.",
                            "Prompt tốt giúp mô hình biết vai trò, mục tiêu và ràng buộc.",
                            "Đánh giá cần đo theo hành vi người dùng, không chỉ cảm giác câu trả lời hay.",
                        ],
                    }
                ],
            }
        ],
    },
    {
        "id": "day02",
        "title": "Day02",
        "summary": "1 tài liệu · PUBLISHED",
        "status": "PUBLISHED",
        "materials": [
            {
                "id": "day02-product",
                "title": "day02-ai-product-scoping.pdf",
                "filename": "day02-ai-product-scoping.pdf",
                "pages": 42,
                "slides": [
                    {
                        "page": 1,
                        "layout": "concept",
                        "title": "AI Product Scoping",
                        "subtitle": "Từ vấn đề thật đến lát cắt prototype",
                        "eyebrow": "Day02 · Product Thinking",
                        "key_points": [
                            "Bắt đầu bằng pain cụ thể: ai, đang làm gì, vướng ở đâu, hậu quả gì.",
                            "Một prototype tốt chỉ cần một người dùng, một việc, một quyết định AI.",
                            "Nguồn sự thật quyết định chatbot có được phép trả lời hay phải hỏi lại.",
                        ],
                    }
                ],
            }
        ],
    },
    {
        "id": "day03",
        "title": "Day03",
        "summary": "2 tài liệu · PUBLISHED",
        "status": "STUDYING",
        "materials": [
            {
                "id": "day03-react",
                "title": "day03-tu-chatbot-den-agentic-agent-react.pdf",
                "filename": "day03-tu-chatbot-den-agentic-agent-react.pdf",
                "pages": 46,
                "slides": [
                    {
                        "page": 1,
                        "layout": "cover",
                        "title": "Từ Chatbot Đến Agentic Agent",
                        "subtitle": "AICB-P1 · Ngày 3 · Design Pattern ReAct",
                        "eyebrow": "VINUNIVERSITY",
                        "footer": "VinUniversity · Phase 1 · Tuần 1 · 17/03/2026",
                        "key_points": [
                            "Mục tiêu buổi học là phân biệt chatbot trả lời trực tiếp và agent biết dùng công cụ.",
                            "ReAct là mẫu thiết kế cho vòng lặp suy nghĩ, hành động và quan sát.",
                            "Agent cần guardrail để tránh gọi tool sai, lặp vô hạn hoặc trả lời ngoài phạm vi.",
                        ],
                    },
                    {
                        "page": 2,
                        "layout": "prompt",
                        "title": "Hãy suy nghĩ...",
                        "subtitle": "Nếu chatbot có thể gọi công cụ, điều gì thay đổi?",
                        "eyebrow": "Warm-up",
                        "key_points": [
                            "Chatbot thường chỉ sinh câu trả lời từ ngữ cảnh đã có.",
                            "Agent có thể quyết định gọi tool khi thiếu dữ kiện hoặc cần hành động bên ngoài.",
                            "Rủi ro tăng lên vì mỗi action sai có thể tạo hậu quả thật.",
                        ],
                        "callout": "Câu hỏi chính: khi nào chỉ cần chatbot, khi nào cần agent?",
                    },
                    {
                        "page": 3,
                        "layout": "compare",
                        "title": "Chatbot vs Agent",
                        "subtitle": "Khác biệt nằm ở quyền hành động",
                        "eyebrow": "Core concept",
                        "columns": [
                            {
                                "title": "Chatbot",
                                "items": [
                                    "Nhận câu hỏi và trả lời bằng text.",
                                    "Phụ thuộc mạnh vào prompt và context.",
                                    "Phù hợp giải thích, tóm tắt, hướng dẫn học.",
                                ],
                            },
                            {
                                "title": "Agent",
                                "items": [
                                    "Tự chọn bước tiếp theo trong một vòng lặp.",
                                    "Có thể gọi tool, đọc kết quả rồi quyết định tiếp.",
                                    "Phù hợp khi cần tra cứu, thao tác, kiểm tra trạng thái.",
                                ],
                            },
                        ],
                        "key_points": [
                            "Agent không chỉ trả lời; agent có thể hành động qua công cụ.",
                            "Càng nhiều quyền hành động thì càng cần ràng buộc, log và kiểm thử.",
                        ],
                    },
                    {
                        "page": 4,
                        "layout": "loop",
                        "title": "ReAct Loop",
                        "subtitle": "Reasoning + Acting trong một chu kỳ có quan sát",
                        "eyebrow": "Design pattern",
                        "steps": [
                            ("Thought", "Xác định mình cần biết hoặc cần làm gì tiếp."),
                            ("Action", "Gọi một tool cụ thể với input rõ ràng."),
                            ("Observation", "Đọc kết quả tool và cập nhật hướng giải."),
                            ("Answer", "Trả lời người học bằng kết luận có căn cứ."),
                        ],
                        "key_points": [
                            "ReAct buộc model tách phần suy luận nội bộ, hành động và quan sát.",
                            "Prototype nên log từng action để debug lỗi agent.",
                            "Giới hạn số vòng lặp là guardrail tối thiểu.",
                        ],
                    },
                    {
                        "page": 5,
                        "layout": "tool",
                        "title": "Tool Calling",
                        "subtitle": "Cho model một cách làm việc với hệ thống thật",
                        "eyebrow": "Implementation",
                        "key_points": [
                            "Tool schema cần mô tả input, output và điều kiện sử dụng.",
                            "Không cho tool quyền rộng hơn nhu cầu của lát cắt prototype.",
                            "Khi tool lỗi, agent cần báo thiếu căn cứ thay vì bịa kết quả.",
                        ],
                        "code": """tools = [{
    "name": "search_lesson",
    "description": "Find relevant lesson excerpts",
    "parameters": {"query": "string", "page": "integer"}
}]""",
                    },
                    {
                        "page": 6,
                        "layout": "guardrail",
                        "title": "Guardrails Cho Tutor",
                        "subtitle": "Giữ câu trả lời đúng nguồn, đúng phạm vi, đúng mức hỗ trợ",
                        "eyebrow": "Safety",
                        "key_points": [
                            "Nếu slide không có căn cứ, tutor phải nói rõ và hỏi thêm.",
                            "Mỗi câu trả lời nên kèm trích dẫn trang hoặc đoạn đang dùng.",
                            "Tutor nên hỏi lại một câu ngắn để kiểm tra hiểu bài.",
                        ],
                        "callout": "Một tutor tốt không chỉ trả lời đúng; nó còn giúp người học tự phát hiện lỗ hổng hiểu biết.",
                    },
                ],
            },
            {
                "id": "day03-d302",
                "title": "Day03-D302-tu-chatbot-den-agent.pdf",
                "filename": "Day03-D302-tu-chatbot-den-agent.pdf",
                "pages": 60,
                "slides": [
                    {
                        "page": 1,
                        "layout": "concept",
                        "title": "Agentic Agent Practice",
                        "subtitle": "Bài thực hành thiết kế ReAct agent",
                        "eyebrow": "Day03 · D302",
                        "key_points": [
                            "Chọn một workflow nhỏ có thể demo trong 5 phút.",
                            "Viết rõ tool nào được gọi và bằng chứng nào được dùng.",
                            "Đo lỗi theo tình huống thật, không chỉ theo test case đẹp.",
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "day04",
        "title": "Day04",
        "summary": "3 tài liệu · PUBLISHED",
        "status": "PUBLISHED",
        "materials": [
            {
                "id": "day04-prompt",
                "title": "day04-prompt-engineering.pdf",
                "filename": "day04-prompt-engineering.pdf",
                "pages": 48,
                "slides": [
                    {
                        "page": 1,
                        "layout": "concept",
                        "title": "Prompt Engineering",
                        "subtitle": "Chỉ thị, ví dụ và tiêu chí đánh giá",
                        "eyebrow": "Day04",
                        "key_points": [
                            "Prompt cần nêu vai trò, mục tiêu, dữ liệu được phép dùng và dạng output.",
                            "Few-shot giúp ổn định format khi task có chuẩn chấm rõ.",
                            "Prompt không thay thế được nguồn dữ liệu đáng tin.",
                        ],
                    }
                ],
            }
        ],
    },
    {
        "id": "day05",
        "title": "Day05",
        "summary": "3 tài liệu · PUBLISHED",
        "status": "PUBLISHED",
        "materials": [
            {
                "id": "day05-eval",
                "title": "day05-evaluation-validation.pdf",
                "filename": "day05-evaluation-validation.pdf",
                "pages": 35,
                "slides": [
                    {
                        "page": 1,
                        "layout": "concept",
                        "title": "Evaluation & Validation",
                        "subtitle": "Golden set, rubric và user test",
                        "eyebrow": "Day05",
                        "key_points": [
                            "Golden set phải đại diện cho tình huống người học thật sự hỏi.",
                            "Validation cần ghi nhận cả phản hồi tích cực và thất bại.",
                            "Kết quả đo trung thực quan trọng hơn việc cố làm đẹp số liệu.",
                        ],
                    }
                ],
            }
        ],
    },
]


def compact_text_lines(text: str, limit: int = 7) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip()
        if len(line) < 2:
            continue
        if line.isdigit():
            continue
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


@st.cache_data(show_spinner=False)
def pdf_page_count(pdf_path: str) -> int:
    if fitz is None:
        return 1
    try:
        with fitz.open(pdf_path) as doc:
            return max(doc.page_count, 1)
    except Exception:
        return 1


@st.cache_data(show_spinner=False)
def pdf_page_text(pdf_path: str, page: int) -> str:
    if fitz is None:
        return ""
    try:
        with fitz.open(pdf_path) as doc:
            page_index = min(max(page - 1, 0), doc.page_count - 1)
            return doc.load_page(page_index).get_text("text").strip()
    except Exception:
        return ""


@st.cache_data(show_spinner=False)
def pdf_page_png(pdf_path: str, page: int, zoom_percent: int) -> bytes:
    if fitz is None:
        return b""
    with fitz.open(pdf_path) as doc:
        page_index = min(max(page - 1, 0), doc.page_count - 1)
        matrix = fitz.Matrix(1.55 * zoom_percent / 100, 1.55 * zoom_percent / 100)
        pixmap = doc.load_page(page_index).get_pixmap(matrix=matrix, alpha=False)
        return pixmap.tobytes("png")


@st.cache_data(show_spinner=False)
def pdf_page_image_data_uri(pdf_path: str, page: int) -> str:
    image = pdf_page_png(pdf_path, page, 100)
    image_b64 = base64.b64encode(image).decode("ascii")
    return f"data:image/png;base64,{image_b64}"


@st.cache_data(show_spinner=False)
def pdf_page_size(pdf_path: str, page: int) -> tuple[float, float]:
    if fitz is None:
        return (1.0, 1.0)
    with fitz.open(pdf_path) as doc:
        page_index = min(max(page - 1, 0), doc.page_count - 1)
        rect = doc.load_page(page_index).rect
        return (float(rect.width), float(rect.height))


@st.cache_data(show_spinner=False)
def pdf_page_words(pdf_path: str, page: int) -> list[tuple[float, float, float, float, str]]:
    if fitz is None:
        return []
    with fitz.open(pdf_path) as doc:
        page_index = min(max(page - 1, 0), doc.page_count - 1)
        words = doc.load_page(page_index).get_text("words")
        return [
            (float(x0), float(y0), float(x1), float(y1), str(text))
            for x0, y0, x1, y1, text, *_ in words
            if str(text).strip()
        ]


@st.cache_data(show_spinner=False)
def pdf_file_bytes(pdf_path: str) -> bytes:
    return Path(pdf_path).read_bytes()


@st.cache_data(show_spinner=False)
def asset_data_uri(path: str) -> str:
    asset = Path(path)
    if not asset.exists():
        return ""
    suffix = asset.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(suffix, "application/octet-stream")
    return f"data:{mime};base64,{base64.b64encode(asset.read_bytes()).decode('ascii')}"


def build_pdf_decks() -> list[dict[str, Any]]:
    if not SLIDE_PDF_DIR.exists():
        return []

    decks: list[dict[str, Any]] = []
    for pdf_path in sorted(SLIDE_PDF_DIR.glob("Day*.pdf")):
        day_id = pdf_path.stem.lower()
        material_id = f"{day_id}-pdf"
        pages = pdf_page_count(str(pdf_path.resolve()))
        decks.append(
            {
                "id": day_id,
                "title": pdf_path.stem,
                "summary": f"1 tài liệu · {pages} trang · PUBLISHED",
                "status": "STUDYING" if day_id == "day03" else "PUBLISHED",
                "materials": [
                    {
                        "id": material_id,
                        "title": pdf_path.name,
                        "filename": pdf_path.name,
                        "pages": pages,
                        "pdf_path": str(pdf_path.resolve()),
                        "slides": [],
                    }
                ],
            }
        )
    return decks


def load_decks() -> tuple[list[dict[str, Any]], str | None]:
    """Load curated metadata, auto-detected PDFs, or demo slides."""
    if not EXTERNAL_DECKS_PATH.exists():
        pdf_decks = build_pdf_decks()
        if pdf_decks:
            return pdf_decks, None
        return DEMO_DECKS, None

    try:
        payload = json.loads(EXTERNAL_DECKS_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        pdf_decks = build_pdf_decks()
        if pdf_decks:
            return pdf_decks, f"Không đọc được slides/decks.json, đang dùng PDF tự phát hiện: {exc}"
        return DEMO_DECKS, f"Không đọc được slides/decks.json: {exc}"

    if isinstance(payload, dict) and isinstance(payload.get("days"), list):
        return payload["days"], None
    if isinstance(payload, list):
        return payload, None
    return DEMO_DECKS, "slides/decks.json cần là list hoặc object có field days."


DECKS, DECK_LOAD_WARNING = load_decks()


def flatten_materials(decks: list[dict[str, Any]]) -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    lookup: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for deck in decks:
        for material in deck.get("materials", []):
            lookup[material["id"]] = (deck, material)
    return lookup


MATERIAL_LOOKUP = flatten_materials(DECKS)
if "day03-pdf" in MATERIAL_LOOKUP:
    DEFAULT_MATERIAL_ID = "day03-pdf"
elif "day03-react" in MATERIAL_LOOKUP:
    DEFAULT_MATERIAL_ID = "day03-react"
else:
    DEFAULT_MATERIAL_ID = next(iter(MATERIAL_LOOKUP))


def ensure_state() -> None:
    defaults = {
        "material_id": DEFAULT_MATERIAL_ID,
        "page": 1,
        "zoom": 100,
        "selected_passage": "",
        "highlight_mode": False,
        "ocr_cache": {},
        "highlight_error": "",
        "quiz_session": None,
        "chat_history": [],
        "notes": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.material_id not in MATERIAL_LOOKUP:
        st.session_state.material_id = DEFAULT_MATERIAL_ID
        st.session_state.page = 1


def current_deck_material() -> tuple[dict[str, Any], dict[str, Any]]:
    return MATERIAL_LOOKUP[st.session_state.material_id]


def slide_by_page(material: dict[str, Any], page: int) -> dict[str, Any]:
    for slide in material.get("slides", []):
        if int(slide.get("page", -1)) == page:
            slide = dict(slide)
            if material.get("pdf_path"):
                text = pdf_page_text(material["pdf_path"], page)
                slide["pdf_text"] = text
                if not slide.get("key_points"):
                    slide["key_points"] = compact_text_lines(text, limit=6)[1:]
            return slide

    if material.get("pdf_path"):
        text = pdf_page_text(material["pdf_path"], page)
        lines = compact_text_lines(text, limit=7)
        title = lines[0] if lines else f"Trang {page}"
        return {
            "page": page,
            "layout": "pdf",
            "title": title,
            "subtitle": f"Trang PDF thực tế từ {material.get('filename', 'slide deck')}",
            "eyebrow": material.get("filename", "PDF"),
            "key_points": lines[1:] if len(lines) > 1 else lines,
            "pdf_text": text,
        }

    return {
        "page": page,
        "layout": "placeholder",
        "title": f"Trang {page} đang chờ slide mẫu",
        "subtitle": "Thêm nội dung thật trong codebase/slides/decks.json khi nhóm có file mẫu.",
        "eyebrow": "Placeholder",
        "key_points": [
            "Tutor vẫn dùng tiêu đề tài liệu, số trang và ghi chú hiện có làm ngữ cảnh.",
            "Khi thêm slide thật, điền title, subtitle, key_points, callout hoặc code.",
            "Câu trả lời sẽ tự kèm trích dẫn theo số trang hiện tại.",
        ],
        "callout": "Trang này là placeholder để demo luồng học trước khi có slide thật.",
    }


def material_page_count(material: dict[str, Any]) -> int:
    return max(int(material.get("pages", 1)), 1)


def set_material(material_id: str) -> None:
    st.session_state.material_id = material_id
    st.session_state.page = 1
    st.session_state.selected_passage = ""


def move_page(delta: int) -> None:
    _, material = current_deck_material()
    st.session_state.page = min(
        max(1, st.session_state.page + delta),
        material_page_count(material),
    )


def clean_join(items: list[str]) -> str:
    return " ".join(item.strip() for item in items if item and item.strip())


def slide_context(slide: dict[str, Any], material: dict[str, Any], selected: str = "") -> str:
    pdf_text = slide.get("pdf_text", "").strip()
    parts = [
        f"Tài liệu: {material.get('title', material.get('filename', 'slide deck'))}",
        f"Trang: {slide.get('page')}",
        f"Tiêu đề: {slide.get('title', '')}",
        f"Phụ đề: {slide.get('subtitle', '')}",
        "Ý chính: " + clean_join(slide.get("key_points", [])),
    ]
    if pdf_text:
        parts.append("Nội dung trích xuất từ PDF:\n" + pdf_text[:4000])
    if slide.get("callout"):
        parts.append(f"Ghi chú nổi bật: {slide['callout']}")
    if slide.get("code"):
        parts.append(f"Code trên slide: {slide['code']}")
    if selected:
        parts.append(f"Nội dung học viên đã chọn: {selected}")
    return "\n".join(parts)


def get_llm_config() -> tuple[str, str, str | None, str | None, str]:
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    if not provider:
        provider = "openai" if os.getenv("OPENAI_API_KEY") else "deepseek"

    if provider == "openai":
        return (
            "openai",
            "OpenAI",
            os.getenv("OPENAI_API_KEY"),
            os.getenv("OPENAI_BASE_URL") or None,
            os.getenv("LLM_MODEL") or os.getenv("OPENAI_DEFAULT_MODEL") or "gpt-4.1-mini",
        )

    return (
        "deepseek",
        "DeepSeek",
        os.getenv("DEEPSEEK_API_KEY"),
        os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    )


def llm_status() -> tuple[bool, str, str]:
    _provider, label, api_key, _base_url, model = get_llm_config()
    return bool(api_key and OpenAI is not None), label, model


def get_llm_answer(
    question: str,
    slide: dict[str, Any],
    material: dict[str, Any],
    selected_passage: str,
) -> str | None:
    if OpenAI is None:
        return None

    provider, _label, api_key, base_url, model = get_llm_config()
    if not api_key:
        return None

    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    history = st.session_state.chat_history[-6:]
    context_text = "Ngữ cảnh slide:\n" + slide_context(slide, material, selected_passage)
    page_number = int(slide.get("page", st.session_state.page))
    can_attach_page_image = (
        provider == "openai"
        and bool(material.get("pdf_path"))
        and not slide.get("pdf_text", "").strip()
    )
    if can_attach_page_image:
        context_text += (
            "\n\nTrang PDF này không có text trích xuất được. "
            f"Hãy đọc nội dung trực tiếp từ ảnh slide đính kèm và trả lời theo [trang {page_number}]."
        )

    context_message: dict[str, Any]
    if can_attach_page_image:
        context_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": context_text},
                {
                    "type": "image_url",
                    "image_url": {"url": pdf_page_image_data_uri(material["pdf_path"], page_number)},
                },
            ],
        }
    else:
        context_message = {"role": "user", "content": context_text}

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "Bạn là VLearn Tutor, trợ lý học theo ngữ cảnh slide. "
                "Chỉ trả lời dựa trên ngữ cảnh được cung cấp. Nếu thiếu căn cứ, nói rõ thiếu căn cứ "
                "và đề xuất người học mở đúng trang hoặc cung cấp thêm nội dung đã chọn. "
                "Trả lời ngắn, có cấu trúc, bằng tiếng Việt. Luôn kèm trích dẫn dạng [trang N]. "
                "Kết thúc bằng một câu hỏi kiểm tra hiểu bài khi phù hợp."
            ),
        },
        context_message,
    ]
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=700,
    )
    return response.choices[0].message.content or ""


def ocr_pdf_page_with_openai(pdf_path: str, page: int) -> str:
    provider, _label, api_key, base_url, model = get_llm_config()
    if provider != "openai" or not api_key or OpenAI is None:
        return ""

    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Bạn là bộ trích xuất chữ từ slide. "
                    "Đọc ảnh slide và trả về toàn bộ chữ nhìn thấy được, giữ heading và bullet nếu có. "
                    "Không giải thích, không thêm kiến thức ngoài ảnh."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Trích xuất chữ trên slide trang {page}."},
                    {
                        "type": "image_url",
                        "image_url": {"url": pdf_page_image_data_uri(pdf_path, page)},
                    },
                ],
            },
        ],
        temperature=0,
        max_tokens=1200,
    )
    return (response.choices[0].message.content or "").strip()


def page_text_for_highlight(material: dict[str, Any], page: int) -> tuple[str, str]:
    pdf_path = material.get("pdf_path")
    if not pdf_path:
        slide = slide_by_page(material, page)
        text = "\n".join(
            part
            for part in [
                slide.get("title", ""),
                slide.get("subtitle", ""),
                "\n".join(slide.get("key_points", [])),
                slide.get("callout", ""),
            ]
            if part
        ).strip()
        return text, "metadata"

    text = pdf_page_text(pdf_path, page).strip()
    if text:
        return text, "pdf_text"

    cache_key = f"{material['id']}:{page}"
    cache = st.session_state.setdefault("ocr_cache", {})
    if cache_key not in cache:
        try:
            cache[cache_key] = ocr_pdf_page_with_openai(pdf_path, page)
            st.session_state.highlight_error = ""
        except Exception as exc:
            cache[cache_key] = ""
            st.session_state.highlight_error = f"Không OCR được trang này: {exc}"
    return cache.get(cache_key, ""), "openai_ocr"


def parse_json_object(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def normalize_quiz_items(payload: dict[str, Any], fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    raw_questions = payload.get("questions", [])
    items: list[dict[str, Any]] = []
    for raw in raw_questions:
        question = str(raw.get("question", "")).strip()
        options = raw.get("options", {})
        if isinstance(options, list):
            options = {chr(65 + idx): str(value) for idx, value in enumerate(options[:4])}
        if not isinstance(options, dict):
            continue
        normalized_options = {
            key: str(options.get(key, "")).strip()
            for key in ["A", "B", "C", "D"]
            if str(options.get(key, "")).strip()
        }
        raw_correct = str(raw.get("correct") or raw.get("answer") or raw.get("correct_answer") or "").upper()
        correct_match = re.search(r"[ABCD]", raw_correct)
        correct = correct_match.group(0) if correct_match else ""
        explanation = str(raw.get("explanation", "")).strip()
        if question and len(normalized_options) == 4 and correct in normalized_options:
            items.append(
                {
                    "question": question,
                    "options": normalized_options,
                    "correct": correct,
                    "explanation": explanation or "Đáp án này khớp với nội dung trên slide.",
                }
            )
    return items[:3] or fallback


def fallback_quiz_items(slide: dict[str, Any], material: dict[str, Any], selected: str) -> list[dict[str, Any]]:
    page = int(slide.get("page", st.session_state.page))
    topic = (
        selected.strip()
        or slide.get("title", "").strip()
        or slide.get("subtitle", "").strip()
        or f"nội dung trang {page}"
    )
    return [
        {
            "question": "Ý chính của trang này liên quan nhất đến điều gì?",
            "options": {
                "A": topic,
                "B": "Chính sách học phí",
                "C": "Lịch nghỉ học",
                "D": "Thông tin không có trên slide",
            },
            "correct": "A",
            "explanation": f"Phương án A bám vào nội dung/ngữ cảnh hiện có của [trang {page}].",
        },
        {
            "question": "Khi tutor không có đủ căn cứ từ slide, cách phản hồi đúng là gì?",
            "options": {
                "A": "Bịa câu trả lời cho đủ ý",
                "B": "Nói rõ thiếu căn cứ và yêu cầu thêm ngữ cảnh",
                "C": "Đưa đáp án bài kiểm tra",
                "D": "Trích dẫn một trang chưa kiểm tra",
            },
            "correct": "B",
            "explanation": "Tutor phải bám nguồn và tránh đoán khi thiếu context.",
        },
        {
            "question": "Vì sao câu trả lời nên ghi [trang]?",
            "options": {
                "A": "Để người học tự kiểm tra lại nguồn",
                "B": "Để câu trả lời dài hơn",
                "C": "Để thay thế việc đọc slide",
                "D": "Để bỏ qua ngữ cảnh",
            },
            "correct": "A",
            "explanation": "Citation giúp người học kiểm chứng nội dung trả lời.",
        },
    ]


def generate_quiz_items(slide: dict[str, Any], material: dict[str, Any], selected: str) -> list[dict[str, Any]]:
    fallback = fallback_quiz_items(slide, material, selected)
    provider, _label, api_key, base_url, model = get_llm_config()
    if OpenAI is None or not api_key:
        return fallback

    page = int(slide.get("page", st.session_state.page))
    context_text = (
        "Tạo đúng 3 câu hỏi trắc nghiệm để kiểm tra hiểu bài từ slide hiện tại.\n"
        "Chỉ dùng nội dung trong context/ảnh slide. Không hỏi thông tin vụn vặt như tên người trình bày hoặc ngày tháng nếu không quan trọng cho bài học.\n"
        "Không lộ đáp án trong câu hỏi/options. Trả về JSON thuần, không markdown, theo schema:\n"
        '{"questions":[{"question":"...","options":{"A":"...","B":"...","C":"...","D":"..."},"correct":"A","explanation":"..."}]}\n\n'
        + slide_context(slide, material, selected)
    )
    can_attach_page_image = (
        provider == "openai"
        and bool(material.get("pdf_path"))
        and not slide.get("pdf_text", "").strip()
    )
    if can_attach_page_image:
        content: str | list[dict[str, Any]] = [
            {"type": "text", "text": context_text},
            {
                "type": "image_url",
                "image_url": {"url": pdf_page_image_data_uri(material["pdf_path"], page)},
            },
        ]
    else:
        content = context_text

    try:
        client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Bạn tạo quiz tương tác cho VLearn Tutor. Trả về JSON hợp lệ, không kèm đáp án trong phần options.",
                },
                {"role": "user", "content": content},
            ],
            temperature=0.2,
            max_tokens=1400,
        )
        payload = parse_json_object(response.choices[0].message.content or "")
        return normalize_quiz_items(payload, fallback)
    except Exception as exc:
        st.session_state.highlight_error = f"Không tạo quiz bằng LLM được, đang dùng quiz dự phòng: {exc}"
        return fallback


def start_quiz(material: dict[str, Any], slide: dict[str, Any]) -> None:
    selected = st.session_state.selected_passage.strip()
    items = generate_quiz_items(slide, material, selected)
    page = int(slide.get("page", st.session_state.page))
    st.session_state.quiz_session = {
        "id": f"{st.session_state.material_id}_{page}_{len(st.session_state.chat_history)}",
        "material_id": st.session_state.material_id,
        "page": page,
        "index": 0,
        "questions": items,
    }
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": f"Mình sẽ kiểm tra nhanh [trang {page}] bằng {len(items)} câu trắc nghiệm. Chọn một đáp án để mình phản hồi.",
        }
    )


def answer_quiz(choice: str) -> None:
    quiz = st.session_state.get("quiz_session")
    if not quiz:
        return
    index = int(quiz.get("index", 0))
    questions = quiz.get("questions", [])
    if index >= len(questions):
        st.session_state.quiz_session = None
        return

    item = questions[index]
    selected_text = html.escape(item["options"].get(choice, ""))
    correct = item["correct"]
    is_correct = choice == correct
    correct_text = html.escape(item["options"][correct])
    explanation = html.escape(item["explanation"])
    status_html = (
        '<span style="color:#07824f;font-weight:900;">Đúng</span>'
        if is_correct
        else '<span style="color:#c91f37;font-weight:900;">Sai</span>'
    )
    st.session_state.chat_history.append({"role": "user", "content": f"Chọn {choice}. {selected_text}"})
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": textwrap.dedent(
                f"""
                <div>
                    <div>{status_html}</div>
                    <div><strong>Đáp án đúng:</strong> {correct}. {correct_text}</div>
                    <div style="margin-top:6px;"><strong>Giải thích:</strong> {explanation}</div>
                </div>
                """
            ).strip(),
            "html": True,
        },
    )
    quiz["index"] = index + 1
    if quiz["index"] >= len(questions):
        st.session_state.chat_history.append({"role": "assistant", "content": "Bạn đã hoàn thành phần kiểm tra nhanh."})
        st.session_state.quiz_session = None
    else:
        st.session_state.quiz_session = quiz


def is_quiz_request(question: str) -> bool:
    lower = question.lower()
    return any(term in lower for term in ["kiểm tra", "kiem tra", "trắc nghiệm", "trac nghiem", "mcq", "quiz"])


def fallback_answer(question: str, slide: dict[str, Any], material: dict[str, Any], selected: str) -> str:
    lower_question = question.lower()
    page = slide.get("page", st.session_state.page)
    pdf_lines = compact_text_lines(slide.get("pdf_text", ""), limit=8)
    points = slide.get("key_points", []) or pdf_lines[1:6]
    context_line = selected.strip() or (points[0] if points else slide.get("subtitle", "nội dung trang này"))

    if any(term in lower_question for term in ["tóm tắt", "tom tat", "summary", "summarize"]):
        bullets = "\n".join(f"- {point}" for point in points[:4]) or f"- {context_line}"
        return (
            f"Tóm tắt [trang {page}]:\n{bullets}\n\n"
            "Câu kiểm tra: ý nào trên trang này là quan trọng nhất với bài học hiện tại?"
        )

    if any(term in lower_question for term in ["kiểm tra", "kiem tra", "quiz", "hỏi lại", "hoi lai"]):
        topic = context_line if context_line != "nội dung trang này" else f"nội dung chính của trang {page}"
        return (
            f"3 câu trắc nghiệm [trang {page}]:\n\n"
            f"1. Ý chính của trang này liên quan nhất đến điều gì?\n"
            f"A. {topic}\n"
            "B. Chính sách học phí\n"
            "C. Lịch nghỉ học\n"
            "D. Thông tin không có trên slide\n"
            "Đáp án: A. Vì đây là nội dung có trong ngữ cảnh hiện tại.\n\n"
            "2. Khi tutor không có đủ căn cứ từ slide, cách phản hồi đúng là gì?\n"
            "A. Bịa câu trả lời cho đủ ý\n"
            "B. Nói rõ thiếu căn cứ và yêu cầu thêm ngữ cảnh\n"
            "C. Đưa đáp án bài kiểm tra\n"
            "D. Trích dẫn một trang chưa kiểm tra\n"
            "Đáp án: B. Vì tutor phải bám nguồn và tránh đoán.\n\n"
            "3. Vì sao cần ghi rõ [trang] khi trả lời?\n"
            "A. Để người học kiểm tra lại nguồn\n"
            "B. Để câu trả lời dài hơn\n"
            "C. Để thay thế việc đọc slide\n"
            "D. Để bỏ qua ngữ cảnh\n"
            "Đáp án: A. Vì citation giúp người học tự xác minh."
        )

    if any(term in lower_question for term in ["react", "agent", "tool", "chatbot"]):
        if slide.get("pdf_text") and not any(
            keyword in slide["pdf_text"].lower()
            for keyword in ["react", "agent", "tool", "chatbot", "llm"]
        ):
            return (
                f"Mình chưa thấy đủ căn cứ trên [trang {page}] để trả lời chắc về ReAct, agent hoặc tool. "
                "Bạn hãy chuyển đến trang có nội dung liên quan hoặc dán nội dung đã chọn để mình giải thích đúng nguồn."
            )
        return (
            f"Dựa trên [trang {page}], ý chính là: chatbot chủ yếu sinh câu trả lời từ ngữ cảnh, "
            "còn agent có thêm quyền chọn hành động như gọi tool, đọc observation rồi mới kết luận. "
            "Vì agent có thể tác động ra ngoài phần trả lời text, nhóm cần guardrail: giới hạn vòng lặp, "
            "schema tool rõ ràng và log từng bước.\n\n"
            "Câu kiểm tra: trong prototype của bạn, tool nào là tool nhỏ nhất nhưng vẫn chứng minh được giá trị?"
        )

    if any(term in lower_question for term in ["trích dẫn", "citation", "nguồn", "can cu", "căn cứ"]):
        return (
            f"Căn cứ hiện có nằm ở [trang {page}] của `{material.get('filename', material.get('title'))}`. "
            f"Đoạn liên quan nhất là: \"{context_line}\". Nếu muốn tutor chính xác hơn, hãy dán nội dung đã chọn "
            "hoặc thêm nội dung slide thật vào `slides/decks.json`."
        )

    return (
        f"Mình sẽ giải thích dựa trên [trang {page}]. Ý quan trọng là: {context_line}. "
        "Khi học phần này, hãy tự hỏi: hệ thống đang chỉ trả lời bằng text hay được phép thực hiện hành động "
        "qua tool? Câu trả lời quyết định thiết kế guardrail và cách đánh giá lỗi.\n\n"
        "Câu kiểm tra: bạn sẽ đo lỗi của tutor ở tình huống này bằng tiêu chí nào?"
    )


def ask_tutor(question: str) -> None:
    question = question.strip()
    if not question:
        return

    _, material = current_deck_material()
    slide = slide_by_page(material, st.session_state.page)
    selected = st.session_state.selected_passage.strip()
    st.session_state.chat_history.append({"role": "user", "content": question})

    try:
        answer = get_llm_answer(question, slide, material, selected)
    except Exception as exc:
        answer = (
            "LLM chưa trả lời được ở lượt này, nên mình dùng chế độ demo. "
            f"Lỗi kỹ thuật: {exc}"
        )

    if not answer:
        answer = fallback_answer(question, slide, material, selected)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})


def html_list(items: list[str]) -> str:
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def render_slide(slide: dict[str, Any], material: dict[str, Any], preview: bool = False) -> str:
    layout = slide.get("layout", "concept")
    page = int(slide.get("page", 1))
    title = html.escape(slide.get("title", f"Trang {page}"))
    subtitle = html.escape(slide.get("subtitle", ""))
    eyebrow = html.escape(slide.get("eyebrow", "Slide"))
    filename = html.escape(material.get("filename", material.get("title", "")))
    preview_class = " is-preview" if preview else ""

    if layout == "cover":
        body = f"""
<div class="cover-panel">
    <div class="brand-mark">V</div>
    <div class="cover-brand">{eyebrow}</div>
    <h1>{title}</h1>
    <p>{subtitle}</p>
    <div class="cover-footer">{html.escape(slide.get("footer", ""))}</div>
</div>
"""
    elif layout == "compare":
        columns = slide.get("columns", [])
        column_html = ""
        for col in columns[:2]:
            column_html += f"""
<div class="compare-card">
    <h3>{html.escape(col.get("title", ""))}</h3>
    <ul>{html_list(col.get("items", []))}</ul>
</div>
"""
        body = f"""
<div class="slide-heading">
    <span>{eyebrow}</span>
    <h2>{title}</h2>
    <p>{subtitle}</p>
</div>
<div class="compare-grid">{column_html}</div>
"""
    elif layout == "loop":
        steps = slide.get("steps", [])
        step_html = ""
        for idx, step in enumerate(steps, start=1):
            label, desc = step
            step_html += f"""
<div class="loop-step">
    <div class="step-index">{idx}</div>
    <div><strong>{html.escape(label)}</strong><p>{html.escape(desc)}</p></div>
</div>
"""
        body = f"""
<div class="slide-heading">
    <span>{eyebrow}</span>
    <h2>{title}</h2>
    <p>{subtitle}</p>
</div>
<div class="loop-grid">{step_html}</div>
"""
    elif layout == "tool":
        code = html.escape(slide.get("code", ""))
        body = f"""
<div class="slide-heading">
    <span>{eyebrow}</span>
    <h2>{title}</h2>
    <p>{subtitle}</p>
</div>
<div class="split-grid">
    <ul class="large-points">{html_list(slide.get("key_points", []))}</ul>
    <pre>{code}</pre>
</div>
"""
    else:
        body = f"""
<div class="slide-heading">
    <span>{eyebrow}</span>
    <h2>{title}</h2>
    <p>{subtitle}</p>
</div>
<ul class="large-points">{html_list(slide.get("key_points", []))}</ul>
"""
        if slide.get("callout"):
            body += f"""<div class="slide-callout">{html.escape(slide["callout"])}</div>"""

    raw_html = f"""
<section class="sheet{preview_class}">
    <div class="sheet-meta">
        <span>Trang {page} / {material_page_count(material)}</span>
        <span>{filename}</span>
    </div>
    <div class="slide-canvas {html.escape(layout)}">
        {body}
    </div>
</section>
"""
    return textwrap.dedent(raw_html).strip()

def render_pdf_text_layer(pdf_path: str, page: int) -> str:
    page_width, page_height = pdf_page_size(pdf_path, page)
    if page_width <= 0 or page_height <= 0:
        return ""

    spans: list[str] = []
    for x0, y0, x1, y1, text in pdf_page_words(pdf_path, page):
        left = max(0.0, min(100.0, x0 / page_width * 100))
        top = max(0.0, min(100.0, y0 / page_height * 100))
        width = max(0.1, min(100.0 - left, (x1 - x0) / page_width * 100))
        height = max(0.1, min(100.0 - top, (y1 - y0) / page_height * 100))
        spans.append(
            "<span style="
            f"'left:{left:.3f}%;top:{top:.3f}%;width:{width:.3f}%;height:{height:.3f}%;'"
            f">{html.escape(text)}</span>"
        )
    return "".join(spans)


def render_pdf_sheet(material: dict[str, Any], page: int) -> str:
    slide = slide_by_page(material, page)
    filename = html.escape(material.get("filename", material.get("title", "")))
    title = html.escape(slide.get("title", f"Trang {page}"))
    pdf_path = material["pdf_path"]

    try:
        image = pdf_page_png(pdf_path, page, st.session_state.zoom)
    except Exception as exc:
        fallback_slide = {
            "page": page,
            "layout": "placeholder",
            "title": f"Không render được PDF trang {page}",
            "subtitle": str(exc),
            "eyebrow": "PDF render error",
            "key_points": [
                "Kiểm tra PyMuPDF đã được cài trong môi trường chạy app.",
                "Nếu chỉ cần demo tutor, phần text trích xuất vẫn có thể được dùng làm ngữ cảnh.",
            ],
        }
        return render_slide(fallback_slide, material)

    image_b64 = base64.b64encode(image).decode("ascii")
    return textwrap.dedent(
        f"""
        <section class="sheet pdf-sheet" id="pdf-page-{page}">
            <div class="sheet-meta">
                <span>Trang {page} / {material_page_count(material)}</span>
                <span>{filename}</span>
            </div>
            <div class="pdf-frame">
                <img src="data:image/png;base64,{image_b64}" alt="{title}" />
            </div>
        </section>
        """
    ).strip()


def render_pdf_document(material: dict[str, Any]) -> None:
    pdf_path = material.get("pdf_path")
    if not pdf_path:
        return

    total_pages = material_page_count(material)
    current_page = st.session_state.page
    with st.container(height=650, border=False, key=f"pdf_scroller_{material['id']}"):
        for page in range(1, total_pages + 1):
            st.markdown(render_pdf_sheet(material, page), unsafe_allow_html=True)
    components.html(
        textwrap.dedent(
            f"""
            <script>
            const target = window.parent.document.getElementById("pdf-page-{current_page}");
            if (target) {{
                target.scrollIntoView({{ block: "start", behavior: "auto" }});
            }}
            </script>
            """
        ).strip(),
        height=0,
    )


def render_css() -> None:
    st.markdown(
        textwrap.dedent(
            """
<style>
    :root {
        --ink: #142033;
        --muted: #6d7e98;
        --line: #dbe4ef;
        --blue: #145da0;
        --blue-strong: #0a4a8a;
        --blue-soft: #e7f1fb;
        --panel: #f8fbff;
        --paper: #fffdf5;
        --green: #00856f;
        --red: #c91f37;
    }

    .stApp {
        background: #f3f7fb;
        color: var(--ink);
    }

    header, footer, #MainMenu {
        visibility: hidden;
    }

    .block-container {
        max-width: 100%;
        padding: 0.65rem 1rem 0.8rem;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.62rem;
    }

    .topbar {
        height: 58px;
        display: grid;
        grid-template-columns: 220px 1fr auto;
        align-items: center;
        gap: 16px;
        padding: 0 14px;
        border-bottom: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 1px 8px rgba(20, 32, 51, 0.06);
        margin: -0.65rem -1rem 0.5rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 800;
        font-size: 1.25rem;
    }

    .brand-logo-crop {
        width: 132px;
        height: 50px;
        overflow: hidden;
        position: relative;
        flex: 0 0 auto;
    }

    .brand-logo-img {
        width: 128px;
        height: 128px;
        object-fit: contain;
        object-position: center;
        display: block;
        transform: translateY(-29px);
    }

    .doc-title strong {
        display: block;
        font-size: 1.04rem;
        line-height: 1.15;
    }

    .doc-title span,
    .top-actions {
        color: var(--muted);
        font-size: 0.78rem;
    }

    .top-actions {
        display: flex;
        gap: 8px;
        align-items: center;
        white-space: nowrap;
    }

    .pill {
        border: 1px solid var(--line);
        background: white;
        border-radius: 999px;
        padding: 6px 11px;
        font-weight: 700;
        color: var(--blue-strong);
    }

    .panel-title {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 11px 10px;
        border-bottom: 1px solid var(--line);
    }

    .panel-icon {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        display: grid;
        place-items: center;
        border: 1px solid #cbdcf0;
        background: var(--blue-soft);
        color: var(--blue-strong);
        font-weight: 900;
    }

    .panel-title h2 {
        font-size: 1rem;
        margin: 0;
        letter-spacing: 0;
    }

    .panel-title p {
        margin: 1px 0 0;
        color: var(--muted);
        font-size: 0.78rem;
    }

    .day-card {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #fbfdff;
        padding: 12px;
        margin-bottom: 10px;
    }

    .day-card.active {
        border-color: #9fc5ee;
        background: #eef6ff;
    }

    .day-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
    }

    .day-title {
        font-weight: 800;
        font-size: 0.95rem;
    }

    .day-summary {
        color: #8496b2;
        font-size: 0.74rem;
        margin-top: 3px;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    .status-chip {
        border-radius: 999px;
        background: #d9e8f3;
        color: var(--blue-strong);
        padding: 4px 10px;
        font-size: 0.67rem;
        font-weight: 900;
    }

    .toolbar {
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        gap: 12px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        padding: 8px 10px;
        box-shadow: 0 2px 8px rgba(20, 32, 51, 0.06);
    }

    .tool-group {
        display: flex;
        gap: 6px;
        align-items: center;
        flex-wrap: wrap;
    }

    .tool-button {
        border: 1px solid var(--line);
        background: #f9fbfe;
        color: #33445f;
        border-radius: 8px;
        padding: 7px 11px;
        font-size: 0.78rem;
        font-weight: 800;
    }

    .tool-button.active {
        color: var(--blue-strong);
        background: #eaf4ff;
        border-color: #b8d6f3;
    }

    .context-pill {
        min-height: 2.35rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #b8d6f3;
        background: #eaf4ff;
        color: var(--blue-strong);
        border-radius: 8px;
        padding: 0 11px;
        font-size: 0.78rem;
        font-weight: 900;
        white-space: nowrap;
    }

    .stage {
        height: calc(100vh - 155px);
        min-height: 620px;
        overflow: auto;
        border-left: 1px solid var(--line);
        border-right: 1px solid var(--line);
        background:
            linear-gradient(#ece6d4 1px, transparent 1px),
            var(--paper);
        background-size: 100% 31px;
        padding: 18px 22px 36px;
    }

    .pdf-scroller,
    div[class*="st-key-pdf_scroller"] {
        height: calc(100vh - 155px) !important;
        min-height: 620px;
        overflow: auto !important;
        border-left: 1px solid var(--line);
        border-right: 1px solid var(--line);
        background:
            linear-gradient(#ece6d4 1px, transparent 1px),
            var(--paper);
        background-size: 100% 31px;
        padding: 18px 22px 36px;
    }

    .pdf-scroller > div[data-testid="stVerticalBlock"],
    div[class*="st-key-pdf_scroller"] div[data-testid="stVerticalBlock"] {
        gap: 0;
    }
    .sheet {
        max-width: 980px;
        margin: 0 auto 30px;
        background: rgba(255, 253, 245, 0.96);
        border: 1px solid #8cc2ea;
        border-radius: 8px;
        padding: 18px 20px 22px;
        box-shadow: 0 3px 12px rgba(20, 32, 51, 0.12);
    }

    .sheet.is-preview {
        opacity: 0.76;
    }

    .sheet-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        color: #8294b0;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .pdf-sheet {
        background: #ffffff;
        padding: 14px;
        max-width: 980px;
    }

    .pdf-frame {
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        background: #ffffff;
        border: 1px solid #e3e9f2;
    }

    .pdf-frame img {
        display: block;
        width: 100%;
        height: auto;
    }

    .slide-canvas {
        min-height: 325px;
        border-radius: 8px;
        overflow: hidden;
        background: #ffffff;
        border: 1px solid #e3e9f2;
        position: relative;
    }

    .slide-canvas.cover {
        min-height: 326px;
        background:
            linear-gradient(rgba(10, 74, 138, 0.75), rgba(10, 74, 138, 0.62)),
            radial-gradient(circle at 78% 48%, rgba(255, 255, 255, 0.18), transparent 24%),
            linear-gradient(145deg, #0e4d86 0%, #2c74ad 45%, #9bb7c6 100%);
        color: white;
    }

    .cover-panel {
        min-height: 326px;
        display: grid;
        place-items: center;
        align-content: center;
        gap: 10px;
        text-align: center;
        padding: 34px;
    }

    .brand-mark {
        width: 50px;
        height: 50px;
        display: grid;
        place-items: center;
        clip-path: polygon(50% 0, 100% 30%, 100% 68%, 50% 100%, 0 68%, 0 30%);
        background: white;
        color: var(--blue-strong);
        font-weight: 900;
        font-size: 1.45rem;
    }

    .cover-brand {
        font-weight: 900;
        font-size: 1.42rem;
    }

    .cover-panel h1 {
        font-size: 1.72rem;
        margin: 18px 0 0;
        letter-spacing: 0;
    }

    .cover-panel p {
        margin: 0;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.92);
    }

    .cover-footer {
        margin-top: 34px;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .slide-heading {
        padding: 34px 42px 10px;
    }

    .slide-heading span {
        color: var(--red);
        font-size: 0.74rem;
        text-transform: uppercase;
        font-weight: 900;
    }

    .slide-heading h2 {
        margin: 8px 0 4px;
        font-size: 1.7rem;
        letter-spacing: 0;
    }

    .slide-heading p {
        color: var(--muted);
        margin: 0;
        font-size: 0.95rem;
    }

    .large-points {
        padding: 6px 56px 22px 64px;
        margin: 0;
        color: #20314a;
        line-height: 1.75;
        font-size: 0.95rem;
    }

    .slide-callout {
        margin: 4px 42px 34px;
        border-left: 4px solid var(--red);
        background: #fff6f3;
        padding: 12px 14px;
        color: #54322b;
        font-weight: 700;
        border-radius: 0 8px 8px 0;
    }

    .compare-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
        padding: 12px 42px 38px;
    }

    .compare-card {
        border: 1px solid #d8e3ee;
        background: #f8fbff;
        border-radius: 8px;
        padding: 18px 18px 12px;
        min-height: 190px;
    }

    .compare-card h3 {
        margin: 0 0 10px;
        color: var(--blue-strong);
    }

    .compare-card ul {
        margin: 0;
        padding-left: 20px;
        line-height: 1.55;
        color: #253650;
    }

    .loop-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
        padding: 16px 42px 38px;
    }

    .loop-step {
        display: grid;
        grid-template-columns: 42px 1fr;
        gap: 12px;
        align-items: start;
        border: 1px solid #d8e3ee;
        background: #f9fbfe;
        border-radius: 8px;
        padding: 14px;
    }

    .step-index {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: grid;
        place-items: center;
        background: var(--blue-strong);
        color: white;
        font-weight: 900;
    }

    .loop-step p {
        margin: 4px 0 0;
        color: var(--muted);
        line-height: 1.45;
    }

    .split-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 18px;
        padding: 12px 42px 38px;
    }

    .split-grid .large-points {
        padding: 0 0 0 20px;
    }

    pre {
        margin: 0;
        border-radius: 8px;
        padding: 16px;
        background: #162235;
        color: #e9f1fb;
        overflow: auto;
        font-size: 0.78rem;
        line-height: 1.55;
    }

    .chat-context {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: white;
        padding: 11px 12px;
        color: var(--muted);
        font-size: 0.76rem;
    }

    .chat-context strong {
        display: block;
        color: var(--ink);
        font-size: 0.85rem;
        margin-bottom: 2px;
    }

    .assistant-empty {
        border: 1px solid var(--line);
        background: white;
        border-radius: 8px;
        padding: 16px;
        line-height: 1.55;
        color: var(--ink);
        box-shadow: 0 1px 5px rgba(20, 32, 51, 0.06);
    }

    .small-muted {
        color: var(--muted);
        font-size: 0.75rem;
        line-height: 1.45;
    }

    div.stButton > button {
        background: white !important;
        color: black !important;
        border: 1px solid #d0d7de !important;
        border-radius: 8px;
        min-height: 2.35rem;
        font-weight: 800;
        letter-spacing: 0;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 8px;
    }

    @media (max-width: 960px) {
        .topbar {
            grid-template-columns: 1fr;
            height: auto;
            padding: 10px 14px;
        }

        .top-actions {
            display: none;
        }

        .toolbar {
            grid-template-columns: 1fr;
        }

        .stage {
            height: auto;
            min-height: 0;
            padding: 12px;
        }

        .compare-grid,
        .loop-grid,
        .split-grid {
            grid-template-columns: 1fr;
        }

        .slide-heading,
        .compare-grid,
        .loop-grid,
        .split-grid {
            padding-left: 22px;
            padding-right: 22px;
        }

        .large-points {
            padding-left: 42px;
            padding-right: 22px;
        }
    }
</style>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def render_topbar(material: dict[str, Any]) -> None:
    ready, llm_label, model = llm_status()
    status = f"{llm_label} ready" if ready else "Demo tutor"
    logo_uri = asset_data_uri(str(LOGO_PATH))
    brand_html = (
        f'<div class="brand-logo-crop"><img class="brand-logo-img" src="{logo_uri}" alt="VinUniversity" /></div>'
        if logo_uri
        else '<strong>VLearn</strong>'
    )
    st.markdown(
        textwrap.dedent(
            f"""
            <div class="topbar">
                <div class="brand">{brand_html}</div>
                <div class="doc-title">
                    <strong>{html.escape(material.get("title", ""))}</strong>
                    <span>COMP2010 · Lecture material · contextual study mode</span>
                </div>
                <div class="top-actions">
                    <span class="pill">VI</span>
                    <span class="pill">{status}</span>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def render_left_panel() -> None:
    st.markdown(
        textwrap.dedent(
            """
            <div class="panel-title">
                <div class="panel-icon">B</div>
                <div>
                    <h2>Học liệu môn học</h2>
                    <p>Chương, slide và tài liệu đã upload</p>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

    if DECK_LOAD_WARNING:
        st.warning(DECK_LOAD_WARNING)

    for deck in DECKS:
        active = any(m["id"] == st.session_state.material_id for m in deck.get("materials", []))
        st.markdown(
            textwrap.dedent(
                f"""
                <div class="day-card{' active' if active else ''}">
                    <div class="day-row">
                        <div>
                            <div class="day-title">{html.escape(deck.get("title", ""))}</div>
                            <div class="day-summary">{html.escape(deck.get("summary", ""))}</div>
                        </div>
                        <div class="status-chip">{html.escape(deck.get("status", "PUBLISHED"))}</div>
                    </div>
                </div>
                """
            ).strip(),
            unsafe_allow_html=True,
        )

        if active:
            for material in deck.get("materials", []):
                selected = material["id"] == st.session_state.material_id
                label = f"{material.get('title', 'deck')} · {material_page_count(material)} trang"
                if st.button(
                    label,
                    key=f"material_{material['id']}",
                    use_container_width=True,
                    type="primary" if selected else "secondary",
                ):
                    set_material(material["id"])
                    st.rerun()
        else:
            first_material = deck.get("materials", [{}])[0].get("id")
            if first_material and st.button("Mở tài liệu", key=f"open_{deck['id']}", use_container_width=True):
                set_material(first_material)
                st.rerun()

    st.markdown(
        textwrap.dedent(
            """
            <p class="small-muted">
            App tự đọc PDF trong <code>../Slide-AIThucChien</code>. Dùng <code>slides/decks.json</code> nếu cần metadata chi tiết hơn.
            </p>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def render_toolbar(material: dict[str, Any]) -> None:
    page = st.session_state.page
    total_pages = material_page_count(material)

    if material.get("pdf_path"):
        with st.container():
            nav_cols = st.columns([0.75, 1.4, 1.0, 0.55, 0.8, 0.55, 1.9, 1.0], gap="small")
            with nav_cols[0]:
                if st.button(
                    "Đọc",
                    use_container_width=True,
                    type="primary" if not st.session_state.highlight_mode else "secondary",
                    key="read_mode_pdf",
                ):
                    st.session_state.highlight_mode = False
                    st.rerun()
            with nav_cols[1]:
                if st.button(
                    "Highlight",
                    use_container_width=True,
                    type="primary" if st.session_state.highlight_mode else "secondary",
                    key="highlight_mode_pdf",
                ):
                    st.session_state.highlight_mode = True
                    with st.spinner("Đang đọc chữ trên trang..."):
                        text, _source = page_text_for_highlight(material, page)
                    st.session_state.selected_passage = text
                    st.rerun()
            with nav_cols[2]:
                if st.button("Copy text", use_container_width=True, key="copy_text_pdf"):
                    with st.spinner("Đang lấy text trên trang..."):
                        text, _source = page_text_for_highlight(material, page)
                    st.session_state.selected_passage = text[:4000]
                    st.rerun()
            with nav_cols[3]:
                if st.button("<", use_container_width=True, disabled=page <= 1, key="prev_top_pdf"):
                    move_page(-1)
                    st.rerun()
            with nav_cols[4]:
                selected_page = st.number_input(
                    "Trang",
                    min_value=1,
                    max_value=total_pages,
                    value=page,
                    step=1,
                    label_visibility="collapsed",
                    key=f"page_picker_pdf_{st.session_state.material_id}_{page}",
                )
                if int(selected_page) != page:
                    st.session_state.page = int(selected_page)
                    st.rerun()
            with nav_cols[5]:
                if st.button(">", use_container_width=True, disabled=page >= total_pages, key="next_top_pdf"):
                    move_page(1)
                    st.rerun()
            with nav_cols[6]:
                st.markdown(
                    f"<div class='context-pill'>Ngữ cảnh tutor: trang {page} / {total_pages}</div>",
                    unsafe_allow_html=True,
                )
            with nav_cols[7]:
                st.download_button(
                    "PDF gốc",
                    data=pdf_file_bytes(material["pdf_path"]),
                    file_name=material.get("filename", "slides.pdf"),
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_pdf",
                )
        return

    st.markdown(
        textwrap.dedent(
            f"""
            <div class="toolbar">
                <div class="tool-group">
                    <span class="tool-button active">Đọc</span>
                    <span class="tool-button">Bút</span>
                    <span class="tool-button">Highlight</span>
                    <span class="tool-button">...</span>
                </div>
                <div class="tool-group" style="justify-content:center;">
                    <span class="tool-button active">Trang {page} · 1 note</span>
                    <span class="tool-button">-</span>
                    <span class="tool-button">{st.session_state.zoom}%</span>
                    <span class="tool-button">+</span>
                </div>
                <div class="tool-group" style="justify-content:flex-end;">
                    <span class="tool-button">+</span>
                    <span class="tool-button">Tải</span>
                    <span class="tool-button">Hoàn tác</span>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

    nav_cols = st.columns([1, 1, 6, 1, 1])
    with nav_cols[0]:
        if st.button("<", use_container_width=True, disabled=page <= 1, key="prev_top"):
            move_page(-1)
            st.rerun()
    with nav_cols[1]:
        if st.button(">", use_container_width=True, disabled=page >= total_pages, key="next_top"):
            move_page(1)
            st.rerun()
    with nav_cols[3]:
        if st.button("- Zoom", use_container_width=True, key="zoom_out"):
            st.session_state.zoom = max(80, st.session_state.zoom - 10)
            st.rerun()
    with nav_cols[4]:
        if st.button("+ Zoom", use_container_width=True, key="zoom_in"):
            st.session_state.zoom = min(130, st.session_state.zoom + 10)
            st.rerun()


def render_highlight_panel(material: dict[str, Any]) -> None:
    if not st.session_state.highlight_mode:
        return

    page = st.session_state.page
    text = st.session_state.selected_passage.strip()
    if not text:
        message = st.session_state.get("highlight_error") or (
            "Trang này không có text trích xuất được. Bấm Highlight lại để OCR bằng OpenAI hoặc dán nội dung vào ô tutor."
        )
        st.info(message)
        return

    widget_key = f"highlight_text_{st.session_state.material_id}_{page}"
    if st.session_state.get(widget_key) != text:
        st.session_state[widget_key] = text

    edited = st.text_area(
        "Text trên trang để highlight/copy",
        height=150,
        key=widget_key,
    )
    st.session_state.selected_passage = edited


def render_slide_stage(material: dict[str, Any]) -> None:
    page = st.session_state.page
    total_pages = material_page_count(material)
    scale = st.session_state.zoom / 100
    is_pdf = bool(material.get("pdf_path") and fitz is not None)

    if is_pdf:
        render_pdf_document(material)
    else:
        current = slide_by_page(material, page)
        next_slide = slide_by_page(material, page + 1) if page < total_pages else None

        content = textwrap.dedent(
            f"""
            <div class="stage" style="font-size:{scale:.2f}rem;">
                {render_slide(current, material)}
                {render_slide(next_slide, material, preview=True) if next_slide else ""}
            </div>
            """
        ).strip()
        st.markdown(content, unsafe_allow_html=True)

    note_key = f"{st.session_state.material_id}:{page}"
    notes = st.session_state.notes
    notes[note_key] = st.text_area(
        "Note riêng của trang",
        value=notes.get(note_key, ""),
        placeholder="Kéo đến trang này để mở note riêng của trang.",
        height=88,
        key=f"note_{note_key}",
    )

    if is_pdf:
        return

    bottom = st.columns([1, 3, 1])
    with bottom[0]:
        if st.button("< Trang trước", use_container_width=True, disabled=page <= 1, key="prev_bottom"):
            move_page(-1)
            st.rerun()
    with bottom[1]:
        st.markdown(
            f"<p style='text-align:center;color:#60708a;font-weight:800;'>Trang {page} / {total_pages}</p>",
            unsafe_allow_html=True,
        )
    with bottom[2]:
        if st.button("Trang sau >", use_container_width=True, disabled=page >= total_pages, key="next_bottom"):
            move_page(1)
            st.rerun()


def render_quiz_widget() -> None:
    quiz = st.session_state.get("quiz_session")
    if not quiz:
        return
    if quiz.get("material_id") != st.session_state.material_id or int(quiz.get("page", 0)) != st.session_state.page:
        return

    index = int(quiz.get("index", 0))
    questions = quiz.get("questions", [])
    if index >= len(questions):
        st.session_state.quiz_session = None
        return

    item = questions[index]
    with st.chat_message("assistant"):
        st.markdown(f"**Câu {index + 1}/{len(questions)}.** {item['question']}")
        for key in ["A", "B", "C", "D"]:
            label = item["options"][key]
            if st.button(
                f"{key}. {label}",
                key=f"quiz_{quiz['id']}_{index}_{key}",
                use_container_width=True,
            ):
                answer_quiz(key)
                st.rerun()


def render_chat_panel(material: dict[str, Any], slide: dict[str, Any]) -> None:
    api_ready, llm_label, model = llm_status()
    st.markdown(
        textwrap.dedent(
            """
            <div class="panel-title">
                <div class="panel-icon">AI</div>
                <div>
                    <h2>VLearn Tutor</h2>
                    <p>Trợ lý học theo ngữ cảnh</p>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )
    st.markdown(
        textwrap.dedent(
            f"""
            <div class="chat-context">
                <strong>Ngữ cảnh: Slide trang {slide.get("page")}</strong>
                {html.escape(slide.get("title", ""))}<br>
                {f"{llm_label} API đã sẵn sàng. Model: {html.escape(model)}." if api_ready else "Chế độ demo: thêm API key để gọi LLM thật."}
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

    st.text_area(
        "Ngữ cảnh chọn",
        key="selected_passage",
        placeholder="Dán nội dung bạn muốn hỏi để tutor giải thích đúng ngữ cảnh...",
        height=92,
        label_visibility="collapsed",
    )

    quick_cols = st.columns(3)
    with quick_cols[0]:
        if st.button("Tóm tắt", use_container_width=True):
            ask_tutor("Tóm tắt trang này trong 3 ý.")
            st.rerun()
    with quick_cols[1]:
        if st.button("Kiểm tra", use_container_width=True):
            with st.spinner("Đang tạo câu hỏi kiểm tra..."):
                start_quiz(material, slide)
            st.rerun()
    with quick_cols[2]:
        if st.button("Giải thích", use_container_width=True):
            ask_tutor("Giải thích nội dung đã chọn bằng ví dụ dễ hiểu.")
            st.rerun()

    with st.container():
        if not st.session_state.chat_history:
            st.markdown(
                textwrap.dedent(
                    """
                    <div class="assistant-empty">
                        Xin chào! Mình là VLearn Tutor. Bạn có thể chọn nội dung trên slide,
                        dán vào ô ngữ cảnh, rồi hỏi hoặc gửi câu hỏi tự do.
                    </div>
                    """
                ).strip(),
                unsafe_allow_html=True,
            )
        for msg in st.session_state.chat_history:
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                st.markdown(msg["content"], unsafe_allow_html=bool(msg.get("html")))
        render_quiz_widget()

    with st.form("chat_form", clear_on_submit=True):
        chat_cols = st.columns([5, 1])
        with chat_cols[0]:
            question = st.text_input(
                "Nhập câu hỏi",
                label_visibility="collapsed",
                placeholder="Nhập câu hỏi về tài liệu...",
            )
        with chat_cols[1]:
            submitted = st.form_submit_button("Gửi", use_container_width=True)
    if submitted:
        if is_quiz_request(question):
            st.session_state.chat_history.append({"role": "user", "content": question.strip()})
            with st.spinner("Đang tạo câu hỏi kiểm tra..."):
                start_quiz(material, slide)
        else:
            ask_tutor(question)
        st.rerun()


ensure_state()
_deck, material = current_deck_material()
current_slide = slide_by_page(material, st.session_state.page)

render_css()
render_topbar(material)

left, middle, right = st.columns([1.18, 3.32, 1.6], gap="medium")
with left:
    render_left_panel()
with middle:
    render_toolbar(material)
    render_highlight_panel(material)
    render_slide_stage(material)
with right:
    render_chat_panel(material, current_slide)
