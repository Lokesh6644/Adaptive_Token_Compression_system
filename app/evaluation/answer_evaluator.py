import re


class AnswerEvaluator:

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip().lower()

    def evaluate(self, predicted, actual):

        predicted_text = self.normalize(predicted)
        actual_text = self.normalize(actual)

        # Exact match
        if predicted_text == actual_text:
            return True

        # If the expected answer is numerical,
        # extract numbers from Claude's response.
        actual_numbers = re.findall(
            r"-?\d+(?:\.\d+)?",
            actual_text
        )

        predicted_numbers = re.findall(
            r"-?\d+(?:\.\d+)?",
            predicted_text
        )

        if actual_numbers and predicted_numbers:

            return (
                predicted_numbers[-1]
                == actual_numbers[-1]
            )

        return False