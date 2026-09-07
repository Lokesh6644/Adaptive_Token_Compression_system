import time

from app.compression.budget_controller import BudgetController
from app.compression.llmlingua2_compressor import LLMLingua2Compressor
from app.compression.semantic_guard import SemanticGuard
from app.compression.difficulty import DifficultyScorer
from app.compression.ratio_selector import RatioSelector


class AdaptiveCompressor:

    def __init__(self, semantic_guard=None):

        self.controller = BudgetController()
        self.compressor = LLMLingua2Compressor()
        self.semantic_guard = semantic_guard or SemanticGuard()
        self.difficulty_scorer = DifficultyScorer()
        self.ratio_selector = RatioSelector()

    def compress(self, tokens, budget=None):

        if not tokens:
            return {
                "tokens": [],
                "semantic_similarity": 1.0,
                "guard_passed": True,
                "budget": 1.0,
                "original_tokens": 0,
                "compressed_tokens": 0,
                "compression_ratio": 1.0,
                "compression_time": 0.0
            }

        text = " ".join(tokens)
        difficulty = self.difficulty_scorer.score(text)

        if budget is None:
            budget = self.controller.initial_budget(difficulty)

        if len(tokens) <= 12:
            budget = max(budget, 0.70)

        if len(tokens) <= 6:
            budget = 1.0

        # --------------------------------
        # Measure actual LLMLingua work
        # --------------------------------

        start = time.perf_counter()

        result = self.compressor.compress(
            text,
            rate=budget
        )

        compression_time = round(
            time.perf_counter() - start,
            4
        )

        compressed_text = result["compressed_text"]

        original_tokens = result["original_tokens"]
        compressed_tokens = result["compressed_tokens"]

        compression_ratio = (
            compressed_tokens / original_tokens
            if original_tokens > 0
            else 1.0
        )

        # --------------------------------
        # Semantic Guard Verification
        # --------------------------------
        guard_result = self.semantic_guard.verify(
            original_text=text,
            compressed_text=compressed_text
        )

        return {
            "tokens": compressed_text.split(),

            "difficulty": difficulty,

            "ratio": compression_ratio,

            "semantic_similarity": guard_result["similarity"],

            "guard_passed": guard_result["passed"],

            "guard_threshold": guard_result["threshold"],

            "budget": budget,

            "original_tokens":
                original_tokens,

            "compressed_tokens":
                compressed_tokens,

            "compression_ratio":
                compression_ratio,

            "compression_time":
                compression_time
        }