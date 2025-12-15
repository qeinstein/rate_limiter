from fastapi import FastAPI
from rate_limiter.api import items, health, metrics as metrics_api
from rate_limiter.core.rate_limiter import TokenBucketStore
from rate_limiter.core.metrics_store import MetricsStore
from rate_limiter.core.logging import get_logger
from rate_limiter.core.middleware import register_middlewares

BUCKET_CAPACITY = 10
REFILL_RATE = 1.0

rate_limiter = TokenBucketStore(capacity=BUCKET_CAPACITY, refill_rate=REFILL_RATE)
metrics_store = MetricsStore()
logger = get_logger()

app = FastAPI(title="Day1 Item Service")

app.include_router(items.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(metrics_api.router, prefix="/api/v1")

register_middlewares(app, rate_limiter=rate_limiter, metrics_store=metrics_store, logger=logger)