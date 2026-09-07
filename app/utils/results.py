import pandas as pd
from pathlib import Path


RESULT_FILE = Path("results/baseline_results.csv")


def load_results():

    if not RESULT_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(RESULT_FILE)


def summarize_results(benchmark=None):

    df = load_results()

    if df.empty:
        print("No results found.")
        return

    if benchmark:
        df = df[df["benchmark"] == benchmark]

    if df.empty:
        print("No matching results.")
        return

    print("\n" + "=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)

    print(f"Samples: {len(df)}")

    print(
        f"Average input tokens: "
        f"{df['input_tokens'].mean():.2f}"
    )

    print(
        f"Average output tokens: "
        f"{df['output_tokens'].mean():.2f}"
    )

    print(
        f"Average total tokens: "
        f"{df['total_tokens'].mean():.2f}"
    )

    print(
        f"Average latency: "
        f"{df['latency'].mean():.3f}s"
    )

    if "correct" in df.columns:

        accuracy = df["correct"].mean() * 100

        print(
            f"Accuracy: {accuracy:.2f}%"
        )

    if "estimated_cost" in df.columns:

        print(
            f"Total estimated cost: "
            f"${df['estimated_cost'].sum():.8f}"
        )