from graph.state import InterviewState
from langchain_core.messages import AIMessage

def generate_report_node(state: InterviewState):
    reports = state.get("evaluation_report", [])
    report_text = "\n".join([f"- **{r['topic']}**: {r['score']}/10. {r['feedback']}" for r in reports])
    final_message = "That concludes our interview! Thank you for your time.\n\n### 📝 Interviewer Private Report\n" + report_text
    return {"messages": [AIMessage(content=final_message)]}