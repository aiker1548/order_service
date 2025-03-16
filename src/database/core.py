from typing import AsyncGenerator, Annotated

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request, Depends

from config import config as settings # Предполагается, что у вас есть модуль настроек

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]


async def get_db(request: Request) -> AsyncGenerator:
    db = request.state.db
    yield db

DbDependency = Annotated[AsyncGenerator, Depends(get_db)]