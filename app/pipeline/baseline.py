from app.llm.anthropic_client import ClaudeClient
from app.llm.metrics import Metrics


class BaselinePipeline:

    def __init__(self):

        self.client = ClaudeClient()
        self.metrics = Metrics()

    def run(self, prompt):

        self.metrics.start_timer()

        response = self.client.generate(prompt)

        latency = self.metrics.stop_timer()

        metric_data = self.metrics.build_metrics(response)

        metric_data["latency"] = latency

        metric_data["model"] = response.model

        metric_data["prompt"] = prompt

        metric_data["response"] = response.content[0].text

        return metric_data