from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from sympy.physics.units import temperature

from config.settings import DEFAULT_MODEL
from config.settings import OLLAMA_gemma1b,OLLAMA_R11_5b,OLLAMA_qwen3b


# def get_llm():
#     # This ensures the LLM is only initialized after the user provides the API key in the UI
#     return init_chat_model(DEFAULT_MODEL)


# def get_llm():
#     "use locally ollama model gemma3:1b, deepseek-r1:1.5b"
#
#     return ChatOllama(
#         model=OLLAMA_gemma1b,
#         temperature=0.2,
#     )

def get_llm(task: str ="default"):

    if task in ["intent","clarify","followup"]:
        model = OLLAMA_gemma1b
    elif task in ["plan","evaluate","question"]:
        model = OLLAMA_qwen3b
    else:
        model = OLLAMA_R11_5b

    return ChatOllama(
        model = model,
        temperature=0.2,
    )