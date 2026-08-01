# Reflection - 2A202602012 - Phùng Văn Đạt

## My owned part

I was responsible for defining the product specification, setting the quality bar, designing the prompt and evaluation strategy, and creating the golden test cases. I also helped analyze the VLearn chat history to identify common user pain points and translated those findings into evaluation scenarios for the tutor.

## What changed because of evidence or testing

After reviewing the chat history and conducting validation, we found that many students asked short or ambiguous questions such as "ý này là gì?" or requested information outside the current slide. Based on these findings, we updated the prompt so the tutor first checks whether enough context is available, asks for clarification when necessary, and refuses to answer questions that are not grounded in the uploaded learning material.

## One technical/product decision I can explain

One important decision was to restrict the tutor to answering only from the current slide or uploaded document instead of using general LLM knowledge. Although this sometimes results in the tutor refusing to answer, it significantly reduces hallucinations and helps students trust the information they receive. We also defined a quality bar requiring at least 80% evaluation success with zero unsupported claims.

## What failed or stayed weak

The prototype still has limitations with image-only PDF slides because OCR is not fully implemented. Very short questions can also require additional clarification before the tutor can provide a useful answer. In addition, the first evaluation baseline achieved 52 out of 67 test cases, showing that prompt refinement is still needed.

## If we had one more week

We would improve OCR and VLM support for scanned slides, optimize prompt handling for ambiguous questions, enhance citation and page highlighting, and expand the evaluation set with more real user conversations. We would also add features such as multi-slide summarization, flashcard generation, and conversation memory across pages.

