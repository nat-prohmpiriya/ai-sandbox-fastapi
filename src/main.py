from fastapi import FastAPI
from typing import Dict

from src.middlewares.auth import FirebaseAuthMiddleware

from src.routes.auth import router as auth_router

app: FastAPI = FastAPI()

app.add_middleware(
    FirebaseAuthMiddleware
)
app.include_router(auth_router)


@app.get("/", response_model=Dict[str, str])
def read_root() -> Dict[str, str]:
    return {"message": "App is running"}

