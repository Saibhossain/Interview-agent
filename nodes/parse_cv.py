from graph.state import InterviewState

from langchain_community.document_loaders import PyPDFLoader

def parse_cv_node(state: InterviewState):
    try:
        loader = PyPDFLoader(state["pdf_path"])
        cv_text = "\n".join([page.page_content for page in loader.load()])
        return {"cv_text": cv_text}
    except Exception:
        return {"cv_text": "Error reading CV. Ask general software engineering questions."}