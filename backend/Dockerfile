# Stage 1: Builder
FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy only the necessary files from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the application into the container.
COPY *.py ./
COPY sample.pdf ./sample.pdf

WORKDIR /app

CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "8080", "--host", "0.0.0.0"]
#ENTRYPOINT ["/app/.venv/bin/uvicorn", "main:app", "--host=0.0.0.0", "--port=8080"]
#CMD ["sh", "-c", "pwd && ls -la &&  ls -la .venv/bin && tail -f /dev/null"]