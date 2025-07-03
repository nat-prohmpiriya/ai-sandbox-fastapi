from typing import List, Type
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie, Document

async def init_mongodb(
    uri: str,
    db_name: str,
    document_models: List[Type[Document]]
) -> AsyncIOMotorDatabase:
    client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
    db: AsyncIOMotorDatabase = client[db_name]
    await init_beanie(database=db, document_models=document_models)
    return db