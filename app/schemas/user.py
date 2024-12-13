from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserCreate):
    id: UUID

    class Config:
        orm_mode = True
