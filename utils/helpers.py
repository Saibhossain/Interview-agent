import os
import uuid


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def generate_thread_id() -> str:
    return str(uuid.uuid4())