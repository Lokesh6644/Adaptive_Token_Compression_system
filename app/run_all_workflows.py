import sys
import json
import time
from pathlib import Path
import pandas as pd

from app.benchmarks.gsm8k_loader import GSM8KLoader
from app.runners.BenchmarkRunner import BenchmarkRunner
from app.pipeline.baseline import BaselinePipeline
from app.pipeline.adaptive import AdaptivePipeline
import app.test_semantic_guard as sg_test
import app.test_phase3_pipeline as p3_test


def run_semantic_guard_workflow(out_dir: Path):
    print("\n" + "=" * 70)
    print(">>> WORKFLOW 1: SEMANTIC GUARD VERIFICATION")
    print("=" * 70)
    sg_test.main()


def run_baseline_workflow(out_dir: Path, limit=3):
    print("\n" + "=" * 70)
    print(f">>> WORKFLOW 2: BASELINE RUNNER (GSM8K, limit={limit})")
    print("=" * 70)
    loader = GSM8KLoader()
    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name="gsm8k_baseline",
        pipeline=BaselinePipeline(),
        result_file=str(out_dir / "baseline_results.csv")
    )
    runner.run(limit=limit)


def run_adaptive_workflow(out_dir: Path, limit=3):
    print("\n" + "=" * 70)
    print(f">>> WORKFLOW 3: ADAPTIVE COMPRESSION RUNNER (GSM8K, limit={limit})")
    print("=" * 70)
    loader = GSM8KLoader()
    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name="gsm8k_adaptive",
        pipeline=AdaptivePipeline(),
        result_file=str(out_dir / "adaptive_results.csv")
    )
    runner.run(limit=limit)


def run_fixed_ratio_workflow(out_dir: Path, ratio=0.5, limit=3):
    print("\n" + "=" * 70)
    print(f">>> WORKFLOW 4: FIXED RATIO COMPRESSION (GSM8K, ratio={ratio}, limit={limit})")
    print("=" * 70)
    loader = GSM8KLoader()
    runner = BenchmarkRunner(
        loader=loader,
        benchmark_name=f"gsm8k_fixed_{int(ratio*100)}",
        pipeline=BaselinePipeline(compression_ratio=ratio),
        result_file=str(out_dir / "fixed_ratio_results.csv")
    )
    runner.run(limit=limit)


def run_phase3_benchmark_workflow(out_dir: Path):
    print("\n" + "=" * 70)
    print(">>> WORKFLOW 5: PHASE 3 COMPARATIVE BENCHMARK")
    print("=" * 70)
    p3_test.main()


def generate_overall_summary(out_dir: Path):
    print("\n" + "=" * 70)
    print(">>> GENERATING UNIFIED WORKFLOW SUMMARY")
    print("=" * 70)

    summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files_generated": []
    }

    # Inspect all generated CSV files in results
    csv_files = list(out_dir.glob("*.csv"))
    tables_md = []

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            summary["files_generated"].append({
                "file": csv_file.name,
                "rows": len(df),
                "columns": list(df.columns)
            })

            tables_md.append(f"### {csv_file.name} ({len(df)} records)")
            # Show summary columns if present
            display_cols = [c for c in ["method", "benchmark", "prompt", "original_tokens", "compressed_tokens", "token_reduction", "token_reduction_pct", "semantic_similarity", "guard_passed", "correct", "latency", "total_latency"] if c in df.columns]
            if not display_cols:
                display_cols = list(df.columns[:8])
            
            sample_df = df[display_cols].head(5)
            tables_md.append(sample_df.to_markdown(index=False))
            tables_md.append("\n")
        except Exception as e:
            print(f"Error summarizing {csv_file}: {e}")

    # Write summary JSON
    summary_json_path = out_dir / "workflow_summary.json"
    with open(summary_json_path, "w") as f:
        json.dump(summary, f, indent=2)

    # Write summary Markdown
    summary_md_path = out_dir / "workflow_summary.md"
    md_content = f"# All Workflows Execution Summary\n\nGenerated: {summary['generated_at']}\n\n"
    md_content += "## Generated Result Artifacts\n\n"
    for item in summary["files_generated"]:
        md_content += f"- **[{item['file']}](./{item['file']})**: {item['rows']} records\n"
    md_content += "\n## Data Previews\n\n"
    md_content += "\n".join(tables_md)

    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[SUCCESS] Unified summary written to:\n - {summary_json_path}\n - {summary_md_path}")


def main():
    out_dir = Path("results")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Clean existing CSV and JSON results for a fresh run
    for old_file in out_dir.glob("*.csv"):
        old_file.unlink()
    for old_file in out_dir.glob("*.json"):
        old_file.unlink()

    # Run workflows
    run_semantic_guard_workflow(out_dir)

    print("\nPacing requests for rate limits...")
    time.sleep(5)
    run_baseline_workflow(out_dir, limit=3)

    print("\nPacing requests for rate limits...")
    time.sleep(10)
    run_adaptive_workflow(out_dir, limit=3)

    print("\nPacing requests for rate limits...")
    time.sleep(10)
    run_fixed_ratio_workflow(out_dir, ratio=0.5, limit=3)

    print("\nPacing requests for rate limits...")
    time.sleep(5)
    run_phase3_benchmark_workflow(out_dir)

    # Compile unified summary
    generate_overall_summary(out_dir)

    print("\n" + "=" * 70)
    print("ALL WORKFLOWS COMPLETED SUCCESSFULLY! All results saved in 'results/' folder.")
    print("=" * 70)


if __name__ == "__main__":
    main()
