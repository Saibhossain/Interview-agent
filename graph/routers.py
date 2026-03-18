
def route_interview_manager(state):
    return "next_question" if state.get("current_topic") else "end_interview"


def route_analyze_input(state):
    return state.get("current_intent")


def route_evaluate_answer(state):
    if state.get("needs_follow_up") and state.get("follow_up_count", 0) < 1:
        return "follow_up"
    return "topic_complete"