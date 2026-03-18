from graph.state import InterviewState
from graph.state import InterviewPlan
from config.llm_config import get_llm
from prompts.planner_prompts import PLAN_INTERVIEW_PROMPT
from langchain_core.prompts import ChatPromptTemplate

def plan_interview_node(state: InterviewState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(PLAN_INTERVIEW_PROMPT)
    chain = prompt | llm.with_structured_output(InterviewPlan)
    result = chain.invoke({"cv_text": state["cv_text"]})
    return {"interview_plan": result.topics}