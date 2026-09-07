import time
import json
from pathlib import Path
import pandas as pd

from app.llm.anthropic_client import ClaudeClient

from app.compression.llmlingua2_compressor import (
    LLMLingua2Compressor
)

from app.compression.adaptive import AdaptiveCompressor


QUESTIONS = [
    {
        "question": "What is 2 + 2?",
        "answer": "4"
    },
    {
        "question": (
            "John has 10 apples. He gives 3 to his friend "
            "and then buys 5 more. How many apples does he have?"
        ),
        "answer": "12"
    },
    {
        "question": (
            "A train travels 60 km in 2 hours. "
            "What is its average speed?"
        ),
        "answer": "30"
    },
    {
        "question": (
            "There are 24 students in a class. "
            "If they are divided equally into 4 groups, "
            "how many students are in each group?"
        ),
        "answer": "6"
    },
    {
        "question": (
            "A shop gives a 20% discount on a ₹500 item. "
            "What is the final price?"
        ),
        "answer": "400"
    }
]


def check_answer(response, expected):

    return expected.lower() in response.lower()


def run_baseline(
    client,
    tokenizer,
    question,
    expected
):

    start = time.time()

    result = client.generate(question)

    latency = time.time() - start

    original_tokens = tokenizer.count_tokens(
        question
    )

    return {
        "method": "Baseline",
        "original_tokens": original_tokens,
        "compressed_tokens": original_tokens,
        "tokens_saved": 0,
        "compression_percent": 0.0,
        "latency": latency,
        "correct": check_answer(
            result["text"],
            expected
        ),
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"]
    }


def run_fixed(
    client,
    compressor,
    question,
    expected
):

    compression_start = time.time()

    compression_result = compressor.compress(
        question,
        rate=0.5
    )

    compression_latency = (
        time.time() - compression_start
    )

    compressed_prompt = (
        compression_result["compressed_text"]
    )

    llm_start = time.time()

    result = client.generate(
        compressed_prompt
    )

    llm_latency = time.time() - llm_start

    original_tokens = (
        compression_result["original_tokens"]
    )

    compressed_tokens = (
        compression_result["compressed_tokens"]
    )

    tokens_saved = (
        original_tokens -
        compressed_tokens
    )

    compression_percent = (
        tokens_saved / original_tokens * 100
        if original_tokens > 0
        else 0
    )

    return {
        "method": "Fixed LLMLingua-2",
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "tokens_saved": tokens_saved,
        "compression_percent": compression_percent,
        "compression_latency": compression_latency,
        "llm_latency": llm_latency,
        "latency": (
            compression_latency +
            llm_latency
        ),
        "correct": check_answer(
            result["text"],
            expected
        ),
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"]
    }


def run_adaptive(
    client,
    compressor,
    question,
    expected
):

    start = time.time()

    compression_result = compressor.compress(
        question.split()
    )

    compressed_prompt = " ".join(
        compression_result["tokens"]
    )

    result = client.generate(
        compressed_prompt
    )

    latency = time.time() - start

    original_tokens = (
        compression_result["original_tokens"]
    )

    compressed_tokens = (
        compression_result["compressed_tokens"]
    )

    tokens_saved = (
        original_tokens -
        compressed_tokens
    )

    compression_percent = (
        tokens_saved / original_tokens * 100
        if original_tokens > 0
        else 0
    )

    return {
        "method": "Adaptive LLMLingua-2",
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "tokens_saved": tokens_saved,
        "compression_percent": compression_percent,
        "budget": compression_result["budget"],
        "difficulty": compression_result["difficulty"],
        "latency": latency,
        "correct": check_answer(
            result["text"],
            expected
        ),
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"]
    }


def print_result(result):

    print("\nMethod:", result["method"])

    print(
        "Original tokens:",
        result["original_tokens"]
    )

    print(
        "Compressed tokens:",
        result["compressed_tokens"]
    )

    print(
        "Tokens saved:",
        result["tokens_saved"]
    )

    print(
        "Token reduction:",
        round(
            result["compression_percent"],
            2
        ),
        "%"
    )

    print(
        "Claude input tokens:",
        result["input_tokens"]
    )

    print(
        "Claude output tokens:",
        result["output_tokens"]
    )

    print(
        "Latency:",
        round(result["latency"], 3),
        "seconds"
    )

    print(
        "Correct:",
        result["correct"]
    )

    if "budget" in result:
        print(
            "Budget:",
            result["budget"]
        )

    if "difficulty" in result:
        print(
            "Difficulty:",
            result["difficulty"]
        )


def main():

    print("=" * 70)
    print("PHASE 3.7 — CONTROLLED LLMLINGUA-2 BENCHMARK")
    print("=" * 70)

    client = ClaudeClient()

    compressor = LLMLingua2Compressor()

    adaptive_compressor = AdaptiveCompressor()

    # Same tokenizer for every method
    tokenizer = compressor

    results = []

    for i, item in enumerate(QUESTIONS, 1):

        question = item["question"]
        expected = item["answer"]

        print("\n" + "=" * 70)
        print(
            f"QUESTION {i}/{len(QUESTIONS)}"
        )
        print("=" * 70)

        print(question)

        baseline = run_baseline(
            client,
            tokenizer,
            question,
            expected
        )

        fixed = run_fixed(
            client,
            compressor,
            question,
            expected
        )

        adaptive = run_adaptive(
            client,
            adaptive_compressor,
            question,
            expected
        )

        for res in (baseline, fixed, adaptive):
            res["question_id"] = i
            res["question"] = question
            res["expected_answer"] = expected

        results.extend([
            baseline,
            fixed,
            adaptive
        ])

        print_result(baseline)
        print_result(fixed)
        print_result(adaptive)

    print("\n")
    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    methods = [
        "Baseline",
        "Fixed LLMLingua-2",
        "Adaptive LLMLingua-2"
    ]

    summary_data = {}

    for method in methods:

        method_results = [
            r for r in results
            if r["method"] == method
        ]

        accuracy = (
            sum(
                r["correct"]
                for r in method_results
            )
            / len(method_results)
            * 100
        )

        avg_original = (
            sum(
                r["original_tokens"]
                for r in method_results
            )
            / len(method_results)
        )

        avg_compressed = (
            sum(
                r["compressed_tokens"]
                for r in method_results
            )
            / len(method_results)
        )

        avg_saved = (
            sum(
                r["tokens_saved"]
                for r in method_results
            )
            / len(method_results)
        )

        avg_reduction = (
            sum(
                r["compression_percent"]
                for r in method_results
            )
            / len(method_results)
        )

        avg_latency = (
            sum(
                r["latency"]
                for r in method_results
            )
            / len(method_results)
        )

        avg_input = (
            sum(
                r["input_tokens"]
                for r in method_results
            )
            / len(method_results)
        )

        avg_output = (
            sum(
                r["output_tokens"]
                for r in method_results
            )
            / len(method_results)
        )

        print("\n" + method)
        print("-" * 40)

        print(
            "Accuracy:",
            round(accuracy, 2),
            "%"
        )

        print(
            "Average original tokens:",
            round(avg_original, 2)
        )

        print(
            "Average compressed tokens:",
            round(avg_compressed, 2)
        )

        print(
            "Average tokens saved:",
            round(avg_saved, 2)
        )

        print(
            "Average token reduction:",
            round(avg_reduction, 2),
            "%"
        )

        print(
            "Average Claude input tokens:",
            round(avg_input, 2)
        )

        print(
            "Average Claude output tokens:",
            round(avg_output, 2)
        )

        print(
            "Average total latency:",
            round(avg_latency, 3),
            "seconds"
        )

        summary_data[method] = {
            "accuracy_pct": round(accuracy, 2),
            "avg_original_tokens": round(avg_original, 2),
            "avg_compressed_tokens": round(avg_compressed, 2),
            "avg_tokens_saved": round(avg_saved, 2),
            "avg_token_reduction_pct": round(avg_reduction, 2),
            "avg_claude_input_tokens": round(avg_input, 2),
            "avg_claude_output_tokens": round(avg_output, 2),
            "avg_total_latency_sec": round(avg_latency, 3)
        }

    out_path = Path("results")
    out_path.mkdir(parents=True, exist_ok=True)

    csv_file = out_path / "phase3_benchmark_results.csv"
    pd.DataFrame(results).to_csv(csv_file, index=False)

    summary_file = out_path / "phase3_benchmark_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary_data, f, indent=2)

    print(f"\n[SUCCESS] Phase 3 results saved to:\n - {csv_file}\n - {summary_file}")


if __name__ == "__main__":
    main()