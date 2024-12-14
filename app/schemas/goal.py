from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class GoalBase(BaseModel):
    periodicity: str
    value: int
    unitType: str


class GoalUpdate(BaseModel):
    periodicity: Optional[str] = None
    value: Optional[int] = None
    unitType: Optional[str] = None


class Goal(GoalBase):
    id: UUID

    class Config:
        orm_mode = True
