import time
from collections import Counter
from threading import Lock


class Metrics:
    def __init__(self):
        self._lock = Lock()

        self.requests_total = 0
        self.requests_failed = 0

        self.request_duration_total = 0.0

        self.routes = Counter()
        self.tools = Counter()

    def record_request(
        self,
        duration: float,
        success: bool = True,
    ):
        with self._lock:
            self.requests_total += 1
            self.request_duration_total += duration

            if not success:
                self.requests_failed += 1

    def record_route(self, route: str):
        with self._lock:
            self.routes[route] += 1

    def record_tool(self, tool_name: str):
        with self._lock:
            self.tools[tool_name] += 1

    def snapshot(self) -> dict:
        with self._lock:
            average_duration = 0.0

            if self.requests_total:
                average_duration = (
                    self.request_duration_total
                    / self.requests_total
                )

            return {
                "requests_total": self.requests_total,
                "requests_failed": self.requests_failed,
                "average_request_duration_ms": round(
                    average_duration * 1000,
                    2,
                ),
                "routes": dict(self.routes),
                "tools": dict(self.tools),
            }


metrics = Metrics()