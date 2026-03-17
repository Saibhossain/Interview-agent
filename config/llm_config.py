from langchain.chat_models import init_chat_model

def get_llm():
    # This ensures the LLM is only initialized after the user provides the API key in the UI
    return init_chat_model("google_genai:gemini-2.5-flash-lite")