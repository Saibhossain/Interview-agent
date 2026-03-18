from graph.state import InterviewState
from config.llm_config import get_llm
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from prompts.interview_prompts import FOLLOWUP_PROMPT


def ask_followup_node(state: InterviewState):
    llm = get_llm()
    answer = state["messages"][-1].content
    prompt = ChatPromptTemplate.from_template(FOLLOWUP_PROMPT)
    response = (prompt | llm).invoke({"answer": answer})
    return {"messages": [AIMessage(content=response.content)], "follow_up_count": state.get("follow_up_count", 0) + 1}