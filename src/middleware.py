from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from src.database.core import db


class MongoDBMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Прокидываем базу данных в request.state.db
        request.state.db = db
        # Обрабатываем запрос
        response = await call_next(request)
        return response
