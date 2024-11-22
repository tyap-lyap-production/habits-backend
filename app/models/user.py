from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class User(Base):
    __tablename__ = "person"

    user_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    login = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    habits = relationship("Habit", back_populates="user")