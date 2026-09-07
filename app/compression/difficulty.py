class DifficultyScorer:

    def score(self, text):
        words = text.split()

        if not words:
            return 0.0

        word_count = len(words)

        # Basic complexity signals
        length_score = min(word_count / 100, 1.0)

        number_count = sum(
            any(char.isdigit() for char in word)
            for word in words
        )
        number_score = min(number_count / 10, 1.0)

        question_score = 0.2 if "?" in text else 0.0

        # Weighted difficulty
        difficulty = (
            0.5 * length_score +
            0.3 * number_score +
            0.2 * question_score
        )

        return min(difficulty, 1.0)