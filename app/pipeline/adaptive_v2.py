from app.llm.anthropic_client import ClaudeClient
from app.llm.metrics import Metrics

from app.compression.adaptive import AdaptiveCompressor
from app.cost_gate import CostGate


class AdaptivePipelineV2:

    def __init__(self):

        self.client = ClaudeClient()
        self.metrics = Metrics()

        self.compressor = AdaptiveCompressor()

        self.cost_gate = CostGate(
            min_tokens=30,
            estimated_compression_ratio=0.60,
            compression_overhead=20
        )

    def run(self, question):

        original_tokens = question.split()

        original_word_count = len(
            original_tokens
        )

        estimate = self.cost_gate.estimate_savings(
            original_word_count
        )

        decision = self.cost_gate.decision(
            original_word_count
        )

        # =================================
        # SKIP
        # =================================

        if decision == "SKIP":

            answer = self.client.generate(
                question
            )

            return {
                "question": question,
                "answer": answer,

                "decision": "SKIP",

                "difficulty": None,
                "budget": None,

                "original_tokens":
                    original_word_count,

                "compressed_tokens":
                    original_word_count,

                "compression_ratio": 1.0,

                "compression_time": 0.0,

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
                    ],

                "actual_input_tokens":
                    answer["input_tokens"],

                "actual_output_tokens":
                    answer["output_tokens"]
            }

        # =================================
        # COMPRESS
        # =================================

        compression_result = (
            self.compressor.compress(
                original_tokens
            )
        )

        compressed_prompt = " ".join(
            compression_result["tokens"]
        )

        answer = self.client.generate(
            compressed_prompt
        )

        return {
            "question": question,
            "answer": answer,

            "decision": "COMPRESS",

            "difficulty":
                compression_result["difficulty"],

            "budget":
                compression_result["budget"],

            "original_tokens":
                compression_result["original_tokens"],

            "compressed_tokens":
                compression_result["compressed_tokens"],

            "compression_ratio":
                compression_result["compression_ratio"],

            "compression_time":
                compression_result["compression_time"],

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
                ],

            "actual_input_tokens":
                answer["input_tokens"],

            "actual_output_tokens":
                answer["output_tokens"]
        }