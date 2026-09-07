from app.llm.anthropic_client import ClaudeClient


client = ClaudeClient()

result = client.generate(
    "What is 2 + 2?"
)

print("Model:", result["model"])
print("Response:", result["text"])
print("Input tokens:", result["input_tokens"])
print("Output tokens:", result["output_tokens"])