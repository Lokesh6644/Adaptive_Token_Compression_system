from app.benchmarks.gsm8k_loader import GSM8KLoader
from app.runners.BenchmarkRunner import BenchmarkRunner
from app.pipeline.adaptive import AdaptivePipeline
from app.utils.results import summarize_results


def main():

    loader = GSM8KLoader()

    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name="gsm8k_adaptive",
        pipeline=AdaptivePipeline(),
        result_file="results/adaptive_results.csv"
    )

    runner.run(limit=3)

    summarize_results("gsm8k_adaptive")


if __name__ == "__main__":
    main()