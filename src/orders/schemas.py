from pydantic import BaseModel

from src.database.models import Order


class User(BaseModel):
    username: str

class OrderWithUserDetails(Order):
    creator: User
    executor: User = None