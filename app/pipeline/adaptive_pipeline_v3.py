from app.llm.anthropic_client import ClaudeClient

from app.compression.adaptive import AdaptiveCompressor
from app.compression.budget_controller import BudgetController
from app.utils.config import FALLBACK_STRATEGY


class AdaptivePipelineV3:

    def __init__(self):

        self.client = ClaudeClient()

        self.compressor = AdaptiveCompressor()

        self.controller = BudgetController()

    def run(self, question, expected_answer=None):

        original_tokens = question.split()

        # -----------------------------------------
        # Step 1: Determine initial compression
        # -----------------------------------------

        first_result = self.compressor.compress(
            original_tokens
        )

        current_budget = first_result["budget"]

        attempts = []

        while True:

            # -------------------------------------
            # Step 2: Compress using current budget
            # -------------------------------------

            if current_budget == first_result["budget"]:

                compression_result = first_result

            else:

                compression_result = self.compressor.compress(
                    original_tokens,
                    budget=current_budget
                )

            # Check if Semantic Guard rejected compression
            if not compression_result["guard_passed"] and current_budget < 1.0:
                if FALLBACK_STRATEGY == "DISCARD":
                    # Directly fallback to uncompressed prompt (budget 1.0)
                    current_budget = 1.0
                    continue
                else:
                    # Escalate to next budget tier
                    next_b = self.controller.next_budget(current_budget)
                    if next_b != current_budget:
                        current_budget = next_b
                        continue

            compressed_prompt = " ".join(
                compression_result["tokens"]
            )

            # -------------------------------------
            # Step 3: Send to Claude / LLM
            # -------------------------------------

            result = self.client.generate(
                compressed_prompt
            )

            # -------------------------------------
            # Step 4: Evaluate
            # -------------------------------------

            correct = None

            if expected_answer is not None:

                correct = (
                    expected_answer.lower()
                    in result["text"].lower()
                )

            attempts.append({
                "budget": current_budget,

                "compressed_prompt":
                    compressed_prompt,

                "original_tokens":
                    compression_result["original_tokens"],

                "compressed_tokens":
                    compression_result["compressed_tokens"],

                "compression_ratio":
                    compression_result["compression_ratio"],

                "semantic_similarity":
                    compression_result["semantic_similarity"],

                "guard_passed":
                    compression_result["guard_passed"],

                "answer":
                    result["text"],

                "input_tokens":
                    result["input_tokens"],

                "output_tokens":
                    result["output_tokens"],

                "correct":
                    correct
            })

            # -------------------------------------
            # Step 5: Stop if correct
            # -------------------------------------

            if correct is True:

                break

            # -------------------------------------
            # If no evaluator supplied
            # -------------------------------------

            if expected_answer is None:

                break

            # -------------------------------------
            # Step 6: Increase budget
            # -------------------------------------

            next_budget = self.controller.next_budget(
                current_budget
            )

            # No more budgets available
            if next_budget == current_budget:

                break

            current_budget = next_budget

        # -----------------------------------------
        # Final result
        # -----------------------------------------

        final = attempts[-1]

        return {
            "question": question,

            "final_answer":
                final["answer"],

            "final_budget":
                final["budget"],

            "semantic_similarity":
                final["semantic_similarity"],

            "guard_passed":
                final["guard_passed"],

            "original_tokens":
                final["original_tokens"],

            "compressed_tokens":
                final["compressed_tokens"],

            "compression_ratio":
                final["compression_ratio"],

            "correct":
                final["correct"],

            "attempts":
                attempts
        }