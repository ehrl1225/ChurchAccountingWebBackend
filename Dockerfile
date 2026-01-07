FROM python:3.14.0-slim
LABEL authors="js"

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock alembic.ini .env ./
RUN uv sync

COPY src/ ./src/
COPY alembic ./alembic

ENV PYTHONPATH="/app/src/main:/app"

RUN uv run alembic upgrade head
CMD ["uv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
