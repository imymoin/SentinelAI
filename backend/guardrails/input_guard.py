BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "reveal your instructions",
    "show me your system prompt",
    "bypass security",
]


def validate_input(user_input: str) -> tuple[bool, str]:

    text = user_input.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in text:
            return (
                False,
                "Request blocked by SentinelAI security policy."
            )

    return True, "Input approved."