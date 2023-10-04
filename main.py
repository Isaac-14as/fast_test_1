import datetime
from enum import Enum
from typing import *

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
# from fastapi.exceptions import ValidationError
from pydantic import BaseModel, Field, ValidationError



app = FastAPI(
    title="test_1"
)

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail":exc.errors()}),
    )

fake_users = [
    {"id": 1, "role": "admin", "name": "Dmitriy"},
    {"id": 2, "role": "investor", "name": "Oleg"},
    {"id": 3, "role": "trader", "name": "Vova"},
]

class DegrrType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: str

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {"id": 1, "user_id": 1, "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "price": 333, "amount": 2.12},
]

@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]



fake_users2 = [
    {"id": 1, "role": "admin", "name": "Dmitriy"},
    {"id": 2, "role": "investor", "name": "Oleg"},
    {"id": 3, "role": "trader", "name": "Vova"},
]

@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"state": 200, "data": current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}