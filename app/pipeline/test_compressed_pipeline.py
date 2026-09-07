from app.pipeline.baseline import BaselinePipeline


pipeline = BaselinePipeline(compression_ratio=0.5)

prompt = """
What is the capital of France?
Answer with only the city name.
"""

result = pipeline.run(prompt)

print("\nOriginal prompt:")
print(result["original_prompt"])

print("\nCompressed prompt:")
print(result["prompt"])

print("\nResponse:")
print(result["response"])

print("\nInput tokens:", result["input_tokens"])
print("Output tokens:", result["output_tokens"])
print("Latency:", result["latency"])