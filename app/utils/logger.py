import pandas as pd
from pathlib import Path

RESULT_FILE = Path("results/baseline_results.csv")

COLUMNS = [
    "timestamp",
    "model",
    "prompt",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "latency",
    "response",
]


def log_result(data):
    RESULT_FILE.parent.mkdir(exist_ok=True)

    df = pd.DataFrame([data])

    # Ensure consistent column order
    df = df.reindex(columns=COLUMNS)

    if RESULT_FILE.exists():
        df.to_csv(
            RESULT_FILE,
            mode="a",
            header=False,
            index=False,
        )
    else:
        df.to_csv(
            RESULT_FILE,
            index=False,
        )