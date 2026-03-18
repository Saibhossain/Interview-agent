from langchain.chat_models import init_chat_model
from config.settings import DEFAULT_MODEL

def get_llm():
    # This ensures the LLM is only initialized after the user provides the API key in the UI
    return init_chat_model(DEFAULT_MODEL)