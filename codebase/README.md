# VLearn Tutor Prototype

Streamlit prototype for a VLearn-like study interface:

- left panel: uploaded lecture materials grouped by day
- middle panel: PDF slide viewer with page navigation
- right panel: contextual tutor backed by OpenAI or DeepSeek when an API key is set

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
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4.1-mini
OPENAI_DEFAULT_MODEL=gpt-4.1-mini
```

## Real vs mock

Real:

- PDF detection from `../Slide-AIThucChien`
- PDF rendering through PyMuPDF
- page context extraction when the PDF contains real text
- OpenAI/DeepSeek chat call when the matching API key is present

Mock / partial:

- course membership and publishing workflow
- note persistence beyond Streamlit session state
- OCR for image-only PDF slides
- automated batch eval runner
