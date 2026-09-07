from app.llm.gemini_client import GeminiClient


client = GeminiClient()

response = client.generate(
    "What is 15 + 27? Answer with only the number."
)

print(response["text"])