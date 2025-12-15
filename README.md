Sarcasm Challenge

---

# Rate Limiter Service (FastAPI)

A minimal, production-grade FastAPI service implementing:

* **Token-bucket rate limiting** per client
* **Mandatory client identification** via headers
* **Request metrics collection**
* **Deterministic middleware behavior**
* **Full test coverage with pytest**

This project is intentionally small but architecturally correct: proper packaging, absolute imports, middleware correctness, and explicit API contracts.

---

## Features

* **Rate limiting**

  * Token Bucket algorithm
  * Per-client isolation using `x-client-id`
* **Metrics**

  * Counts total requests per `path#METHOD`
  * Thread-safe singleton metrics store
* **Middleware**

  * Rejects requests without required headers
  * Measures latency
  * Updates metrics post-response
* **REST API**

  * CRUD-like item endpoint
  * Health endpoint
  * Metrics endpoint
* **Tested**

  * Pytest + FastAPI TestClient
  * Covers middleware, metrics, rate limiting, and validation

---

## Project Structure

```text
rate_limiter/
├── api/
│   ├── health.py
│   ├── items.py
│   └── metrics.py
├── core/
│   ├── middleware.py
│   ├── metrics_store.py
│   └── rate_limiter.py
├── models/
│   └── item.py
├── tests/
│   ├── test_items.py
│   ├── test_metrics.py
│   ├── test_middleware.py
│   └── test_rate_limiter.py
├── proxy.py
├── __init__.py
├── requirements.txt
└── Dockerfile
```

**Key point:**
`rate_limiter/` is a real Python package. All imports are absolute.

---

## API Contract

### Required Header

All requests **must** include:

```http
x-client-id: <string>
```

Missing header → `400 Bad Request`

---

### Endpoints

#### Health

```http
GET /api/v1/health
```

Response:

```json
{ "status": "ok" }
```

---

#### Items

```http
GET  /api/v1/items
POST /api/v1/items
```

POST body:

```json
{
  "name": "item-name",
  "price": 100
}
```

Validation:

* `price <= 0` → `422 Unprocessable Entity` (Pydantic)

---

#### Metrics

```http
GET /api/v1/metrics
```

Response:

```json
{
  "requests_total": {
    "/api/v1/health#GET": 2,
    "/api/v1/items#GET": 1
  }
}
```

Metrics are updated **after** each request completes.

---

## Rate Limiting

* Token Bucket algorithm
* Enforced in middleware
* Per-client isolation via `x-client-id`
* Remaining tokens included in logs

---

## Middleware Design Notes

* Implemented using `BaseHTTPMiddleware`
* **Blocking behavior returns a Response**, not an exception
  (required for correctness in Starlette/FastAPI)
* Middleware responsibilities:

  1. Validate client header
  2. Enforce rate limit
  3. Measure latency
  4. Update metrics

---

## Setup & Installation

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```
---

## Running the Service

```bash
uvicorn rate_limiter.proxy:app --reload
```

---

## Running Tests

```bash
pytest
```

Expected output:

```text
7 passed in <2s
```

---

## Why This Project Exists

This is not a demo toy.

It intentionally demonstrates:

* Correct Python packaging
* Middleware pitfalls in FastAPI
* Deterministic request handling
* Observable backend behavior
* Test-driven API contracts

It’s designed to be **small but correct**, not feature-bloated.

---

## License

Fluxx
