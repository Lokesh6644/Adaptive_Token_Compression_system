from app.compression.adaptive import AdaptiveCompressor


compressor = AdaptiveCompressor()


samples = [
    "What is 2 + 2?",
    "What is 15% of 240?",
    "A train travels 120 km in 2 hours. If it increases its speed by 25%, how long will it take to travel 300 km?"
]


for text in samples:

    tokens = text.split()

    result = compressor.compress(tokens)

    compressed_tokens = result["tokens"]

    print("\nText:", text)

    print(
        "Original tokens:",
        len(tokens)
    )

    print(
        "Compressed tokens:",
        len(compressed_tokens)
    )

    print(
        "Difficulty:",
        round(result["difficulty"], 3)
    )

    print(
        "Selected ratio:",
        result["ratio"]
    )

    print(
        "Compressed:",
        " ".join(compressed_tokens)
    )