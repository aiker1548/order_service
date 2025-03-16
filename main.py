from fastapi import FastAPI

from src.middleware import MongoDBMiddleware  
from src.orders.views import router as order_router

app = FastAPI()

app.add_middleware(MongoDBMiddleware) #second

app.include_router(order_router)




