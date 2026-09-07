from app.compression.ratio_selector import RatioSelector


selector = RatioSelector()

scores = [0.10, 0.29, 0.30, 0.45, 0.59, 0.60, 0.85]

for score in scores:
    ratio = selector.select(score)

    print(
        f"Difficulty: {score:.2f} "
        f"→ Compression Ratio: {ratio:.2f}"
    )