from datasets import load_dataset

from app.benchmarks.base_loader import BaseLoader


class GSM8KLoader(BaseLoader):

    def load(self, limit=10):

        # Load candidate pool.
        # This does NOT call Claude/Gemini.
        dataset = load_dataset(
            "openai/gsm8k",
            "main",
            split="test[:20]"
        )

        candidates = []

        for index, item in enumerate(dataset):

            candidates.append({
                "id": index,
                "prompt": item["question"],
                "reference": item["answer"],
                "metadata": {
                    "type": "math"
                }
            })

        # Sort by prompt length
        candidates.sort(
            key=lambda x: len(x["prompt"].split())
        )

        # Prevent requesting more samples than available
        limit = min(limit, len(candidates))

        # Select evenly distributed samples
        if limit == 1:

            selected = [
                candidates[len(candidates) // 2]
            ]

        else:

            indices = [
                round(
                    i * (len(candidates) - 1) / (limit - 1)
                )
                for i in range(limit)
            ]

            selected = [
                candidates[index]
                for index in indices
            ]

        # Assign difficulty groups
        for position, sample in enumerate(selected):

            if position == 0:

                sample["metadata"][
                    "difficulty_group"
                ] = "easy_candidate"

            elif position == len(selected) - 1:

                sample["metadata"][
                    "difficulty_group"
                ] = "hard_candidate"

            else:

                sample["metadata"][
                    "difficulty_group"
                ] = "medium_candidate"

        return selected