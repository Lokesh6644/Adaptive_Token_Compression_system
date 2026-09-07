from app.llm.gemini_client import GeminiClient
from app.llm.metrics import Metrics
from app.compression.adaptive import AdaptiveCompressor


class AdaptivePipeline:

    def __init__(self):

        self.client = GeminiClient()
        self.metrics = Metrics()

        self.compressor = AdaptiveCompressor()

    def run(self, prompt):

        self.metrics.start_timer()

        original_prompt = prompt

        # Count original tokens
        original_token_count = len(prompt.split())

        # Convert prompt to tokens
        tokens = prompt.split()

        # Adaptive compression
        result = self.compressor.compress(tokens)

        compressed_tokens = result["tokens"]

        # Convert tokens back to prompt
        prompt = " ".join(compressed_tokens)

        compressed_token_count = len(compressed_tokens)

        # Compression metrics
        compression_ratio = (
            compressed_token_count / original_token_count
            if original_token_count > 0
            else 1
        )

        token_reduction = 1 - compression_ratio

        # Send compressed prompt to Gemini
        response = self.client.generate(prompt)

        latency = self.metrics.stop_timer()

        metric_data = {

            # Compression metrics
            "original_token_count": original_token_count,
            "compressed_token_count": compressed_token_count,
            "compression_ratio": compression_ratio,
            "token_reduction": token_reduction,

            # Adaptive information
            "difficulty": result["difficulty"],
            "selected_ratio": result["ratio"],
            "semantic_similarity": result["semantic_similarity"],
            "guard_passed": result["guard_passed"],

            # Model information
            "model": response["model"],

            # Prompts
            "original_prompt": original_prompt,
            "prompt": prompt,

            # Response
            "response": response["text"],

            # LLM metrics
            "input_tokens": response["input_tokens"],
            "output_tokens": response["output_tokens"],

            "total_tokens": (
                response["input_tokens"]
                + response["output_tokens"]
            ),

            "latency": latency
        }

        return metric_data