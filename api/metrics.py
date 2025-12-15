from fastapi import APIRouter
from rate_limiter.core.metrics_store import metrics_store_singleton

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    return metrics_store_singleton.snapshot()