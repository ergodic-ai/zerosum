from llms.client_openai import openai_query


def get_client(client_type: str, system_query: str):
    if client_type == "gpt-4o":
        return openai_query(system_query)
    else:
        raise ValueError(f"Client type {client_type} not supported")
