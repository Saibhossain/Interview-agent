from langgraph.graph import StateGraph, END
from graph.state import InterviewState
from graph.memory import get_memory
from graph.routers import (
    route_interview_manager,
    route_analyze_input,
    route_evaluate_answer)
from nodes.parse_cv import parse_cv_node
from nodes.plan_interview import plan_interview_node
from nodes.manager import manager_node
from nodes.ask_question import ask_main_question_node
from nodes.analyze_input import analyze_input_node
from nodes.clarification import handle_clarification_node
from nodes.evaluate import evaluate_answer_node
from nodes.followup import ask_followup_node
from nodes.report import generate_report_node



def build_graph():

    builder = StateGraph(InterviewState)

    builder.add_node("parse_cv", parse_cv_node)
    builder.add_node("plan_interview", plan_interview_node)
    builder.add_node("interview_manager", manager_node)
    builder.add_node("ask_main_question", ask_main_question_node)
    builder.add_node("analyze_input", analyze_input_node)
    builder.add_node("handle_clarification", handle_clarification_node)
    builder.add_node("evaluate_answer", evaluate_answer_node)
    builder.add_node("ask_followup", ask_followup_node)
    builder.add_node("generate_report", generate_report_node)


    builder.set_entry_point("parse_cv")
    builder.add_edge("parse_cv", "plan_interview")
    builder.add_edge("plan_interview", "interview_manager")

    builder.add_conditional_edges(
        "interview_manager",
        route_interview_manager,
        {
            "next_question": "ask_main_question",
            "end_interview": "generate_report",
        },
    )

    # Keep the behavior close to your original design
    for node in ["ask_main_question", "ask_followup", "handle_clarification"]:
        builder.add_edge(node, "analyze_input")

    builder.add_conditional_edges(
        "analyze_input",
        route_analyze_input,
        {
            "evaluate": "evaluate_answer",
            "clarify": "handle_clarification",
        },
    )

    builder.add_conditional_edges(
        "evaluate_answer",
        route_evaluate_answer,
        {
            "follow_up": "ask_followup",
            "topic_complete": "interview_manager",
        },
    )

    builder.add_edge("generate_report", END)

    memory = get_memory()
    return builder.compile(checkpointer=memory,interrupt_before=["analyze_input"])