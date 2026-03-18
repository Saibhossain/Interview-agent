from pydantic import BaseModel, Field
from typing import TypedDict, List, Annotated, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator


class InterviewPlan(BaseModel):
    topics: List[str] = Field(description="3-5 specific technical or behavioral topics to cover.")

class IntentAnalysis(BaseModel):
    intent: Literal["evaluate", "clarify"] = Field(description="Return 'clarify' if asking a question, 'evaluate' if answering.")

class EvaluationResult(BaseModel):
    score: int
    feedback: str
    needs_follow_up: bool

class InterviewState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    pdf_path: str
    cv_text: str
    interview_plan: List[str]
    current_topic: str
    follow_up_count: int
    current_intent: str
    needs_follow_up: bool
    evaluation_report: Annotated[List[dict], operator.add]