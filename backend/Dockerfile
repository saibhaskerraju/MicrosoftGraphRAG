# Stage 1: Builder
FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir uv

# Copy the application into the container.
COPY . /app

WORKDIR /app

# Install dependencies
RUN uv sync --frozen --no-cache

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy only the necessary files from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

ENTRYPOINT ["/app/.venv/bin/uvicorn", "main:app", "--host=0.0.0.0", "--port=8080"]
#CMD ["sh", "-c", "pwd && ls -la &&  ls -la .venv/bin && tail -f /dev/null"]