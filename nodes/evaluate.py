

def evaluate_answer_node(state: InterviewState):
    llm = get_llm()
    question = [m.content for m in state["messages"] if isinstance(m, AIMessage)][-1]
    answer = state["messages"][-1].content
    prompt = ChatPromptTemplate.from_template(
        "Topic: {topic}\nQuestion: {question}\nAnswer: {answer}\nScore out of 10. Does it need a follow-up (too brief/missed edge cases)?"
    )
    result = (prompt | llm.with_structured_output(EvaluationResult)).invoke({
        "topic": state["current_topic"], "question": question, "answer": answer
    })
    report_entry = {"topic": state["current_topic"], "score": result.score, "feedback": result.feedback}
    return {"needs_follow_up": result.needs_follow_up, "evaluation_report": [report_entry]}