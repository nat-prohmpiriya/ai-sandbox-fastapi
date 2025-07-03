from fastapi import FastAPI
from typing import Dict

from src.models.mongo_init import init_mongodb
from src.models.user import User
from src.config.settings import settings
from src.middlewares.auth import FirebaseAuthMiddleware
from src.routes.auth import router as auth_router
from src.routes.user import router as user_router
from src.routes.chat import router as chat_router


app: FastAPI = FastAPI(root_path="/api/v1")

@app.on_event("startup")
async def on_startup() -> None:
    await init_mongodb(
        uri=settings.mongodb_url,
        db_name=settings.db_name,
        document_models=[User]
    )

app.add_middleware(
    FirebaseAuthMiddleware
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)

@app.get("/", response_model=Dict[str, str])
def read_root() -> Dict[str, str]:
    return {"message": "App is running"}

