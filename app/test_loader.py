from app.benchmarks.gsm8k_loader import GSM8KLoader

loader = GSM8KLoader()

dataset = loader.load(limit=3)

for sample in dataset:

    print(sample)

    print("-" * 80)