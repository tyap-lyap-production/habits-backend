from sqlalchemy import Column, UUID, Integer, Float, String
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid


class Goal(Base):
    __tablename__ = "goal"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    unit_type = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    periodicity = Column(String, nullable=False)

    # Связь с Habit
    habits = relationship("Habit", back_populates="goal", remote_side="Habit.goal_id")
