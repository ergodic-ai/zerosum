from typing import List
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from typing import Optional

from openai.types.chat import ChatCompletionMessageParam

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("OPENAI_API_VERSION")
azure_endpoint = os.getenv("OPENAI_AZURE_ENDPOINT")

if not api_key:
    raise ValueError("API key not found in the environment variables")

if not api_version:
    raise ValueError("API version not found in the environment variables")

if not azure_endpoint:
    raise ValueError("Azure endpoint not found in the environment variables")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint,
)

deployment_name = os.getenv("DEPLOYMENT_NAME")

if not deployment_name:
    raise ValueError("Deployment name not found in the environment variables")


def get_openai_response(
    messages: List[dict[str, str]] | List[ChatCompletionMessageParam],
    temperature=0,
    model=deployment_name,
) -> str:
    """Get a response from OpenAI GPT4. The response can be in JSON or plain text.
    variables:
        query: str: The user query
        system_message: str: The system message to be passed to the model
        response_mode: str: The response mode. Can be "json" or "text"

    output:
        The response from OpenAI GPT4
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


def openai_query(system_query: str):
    def query(prompt: str):
        messages = [
            {"role": "system", "content": system_query},
            {"role": "user", "content": prompt},
        ]

        return get_openai_response(messages)

    return query


def main():
    query = openai_query(
        "You are a helpful assistant that can answer questions and help with tasks. Return your response in JSON format."
    )
    print(query("What is the capital of the moon?"))


if __name__ == "__main__":
    main()
