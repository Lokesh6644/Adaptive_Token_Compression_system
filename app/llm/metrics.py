import time
from datetime import datetime


class Metrics:

    def __init__(self):
        self.start = None

    def start_timer(self):
        self.start = time.perf_counter()

    def stop_timer(self):
        return round(time.perf_counter() - self.start, 3)

    def build_metrics(self, response):

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        }