from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

def test_ollama_connection(model_name: str = "gemma3:1b"):
    print(f"\n🧪 Testing local Ollama connection using model: '{model_name}'...")

    try:
        # Initialize the local LLM
        llm = ChatOllama(
            model=model_name,
            temperature=0,
        )
        print("⏳ Waiting for response...")
        response = llm.invoke([HumanMessage(content="Respond with exactly one word: 'Success'.")])

        print(f"✅ PASSED! Ollama replied: {response.content.strip()}")

    except ConnectionError:
        print("❌ FAILED: Connection refused. Is the Ollama app running in the background?")
    except Exception as e:
        print(
            f"❌ FAILED: An error occurred.\nMake sure you have pulled the model using `ollama pull {model_name}`\nError Details: {e}")


if __name__ == "__main__":
    # Change "llama3.2" to whatever model you downloaded
    test_ollama_connection("gemma3:1b")
