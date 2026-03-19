from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from config.settings import DEFAULT_MODEL
from config.settings import OLLAMA_MODEL


# def get_llm():
#     # This ensures the LLM is only initialized after the user provides the API key in the UI
#     return init_chat_model(DEFAULT_MODEL)


def get_llm():
    "use locally ollama model gemma3:1b, deepseek-r1:1.5b"

    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.2,
    )