import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

SUPPORTED_MODELS = [
    "distil-whisper-large-v3-en",
    "gemma2-9b-it",
    "gemma-7b-it",
    "llama3-groq-70b-8192-tool-use-preview",
    "llama3-groq-8b-8192-tool-use-preview",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-90b-vision-preview",
    "llama-guard-3-8b",
    "llava-v1.5-7b-4096-preview",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "whisper-large-v3",
]


def get_groq_completion(messages: list[dict[str, str]], model: str) -> str:
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    if chat_completion.choices[0].message.content is None:
        raise ValueError("No content in response")

    return chat_completion.choices[0].message.content


def groq_query(system_query: str, model: str):
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Model {model} not supported")

    def query(prompt: str):
        messages = [
            {"role": "system", "content": system_query},
            {"role": "user", "content": prompt},
        ]
        return get_groq_completion(messages, model)

    return query
