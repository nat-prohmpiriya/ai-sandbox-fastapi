from fastapi import FastAPI
from typing import Dict

app: FastAPI = FastAPI()

@app.get("/", response_model=Dict[str, str])
def read_root() -> Dict[str, str]:
    return {"message": "App is running"}

