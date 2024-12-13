from sqlalchemy import Column, String, Date, UUID, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
from datetime import datetime


class Habit(Base):
    __tablename__ = "habit"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("person.user_id"), nullable=False)
    name = Column(String, nullable=False)
    createDate = Column(Date, nullable=False, default=datetime.utcnow)
    goal_id = Column(UUID, ForeignKey("goal.id"))
    status = Column(Integer)

    # Отношения
    user = relationship("User", back_populates="habits")
    goal = relationship("Goal", back_populates="habits")
