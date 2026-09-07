class CostGate:

    """
    Conservative cost-aware compression policy.

    Goal:
        Preserve accuracy first.
        Compress only when meaningful savings
        are expected.

    V2:
        - Uses actual LLMLingua token counts
          for the prompt.
        - Requires sufficient prompt length.
        - Requires meaningful expected savings.
        - Uses conservative compression.
    """

    def __init__(
        self,
        min_tokens=50,
        estimated_compression_ratio=0.75,
        compression_overhead=10
    ):

        self.min_tokens = min_tokens

        self.estimated_compression_ratio = (
            estimated_compression_ratio
        )

        self.compression_overhead = (
            compression_overhead
        )

    def estimate_savings(self, token_count):

        estimated_compressed_tokens = (
            token_count *
            self.estimated_compression_ratio
        )

        estimated_saved_tokens = (
            token_count -
            estimated_compressed_tokens
        )

        estimated_net_savings = (
            estimated_saved_tokens -
            self.compression_overhead
        )

        return {
            "estimated_compressed_tokens":
                round(
                    estimated_compressed_tokens,
                    2
                ),

            "estimated_saved_tokens":
                round(
                    estimated_saved_tokens,
                    2
                ),

            "estimated_net_savings":
                round(
                    estimated_net_savings,
                    2
                )
        }

    def should_compress(self, token_count):

        # 1. Short prompts are not worth compressing.
        if token_count < self.min_tokens:
            return False

        estimate = self.estimate_savings(
            token_count
        )

        # 2. Compression must have meaningful
        # expected net savings.
        if estimate["estimated_net_savings"] <= 0:
            return False

        return True

    def decision(self, token_count):

        if self.should_compress(token_count):
            return "COMPRESS"

        return "SKIP"