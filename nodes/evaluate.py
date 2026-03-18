from graph.state import InterviewState, EvaluationResult
from config.llm_config import get_llm
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from prompts.evaluation_prompts import EVALUATE_ANSWER_PROMPT

def evaluate_answer_node(state: InterviewState):
    llm = get_llm()
    question = [m.content for m in state["messages"] if isinstance(m, AIMessage)][-1]
    answer = state["messages"][-1].content
    prompt = ChatPromptTemplate.from_template(EVALUATE_ANSWER_PROMPT)
    result = (prompt | llm.with_structured_output(EvaluationResult)).invoke({
        "topic": state["current_topic"], "question": question, "answer": answer
    })
    report_entry = {"topic": state["current_topic"], "score": result.score, "feedback": result.feedback}
    return {"needs_follow_up": result.needs_follow_up, "evaluation_report": [report_entry]}