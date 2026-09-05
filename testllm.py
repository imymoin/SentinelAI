import os

from dotenv import load_dotenv
from litellm import completion

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("API key loaded:", bool(api_key))

response = completion(
    model="groq/openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence."
        }
    ],
    api_key=api_key,
)

print("\nLLM Response:")
print(response.choices[0].message.content)