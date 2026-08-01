# Validation Feedback Log

Use one row per tester/session. Keep quotes short and anonymized.

| Tester | Role / willing user? | Task | Observation | Short quote | Severity | Follow-up |
|---|---|---|---|---|---|---|
| Phạm Quốc Bảo | Student / yes | Ask tutor to explain one slide | Tutor explained the concept correctly based on the current slide and provided a concise summary. | "Giải thích dễ hiểu và đúng nội dung slide." | Low | Keep explanation concise and add highlighted keywords. |
| Nguyễn Dương | Student / yes | Ask ambiguous question | When asked "Ý này là gì?", the tutor requested more context instead of guessing the answer. | "Bot hỏi lại mình đang nói đến phần nào." | Low | Improve automatic use of the current page as default context. |
| Phạm Quốc Bảo | Student / yes | Ask out-of-scope question | When asked about the course deadline, the tutor refused to guess and suggested checking the LMS or instructor announcement. | "Bot không bịa deadline, điều này khá yên tâm." | Low | Add direct links to LMS/course resources if available. |

## Summary

- **Most repeated theme:**
  Users were satisfied when the tutor answered based only on the current slide, but expected it to better understand short or ambiguous questions.

- **Changes to make before demo:**
  - Improve handling of short questions by leveraging the current slide context.
  - Highlight important keywords in explanations.
  - Improve support for image-only slides with OCR/VLM.

- **Kept unchanged with reason:**
  The tutor only answers using the uploaded learning material and refuses unsupported or out-of-scope questions. This reduces hallucination and increases trustworthiness.

- **Backlog after demo:**
  - Multi-slide summarization.
  - Automatic flashcard generation.
  - Conversation memory across pages.
  - Better citation and page highlighting in responses.
