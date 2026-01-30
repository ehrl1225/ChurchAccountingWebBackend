FROM python:3.14.2-slim
LABEL authors="js"

WORKDIR /app

RUN apt update -y
RUn apt install curl -y
RUN pip install uv
RUN apt-get install -y curl

COPY pyproject.toml uv.lock alembic.ini .env .env.* ./
RUN uv sync

COPY ./src/ /app/src/
COPY ./alembic /app/alembic

ENV PYTHONPATH="/app/src/main:/app"
ENV PROFILE="prod"
COPY ./run.sh /app/run.sh

CMD ["/app/run.sh"]
