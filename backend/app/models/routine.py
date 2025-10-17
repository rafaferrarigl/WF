from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    trainer_id = Column(Integer, ForeignKey("users.id"))  # el entrenador que la creó
    client_id = Column(Integer, ForeignKey("users.id"))    # el cliente asignado

    exercises = relationship("Exercise", back_populates="routine")
