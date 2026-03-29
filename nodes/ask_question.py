from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from config.llm_config import get_llm
from config.settings import CV_CONTEXT_LIMIT
from graph.state import InterviewState
from prompts.interview_prompts import ASK_MAIN_QUESTION_PROMPT


def ask_main_question_node(state: InterviewState):
    llm = get_llm("question")
    topic = state.get("current_topic")
    prompt = ChatPromptTemplate.from_template(ASK_MAIN_QUESTION_PROMPT)
    response = (prompt | llm).invoke({"cv_text": state["cv_text"][:CV_CONTEXT_LIMIT], "topic": topic})
    return {"messages": [AIMessage(content=response.content)]}