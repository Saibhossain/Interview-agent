from graph.state import InterviewState
from services.pdf_loader import load_pdf_text
from services.cv_parser import clean_cv_text



def parse_cv_node(state: InterviewState):
    try:
        cv_text = load_pdf_text(state["pdf_path"])
        cv_text = clean_cv_text(cv_text)
        return {"cv_text": cv_text}
    except Exception:
        return {"cv_text": "Error reading CV. Ask general software engineering questions."}
