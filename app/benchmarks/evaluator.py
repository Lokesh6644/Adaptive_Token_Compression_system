import re


class GSM8KEvaluator:

    @staticmethod
    def extract_final_number(text):

        # Find the answer after #### if present
        match = re.search(r"####\s*(-?\d+(?:,\d{3})*(?:\.\d+)?)", text)

        if match:
            return match.group(1).replace(",", "")

        # Otherwise use the last number in the response
        numbers = re.findall(
            r"-?\d+(?:,\d{3})*(?:\.\d+)?",
            text
        )

        if not numbers:
            return None

        return numbers[-1].replace(",", "")

    @staticmethod
    def normalize(value):

        if value is None:
            return None

        try:
            number = float(value)

            if number.is_integer():
                return str(int(number))

            return str(number)

        except ValueError:
            return value.strip()

    @classmethod
    def evaluate(cls, prediction, ground_truth):

        predicted = cls.extract_final_number(prediction)

        actual = cls.extract_final_number(ground_truth)

        predicted = cls.normalize(predicted)
        actual = cls.normalize(actual)

        return {
            "predicted_answer": predicted,
            "actual_answer": actual,
            "correct": predicted == actual
        }