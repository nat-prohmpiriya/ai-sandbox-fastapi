#!/bin/bash

pipenv run uvicorn src.main:app --reload --host 0.0.0.0 --port 5001