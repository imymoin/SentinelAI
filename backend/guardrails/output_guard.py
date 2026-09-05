import re

SENSITIVE_PATTERNS = [
    r"sk-[a-zA-Z0-9_-]+",          # OpenAI-style API key
    r"gsk_[a-zA-Z0-9_-]+",         # Groq API key
    r"password\s*[:=]\s*\S+",
    r"secret\s*[:=]\s*\S+",
]


def validate_output(response: str) -> tuple[bool, str]:
    """
    Validate the final LLM response before sending it to the user.
    """

    if not response or not response.strip():
        return False, "Empty response detected."

    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return False, "Sensitive information detected in output."

    return True, "Output approved."