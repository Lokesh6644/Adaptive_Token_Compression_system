import time
from google import genai
# pyrefly: ignore [missing-import]
from google.genai.errors import APIError

from app.utils.config import GEMINI_API_KEY


class GeminiClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        prompt: str,
        model="gemini-3.6-flash",
        max_tokens=512,
        max_retries=3
    ):
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                usage = response.usage_metadata

                return {
                    "model": model,
                    "text": response.text,
                    "input_tokens": usage.prompt_token_count,
                    "output_tokens": usage.candidates_token_count,
                }
            except APIError as e:
                err_str = str(e)
                if "PerDay" in err_str or attempt == max_retries - 1:
                    print(f"\n[Gemini Quota Exhausted] Falling back to ClaudeClient (Haiku)...")
                    from app.llm.anthropic_client import ClaudeClient
                    return ClaudeClient().generate(prompt, max_tokens=max_tokens)
                elif (e.code == 429 or "RESOURCE_EXHAUSTED" in err_str):
                    wait_time = 14 * (attempt + 1)
                    print(f"\n[Gemini Rate Limit] 429 Quota reached. Backing off for {wait_time}s before retrying (attempt {attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    raise