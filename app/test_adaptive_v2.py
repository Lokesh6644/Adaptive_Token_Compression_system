from app.pipeline.adaptive_v2 import AdaptivePipelineV2


pipeline = AdaptivePipelineV2()


prompt = "What is 2 + 2?"

expected = "4"


result = pipeline.run(
    prompt,
    expected
)


print("\n==============================")
print("ADAPTIVE V2 RESULT")
print("==============================")

print("Original:", result["original_prompt"])

print("Initial budget:",
      result["initial_budget"])

print("Final budget:",
      result["final_budget"])

print("Attempts:",
      result["num_attempts"])

print("Correct:",
      result["correct"])

print("Original tokens:",
      result["original_token_count"])

print("Final compressed tokens:",
      result["compressed_token_count"])

print("Token reduction:",
      round(
          result["token_reduction"] * 100,
          2
      ),
      "%")

print("\nAttempts:")

for i, attempt in enumerate(
    result["attempts"],
    1
):

    print(
        f"\nAttempt {i}"
    )

    print(
        "Budget:",
        attempt["budget"]
    )

    print(
        "Prompt:",
        attempt["prompt"]
    )

    print(
        "Prediction:",
        attempt["prediction"]
    )

    print(
        "Correct:",
        attempt["correct"]
    )