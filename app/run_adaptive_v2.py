from app.benchmarks.gsm8k_loader import GSM8KLoader
from app.runners.BenchmarkRunner import BenchmarkRunner
from app.pipeline.adaptive_v2 import AdaptivePipelineV2
from app.utils.results import summarize_results


def main():

    loader = GSM8KLoader()

    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name="gsm8k_adaptive_v2",
        pipeline=AdaptivePipelineV2()
    )

    runner.run(limit=3)

    summarize_results("gsm8k_adaptive_v2")


if __name__ == "__main__":
    main()