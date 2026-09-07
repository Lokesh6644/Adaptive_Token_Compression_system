from datetime import datetime
import pandas as pd
from pathlib import Path

DEFAULT_RESULT_FILE = Path("results/baseline_results.csv")

STANDARD_COLUMNS = [
    "timestamp",
    "benchmark",
    "sample_id",
    "model",
    "prompt",
    "original_prompt",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "latency",
    "difficulty",
    "budget",
    "compression_ratio",
    "token_reduction",
    "semantic_similarity",
    "guard_passed",
    "response",
    "ground_truth",
    "predicted_answer",
    "actual_answer",
    "correct",
]


def log_result(data, filepath=None):
    target_file = Path(filepath) if filepath else DEFAULT_RESULT_FILE
    target_file.parent.mkdir(parents=True, exist_ok=True)

    row = dict(data)
    if "timestamp" not in row or not row["timestamp"]:
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame([row])

    if target_file.exists():
        try:
            existing_df = pd.read_csv(target_file)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_csv(target_file, index=False)
        except Exception:
            df.to_csv(target_file, mode="a", header=False, index=False)
    else:
        cols = [c for c in STANDARD_COLUMNS if c in df.columns] + [c for c in df.columns if c not in STANDARD_COLUMNS]
        df = df[cols]
        df.to_csv(target_file, index=False)