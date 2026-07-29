# Interview Prep Assistant

A Streamlit chat app that acts as an **expert interview coach**. Ask it interview
questions or topics and it replies with a structured answer: a strong sample
response, the key points to hit, and a short delivery tip. You can hold a running
conversation and ask follow-ups.

Under the hood it calls `openai/gpt-4o-mini` (configurable) through
[OpenRouter](https://openrouter.ai/) using the OpenAI Python SDK.

## Features

- **Multi-turn chat** — ask several questions in a row; the assistant remembers
  the conversation, so follow-ups like "make that answer shorter" work.
- **Tunable model settings** in the sidebar: model, temperature, and max tokens.
- **Editable system prompt** — change how the coach behaves on the fly.
- **Input length guard** — messages are capped to protect against oversized
  requests and runaway token cost.
- **Clear conversation** button to start fresh.

## Requirements

- Python 3.13+
- An [OpenRouter](https://openrouter.ai/) API key
- [uv](https://docs.astral.sh/uv/) (recommended) for dependency management

## Setup

1. **Install dependencies** (creates a local `.venv`):

   ```bash
   uv sync
   ```

2. **Add your API key.** Create a `.env` file in the project root:

   ```
   OPENROUTER_API_KEY=your-openrouter-key-here
   ```

   > `.env` is gitignored — never commit your key.

## Running the app

```bash
uv run streamlit run main.py
```

Streamlit opens the app in your browser (usually at http://localhost:8501).

## Using the app

1. Type a question or topic into the chat box at the bottom
   (e.g. *"How do I answer 'What's your greatest weakness?'"*) and press Enter.
2. Read the coach's structured answer, then ask follow-ups in the same chat.
3. Adjust behavior anytime from the **sidebar**:

   | Setting | What it does |
   | --- | --- |
   | **Model** | Any OpenRouter model slug (e.g. `openai/gpt-4o`, `anthropic/claude-sonnet-5`). |
   | **Temperature** | `0.0` = focused and consistent, higher = more creative/varied (up to `2.0`). |
   | **Limit max tokens** | When off, the model uses its default max length. Turn on to cap response length with the slider. |
   | **System prompt** | The instructions that define the coach's persona and style. |
   | **Clear conversation** | Wipes the chat history and starts over. |

## Notes

- The full conversation is sent to the model on each turn, so very long chats
  gradually cost more tokens. Use **Clear conversation** to reset.
- Changing the model or system prompt affects the **next** message; earlier
  replies in the chat stay as they were.
