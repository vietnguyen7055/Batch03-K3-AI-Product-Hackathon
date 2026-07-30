# Eval artifacts

This folder stores the golden set and run results required by the hackathon README.

Files:

- `golden_set.json` - official 67-case test set for the VLearn Tutor prototype.
- `golden_set_day01.json` - original generated Day01 slide-grounding cases kept as trace/source material.
- `results_run_01.csv` - first baseline run, including passing and failing cases.
- `coverage_summary.md` - short answers for checkpoint questions 2-6.

Quality bar:

> Pass when at least 80% of cases pass, and the tutor never invents unsupported information from outside the document.

Current first-run baseline:

> 52/67

Notes:

- Some cases are predicted/manual baseline results until the full DeepSeek batch runner is connected.
- Cases adapted from real logs use source IDs or short descriptions instead of copying long private data.
