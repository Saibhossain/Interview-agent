from graph.state import InterviewState

def manager_node(state: InterviewState):
    plan = state.get("interview_plan", [])
    if not plan:
        return {"current_topic": None}
    return {"current_topic": plan[0], "interview_plan": plan[1:], "follow_up_count": 0}