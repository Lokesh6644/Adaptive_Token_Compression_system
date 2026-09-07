from app.benchmarks.gsm8k_loader import GSM8KLoader
#from app.runners.benchmark_runner import BenchmarkRunner
from app.runners.BenchmarkRunner import BenchmarkRunner
from app.utils.results import summarize_results


def main():

    loader = GSM8KLoader()

    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name="gsm8k"
    )

    runner.run(limit=10)

    summarize_results("gsm8k")


if __name__ == "__main__":
    main()