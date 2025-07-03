#!/bin/bash

# Run FastAPI app with uvicorn in development mode
pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 5001