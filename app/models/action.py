from sqlalchemy import Column, String, Integer, Date, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Action(Base):
    __tablename__ = "action"

    action_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    status = Column(Integer, nullable=False)  # Например, статус выполнения действия
    title = Column(String, nullable=False)  # Название действия
    updated_at = Column(Date, nullable=False)  # Последнее обновление
    habit_id = Column(UUID, ForeignKey("habit.habit_id"), nullable=False)

    # Связь с привычкой
    habit = relationship("Habit", back_populates="actions")
