#!/bin/bash

# Script to run FastAPI app in production using uvicorn

APP_MODULE="main:app"  # Change 'main' to your Python file name (without .py)
HOST="0.0.0.0"
PORT="5001"
WORKERS=4

# Run FastAPI app with uvicorn and multiple workers
exec pipenv run uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --workers "$WORKERS"