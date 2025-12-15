#the rate limiter gangan

import time
from threading import Lock
from typing import Tuple, Dict

class Bucket:
    __slots__ = ("tokens", "last_ts")
    def __init__(self, tokens: float, last_ts: float):
        self.tokens = tokens
        self.last_ts = last_ts

    
class TokenBucketStore:
    def __init__(self, capacity: int, refill_rate: float, time_func=None ):
        #refill rate is thhe tokens per second
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self._lock = Lock()
        self.time = time_func or time.time
        self._buckets: Dict[str, Bucket] = {}

    
    def _refill(self, bucket: Bucket, now: float):
        elapsed = now - bucket.last_ts
        if elapsed <= 0:
            return
        
        bucket.tokens = min(self.capacity, bucket.tokens + elapsed * self.refill_rate)
        bucket.last_ts = now
    
    def consume(self, client_id: str, tokens: float = 1.0) -> Tuple[bool, int, float]:
        now = self.time()
        with self._lock:
            b = self._buckets.get(client_id)
            if b is None:
                b = Bucket(tokens=self.capacity, last_ts=now)
                self._buckets[client_id] = b
            else:
                self._refill(b, now)

            if b.tokens >= tokens:
                b.tokens -= tokens
                remaining = int(b.tokens)
                return True, remaining, 0.0
            else:
                #time until next token
                needed = tokens - b.tokens
                retry_after = needed / self.refill_rate if self.refill_rate > 0 else float("inf")
                return False, int(b.tokens), retry_after


