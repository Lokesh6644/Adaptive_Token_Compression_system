from anthropic import Anthropic
from app.utils.config import ANTHROPIC_API_KEY


class ClaudeClient:

    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

    def generate(
        self,
        prompt: str,
        model="claude-haiku-4-5-20251001",
        max_tokens=512
    ):

        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response