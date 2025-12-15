from fastapi import Request, Response
from starlette.responses import JSONResponse
from typing import Callable
import time

from rate_limiter.core.logging import log_event
from rate_limiter.core.metrics_store import metrics_store_singleton

#register_middlewares will wire into FastAPI app
def register_middlewares(app, rate_limiter, metrics_store, logger):
    @app.middleware("http")
    async def _middleware(request: Request, call_next: Callable):
        start = time.time()
        #Extract client id
        client_id = request.headers.get("x-client-id")  #or "anonymous"
        path = request.url.path
        method = request.method

        if not client_id:
            #missing header -> reject
            resp = JSONResponse({"detail": "X-Client-ID header required"}, status_code=400)
            metrics_store.increment_request(method, path)
            metrics_store.increment_error(method, path)
            return resp

        allowed, remaining, retry_after = rate_limiter.consume(client_id)
        if not allowed:
            headers = {
                "X-RateLimit-Remaining": str(max(0, remaining)),
                "Retry-After": f"{retry_after:.1f}",
            }
            metrics_store.increment_request(method, path)
            metrics_store.increment_error(method, path)
            return JSONResponse({"detail": "rate limit exceeded"}, status_code=429, headers=headers)

        metrics_store.increment_request(method, path)

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            latency = (time.time() - start) * 1000.0
            event = {
                "ts": time.time(),
                "client": client_id,
                "method": method,
                "path": path,
                "status": 500,
                "latency_ms": latency,
                "error": str(exc),
            }
            log_event(logger, event)
            metrics_store.increment_error(method, path)
            return JSONResponse({"detail": "internal server error"}, status_code=500)

        latency = (time.time() - start) * 1000.0
        status_code = response.status_code
        if status_code >= 400:
            metrics_store.increment_error(method, path)

        event = {
            "ts": time.time(),
            "client": client_id,
            "method": method,
            "path": path,
            "status": status_code,
            "latency_ms": latency,
            "rate_remaining": remaining,
        }
        log_event(logger, event)

        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        return response
