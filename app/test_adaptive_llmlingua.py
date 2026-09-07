from app.compression.adaptive import AdaptiveCompressor


def main():

    print("=" * 60)
    print("ADAPTIVE LLMLINGUA-2 TEST")
    print("=" * 60)

    compressor = AdaptiveCompressor()

    prompts = [
        "What is 2 + 2?",

        """
        John has 10 apples. He gives 3 apples to his friend.
        Then he buys 5 more apples from a shop.
        After that, he gives 2 apples to his sister.
        How many apples does John have now?
        """,

        """
        A train travels 120 kilometers in 2 hours.
        If the train continues at the same speed,
        how far will it travel in 5 hours?
        Explain your reasoning and provide the final answer.
        """
    ]

    for i, prompt in enumerate(prompts, 1):

        tokens = prompt.split()

        result = compressor.compress(tokens)

        print("\n" + "-" * 60)
        print(f"Sample {i}")

        print("\nOriginal:")
        print(prompt.strip())

        print("\nDifficulty:")
        print(result["difficulty"])

        print("Selected budget:")
        print(result["budget"])

        print("Original tokens:")
        print(result["original_tokens"])

        print("Compressed tokens:")
        print(result["compressed_tokens"])

        print("Compression ratio:")
        print(round(result["compression_ratio"], 3))

        print("\nCompressed prompt:")
        print(" ".join(result["tokens"]))


if __name__ == "__main__":
    main()