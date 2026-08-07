from datasets import load_dataset


class GSM8KLoader:

    def __init__(self):
        self.dataset = load_dataset(
            "gsm8k",
            "main",
            split="test"
        )

    def get_samples(self, n=5):

        samples = []

        for item in self.dataset.select(range(n)):
            samples.append({
                "question": item["question"],
                "answer": item["answer"]
            })

        return samples