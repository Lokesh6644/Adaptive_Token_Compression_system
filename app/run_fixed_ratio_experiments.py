from app.benchmarks.gsm8k_loader import GSM8KLoader
from app.runners.BenchmarkRunner import BenchmarkRunner
from app.pipeline.baseline import BaselinePipeline


def run_experiment(ratio, limit=5):

    print("\n" + "=" * 60)

    if ratio == 1.0:
        name = "BASELINE"
    else:
        name = f"FIXED RATIO {ratio * 100:.0f}% RETENTION"

    print(name)
    print("=" * 60)

    loader = GSM8KLoader()

    pipeline = BaselinePipeline(
        compression_ratio=None if ratio == 1.0 else ratio
    )

    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name=f"gsm8k_{int(ratio * 100)}",
        pipeline=pipeline,
        result_file="results/fixed_ratio_results.csv"
    )

    runner.run(limit=limit)


def main():

    experiments = [
        1.00,   # Baseline
        0.75,   # 25% reduction
        0.50,   # 50% reduction
        0.25    # 75% reduction
    ]

    for ratio in experiments:
        run_experiment(ratio)


if __name__ == "__main__":
    main()