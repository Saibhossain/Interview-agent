


def ask_main_question_node(state: InterviewState):
    llm = get_llm()
    topic = state.get("current_topic")
    prompt = ChatPromptTemplate.from_template(
        "CV context: {cv_text}\nCurrent topic: {topic}.\nAsk ONE engaging, open-ended interview question about this topic. No pleasantries."
    )
    response = (prompt | llm).invoke({"cv_text": state["cv_text"][:1000], "topic": topic})
    return {"messages": [AIMessage(content=response.content)]}