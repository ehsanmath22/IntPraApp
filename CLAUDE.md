# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

An interview-preparation Q&A app: the user enters a question or topic and an LLM ("expert interview coach" persona) returns a structured answer with a sample response, key points, and a delivery tip. `main.py` is the deployable Streamlit app; the two notebooks are exploratory variants of the same idea.

## Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency management (`uv.lock` is committed).

```bash
uv sync                      # install dependencies into .venv
uv run streamlit run main.py # run the Streamlit app
uv run jupyter notebook      # open the exploratory notebooks
```

There are no tests, linter, or build step configured.

## Architecture

Three implementations of the same coach, all calling `openai/gpt-4o-mini` through **OpenRouter** (not OpenAI directly — the OpenAI SDK is pointed at `base_url="https://openrouter.ai/api/v1"`):

- `main.py` — Streamlit UI (`st.text_input` → `ask()` → `st.write`), uses the raw `openai` SDK.
- `InterviewApp_with_openai.ipynb` — same raw-SDK `ask()` function, run interactively.
- `InterviewApp_with_langchain.ipynb` — LangChain variant (`ChatPromptTemplate | ChatOpenAI`).

The system prompt defining the "expert interview coach" persona is duplicated across all three files. When changing the coaching behavior, update every copy.

## Configuration

`OPENROUTER_API_KEY` is read from a `.env` file via `python-dotenv` (`load_dotenv()`).

⚠️ **Security note:** `.env` is currently tracked in git and is *not* in `.gitignore`, and it contains a live API key. Before any commit/push, add `.env` to `.gitignore`, remove it from the index (`git rm --cached .env`), and rotate the exposed key.
