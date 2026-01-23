FROM python:3.14.0-slim
LABEL authors="js"

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock alembic.ini .env .env.* ./
RUN uv sync

COPY ./src/ /app/src/
COPY ./alembic /app/alembic

ENV PYTHONPATH="/app/src/main:/app"

CMD ["uv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main.main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
