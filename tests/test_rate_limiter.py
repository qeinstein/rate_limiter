import time
from rate_limiter.core.rate_limiter import TokenBucketStore

class FakeTime:
    def __init__(self, start=1000.0):
        self.t = start
    def now(self):
        return self.t
    def advance(self, s):
        self.t += s

def test_bucket_basic_consumption():
    ft = FakeTime()
    tb = TokenBucketStore(capacity=3, refill_rate=1.0, time_func=ft.now)
    allowed, remaining, _ = tb.consume("u1")
    assert allowed is True
    #capacity starts at 3, consumed 1 => remaining 2
    assert remaining == 2

def test_bucket_exhaust_and_retry():
    ft = FakeTime()
    tb = TokenBucketStore(capacity=2, refill_rate=1.0, time_func=ft.now)
    tb.consume("u1")  # -1 => 1
    tb.consume("u1")  # -1 => 0
    allowed, remaining, retry = tb.consume("u1")
    assert allowed is False
    assert remaining == 0
    assert retry == 1.0  #need one token, refill rate 1/s

def test_refill_after_time():
    ft = FakeTime()
    tb = TokenBucketStore(capacity=5, refill_rate=2.0, time_func=ft.now)
    tb.consume("u1")  
    ft.advance(1.5)   
    allowed, remaining, _ = tb.consume("u1")
    assert allowed is True
    assert remaining == 4  