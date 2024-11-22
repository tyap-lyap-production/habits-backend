from sqlalchemy import Column, Float, Integer, Date, UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Status(Base):
    __tablename__ = "status"

    status_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    current_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)
    unit_type = Column(Integer, nullable=False)  # Например, единицы измерения (часы, минуты и т.д.)
    periodicity = Column(Integer, nullable=False)  # Периодичность (например, 7 для недельной привычки)
    reference_date = Column(Date, nullable=False)
    
    habits = relationship("Habit", back_populates="status", cascade="all, delete-orphan")