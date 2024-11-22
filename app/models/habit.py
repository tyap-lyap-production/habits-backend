from sqlalchemy import Column, String, Date, UUID, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
from datetime import datetime

class Habit(Base):
    __tablename__ = "habit"

    habit_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("person.user_id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    area_id = Column(UUID, ForeignKey("area.area_id"))
    time_of_day = Column(Integer)
    created_date = Column(Date, nullable=False, default=datetime.utcnow)  # Добавлено значение по умолчанию
    goal_id = Column(UUID, ForeignKey("goal.goal_id"))
    priority = Column(Float, nullable=False)
    status_id = Column(UUID, ForeignKey("status.status_id"))

    # Отношения
    user = relationship("User", back_populates="habits")
    area = relationship("Area", back_populates="habits")
    goal = relationship("Goal", back_populates="habits")
    status = relationship("Status", back_populates="habits")
    actions = relationship("Action", back_populates="habit", cascade="all, delete-orphan")
