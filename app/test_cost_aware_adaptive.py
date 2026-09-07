from app.pipeline.adaptive_v2 import AdaptivePipelineV2


pipeline = AdaptivePipelineV2()


tests = [

    "What is 2 + 2?",

    "What is the capital of France?",

    "A farmer has 10 apples and gives 3 apples to his friend. How many apples does he have left?",

    """
    A company has 120 employees. 40 employees work in engineering,
    30 work in sales, and the remaining employees work in marketing.
    The company decides to move 10 employees from marketing to
    engineering. How many employees will engineering have after
    the transfer?
    """,

    """
    Explain the difference between supervised learning and
    unsupervised learning. Include the main objective of each,
    the type of training data used, and provide one practical
    example for each approach.
    """
]


print("\n======================================")
print("COST-AWARE ADAPTIVE PIPELINE")
print("======================================")


for i, prompt in enumerate(tests, 1):

    prompt = " ".join(
        prompt.split()
    )

    print(f"\nTest {i}")
    print("--------------------------------------")

    result = pipeline.run(prompt)

    print(
        "Original tokens:",
        result["original_tokens"]
    )

    print(
        "Decision:",
        result["decision"]
    )

    print(
        "Estimated compressed:",
        result[
            "estimated_compressed_tokens"
        ]
    )

    print(
        "Estimated saved:",
        result[
            "estimated_saved_tokens"
        ]
    )

    print(
        "Estimated net savings:",
        result[
            "estimated_net_savings"
        ]
    )

    print(
        "Actual Claude input:",
        result[
            "actual_input_tokens"
        ]
    )

    print(
        "Final compressed tokens:",
        result[
            "compressed_tokens"
        ]
    )

    print(
        "Compression ratio:",
        result[
            "compression_ratio"
        ]
    )

    print(
        "Answer:",
        result["answer"]["text"]
    )