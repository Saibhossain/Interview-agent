from services.cv_parser import clean_cv_text, truncate_cv_text


def test_clean_cv_text():
    raw = "Line 1\n\n  Line 2  \n"
    cleaned = clean_cv_text(raw)
    assert "Line 1" in cleaned
    assert "Line 2" in cleaned


def test_truncate_cv_text():
    text = "a" * 2000
    truncated = truncate_cv_text(text, 1000)
    assert len(truncated) == 1000