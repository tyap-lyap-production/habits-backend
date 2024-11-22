from sqlalchemy import Column, UUID, Integer, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Goal(Base):
    __tablename__ = "goal"

    goal_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    unit_type = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    periodicity = Column(Integer, nullable=False)

    # Связь с Habit
    habits = relationship("Habit", back_populates="goal", remote_side="Habit.goal_id")
