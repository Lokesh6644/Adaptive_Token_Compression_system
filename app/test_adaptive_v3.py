from app.pipeline.adaptive_pipeline_v3 import (
    AdaptivePipelineV3
)


def main():

    print("=" * 70)
    print("PHASE 3.8 — FEEDBACK ADAPTIVE COMPRESSION")
    print("=" * 70)

    pipeline = AdaptivePipelineV3()

    question = """
    John has 10 apples. He gives 3 apples to his friend.
    Then he buys 5 more apples from a shop.
    After that, he gives 2 apples to his sister.
    How many apples does John have now?
    """

    result = pipeline.run(
        question,
        expected_answer="10"
    )

    print("\nQuestion:")
    print(question)

    print("\nFinal answer:")
    print(result["final_answer"])

    print("\nFinal budget:")
    print(result["final_budget"])

    print("\nDifficulty:")
    print(result["difficulty"])

    print("\nFinal compressed tokens:")
    print(result["compressed_tokens"])

    print("\nCorrect:")
    print(result["correct"])

    print("\n" + "-" * 70)
    print("ATTEMPT HISTORY")
    print("-" * 70)

    for i, attempt in enumerate(
        result["attempts"],
        1
    ):

        print(f"\nAttempt {i}")

        print(
            "Budget:",
            attempt["budget"]
        )

        print(
            "Compressed tokens:",
            attempt["compressed_tokens"]
        )

        print(
            "Correct:",
            attempt["correct"]
        )

        print(
            "Prompt:",
            attempt["compressed_prompt"]
        )


if __name__ == "__main__":
    main()