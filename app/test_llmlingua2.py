from llmlingua import PromptCompressor


def main():
    print("=" * 50)
    print("LLMLINGUA-2 STANDALONE TEST")
    print("=" * 50)

    compressor = PromptCompressor(
        model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
        device_map="cpu",
        use_llmlingua2=True
    )

    prompt = """
    John has 5 apples. He buys 3 more apples from the store.
    Then he gives 2 apples to his friend and eats 1 apple.
    How many apples does John have left?
    Explain your reasoning step by step and provide the final answer.
    """

    print("\nOriginal prompt:")
    print(prompt)

    result = compressor.compress_prompt(
        prompt,
        rate=0.5
    )

    compressed = result["compressed_prompt"]

    print("\nCompressed prompt:")
    print(compressed)

    print("\n" + "=" * 50)
    print("RESULT")
    print("=" * 50)

    print("Original characters:", len(prompt))
    print("Compressed characters:", len(compressed))

    print("\nCompression result:")
    print(result)


if __name__ == "__main__":
    main()