import re


EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


def contains_email(text: str) -> bool:
    """Return whether text contains an email address."""
    return bool(EMAIL_PATTERN.search(text))
