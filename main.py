import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Instantiate the client, pointing it at OpenRouter.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_retries=2,
)

DEFAULT_SYSTEM_PROMPT = (
    "You are an expert interview coach. When given a question or topic, "
    "provide a clear, structured, and practical answer to help the user "
    "prepare for job interviews. Include a strong sample answer where "
    "appropriate, key points to hit, and a short tip on delivery. "
    "Keep it focused and easy to read."
)

st.title('Type Your Question or Topic for Interview Preparation ...')

st.sidebar.header("Model settings")

model = st.sidebar.text_input(
    "Model",
    value="openai/gpt-4o-mini",
    help="Any model slug supported by OpenRouter (e.g. openai/gpt-4o, anthropic/claude-sonnet-5).",
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.0,
    step=0.1,
    help="Higher values make output more random; lower values make it more focused and deterministic.",
)

limit_tokens = st.sidebar.checkbox(
    "Limit max tokens",
    value=False,
    help="When off, the model uses its default maximum output length.",
)
max_tokens = st.sidebar.slider(
    "Max tokens",
    min_value=1,
    max_value=8192,
    value=1024,
    step=1,
    disabled=not limit_tokens,
    help="Maximum number of tokens to generate in the response.",
)

system_prompt = st.sidebar.text_area(
    "System prompt",
    value=DEFAULT_SYSTEM_PROMPT,
    height=200,
    help="Instructions that define how the assistant behaves.",
)

# Security guard: cap input length to prevent abuse (runaway token cost /
# oversized payloads). OpenRouter still enforces its own limits, but rejecting
# here avoids sending the request at all.
MAX_INPUT_CHARS = 2000

input_text = st.text_input(
    "Enter your Question or Topic here",
    max_chars=MAX_INPUT_CHARS,
)

def ask(
    question: str,
    system_prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
) -> str:
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question:{question}"},
        ],
    )
    return completion.choices[0].message.content

if input_text:
    question = input_text.strip()
    if not question:
        st.warning("Please enter a question or topic.")
    elif len(question) > MAX_INPUT_CHARS:
        st.error(
            f"Input too long ({len(question)} characters). "
            f"Please keep it under {MAX_INPUT_CHARS} characters."
        )
    else:
        st.write(
            ask(
                question,
                system_prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens if limit_tokens else None,
            )
        )

# To run this code, write-  streamlit run gemini_app_qa.py

