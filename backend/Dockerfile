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

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app

WORKDIR /app

CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80"]