# Demo Slides - 6 Pages

This markdown file is the source outline for `demo-slides.pdf`.

## 1. User pain

Students read lecture PDFs in VLearn but often ask short or vague questions. A generic chatbot may answer without knowing the current slide.

## 2. Chosen slice

One student, one PDF page, one tutor decision: answer from the current slide context, ask for clarification, or refuse unsupported requests.

## 3. Prototype

The app has a left material list, middle PDF slide viewer, and right contextual tutor. DeepSeek is used when the API key is present.

## 4. Eval result

Golden set: 67 cases. First baseline: 52/67. Quality bar: at least 80%, with zero unsupported hallucination.

## 5. Validation

Run five user-test sessions. Log whether students can navigate, select/copy context, and detect when the tutor refuses unsupported questions.

## 6. One more week

Add OCR for image-only slides, an automated eval runner, better source citations, and persistent notes/highlights.
