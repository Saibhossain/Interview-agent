import os

APP_TITLE = "AI Technical Interviewer"
APP_ICON = "🎙️"
LAYOUT = "wide"

TEMP_DIR = "temp"
DATA_DIR = "data"
OUTPUT_DIR = os.path.join(DATA_DIR, "outputs")
SAMPLE_CV_DIR = os.path.join(DATA_DIR, "sample_cv")

DEFAULT_MODEL = "google_genai:gemini-2.5-flash-lite"
CV_CONTEXT_LIMIT = 1000
MAX_FOLLOWUPS = 1

OLLAMA_MODEL="gemma3:1b"