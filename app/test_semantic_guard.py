import time
from app.compression.semantic_guard import SemanticGuard
from app.compression.adaptive import AdaptiveCompressor
from app.utils.config import SIMILARITY_THRESHOLD, EMBEDDING_MODEL_NAME


TEST_CASES = [
    {
        "original": "John has 10 apples. He gives 3 to his friend and then buys 5 more. How many apples does he have?",
        "good_compression": "John has 10 apples. Gives 3 to friend, buys 5 more. How many apples?",
        "bad_compression": "John 10 friend buys apples?"
    },
    {
        "original": "A train travels 60 km in 2 hours. What is its average speed in kilometers per hour?",
        "good_compression": "Train travels 60 km in 2 hours. What average speed?",
        "bad_compression": "Train 60 2 speed?"
    },
    {
        "original": "There are 24 students in a class. If they are divided equally into 4 groups, how many students are in each group?",
        "good_compression": "24 students divided equally into 4 groups. How many per group?",
        "bad_compression": "24 4 group?"
    }
]


import json
from pathlib import Path
import pandas as pd


def test_standalone_guard(output_dir="results"):
    print("\n" + "=" * 70)
    print("1. STANDALONE SEMANTIC GUARD TEST")
    print(f"Model: {EMBEDDING_MODEL_NAME} | Threshold: {SIMILARITY_THRESHOLD}")
    print("=" * 70)

    guard = SemanticGuard()
    records = []

    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Original        : {case['original']}")

        good_res = guard.verify(case['original'], case['good_compression'])
        print(f"Good Compression: {case['good_compression']}")
        print(f"  -> Similarity : {good_res['similarity']} | Passed: {good_res['passed']}")

        bad_res = guard.verify(case['original'], case['bad_compression'])
        print(f"Bad Compression : {case['bad_compression']}")
        print(f"  -> Similarity : {bad_res['similarity']} | Passed: {bad_res['passed']}")

        records.append({
            "test_type": "standalone",
            "case_id": i,
            "original_text": case["original"],
            "compressed_text": case["good_compression"],
            "compression_type": "good_compression",
            "semantic_similarity": good_res["similarity"],
            "threshold": good_res["threshold"],
            "guard_passed": good_res["passed"],
            "original_tokens": len(case["original"].split()),
            "compressed_tokens": len(case["good_compression"].split()),
            "token_reduction_pct": round((1 - len(case["good_compression"].split()) / len(case["original"].split())) * 100, 2),
            "compression_time_sec": None
        })

        records.append({
            "test_type": "standalone",
            "case_id": i,
            "original_text": case["original"],
            "compressed_text": case["bad_compression"],
            "compression_type": "bad_compression",
            "semantic_similarity": bad_res["similarity"],
            "threshold": bad_res["threshold"],
            "guard_passed": bad_res["passed"],
            "original_tokens": len(case["original"].split()),
            "compressed_tokens": len(case["bad_compression"].split()),
            "token_reduction_pct": round((1 - len(case["bad_compression"].split()) / len(case["original"].split())) * 100, 2),
            "compression_time_sec": None
        })

    return records


def test_adaptive_compressor_with_guard(output_dir="results"):
    print("\n" + "=" * 70)
    print("2. ADAPTIVE COMPRESSOR WITH SEMANTIC GUARD TEST")
    print("=" * 70)

    compressor = AdaptiveCompressor()

    results = []
    records = []

    for i, case in enumerate(TEST_CASES, 1):
        tokens = case["original"].split()
        res = compressor.compress(tokens)

        results.append(res)

        compressed_str = " ".join(res["tokens"])

        print(f"\nPrompt {i}: {case['original']}")
        print(f"Compressed ({res['compressed_tokens']}/{res['original_tokens']} tokens, Budget {res['budget']}): {compressed_str}")
        print(f"Semantic Similarity: {res['semantic_similarity']:.4f} | Guard Passed: {res['guard_passed']} (Threshold: {res['guard_threshold']})")
        print(f"Compression Latency: {res['compression_time']}s")

        reduction_pct = round((1 - res['compressed_tokens'] / res['original_tokens']) * 100, 2) if res['original_tokens'] > 0 else 0.0

        records.append({
            "test_type": "adaptive_with_guard",
            "case_id": i,
            "original_text": case["original"],
            "compressed_text": compressed_str,
            "compression_type": "adaptive",
            "semantic_similarity": res["semantic_similarity"],
            "threshold": res["guard_threshold"],
            "guard_passed": res["guard_passed"],
            "original_tokens": res["original_tokens"],
            "compressed_tokens": res["compressed_tokens"],
            "token_reduction_pct": reduction_pct,
            "compression_time_sec": res["compression_time"]
        })

    avg_sim = sum(r['semantic_similarity'] for r in results) / len(results)
    pass_rate = (sum(1 for r in results if r['guard_passed']) / len(results)) * 100
    avg_reduction = (1 - sum(r['compressed_tokens'] for r in results) / sum(r['original_tokens'] for r in results)) * 100

    print("\n" + "=" * 70)
    print("SUMMARY METRICS")
    print("=" * 70)
    print(f"Average Semantic Similarity: {avg_sim:.4f}")
    print(f"Semantic Guard Pass Rate   : {pass_rate:.1f}%")
    print(f"Average Token Reduction    : {avg_reduction:.1f}%")

    summary = {
        "model_name": EMBEDDING_MODEL_NAME,
        "guard_threshold": SIMILARITY_THRESHOLD,
        "total_prompts_tested": len(results),
        "average_semantic_similarity": round(avg_sim, 4),
        "semantic_guard_pass_rate_pct": round(pass_rate, 2),
        "average_token_reduction_pct": round(avg_reduction, 2),
    }

    return records, summary


def main():
    out_path = Path("results")
    out_path.mkdir(parents=True, exist_ok=True)

    standalone_records = test_standalone_guard(out_path)
    adaptive_records, summary = test_adaptive_compressor_with_guard(out_path)

    all_records = standalone_records + adaptive_records
    df = pd.DataFrame(all_records)
    csv_file = out_path / "semantic_guard_results.csv"
    df.to_csv(csv_file, index=False)

    summary_file = out_path / "semantic_guard_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n[SUCCESS] Results saved to:\n - {csv_file}\n - {summary_file}")


if __name__ == "__main__":
    main()
