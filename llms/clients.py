from llms.client_openai import openai_query
from llms.client_groq import groq_query
from llms.client_groq import SUPPORTED_MODELS


def get_client(client_type: str, system_query: str):
    if client_type == "gpt-4o":
        return openai_query(system_query)
    else:
        if client_type in SUPPORTED_MODELS:
            return groq_query(system_query, client_type)
        raise ValueError(f"Client type {client_type} not supported")
