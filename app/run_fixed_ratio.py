from app.benchmarks.gsm8k_loader import GSM8KLoader
from app.runners.BenchmarkRunner import BenchmarkRunner
from app.pipeline.baseline import BaselinePipeline
from app.utils.results import summarize_results


def main():

    loader = GSM8KLoader()

    pipeline = BaselinePipeline(
        compression_ratio=0.5
    )

    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name="gsm8k_fixed_ratio_50",
        pipeline=pipeline
    )

    runner.run(limit=5)

    summarize_results("gsm8k_fixed_ratio_50")


if __name__ == "__main__":
    main()