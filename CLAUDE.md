# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the project

```bash
python main.py          # entry point (hello world stub)
streamlit run app.py    # Streamlit feedback app
pytest test_app.py      # run tests
pytest test_app.py -k "test_name"  # run a single test
```

## Environment

- Python via Anaconda (`anaconda32025`)
- Jupyter notebooks used for experimentation
- Google Gemini API accessed via `google-genai` SDK; key stored in `GEMINI_API_KEY` environment variable

## Architecture

The project currently has two independent components:

- **`app.py`** — Streamlit feedback form. `save_feedback(feedback: str) -> bool` is the core logic: strips, validates, and appends to `feedback.txt`. The Streamlit UI calls this function.
- **`main.py`** — Standalone entry point, currently a placeholder.
- **`test_app.py`** — pytest tests covering `save_feedback`. Tests use `tmp_path` + `monkeypatch.chdir` to isolate file writes.
