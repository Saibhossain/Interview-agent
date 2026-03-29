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

OLLAMA_gemma1b="gemma3:1b"
OLLAMA_R11_5b="deepseek-r1:1.5b"
OLLAMA_qwen3b="qwen2.5:3b"