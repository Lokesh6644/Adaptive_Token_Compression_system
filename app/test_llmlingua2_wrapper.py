from app.compression.llmlingua2_compressor import LLMLingua2Compressor


def main():

    print("=" * 50)
    print("LLMLINGUA-2 WRAPPER TEST")
    print("=" * 50)

    compressor = LLMLingua2Compressor()

    prompt = """
    John has 10 apples. He gives 3 apples to his friend.
    Then he buys 5 more apples from a shop.
    After that, he gives 2 apples to his sister.
    How many apples does John have now?
    """

    result = compressor.compress(
        prompt,
        rate=0.5
    )

    print("\nOriginal:")
    print(result["original_text"])

    print("\nCompressed:")
    print(result["compressed_text"])

    print("\nStatistics:")
    print("Requested rate:", result["rate"])
    print("Original tokens:", result["original_tokens"])
    print("Compressed tokens:", result["compressed_tokens"])


if __name__ == "__main__":
    main()