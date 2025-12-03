FROM python:3.14.0-slim
LABEL authors="js"

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY src/ ./src/

CMD ["uv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
