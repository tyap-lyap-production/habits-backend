from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class AreaBase(BaseModel):
    name: str
    created_date: date
    priority: float


class AreaUpdate(BaseModel):
    name: Optional[str] = None
    created_date: Optional[date] = None
    priority: Optional[float] = None


class Area(AreaBase):
    id: UUID

    class Config:
        orm_mode = True
