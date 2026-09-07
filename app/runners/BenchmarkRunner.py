from app.pipeline.baseline import BaselinePipeline
from app.benchmarks.evaluator import GSM8KEvaluator
from app.utils.logger import log_result


class BenchmarkRunner:

    def __init__(
        self,
        loader,
        benchmark_name,
        pipeline=None,
        result_file=None
    ):

        self.loader = loader
        self.benchmark_name = benchmark_name
        self.pipeline = pipeline or BaselinePipeline()
        self.result_file = result_file

    def run(self, limit=3):

        dataset = self.loader.load(limit=limit)

        correct_count = 0

        for index, sample in enumerate(dataset):

            question = sample["prompt"]
            ground_truth = sample["reference"]

            print(
                f"\nRunning sample "
                f"{index + 1}/{limit}"
            )

            # --------------------------------
            # Run pipeline
            # --------------------------------

            if getattr(
                self.pipeline,
                "requires_ground_truth",
                False
            ):

                result = self.pipeline.run(
                    question,
                    ground_truth
                )

            else:

                result = self.pipeline.run(
                    question
                )

            # --------------------------------
            # Compression metrics
            # --------------------------------

            if "difficulty" in result:

                print(
                    f"Difficulty: "
                    f"{result['difficulty']:.3f}"
                )

                if "initial_budget" in result:

                    print(
                        f"Initial budget: "
                        f"{result['initial_budget']:.2f}"
                    )

                    print(
                        f"Final budget: "
                        f"{result['final_budget']:.2f}"
                    )

                    print(
                        f"Attempts: "
                        f"{result['num_attempts']}"
                    )

                elif "selected_ratio" in result:

                    print(
                        f"Selected ratio: "
                        f"{result['selected_ratio']:.2f}"
                    )

                print(
                    f"Original tokens: "
                    f"{result['original_token_count']}"
                )

                print(
                    f"Compressed tokens: "
                    f"{result['compressed_token_count']}"
                )

                print(
                    f"Token reduction: "
                    f"{result['token_reduction'] * 100:.2f}%"
                )

                print(
                    f"Compressed prompt: "
                    f"{result['prompt']}"
                )

            # --------------------------------
            # Final benchmark evaluation
            # --------------------------------

            evaluation = GSM8KEvaluator.evaluate(
                result["response"],
                ground_truth
            )

            result["benchmark"] = self.benchmark_name
            result["sample_id"] = sample["id"]
            result["ground_truth"] = ground_truth

            result["predicted_answer"] = (
                evaluation["predicted_answer"]
            )

            result["actual_answer"] = (
                evaluation["actual_answer"]
            )

            result["correct"] = (
                evaluation["correct"]
            )

            if evaluation["correct"]:
                correct_count += 1

            # --------------------------------
            # Save result
            # --------------------------------

            log_result(result, filepath=self.result_file)

            # --------------------------------
            # Metrics
            # --------------------------------

            print(
                f"Input tokens: "
                f"{result['input_tokens']}"
            )

            print(
                f"Output tokens: "
                f"{result['output_tokens']}"
            )

            print(
                f"Total tokens: "
                f"{result['total_tokens']}"
            )

            print(
                f"Latency: "
                f"{result['latency']} seconds"
            )

            print(
                f"Predicted: "
                f"{result['predicted_answer']}"
            )

            print(
                f"Actual: "
                f"{result['actual_answer']}"
            )

            print(
                f"Correct: "
                f"{result['correct']}"
            )

        accuracy = (
            correct_count / limit
            if limit > 0
            else 0
        )

        print("\n" + "=" * 50)
        print("BENCHMARK COMPLETE")
        print("=" * 50)

        print(
            f"Accuracy: "
            f"{accuracy * 100:.2f}%"
        )