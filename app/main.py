# from app.llm.anthropic_client import ClaudeClient
# from app.llm.metrics import Metrics
# from app.utils.logger import log_result

# client = ClaudeClient()
# metrics = Metrics()

# prompt = "Summarize the importance of renewable energy in 100 words."

# metrics.start_timer()

# response = client.generate(prompt)

# latency = metrics.stop_timer()

# print(response)

# print(f"\nLatency: {latency:.2f} seconds")

# log_result(
#     {
#         "Prompt": prompt,
#         "Latency": latency,
#         "Response": response
#     }
# )

# print("\nSaved to CSV.")


from app.pipeline.baseline import BaselinePipeline
from app.utils.logger import log_result

pipeline = BaselinePipeline()

result = pipeline.run(
    "Explain Newton's Second Law in simple words."
)

print(result["response"])

print()

print(result)

log_result(result)