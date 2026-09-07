import re


QUESTION_WORDS = {
    "what",
    "why",
    "how",
    "when",
    "where",
    "which",
    "who",
    "calculate",
    "find",
    "determine",
}

NEGATION_WORDS = {
    "not",
    "no",
    "never",
    "without",
    "except",
    "least",
    "cannot",
    "can't",
}

STOPWORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "to",
    "of",
    "in",
    "on",
    "for",
    "and",
    "or",
    "with",
    "as",
    "at",
    "by",
    "it",
    "this",
    "that",
}


class TokenImportance:

    def score(self, token):

        word = token.lower().strip()

        score = 1.0

        # Numbers
        if re.search(r"\d", word):
            score += 4.0

        # Percentage
        if "%" in word:
            score += 3.0

        # Mathematical operators
        if any(op in word for op in ["+", "-", "*", "/", "="]):
            score += 3.0

        # Question words
        if word.strip("?,.!") in QUESTION_WORDS:
            score += 3.0

        # Negation
        if word.strip("?,.!") in NEGATION_WORDS:
            score += 4.0

        # Units
        units = {
            "km",
            "m",
            "cm",
            "mm",
            "kg",
            "g",
            "mg",
            "hr",
            "hrs",
            "hour",
            "hours",
            "min",
            "minutes",
            "sec",
            "seconds",
            "%",
        }

        if word.strip("?,.!") in units:
            score += 3.0

        # Common filler words
        if word.strip("?,.!") in STOPWORDS:
            score -= 0.5

        return max(score, 0.1)