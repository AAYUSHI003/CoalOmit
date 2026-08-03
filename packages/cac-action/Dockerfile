FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY packages/cac-core /app/packages/cac-core
COPY packages/cac-cli /app/packages/cac-cli
COPY packages/cac-action /app/packages/cac-action

RUN pip install --no-cache-dir -e /app/packages/cac-core -e /app/packages/cac-cli requests

ENTRYPOINT ["python", "/app/packages/cac-action/src/entrypoint.py"]
