from graph.state import InterviewState
from config.llm_config import get_llm
from graph.state import IntentAnalysis
from langchain_core.prompts import ChatPromptTemplate

def analyze_input_node(state: InterviewState):
    llm = get_llm()
    last_message = state["messages"][-1].content
    prompt = ChatPromptTemplate.from_template("Message: '{message}'\nIs the candidate answering, or asking for clarification/help?")
    result = (prompt | llm.with_structured_output(IntentAnalysis)).invoke({"message": last_message})
    return {"current_intent": result.intent}