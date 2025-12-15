from threading import Lock
from typing import Dict, Any, Tuple

class MetricsStore:
    def __init__(self):
        self._req_counts = {}  #Key -> int
        self._err_counts = {}
        self._lock = Lock()

    def _key(self, method: str, path: str) -> str:
        return f"{path}#{method}"

    def increment_request(self, method: str, path: str):
        k = self._key(method, path)
        with self._lock:
            self._req_counts[k] = self._req_counts.get(k, 0) + 1

    def increment_error(self, method: str, path: str):
        k = self._key(method, path)
        with self._lock:
            self._err_counts[k] = self._err_counts.get(k, 0) + 1

    def snapshot(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {
                "requests_total": dict(self._req_counts),
                "errors_total": dict(self._err_counts),
            }

metrics_store_singleton = MetricsStore()

def get_global_metrics_store() -> MetricsStore:
    return metrics_store_singleton
