import re


def extract_links(text: str):
    if not text:
        return []
    pattern = r"(https?://[^\s]+|www\.[^\s]+|github\.com/[^\s]+|linkedin\.com/[^\s]+)"
    return re.findall(pattern, text)