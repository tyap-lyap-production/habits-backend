from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional
from app.schemas.goal import Goal, GoalBase, GoalUpdate
from app.schemas.status import HabitStatus


class HabitBase(BaseModel):
    name: str
    createDate: date
    goal: GoalBase
    status: HabitStatus


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    createDate: Optional[date] = None
    goal: Optional[GoalUpdate] = None
    status: Optional[HabitStatus]


class Habit(HabitBase):
    id: UUID
    goal: Goal

    class Config:
        orm_mode = True
