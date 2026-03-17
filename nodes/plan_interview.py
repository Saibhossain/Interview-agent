from graph.state import InterviewState
from graph.state import InterviewPlan
from config.llm_config import get_llm

from langchain_core.prompts import ChatPromptTemplate

def plan_interview_node(state: InterviewState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("Identify 3 to 4 core competencies to test based on this CV:\n{cv_text}")
    chain = prompt | llm.with_structured_output(InterviewPlan)
    result = chain.invoke({"cv_text": state["cv_text"]})
    return {"interview_plan": result.topics}