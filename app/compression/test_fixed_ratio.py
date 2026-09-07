from app.compression.fixed_ratio import FixedRatioCompressor


tokens = [
    "The", "capital", "of", "France", "is",
    "Paris", "and", "it", "is", "beautiful"
]

compressor = FixedRatioCompressor(ratio=0.5)

compressed = compressor.compress(tokens)

print("Original tokens:", tokens)
print("Original count:", len(tokens))

print("Compressed tokens:", compressed)
print("Compressed count:", len(compressed))