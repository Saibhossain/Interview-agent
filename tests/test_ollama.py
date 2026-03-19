from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

def test_ollama_connection(model_name: str = "gemma3:1b"):
    print(f"\n Testing local Ollama connection using model: '{model_name}'...")

    try:
        llm = ChatOllama(
            model=model_name,
            temperature=0,
        )
        print("⏳ Waiting for response...")
        # response = llm.invoke([HumanMessage(content="Respond with exactly one word: 'Success'.")])
        response = llm.stream([HumanMessage(content="Explain the concept of an API in exactly one short sentence.")])

        for chunk in response:
            print(chunk.content, end="",flush=True)


        print(f"\n✅ PASSED! Ollama replied complete ")

    except ConnectionError:
        print("FAILED: Connection refused. Is the Ollama app running in the background?")
    except Exception as e:
        print(
            f"FAILED: An error occurred.\nMake sure you have pulled the model using `ollama pull {model_name}`\nError Details: {e}")


if __name__ == "__main__":
    test_ollama_connection("gemma3:1b")
