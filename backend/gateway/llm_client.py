from litellm import completion


def create_completion(**kwargs):
    """Proxy LLM calls through a single backend gateway module."""
    return completion(**kwargs)
