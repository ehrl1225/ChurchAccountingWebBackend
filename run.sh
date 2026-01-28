#!/bin/bash

cd /app
uv run gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --workers 1 &
uv run /app/src/main/common/redis/worker.py &

wait -n

EXIT_CODE=$?
echo "A process has terminated with exit code $EXIT_CODE. Shutting down."
exit $EXIT_CODE