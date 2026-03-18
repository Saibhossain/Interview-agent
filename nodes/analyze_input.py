from langchain_core.prompts import ChatPromptTemplate

from config.llm_config import get_llm
from graph.state import InterviewState, IntentAnalysis
from prompts.interview_prompts import ANALYZE_INPUT_PROMPT

def analyze_input_node(state: InterviewState):
    llm = get_llm()
    last_message = state["messages"][-1].content
    prompt = ChatPromptTemplate.from_template(ANALYZE_INPUT_PROMPT)
    result = (prompt | llm.with_structured_output(IntentAnalysis)).invoke({"message": last_message})
    return {"current_intent": result.intent}