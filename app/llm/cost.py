class GeminiCostCalculator:

    INPUT_PRICE_PER_MILLION = 0.0
    OUTPUT_PRICE_PER_MILLION = 0.0

    @classmethod
    def calculate(cls, input_tokens, output_tokens):

        input_cost = (
            input_tokens
            / 1_000_000
            * cls.INPUT_PRICE_PER_MILLION
        )

        output_cost = (
            output_tokens
            / 1_000_000
            * cls.OUTPUT_PRICE_PER_MILLION
        )

        return input_cost + output_cost