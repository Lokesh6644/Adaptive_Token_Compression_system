from app.benchmarks.gsm8k_loader import GSM8KLoader
from app.runners.BenchmarkRunner import BenchmarkRunner


loader = GSM8KLoader()

runner = BenchmarkRunner(loader)

runner.run(limit=10)