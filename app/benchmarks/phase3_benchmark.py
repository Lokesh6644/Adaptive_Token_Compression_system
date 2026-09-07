import time

from app.cost_gate import CostGate

from app.llm.anthropic_client import ClaudeClient

from app.compression.llmlingua2_compressor import (
    LLMLingua2Compressor
)

from app.compression.adaptive import AdaptiveCompressor
from app.compression.budget_controller import BudgetController

from app.benchmarks.gsm8k_loader import GSM8KLoader
from app.benchmarks.evaluator import GSM8KEvaluator


# ============================================================
# BASELINE
# ============================================================

def run_baseline(
    client,
    tokenizer,
    sample,
    original_tokens
):

    question = sample["prompt"]
    reference = sample["reference"]

    start = time.time()

    result = client.generate(question)

    total_latency = time.time() - start

    evaluation = GSM8KEvaluator.evaluate(
        result["text"],
        reference
    )

    return {
        "method": "Baseline",

        "decision": "BASELINE",

        "original_tokens": original_tokens,
        "compressed_tokens": original_tokens,

        "tokens_saved": 0,
        "token_reduction": 0.0,

        "budget": 1.0,
        "difficulty": None,

        "compression_latency": 0.0,
        "llm_latency": total_latency,
        "total_latency": total_latency,

        "attempts": 1,

        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],

        "correct": evaluation["correct"],

        "predicted": evaluation["predicted_answer"],
        "actual": evaluation["actual_answer"]
    }


# ============================================================
# FIXED LLMLINGUA
# ============================================================

def run_fixed(
    client,
    compressor,
    sample,
    original_tokens
):

    question = sample["prompt"]
    reference = sample["reference"]

    compression_start = time.time()

    compression = compressor.compress(
        question,
        rate=0.50
    )

    compression_latency = (
        time.time() - compression_start
    )

    compressed_prompt = compression[
        "compressed_text"
    ]

    # Count using the SAME LLMLingua tokenizer
    compressed_tokens = compressor.count_tokens(
        compressed_prompt
    )

    llm_start = time.time()

    result = client.generate(
        compressed_prompt
    )

    llm_latency = time.time() - llm_start

    total_latency = (
        compression_latency +
        llm_latency
    )

    tokens_saved = (
        original_tokens -
        compressed_tokens
    )

    token_reduction = (
        tokens_saved /
        original_tokens
        if original_tokens > 0
        else 0.0
    )

    evaluation = GSM8KEvaluator.evaluate(
        result["text"],
        reference
    )

    return {
        "method": "Fixed LLMLingua-2",

        "decision": "COMPRESS",

        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,

        "tokens_saved": tokens_saved,
        "token_reduction": token_reduction,

        "budget": 0.50,
        "difficulty": None,

        "compression_latency": compression_latency,
        "llm_latency": llm_latency,
        "total_latency": total_latency,

        "attempts": 1,

        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],

        "correct": evaluation["correct"],

        "predicted": evaluation["predicted_answer"],
        "actual": evaluation["actual_answer"]
    }


# ============================================================
# ADAPTIVE LLMLINGUA
# ============================================================

def run_adaptive(
    client,
    compressor,
    tokenizer,
    sample,
    original_tokens
):

    question = sample["prompt"]
    reference = sample["reference"]

    compression_start = time.time()

    compression = compressor.compress(
        question.split()
    )

    compressed_prompt = " ".join(
        compression["tokens"]
    )

    # Same tokenizer for every method
    compressed_tokens = tokenizer.count_tokens(
        compressed_prompt
    )

    compression_latency = (
        time.time() - compression_start
    )

    llm_start = time.time()

    result = client.generate(
        compressed_prompt
    )

    llm_latency = time.time() - llm_start

    total_latency = (
        compression_latency +
        llm_latency
    )

    tokens_saved = (
        original_tokens -
        compressed_tokens
    )

    token_reduction = (
        tokens_saved /
        original_tokens
        if original_tokens > 0
        else 0.0
    )

    evaluation = GSM8KEvaluator.evaluate(
        result["text"],
        reference
    )

    return {
        "method": "Adaptive LLMLingua-2",

        "decision": "COMPRESS",

        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,

        "tokens_saved": tokens_saved,
        "token_reduction": token_reduction,

        "budget": compression["budget"],
        "difficulty": compression["difficulty"],

        "compression_latency": compression_latency,
        "llm_latency": llm_latency,
        "total_latency": total_latency,

        "attempts": 1,

        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],

        "correct": evaluation["correct"],

        "predicted": evaluation["predicted_answer"],
        "actual": evaluation["actual_answer"]
    }


# ============================================================
# FEEDBACK ADAPTIVE
# ============================================================

def run_feedback_adaptive(
    client,
    compressor,
    tokenizer,
    controller,
    sample,
    original_tokens
):

    question = sample["prompt"]
    reference = sample["reference"]

    tokens = question.split()

    current_budget = None

    attempts = []

    total_start = time.time()

    while True:

        attempt_start = time.time()

        # -----------------------------------------
        # Compression
        # -----------------------------------------

        compression_start = time.time()

        compression = compressor.compress(
            tokens,
            budget=current_budget
        )

        compression_latency = (
            time.time() - compression_start
        )

        compressed_prompt = " ".join(
            compression["tokens"]
        )

        compressed_tokens = tokenizer.count_tokens(
            compressed_prompt
        )

        # -----------------------------------------
        # Claude
        # -----------------------------------------

        llm_start = time.time()

        result = client.generate(
            compressed_prompt
        )

        llm_latency = (
            time.time() - llm_start
        )

        attempt_latency = (
            time.time() - attempt_start
        )

        # -----------------------------------------
        # Evaluation
        # -----------------------------------------

        evaluation = GSM8KEvaluator.evaluate(
            result["text"],
            reference
        )

        tokens_saved = (
            original_tokens -
            compressed_tokens
        )

        token_reduction = (
            tokens_saved /
            original_tokens
            if original_tokens > 0
            else 0.0
        )

        attempt = {

            "budget":
                compression["budget"],

            "difficulty":
                compression["difficulty"],

            "original_tokens":
                original_tokens,

            "compressed_tokens":
                compressed_tokens,

            "tokens_saved":
                tokens_saved,

            "token_reduction":
                token_reduction,

            "compression_latency":
                compression_latency,

            "llm_latency":
                llm_latency,

            "attempt_latency":
                attempt_latency,

            "input_tokens":
                result["input_tokens"],

            "output_tokens":
                result["output_tokens"],

            "correct":
                evaluation["correct"],

            "predicted":
                evaluation["predicted_answer"],

            "actual":
                evaluation["actual_answer"]
        }

        attempts.append(attempt)

        # -----------------------------------------
        # Correct answer
        # -----------------------------------------

        if evaluation["correct"]:
            break

        # -----------------------------------------
        # Increase budget
        # -----------------------------------------

        next_budget = controller.next_budget(
            compression["budget"]
        )

        if next_budget == compression["budget"]:
            break

        current_budget = next_budget

    total_latency = (
        time.time() - total_start
    )

    final = attempts[-1]

    return {
        "method":
            "Feedback-Adaptive LLMLingua-2",

        "decision":
            "COMPRESS",

        "original_tokens":
            original_tokens,

        "compressed_tokens":
            final["compressed_tokens"],

        "tokens_saved":
            final["tokens_saved"],

        "token_reduction":
            final["token_reduction"],

        "budget":
            final["budget"],

        "difficulty":
            final["difficulty"],

        "compression_latency":
            sum(
                a["compression_latency"]
                for a in attempts
            ),

        "llm_latency":
            sum(
                a["llm_latency"]
                for a in attempts
            ),

        "total_latency":
            total_latency,

        "attempts":
            len(attempts),

        "input_tokens":
            sum(
                a["input_tokens"]
                for a in attempts
            ),

        "output_tokens":
            sum(
                a["output_tokens"]
                for a in attempts
            ),

        "correct":
            final["correct"],

        "predicted":
            final["predicted"],

        "actual":
            final["actual"]
    }


# ============================================================
# COST-AWARE SELECTIVE ADAPTIVE
# ============================================================

def run_cost_aware(
    client,
    compressor,
    tokenizer,
    cost_gate,
    sample,
    original_tokens
):

    question = sample["prompt"]
    reference = sample["reference"]

    # -----------------------------------------
    # Estimate compression benefit
    # -----------------------------------------

    estimate = cost_gate.estimate_savings(
        original_tokens
    )

    decision = cost_gate.decision(
        original_tokens
    )

    # ========================================================
    # SKIP COMPRESSION
    # ========================================================

    if decision == "SKIP":

        llm_start = time.time()

        result = client.generate(
            question
        )

        llm_latency = (
            time.time() - llm_start
        )

        evaluation = GSM8KEvaluator.evaluate(
            result["text"],
            reference
        )

        return {
            "method":
                "Cost-Aware Adaptive LLMLingua-2",

            "decision":
                "SKIP",

            "original_tokens":
                original_tokens,

            "compressed_tokens":
                original_tokens,

            "tokens_saved":
                0,

            "token_reduction":
                0.0,

            "budget":
                1.0,

            "difficulty":
                None,

            "compression_latency":
                0.0,

            "llm_latency":
                llm_latency,

            "total_latency":
                llm_latency,

            "attempts":
                1,

            "input_tokens":
                result["input_tokens"],

            "output_tokens":
                result["output_tokens"],

            "correct":
                evaluation["correct"],

            "predicted":
                evaluation["predicted_answer"],

            "actual":
                evaluation["actual_answer"],

            "estimated_compressed_tokens":
                estimate[
                    "estimated_compressed_tokens"
                ],

            "estimated_saved_tokens":
                estimate[
                    "estimated_saved_tokens"
                ],

            "estimated_net_savings":
                estimate[
                    "estimated_net_savings"
                ]
        }

    # ========================================================
    # COMPRESS
    # ========================================================

    compression_start = time.time()

    compression = compressor.compress(
    question.split(),
    budget=0.75
    )

    compression_latency = (
        time.time() - compression_start
    )

    compressed_prompt = " ".join(
        compression["tokens"]
    )

    compressed_tokens = tokenizer.count_tokens(
        compressed_prompt
    )

    # -----------------------------------------
    # Claude
    # -----------------------------------------

    llm_start = time.time()

    result = client.generate(
        compressed_prompt
    )

    llm_latency = (
        time.time() - llm_start
    )

    total_latency = (
        compression_latency +
        llm_latency
    )

    tokens_saved = (
        original_tokens -
        compressed_tokens
    )

    token_reduction = (
        tokens_saved /
        original_tokens
        if original_tokens > 0
        else 0.0
    )

    evaluation = GSM8KEvaluator.evaluate(
        result["text"],
        reference
    )

    return {
        "method":
            "Cost-Aware Adaptive LLMLingua-2",

        "decision":
            "COMPRESS",

        "original_tokens":
            original_tokens,

        "compressed_tokens":
            compressed_tokens,

        "tokens_saved":
            tokens_saved,

        "token_reduction":
            token_reduction,

        "budget":
            compression["budget"],

        "difficulty":
            compression["difficulty"],

        "compression_latency":
            compression_latency,

        "llm_latency":
            llm_latency,

        "total_latency":
            total_latency,

        "attempts":
            1,

        "input_tokens":
            result["input_tokens"],

        "output_tokens":
            result["output_tokens"],

        "correct":
            evaluation["correct"],

        "predicted":
            evaluation["predicted_answer"],

        "actual":
            evaluation["actual_answer"],

        "estimated_compressed_tokens":
            estimate[
                "estimated_compressed_tokens"
            ],

        "estimated_saved_tokens":
            estimate[
                "estimated_saved_tokens"
            ],

        "estimated_net_savings":
            estimate[
                "estimated_net_savings"
            ]
    }


# ============================================================
# PRINT INDIVIDUAL RESULT
# ============================================================

def print_result(result):

    print(
        f"\n{result['method']}"
    )

    print("-" * 50)

    print(
        "Decision:",
        result["decision"]
    )

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
            result["token_reduction"] * 100,
            2
        ),
        "%"
    )

    print(
        "Budget:",
        result["budget"]
    )

    print(
        "Attempts:",
        result["attempts"]
    )

    print(
        "Compression latency:",
        round(
            result["compression_latency"],
            3
        ),
        "sec"
    )

    print(
        "LLM latency:",
        round(
            result["llm_latency"],
            3
        ),
        "sec"
    )

    print(
        "Total latency:",
        round(
            result["total_latency"],
            3
        ),
        "sec"
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
        "Predicted:",
        result["predicted"]
    )

    print(
        "Actual:",
        result["actual"]
    )

    print(
        "Correct:",
        result["correct"]
    )

    # Cost-aware specific information
    if (
        result["method"]
        == "Cost-Aware Adaptive LLMLingua-2"
    ):

        print(
            "Estimated net savings:",
            result[
                "estimated_net_savings"
            ]
        )


# ============================================================
# MAIN BENCHMARK
# ============================================================

def main():

    print("=" * 75)
    print(
        "PHASE 3 — COST-AWARE SELECTIVE ADAPTIVE COMPRESSION"
    )
    print("=" * 75)

    # -----------------------------------------
    # Clients / models
    # -----------------------------------------

    client = ClaudeClient()

    compressor = LLMLingua2Compressor()

    adaptive_compressor = AdaptiveCompressor()

    controller = BudgetController()

    # -----------------------------------------
    # Cost model V1
    # -----------------------------------------

    cost_gate = CostGate(
        min_tokens=30,
        estimated_compression_ratio=0.60,
        compression_overhead=20
    )

    # SAME tokenizer for every method
    tokenizer = compressor

    # -----------------------------------------
    # Dataset
    # -----------------------------------------

    loader = GSM8KLoader()

    samples = loader.load(
        limit=10
    )

    all_results = []

    # ========================================================
    # RUN ALL METHODS
    # ========================================================

    for index, sample in enumerate(
        samples,
        1
    ):

        print("\n")
        print("=" * 75)

        print(
            f"SAMPLE {index}/{len(samples)}"
        )

        print("=" * 75)

        question = sample["prompt"]

        print(question)

        print(
            "\nDifficulty group:",
            sample["metadata"][
                "difficulty_group"
            ]
        )

        # -----------------------------------------
        # Common original token count
        # -----------------------------------------

        original_tokens = tokenizer.count_tokens(
            question
        )

        print(
            "\nCommon original token count:",
            original_tokens
        )

        # -----------------------------------------
        # Baseline
        # -----------------------------------------

        baseline = run_baseline(
            client,
            tokenizer,
            sample,
            original_tokens
        )

        # -----------------------------------------
        # Fixed LLMLingua
        # -----------------------------------------

        fixed = run_fixed(
            client,
            compressor,
            sample,
            original_tokens
        )

        # -----------------------------------------
        # Adaptive LLMLingua
        # -----------------------------------------

        adaptive = run_adaptive(
            client,
            adaptive_compressor,
            tokenizer,
            sample,
            original_tokens
        )

        # -----------------------------------------
        # Feedback Adaptive
        # -----------------------------------------

        feedback = run_feedback_adaptive(
            client,
            adaptive_compressor,
            tokenizer,
            controller,
            sample,
            original_tokens
        )

        # -----------------------------------------
        # Cost-Aware Adaptive
        # -----------------------------------------

        cost_aware = run_cost_aware(
            client,
            adaptive_compressor,
            tokenizer,
            cost_gate,
            sample,
            original_tokens
        )

        # -----------------------------------------
        # Store results
        # -----------------------------------------

        sample_results = [
            baseline,
            fixed,
            adaptive,
            feedback,
            cost_aware
        ]

        all_results.extend(
            sample_results
        )

        # -----------------------------------------
        # Print sample results
        # -----------------------------------------

        for result in sample_results:

            print_result(result)

    # ========================================================
    # FINAL AGGREGATE RESULTS
    # ========================================================

    print("\n\n")

    print("=" * 75)
    print("FINAL AGGREGATE RESULTS")
    print("=" * 75)

    methods = [
        "Baseline",
        "Fixed LLMLingua-2",
        "Adaptive LLMLingua-2",
        "Feedback-Adaptive LLMLingua-2",
        "Cost-Aware Adaptive LLMLingua-2"
    ]

    for method in methods:

        results = [
            r
            for r in all_results
            if r["method"] == method
        ]

        # -----------------------------------------
        # Accuracy
        # -----------------------------------------

        accuracy = (
            sum(
                r["correct"]
                for r in results
            )
            / len(results)
            * 100
        )

        # -----------------------------------------
        # Average original tokens
        # -----------------------------------------

        avg_original = (
            sum(
                r["original_tokens"]
                for r in results
            )
            / len(results)
        )

        # -----------------------------------------
        # Average compressed tokens
        # -----------------------------------------

        avg_compressed = (
            sum(
                r["compressed_tokens"]
                for r in results
            )
            / len(results)
        )

        # -----------------------------------------
        # Average saved tokens
        # -----------------------------------------

        avg_saved = (
            sum(
                r["tokens_saved"]
                for r in results
            )
            / len(results)
        )

        # -----------------------------------------
        # Average reduction
        # -----------------------------------------

        avg_reduction = (
            sum(
                r["token_reduction"]
                for r in results
            )
            / len(results)
            * 100
        )

        # -----------------------------------------
        # Average latency
        # -----------------------------------------

        avg_latency = (
            sum(
                r["total_latency"]
                for r in results
            )
            / len(results)
        )

        # -----------------------------------------
        # Average attempts
        # -----------------------------------------

        avg_attempts = (
            sum(
                r["attempts"]
                for r in results
            )
            / len(results)
        )

        # -----------------------------------------
        # Total Claude INPUT tokens
        # -----------------------------------------

        total_input_tokens = sum(
            r["input_tokens"]
            for r in results
        )

        # -----------------------------------------
        # Total Claude OUTPUT tokens
        # -----------------------------------------

        total_output_tokens = sum(
            r["output_tokens"]
            for r in results
        )

        # -----------------------------------------
        # Total compression latency
        # -----------------------------------------

        total_compression_latency = sum(
            r["compression_latency"]
            for r in results
        )

        # -----------------------------------------
        # Print aggregate
        # -----------------------------------------

        print("\n")
        print(method)
        print("-" * 50)

        print(
            "Accuracy:",
            round(
                accuracy,
                2
            ),
            "%"
        )

        print(
            "Avg original tokens:",
            round(
                avg_original,
                2
            )
        )

        print(
            "Avg compressed tokens:",
            round(
                avg_compressed,
                2
            )
        )

        print(
            "Avg tokens saved:",
            round(
                avg_saved,
                2
            )
        )

        print(
            "Avg token reduction:",
            round(
                avg_reduction,
                2
            ),
            "%"
        )

        print(
            "Avg total latency:",
            round(
                avg_latency,
                3
            ),
            "sec"
        )

        print(
            "Avg attempts:",
            round(
                avg_attempts,
                2
            )
        )

        print(
            "Total Claude input tokens:",
            total_input_tokens
        )

        print(
            "Total Claude output tokens:",
            total_output_tokens
        )

        print(
            "Total compression latency:",
            round(
                total_compression_latency,
                3
            ),
            "sec"
        )

        # -----------------------------------------
        # Cost-aware decision statistics
        # -----------------------------------------

        if (
            method
            == "Cost-Aware Adaptive LLMLingua-2"
        ):

            compressed_count = sum(
                1
                for r in results
                if r["decision"]
                == "COMPRESS"
            )

            skipped_count = sum(
                1
                for r in results
                if r["decision"]
                == "SKIP"
            )

            print(
                "Compression decisions:",
                compressed_count
            )

            print(
                "Skipped decisions:",
                skipped_count
            )

    # ========================================================
    # FINAL COST-AWARE COMPARISON
    # ========================================================

    baseline_results = [
        r
        for r in all_results
        if r["method"] == "Baseline"
    ]

    cost_aware_results = [
        r
        for r in all_results
        if (
            r["method"]
            == "Cost-Aware Adaptive LLMLingua-2"
        )
    ]

    baseline_input = sum(
        r["input_tokens"]
        for r in baseline_results
    )

    cost_aware_input = sum(
        r["input_tokens"]
        for r in cost_aware_results
    )

    baseline_output = sum(
        r["output_tokens"]
        for r in baseline_results
    )

    cost_aware_output = sum(
        r["output_tokens"]
        for r in cost_aware_results
    )

    # -----------------------------------------
    # Input token savings
    # -----------------------------------------

    net_input_savings = (
        baseline_input -
        cost_aware_input
    )

    net_input_reduction = (
        net_input_savings /
        baseline_input
        * 100
        if baseline_input > 0
        else 0.0
    )

    # -----------------------------------------
    # Total Claude token comparison
    # -----------------------------------------

    baseline_total = (
        baseline_input +
        baseline_output
    )

    cost_aware_total = (
        cost_aware_input +
        cost_aware_output
    )

    net_total_savings = (
        baseline_total -
        cost_aware_total
    )

    net_total_reduction = (
        net_total_savings /
        baseline_total
        * 100
        if baseline_total > 0
        else 0.0
    )

    # -----------------------------------------
    # Accuracy comparison
    # -----------------------------------------

    baseline_accuracy = (
        sum(
            r["correct"]
            for r in baseline_results
        )
        / len(baseline_results)
        * 100
    )

    cost_aware_accuracy = (
        sum(
            r["correct"]
            for r in cost_aware_results
        )
        / len(cost_aware_results)
        * 100
    )

    accuracy_difference = (
        cost_aware_accuracy -
        baseline_accuracy
    )

    # -----------------------------------------
    # Decision counts
    # -----------------------------------------

    compressed_count = sum(
        1
        for r in cost_aware_results
        if r["decision"] == "COMPRESS"
    )

    skipped_count = sum(
        1
        for r in cost_aware_results
        if r["decision"] == "SKIP"
    )

    # ========================================================
    # PRINT FINAL COST-AWARE RESULT
    # ========================================================

    print("\n\n")

    print("=" * 75)
    print("COST-AWARE FINAL COMPARISON")
    print("=" * 75)

    print(
        "\nBaseline accuracy:",
        round(
            baseline_accuracy,
            2
        ),
        "%"
    )

    print(
        "Cost-Aware accuracy:",
        round(
            cost_aware_accuracy,
            2
        ),
        "%"
    )

    print(
        "Accuracy difference:",
        round(
            accuracy_difference,
            2
        ),
        "percentage points"
    )

    print(
        "\nBaseline Claude input tokens:",
        baseline_input
    )

    print(
        "Cost-Aware Claude input tokens:",
        cost_aware_input
    )

    print(
        "Net Claude input tokens saved:",
        net_input_savings
    )

    print(
        "Net Claude input reduction:",
        round(
            net_input_reduction,
            2
        ),
        "%"
    )

    print(
        "\nBaseline total Claude tokens:",
        baseline_total
    )

    print(
        "Cost-Aware total Claude tokens:",
        cost_aware_total
    )

    print(
        "Net total Claude tokens saved:",
        net_total_savings
    )

    print(
        "Net total Claude token reduction:",
        round(
            net_total_reduction,
            2
        ),
        "%"
    )

    print(
        "\nCompression decisions:",
        compressed_count
    )

    print(
        "Skipped decisions:",
        skipped_count
    )

    print("\n")
    print("=" * 75)
    print("PHASE 3 COMPLETE")
    print("=" * 75)


if __name__ == "__main__":
    main()