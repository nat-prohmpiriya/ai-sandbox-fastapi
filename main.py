from fastapi import FastAPI
from typing import Dict

# from services.auth.service import router as auth_router
# Uncomment and edit the import below if your service is in a different location
from routes.auth import router as auth_router

app: FastAPI = FastAPI()

app.include_router(auth_router)


@app.get("/", response_model=Dict[str, str])
def read_root() -> Dict[str, str]:
    return {"message": "App is running"}

