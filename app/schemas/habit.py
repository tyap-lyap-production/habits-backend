from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class HabitBase(BaseModel):
    name: str
    start_date: date
    time_of_day: Optional[int] = None
    priority: float

class HabitCreate(HabitBase):
    user_id: UUID
    area_id: Optional[UUID] = None
    goal_id: Optional[UUID] = None
    status_id: Optional[UUID] = None

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    time_of_day: Optional[int] = None
    priority: Optional[float] = None
    area_id: Optional[UUID] = None
    goal_id: Optional[UUID] = None
    status_id: Optional[UUID] = None

class Habit(HabitBase):
    habit_id: UUID

    class Config:
        orm_mode = True
