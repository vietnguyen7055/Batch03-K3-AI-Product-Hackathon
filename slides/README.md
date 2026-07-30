# Slide deck metadata

The app first loads `slides/decks.json` when it exists. If the file is missing, it auto-detects PDFs from `../Slide-AIThucChien/Day01.pdf` through `Day05.pdf`. If neither source is available, `app.py` falls back to the built-in demo deck.

Minimal schema:

```json
{
  "days": [
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
              "key_points": [
                "Một ý chính trên slide.",
                "Một ý chính khác để tutor dùng làm context."
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

Set `DEEPSEEK_API_KEY` in `.env` to enable the live tutor. Optional overrides: `DEEPSEEK_MODEL` and `DEEPSEEK_BASE_URL`.
