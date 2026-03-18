from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from config.llm_config import get_llm
from graph.state import InterviewState
from prompts.interview_prompts import CLARIFICATION_PROMPT


def handle_clarification_node(state: InterviewState):
    llm = get_llm()
    ai_msg = state["messages"][-2].content
    human_msg = state["messages"][-1].content
    prompt = ChatPromptTemplate.from_template(CLARIFICATION_PROMPT)
    response = (prompt | llm).invoke({"ai_msg": ai_msg, "human_msg": human_msg})
    return {"messages": [AIMessage(content=response.content)]}