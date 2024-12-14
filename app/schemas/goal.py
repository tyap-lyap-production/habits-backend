from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional
from app.schemas.periodicity import HabitPeriodicity


class GoalBase(BaseModel):
    periodicity: HabitPeriodicity
    value: int
    unitType: str


class GoalUpdate(BaseModel):
    periodicity: Optional[HabitPeriodicity] = None
    value: Optional[int] = None
    unitType: Optional[str] = None


class Goal(GoalBase):
    id: UUID

    class Config:
        orm_mode = True
