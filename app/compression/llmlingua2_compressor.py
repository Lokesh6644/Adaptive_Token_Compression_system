from llmlingua import PromptCompressor


class LLMLingua2Compressor:

    def __init__(self):

        self.model_name = (
            "microsoft/"
            "llmlingua-2-bert-base-multilingual-cased-meetingbank"
        )

        self.compressor = PromptCompressor(
            model_name=self.model_name,
            device_map="cpu",
            use_llmlingua2=True
        )

    def compress(self, text, rate=0.5):

        if not text:
            return {
                "original_text": "",
                "compressed_text": "",
                "rate": rate,
                "original_tokens": 0,
                "compressed_tokens": 0
            }

        if rate >= 1.0:

            # LLMLingua tokenizer count
            tokens = self.compressor.tokenizer.encode(
                text,
                add_special_tokens=False
            )

            token_count = len(tokens)

            return {
                "original_text": text,
                "compressed_text": text,
                "rate": 1.0,
                "original_tokens": token_count,
                "compressed_tokens": token_count
            }

        result = self.compressor.compress_prompt(
            text,
            rate=rate
        )

        compressed_text = result["compressed_prompt"]

        return {
            "original_text": text,
            "compressed_text": compressed_text,
            "rate": rate,
            "original_tokens": result.get(
                "origin_tokens", 0
            ),
            "compressed_tokens": result.get(
                "compressed_tokens", 0
            )
        }

    def count_tokens(self, text):

        if not text:
            return 0

        tokens = self.compressor.tokenizer.encode(
            text,
            add_special_tokens=False
        )

        return len(tokens)