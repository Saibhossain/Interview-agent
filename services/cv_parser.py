def clean_cv_text(text: str) -> str:
    if not text:
        return ""
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def truncate_cv_text(text: str, limit: int = 1000) -> str:
    return text[:limit]