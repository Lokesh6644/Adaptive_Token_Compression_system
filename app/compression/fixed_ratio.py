from app.compression.base import Compressor


class FixedRatioCompressor(Compressor):

    def __init__(self, ratio=0.5):
        self.ratio = ratio

    def compress(self, tokens):

        if not tokens:
            return tokens

        keep_count = max(
            1,
            int(len(tokens) * self.ratio)
        )

        return tokens[:keep_count]