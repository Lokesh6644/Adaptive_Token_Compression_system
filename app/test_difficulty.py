from app.compression.difficulty import DifficultyScorer


scorer = DifficultyScorer()

samples = [
    "What is 2 + 2?",
    "What is 15% of 240?",
    "A train travels 120 km in 2 hours. If it increases its speed by 25%, how long will it take to travel 300 km?",
]

for text in samples:
    score = scorer.score(text)

    print("\nText:", text)
    print("Difficulty:", round(score, 3))