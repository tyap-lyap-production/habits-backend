from sqlalchemy import Column, String, Date, UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Area(Base):
    __tablename__ = "area"

    area_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_date = Column(Date, nullable=False)
    priority = Column(String, nullable=False)  # Возможно, это нужно заменить на Enum для определенных значений
    
    habits = relationship("Habit", back_populates="area", cascade="all, delete-orphan")