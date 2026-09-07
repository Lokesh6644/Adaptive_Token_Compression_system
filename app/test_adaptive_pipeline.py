from app.pipeline.adaptive import AdaptivePipeline


pipeline = AdaptivePipeline()


samples = [
    "What is 2 + 2?",
    "What is 15% of 240?",
    "A train travels 120 km in 2 hours. If it increases its speed by 25%, how long will it take to travel 300 km?"
]


for i, prompt in enumerate(samples, 1):

    print(f"\nRunning sample {i}")

    result = pipeline.run(prompt)

    print("Original tokens:", result["original_token_count"])
    print("Compressed tokens:", result["compressed_token_count"])

    print("Difficulty:", round(result["difficulty"], 3))
    print("Selected ratio:", result["selected_ratio"])

    print("Compression ratio:",
          round(result["compression_ratio"], 3))

    print("Token reduction:",
          round(result["token_reduction"], 3))

    print("Prompt sent:", result["prompt"])

    print("Response:", result["response"])

    print("Latency:", round(result["latency"], 3))