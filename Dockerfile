FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt poetry.lock* 

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "proxy:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
