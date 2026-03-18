

def handle_clarification_node(state: InterviewState):
    llm = get_llm()
    ai_msg = state["messages"][-2].content
    human_msg = state["messages"][-1].content
    prompt = ChatPromptTemplate.from_template("You asked: '{ai_msg}'\nCandidate asked: '{human_msg}'\nProvide a helpful, brief clarification.")
    response = (prompt | llm).invoke({"ai_msg": ai_msg, "human_msg": human_msg})
    return {"messages": [AIMessage(content=response.content)]}