# Stage 1: Builder
FROM --platform=amd64 python:3.12-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Stage 2: Runtime
FROM --platform=amd64 python:3.12-slim AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy only the necessary files from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the application into the container.
COPY *.py ./
COPY *.pdf ./

RUN python -m spacy download en_core_web_sm --target /app

# WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "8080", "--host", "0.0.0.0"]
#ENTRYPOINT ["/app/.venv/bin/uvicorn", "main:app", "--port=8080", "--host=0.0.0.0"]
#CMD ["sh", "-c", "pwd && ls -la &&  ls -la .venv/bin && tail -f /dev/null"]