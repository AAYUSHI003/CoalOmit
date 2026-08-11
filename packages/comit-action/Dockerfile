FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY packages/comit-core /app/packages/comit-core
COPY packages/comit-cli /app/packages/comit-cli
COPY packages/comit-action /app/packages/comit-action

RUN pip install --no-cache-dir -e /app/packages/comit-core -e /app/packages/comit-cli requests

ENTRYPOINT ["python", "/app/packages/comit-action/src/entrypoint.py"]
