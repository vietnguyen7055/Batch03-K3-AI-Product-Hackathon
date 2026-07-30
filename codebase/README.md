# VLearn Tutor Prototype

Streamlit prototype for a VLearn-like study interface:

- left panel: uploaded lecture materials grouped by day
- middle panel: PDF slide viewer with page navigation
- right panel: contextual tutor backed by DeepSeek when `DEEPSEEK_API_KEY` is set

## Run locally

```powershell
cd codebase
.\.venv\Scripts\streamlit.exe run app.py
```

Open:

```text
http://localhost:8501
```

## Configuration

Create `codebase/.env`:

```env
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## Real vs mock

Real:

- PDF detection from `../Slide-AIThucChien`
- PDF rendering through PyMuPDF
- page context extraction when the PDF contains real text
- DeepSeek chat call when the API key is present

Mock / partial:

- course membership and publishing workflow
- note persistence beyond Streamlit session state
- OCR for image-only PDF slides
- automated batch eval runner
